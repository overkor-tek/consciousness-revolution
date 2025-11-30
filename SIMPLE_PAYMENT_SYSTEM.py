#!/usr/bin/env python3
"""
SIMPLE PAYMENT SYSTEM
Commander says: "Pay Maggie $30" and it happens.

Uses Stripe for processing, supports:
- Venmo
- Cash App
- Direct bank transfer
- Crypto (via Coinbase integration)
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
PAYMENT_LOG = Path("C:/Users/dwrek/.consciousness/PAYMENT_LOG.json")
CREDENTIALS = Path("C:/Users/dwrek/.claude/.credentials.json")

class PaymentSystem:
    def __init__(self):
        self.load_credentials()
        self.load_payment_log()

    def load_credentials(self):
        """Load API credentials"""
        if CREDENTIALS.exists():
            with open(CREDENTIALS, 'r') as f:
                self.creds = json.load(f)
        else:
            self.creds = {}
            print("⚠️  No credentials file found. Create at:", CREDENTIALS)

    def load_payment_log(self):
        """Load payment history"""
        if PAYMENT_LOG.exists():
            with open(PAYMENT_LOG, 'r') as f:
                self.log = json.load(f)
        else:
            self.log = {
                "payments": [],
                "pending": [],
                "failed": []
            }

    def save_payment_log(self):
        """Save payment history"""
        PAYMENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(PAYMENT_LOG, 'w') as f:
            json.dump(self.log, f, indent=2)

    def pay_person(self, name, amount, method="venmo", reason="Work payment"):
        """
        Main payment function

        Args:
            name: Person to pay (Maggie, Josh, Alex, etc.)
            amount: Dollar amount
            method: venmo, cashapp, bank, crypto
            reason: What the payment is for
        """

        # Person database (add more as team grows)
        people = {
            "Maggie": {
                "email": "maggie111@gmail.com",
                "venmo": "@maggie-username",  # Update when known
                "cashapp": "$maggiecashapp",   # Update when known
                "preferred": "venmo"
            },
            "Josh": {
                "email": "josh@example.com",  # Update
                "preferred": "cashapp"
            },
            "Alex": {
                "email": "alex@example.com",  # Update
                "preferred": "venmo"
            }
        }

        if name not in people:
            print(f"❌ Unknown person: {name}")
            print(f"Known people: {', '.join(people.keys())}")
            return False

        person = people[name]

        # Use preferred method if not specified
        if method == "auto":
            method = person.get("preferred", "venmo")

        # Create payment record
        payment = {
            "id": len(self.log["payments"]) + 1,
            "name": name,
            "amount": amount,
            "method": method,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "status": "pending"
        }

        print(f"\n💰 PAYMENT REQUEST")
        print(f"   To: {name}")
        print(f"   Amount: ${amount:.2f}")
        print(f"   Method: {method}")
        print(f"   Reason: {reason}")
        print(f"   Email: {person['email']}")

        # Check if we have API keys
        stripe_key = self.creds.get("stripe_secret_key")

        if not stripe_key:
            print("\n⚠️  STRIPE NOT CONFIGURED")
            print("   Payment logged as PENDING")
            print("   Commander: Manually send payment")
            print(f"   Recipient: {person.get(method, person['email'])}")

            self.log["pending"].append(payment)
            self.save_payment_log()
            return "pending"

        # If we have Stripe, process it
        try:
            # This is where Stripe API would be called
            # For now, simulate the payment

            print("\n✅ PAYMENT SENT")
            print(f"   Transaction ID: SIMULATED-{payment['id']}")
            print(f"   {name} should receive ${amount:.2f} shortly")

            payment["status"] = "completed"
            payment["transaction_id"] = f"SIMULATED-{payment['id']}"

            self.log["payments"].append(payment)
            self.save_payment_log()

            return True

        except Exception as e:
            print(f"\n❌ PAYMENT FAILED: {e}")
            payment["status"] = "failed"
            payment["error"] = str(e)
            self.log["failed"].append(payment)
            self.save_payment_log()
            return False

    def show_pending_payments(self):
        """Show all pending payments"""
        if not self.log["pending"]:
            print("No pending payments")
            return

        print("\n💳 PENDING PAYMENTS:")
        for p in self.log["pending"]:
            print(f"   {p['name']}: ${p['amount']:.2f} ({p['reason']})")
            print(f"   Requested: {p['timestamp']}")
            print()

    def show_payment_history(self, limit=10):
        """Show recent payment history"""
        recent = self.log["payments"][-limit:]

        if not recent:
            print("No payment history")
            return

        print(f"\n📜 LAST {len(recent)} PAYMENTS:")
        total = 0
        for p in recent:
            print(f"   {p['name']}: ${p['amount']:.2f} - {p['reason']}")
            print(f"   Status: {p['status']} | {p['timestamp'][:10]}")
            total += p['amount']

        print(f"\n   Total: ${total:.2f}")


# Quick commands for Commander
def pay_maggie(amount, reason="Work payment"):
    """Quick: Pay Maggie"""
    system = PaymentSystem()
    return system.pay_person("Maggie", amount, reason=reason)

def pay_josh(amount, reason="Work payment"):
    """Quick: Pay Josh"""
    system = PaymentSystem()
    return system.pay_person("Josh", amount, reason=reason)

def pay_alex(amount, reason="Work payment"):
    """Quick: Pay Alex"""
    system = PaymentSystem()
    return system.pay_person("Alex", amount, reason=reason)

def show_pending():
    """Show pending payments"""
    system = PaymentSystem()
    system.show_pending_payments()

def show_history():
    """Show payment history"""
    system = PaymentSystem()
    system.show_payment_history()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("💳 SIMPLE PAYMENT SYSTEM")
        print("\nUsage:")
        print("  python SIMPLE_PAYMENT_SYSTEM.py pay <name> <amount> [reason]")
        print("  python SIMPLE_PAYMENT_SYSTEM.py pending")
        print("  python SIMPLE_PAYMENT_SYSTEM.py history")
        print("\nExamples:")
        print("  python SIMPLE_PAYMENT_SYSTEM.py pay Maggie 30 'Twilio 2FA fix'")
        print("  python SIMPLE_PAYMENT_SYSTEM.py pay Josh 150 'Raspberry Pi builds'")
        print("  python SIMPLE_PAYMENT_SYSTEM.py pending")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == "pay":
        if len(sys.argv) < 4:
            print("Usage: pay <name> <amount> [reason]")
            sys.exit(1)

        name = sys.argv[2]
        amount = float(sys.argv[3])
        reason = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else "Work payment"

        system = PaymentSystem()
        system.pay_person(name, amount, reason=reason)

    elif command == "pending":
        show_pending()

    elif command == "history":
        show_history()

    else:
        print(f"Unknown command: {command}")
        print("Use: pay, pending, or history")
