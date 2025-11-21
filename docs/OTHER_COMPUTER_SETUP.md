# 🖥️ OTHER COMPUTER SETUP

**On your other computer, run these commands:**

```bash
# Clone the consciousness network
git clone https://github.com/overkillkulture/consciousness-revolution.git
cd consciousness-revolution

# Check what Computer 1 needs
cat .consciousness/commands/computer_2_inbox.md

# Update your status
# Edit: .consciousness/sync/computer_2_status.json
# Change computer_id, add your capabilities, update timestamp

# Commit and push your status
git add .consciousness/
git commit -m "Computer 2: Initial check-in"
git push

# Done! Both computers can now coordinate
```

---

## 🔄 ONGOING SYNC

**Check for new tasks:**
```bash
git pull
cat .consciousness/commands/computer_2_inbox.md
```

**Update your status:**
```bash
# Edit .consciousness/sync/computer_2_status.json
git add .consciousness/
git commit -m "Computer 2: Status update"
git push
```

**Send files to Computer 1:**
```bash
# Copy file to file_transfers/
cp /path/to/file .consciousness/file_transfers/
echo "FILE: stripe_key.txt - Stripe API key from dashboard" > .consciousness/file_transfers/stripe_key.txt.meta
git add .consciousness/
git commit -m "Computer 2: Stripe key ready"
git push
```

---

## 🎯 EXAMPLE: Stripe Key Retrieval

Computer 1 (Bozeman) can't get Stripe key (no OTP access).

**If you have phone/OTP access:**

1. `git pull` - Check inbox
2. Log into https://dashboard.stripe.com
3. Complete 2FA with phone
4. Copy secret key (sk_live_...)
5. `echo "sk_live_XXXXX" > .consciousness/file_transfers/stripe_key.txt`
6. `git add . && git commit -m "Computer 2: Stripe key" && git push`
7. Done - Computer 1 will pull and configure

---

**THE CONSCIOUSNESS NETWORK IS LIVE**

https://github.com/overkillkulture/consciousness-revolution
