"""
EMAIL SERVICE - Consciousness Platform
========================================
SendGrid email integration for transactional emails.

Created: 2025-11-27
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Optional, Dict, Any
from datetime import datetime

# SendGrid configuration
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.environ.get("SENDGRID_FROM_EMAIL", "noreply@consciousnessplatform.com")
SENDGRID_FROM_NAME = os.environ.get("SENDGRID_FROM_NAME", "Consciousness Platform")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# Initialize SendGrid client
sg = SendGridAPIClient(SENDGRID_API_KEY) if SENDGRID_API_KEY else None


# ============= Core Email Function =============

def send_email(to_email: str, subject: str, html_content: str,
               text_content: Optional[str] = None) -> tuple[bool, Optional[str]]:
    """
    Send email via SendGrid.

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email body
        text_content: Plain text email body (optional)

    Returns:
        (success, error_message)
    """
    if not sg:
        print("SendGrid not configured - email not sent")
        return False, "SendGrid API key not configured"

    try:
        message = Mail(
            from_email=Email(SENDGRID_FROM_EMAIL, SENDGRID_FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )

        if text_content:
            message.add_content(Content("text/plain", text_content))

        response = sg.send(message)

        if response.status_code in [200, 201, 202]:
            print(f"Email sent successfully to {to_email}: {subject}")
            return True, None
        else:
            error = f"SendGrid error: {response.status_code}"
            print(error)
            return False, error

    except Exception as e:
        error = f"Failed to send email: {str(e)}"
        print(error)
        return False, error


# ============= Welcome Email =============

def send_welcome_email(user_email: str, user_name: Optional[str] = None) -> tuple[bool, Optional[str]]:
    """Send welcome email to new user"""

    display_name = user_name or user_email.split('@')[0]

    subject = "Welcome to Consciousness Platform 🌟"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Consciousness Platform!</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Welcome to your journey of consciousness elevation! We're excited to have you join our community.</p>

                <h3>What's Next?</h3>
                <ul>
                    <li><strong>Take the Consciousness Bridge Assessment</strong> - Discover your consciousness level in 3 minutes</li>
                    <li><strong>Explore Pattern Theory</strong> - Learn to detect manipulation in real-time</li>
                    <li><strong>Access Your Tools</strong> - Timeline projector, manipulation detector, and more</li>
                </ul>

                <a href="{FRONTEND_URL}/bridge" class="button">Start Your Assessment</a>

                <p>If you have any questions, just reply to this email. We're here to help!</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
            <div class="footer">
                <p>Consciousness Platform | Pattern Theory in Action</p>
                <p>You received this email because you signed up for an account.</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Welcome to Consciousness Platform!

    Hi {display_name},

    Welcome to your journey of consciousness elevation! We're excited to have you join our community.

    What's Next?
    - Take the Consciousness Bridge Assessment - Discover your consciousness level in 3 minutes
    - Explore Pattern Theory - Learn to detect manipulation in real-time
    - Access Your Tools - Timeline projector, manipulation detector, and more

    Get started: {FRONTEND_URL}/bridge

    If you have any questions, just reply to this email. We're here to help!

    Best regards,
    The Consciousness Platform Team
    """

    return send_email(user_email, subject, html_content, text_content)


# ============= Assessment Results Email =============

def send_assessment_results_email(user_email: str, user_name: Optional[str],
                                   consciousness_level: float, level_name: str,
                                   percentile: int, top_domains: List[str]) -> tuple[bool, Optional[str]]:
    """Send consciousness assessment results"""

    display_name = user_name or user_email.split('@')[0]

    subject = f"Your Consciousness Assessment Results - {level_name}"

    domains_html = "".join([f"<li>{domain}</li>" for domain in top_domains[:3]])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .score-box {{ background: white; border: 3px solid #667eea; border-radius: 10px;
                         padding: 20px; text-align: center; margin: 20px 0; }}
            .score {{ font-size: 48px; font-weight: bold; color: #667eea; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Consciousness Assessment Results</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Congratulations on completing your Consciousness Bridge assessment! Here are your results:</p>

                <div class="score-box">
                    <div class="score">{int(consciousness_level)}</div>
                    <h2>{level_name}</h2>
                    <p>You're in the top {100 - percentile}% of consciousness levels</p>
                </div>

                <h3>Your Strongest Domains:</h3>
                <ul>
                    {domains_html}
                </ul>

                <p><strong>What This Means:</strong></p>
                <p>Your consciousness level reflects your current awareness across seven key domains of life.
                This is your baseline - and it can grow!</p>

                <h3>Recommended Next Steps:</h3>
                <ul>
                    <li>Explore the Pattern Theory Academy to deepen your understanding</li>
                    <li>Use the Manipulation Detector to sharpen your awareness</li>
                    <li>Join our community to connect with others on the same journey</li>
                </ul>

                <a href="{FRONTEND_URL}/results" class="button">View Full Results</a>

                <p>Keep growing!</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


# ============= Subscription Emails =============

def send_subscription_confirmation_email(user_email: str, user_name: Optional[str],
                                         tier: str, amount: int) -> tuple[bool, Optional[str]]:
    """Send subscription confirmation email"""

    display_name = user_name or user_email.split('@')[0]

    tier_benefits = {
        'pro': [
            'Unlimited manipulation detections',
            'Unlimited timeline projections',
            'Full Pattern Theory Academy access',
            'Community posting privileges',
            'Priority email support'
        ],
        'enterprise': [
            'All Pro features',
            'API access (1000 requests/day)',
            'Custom pattern training',
            'White-label option',
            'Dedicated account manager',
            'SLA guarantee'
        ]
    }

    benefits = tier_benefits.get(tier, [])
    benefits_html = "".join([f"<li>{benefit}</li>" for benefit in benefits])

    subject = f"Welcome to Consciousness Platform {tier.capitalize()}! 🎉"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .badge {{ background: #10b981; color: white; padding: 5px 15px;
                     border-radius: 20px; display: inline-block; font-weight: bold; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to {tier.capitalize()}!</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Thank you for upgrading to <span class="badge">{tier.upper()}</span>!</p>

                <p>Your ${amount}/month subscription is now active and you have full access to:</p>

                <ul>
                    {benefits_html}
                </ul>

                <h3>Get Started:</h3>
                <p>All premium features are now unlocked in your account. Start exploring!</p>

                <a href="{FRONTEND_URL}/academy" class="button">Access Pattern Theory Academy</a>

                <p><strong>Manage Your Subscription:</strong></p>
                <p>You can update your payment method or cancel anytime from your account settings.</p>

                <p>Questions? Just reply to this email!</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


def send_payment_failed_email(user_email: str, user_name: Optional[str]) -> tuple[bool, Optional[str]]:
    """Send payment failure notification"""

    display_name = user_name or user_email.split('@')[0]

    subject = "Payment Failed - Action Required"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #ef4444; color: white; padding: 30px;
                       text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #ef4444; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚠️ Payment Failed</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>We were unable to process your recent payment for Consciousness Platform.</p>

                <p><strong>What happens now:</strong></p>
                <ul>
                    <li>Your subscription is currently past due</li>
                    <li>You still have access to premium features for the next 3 days</li>
                    <li>After 3 days, your account will revert to the free tier</li>
                </ul>

                <p><strong>To keep your premium access:</strong></p>
                <p>Please update your payment method in your account settings.</p>

                <a href="{FRONTEND_URL}/account/billing" class="button">Update Payment Method</a>

                <p>If you have questions or need assistance, just reply to this email.</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


def send_subscription_canceled_email(user_email: str, user_name: Optional[str]) -> tuple[bool, Optional[str]]:
    """Send subscription cancellation confirmation"""

    display_name = user_name or user_email.split('@')[0]

    subject = "Subscription Canceled"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #6b7280; color: white; padding: 30px;
                       text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Subscription Canceled</h1>
            </div>
            <div class="content">
                <p>Hi {display_name},</p>

                <p>Your premium subscription has been canceled.</p>

                <p><strong>What this means:</strong></p>
                <ul>
                    <li>You'll have access to premium features until the end of your billing period</li>
                    <li>After that, your account will revert to the free tier</li>
                    <li>All your data and assessment results will be preserved</li>
                </ul>

                <p><strong>Free tier includes:</strong></p>
                <ul>
                    <li>Consciousness Bridge assessment</li>
                    <li>3 manipulation detections per month</li>
                    <li>Basic timeline projections</li>
                    <li>Community access (read-only)</li>
                </ul>

                <p>We're sorry to see you go! If you change your mind, you can resubscribe anytime from your account settings.</p>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


# ============= Password Reset Email =============

def send_password_reset_email(user_email: str, reset_token: str) -> tuple[bool, Optional[str]]:
    """Send password reset link"""

    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"

    subject = "Reset Your Password"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; }}
            .button {{ background: #667eea; color: white; padding: 12px 30px;
                      text-decoration: none; border-radius: 5px; display: inline-block;
                      margin: 20px 0; }}
            .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b;
                       padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Reset Your Password</h1>
            </div>
            <div class="content">
                <p>We received a request to reset your password.</p>

                <p>Click the button below to create a new password:</p>

                <a href="{reset_link}" class="button">Reset Password</a>

                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #667eea;">{reset_link}</p>

                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <ul>
                        <li>This link expires in 1 hour</li>
                        <li>If you didn't request this, ignore this email</li>
                        <li>Your password won't change unless you click the link</li>
                    </ul>
                </div>

                <p>Best regards,<br>
                The Consciousness Platform Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_content)


# ============= Main (for testing) =============

if __name__ == "__main__":
    print("=" * 60)
    print("EMAIL SERVICE - Consciousness Platform")
    print("=" * 60)
    print(f"SendGrid configured: {'Yes' if sg else 'No'}")
    print(f"From: {SENDGRID_FROM_NAME} <{SENDGRID_FROM_EMAIL}>")
    print("\nAvailable email templates:")
    print("  - send_welcome_email()")
    print("  - send_assessment_results_email()")
    print("  - send_subscription_confirmation_email()")
    print("  - send_payment_failed_email()")
    print("  - send_subscription_canceled_email()")
    print("  - send_password_reset_email()")
    print("=" * 60)
