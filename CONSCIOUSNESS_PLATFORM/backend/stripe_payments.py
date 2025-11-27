"""
STRIPE PAYMENT INTEGRATION - Consciousness Platform
=====================================================
Stripe subscription management with webhook handling.

Work Order: WO-007
Created: 2025-11-27
"""

import os
import stripe
from flask import Blueprint, request, jsonify
from datetime import datetime
from auth import token_required, get_current_user
from models import User, Subscription, SessionLocal

# Initialize Stripe
stripe.api_key = os.environ.get("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

# Price IDs from Stripe dashboard
STRIPE_PRICE_ID_PRO = os.environ.get("STRIPE_PRICE_ID_PRO")
STRIPE_PRICE_ID_ENTERPRISE = os.environ.get("STRIPE_PRICE_ID_ENTERPRISE")

# Frontend URL for redirects
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# Create blueprint
payments_bp = Blueprint('payments', __name__, url_prefix='/api/payment')


# ============= Subscription Tiers =============

SUBSCRIPTION_TIERS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'features': [
            'Consciousness Bridge assessment',
            '3 manipulation detections per month',
            'Basic timeline projections',
            'Community access (read-only)'
        ],
        'limits': {
            'detections_per_month': 3,
            'projections_per_month': 3,
            'can_post_community': False
        }
    },
    'pro': {
        'name': 'Pro',
        'price': 19,
        'stripe_price_id': STRIPE_PRICE_ID_PRO,
        'features': [
            'All Free features',
            'Unlimited manipulation detections',
            'Unlimited timeline projections',
            'Pattern Theory Academy access',
            'Seven Domains deep analysis',
            'Community posting and discussions',
            'Priority email support'
        ],
        'limits': {
            'detections_per_month': -1,  # unlimited
            'projections_per_month': -1,
            'can_post_community': True
        }
    },
    'enterprise': {
        'name': 'Enterprise',
        'price': 99,
        'stripe_price_id': STRIPE_PRICE_ID_ENTERPRISE,
        'features': [
            'All Pro features',
            'API access (1000 requests/day)',
            'Custom pattern training',
            'White-label option',
            'Dedicated account manager',
            'Custom integrations',
            'SLA guarantee'
        ],
        'limits': {
            'detections_per_month': -1,
            'projections_per_month': -1,
            'api_requests_per_day': 1000,
            'can_post_community': True,
            'white_label': True
        }
    }
}


# ============= Checkout Session =============

@payments_bp.route('/create-checkout', methods=['POST'])
@token_required
def create_checkout_session():
    """
    Create Stripe checkout session for subscription.

    Request body:
    {
        "tier": "pro" | "enterprise"
    }

    Response:
    {
        "success": true,
        "checkout_url": "https://checkout.stripe.com/...",
        "session_id": "cs_..."
    }
    """
    try:
        data = request.get_json()
        tier = data.get('tier')

        if not tier or tier not in ['pro', 'enterprise']:
            return jsonify({'error': 'Invalid tier. Must be "pro" or "enterprise"'}), 400

        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get or create Stripe customer
        db = SessionLocal()
        try:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user.id
            ).first()

            if subscription and subscription.stripe_customer_id:
                customer_id = subscription.stripe_customer_id
            else:
                # Create new Stripe customer
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.full_name,
                    metadata={'user_id': user.id}
                )
                customer_id = customer.id

                # Create subscription record if doesn't exist
                if not subscription:
                    subscription = Subscription(
                        user_id=user.id,
                        stripe_customer_id=customer_id,
                        plan='free',
                        status='active'
                    )
                    db.add(subscription)
                else:
                    subscription.stripe_customer_id = customer_id

                db.commit()

            # Get price ID for tier
            price_id = SUBSCRIPTION_TIERS[tier]['stripe_price_id']

            if not price_id:
                return jsonify({'error': f'Stripe price ID not configured for {tier} tier'}), 500

            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                customer=customer_id,
                mode='subscription',
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1
                }],
                success_url=f"{FRONTEND_URL}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{FRONTEND_URL}/payment/canceled",
                metadata={
                    'user_id': user.id,
                    'tier': tier
                }
            )

            return jsonify({
                'success': True,
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id
            })

        finally:
            db.close()

    except stripe.error.StripeError as e:
        return jsonify({'error': f'Stripe error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Stripe Webhooks =============

@payments_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """
    Handle Stripe webhook events.

    Events handled:
    - checkout.session.completed
    - customer.subscription.updated
    - customer.subscription.deleted
    - invoice.payment_failed
    """
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    event_type = event['type']
    data = event['data']['object']

    if event_type == 'checkout.session.completed':
        handle_checkout_completed(data)
    elif event_type == 'customer.subscription.updated':
        handle_subscription_updated(data)
    elif event_type == 'customer.subscription.deleted':
        handle_subscription_deleted(data)
    elif event_type == 'invoice.payment_failed':
        handle_payment_failed(data)

    return jsonify({'success': True}), 200


def handle_checkout_completed(session):
    """Handle successful checkout - activate subscription"""
    customer_id = session.get('customer')
    subscription_id = session.get('subscription')
    user_id = session.get('metadata', {}).get('user_id')
    tier = session.get('metadata', {}).get('tier')

    if not user_id or not tier:
        print(f"Missing metadata in checkout session: {session.id}")
        return

    db = SessionLocal()
    try:
        # Get subscription record
        subscription = db.query(Subscription).filter(
            Subscription.user_id == int(user_id)
        ).first()

        if not subscription:
            # Create new subscription
            subscription = Subscription(
                user_id=int(user_id),
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                plan=tier,
                status='active'
            )
            db.add(subscription)
        else:
            # Update existing subscription
            subscription.stripe_subscription_id = subscription_id
            subscription.plan = tier
            subscription.status = 'active'

        # Get subscription details from Stripe
        stripe_sub = stripe.Subscription.retrieve(subscription_id)
        subscription.stripe_price_id = stripe_sub['items']['data'][0]['price']['id']
        subscription.current_period_start = datetime.fromtimestamp(stripe_sub['current_period_start'])
        subscription.current_period_end = datetime.fromtimestamp(stripe_sub['current_period_end'])

        # Update user tier
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user:
            user.subscription_tier = tier

        db.commit()

        print(f"Subscription activated: user_id={user_id}, tier={tier}")

    except Exception as e:
        db.rollback()
        print(f"Error handling checkout completed: {e}")
    finally:
        db.close()


def handle_subscription_updated(subscription):
    """Handle subscription update (plan change, renewal, etc.)"""
    customer_id = subscription.get('customer')
    subscription_id = subscription.get('id')
    status = subscription.get('status')

    db = SessionLocal()
    try:
        # Find subscription by Stripe subscription ID
        sub_record = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == subscription_id
        ).first()

        if not sub_record:
            print(f"Subscription not found: {subscription_id}")
            return

        # Update subscription details
        sub_record.status = status
        sub_record.current_period_start = datetime.fromtimestamp(subscription['current_period_start'])
        sub_record.current_period_end = datetime.fromtimestamp(subscription['current_period_end'])
        sub_record.cancel_at_period_end = subscription.get('cancel_at_period_end', False)

        # If subscription is no longer active, downgrade to free
        if status not in ['active', 'trialing']:
            user = db.query(User).filter(User.id == sub_record.user_id).first()
            if user:
                user.subscription_tier = 'free'
            sub_record.plan = 'free'

        db.commit()

        print(f"Subscription updated: {subscription_id}, status={status}")

    except Exception as e:
        db.rollback()
        print(f"Error handling subscription updated: {e}")
    finally:
        db.close()


def handle_subscription_deleted(subscription):
    """Handle subscription cancellation - downgrade to free"""
    subscription_id = subscription.get('id')

    db = SessionLocal()
    try:
        # Find subscription
        sub_record = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == subscription_id
        ).first()

        if not sub_record:
            print(f"Subscription not found: {subscription_id}")
            return

        # Downgrade to free tier
        sub_record.status = 'canceled'
        sub_record.plan = 'free'
        sub_record.canceled_at = datetime.utcnow()

        # Update user tier
        user = db.query(User).filter(User.id == sub_record.user_id).first()
        if user:
            user.subscription_tier = 'free'

        db.commit()

        print(f"Subscription canceled: {subscription_id}")

    except Exception as e:
        db.rollback()
        print(f"Error handling subscription deleted: {e}")
    finally:
        db.close()


def handle_payment_failed(invoice):
    """Handle failed payment - mark subscription at risk"""
    subscription_id = invoice.get('subscription')
    customer_id = invoice.get('customer')

    db = SessionLocal()
    try:
        # Find subscription
        sub_record = db.query(Subscription).filter(
            Subscription.stripe_subscription_id == subscription_id
        ).first()

        if not sub_record:
            print(f"Subscription not found for failed payment: {subscription_id}")
            return

        # Mark as past_due
        sub_record.status = 'past_due'
        db.commit()

        print(f"Payment failed for subscription: {subscription_id}")

        # TODO: Send email notification to user

    except Exception as e:
        db.rollback()
        print(f"Error handling payment failed: {e}")
    finally:
        db.close()


# ============= Customer Portal =============

@payments_bp.route('/create-portal-session', methods=['POST'])
@token_required
def create_portal_session():
    """
    Create Stripe customer portal session.
    Allows user to manage subscription, update payment method, view invoices.

    Response:
    {
        "success": true,
        "portal_url": "https://billing.stripe.com/..."
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db = SessionLocal()
        try:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user.id
            ).first()

            if not subscription or not subscription.stripe_customer_id:
                return jsonify({'error': 'No subscription found'}), 404

            # Create portal session
            portal_session = stripe.billing_portal.Session.create(
                customer=subscription.stripe_customer_id,
                return_url=f"{FRONTEND_URL}/account/billing"
            )

            return jsonify({
                'success': True,
                'portal_url': portal_session.url
            })

        finally:
            db.close()

    except stripe.error.StripeError as e:
        return jsonify({'error': f'Stripe error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Subscription Info =============

@payments_bp.route('/subscription', methods=['GET'])
@token_required
def get_subscription():
    """
    Get current user's subscription info.

    Response:
    {
        "success": true,
        "subscription": {
            "tier": "pro",
            "status": "active",
            "current_period_end": "2025-12-27",
            "cancel_at_period_end": false,
            "features": [...],
            "limits": {...}
        }
    }
    """
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db = SessionLocal()
        try:
            subscription = db.query(Subscription).filter(
                Subscription.user_id == user.id
            ).first()

            tier = user.subscription_tier or 'free'
            tier_info = SUBSCRIPTION_TIERS.get(tier, SUBSCRIPTION_TIERS['free'])

            result = {
                'tier': tier,
                'status': subscription.status if subscription else 'active',
                'features': tier_info['features'],
                'limits': tier_info['limits']
            }

            if subscription and subscription.current_period_end:
                result['current_period_end'] = subscription.current_period_end.isoformat()
                result['cancel_at_period_end'] = subscription.cancel_at_period_end

            return jsonify({
                'success': True,
                'subscription': result
            })

        finally:
            db.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= Tier Information =============

@payments_bp.route('/tiers', methods=['GET'])
def get_tiers():
    """
    Get all subscription tier information.

    Response:
    {
        "success": true,
        "tiers": {
            "free": {...},
            "pro": {...},
            "enterprise": {...}
        }
    }
    """
    return jsonify({
        'success': True,
        'tiers': SUBSCRIPTION_TIERS
    })
