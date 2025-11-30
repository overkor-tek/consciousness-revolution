#!/usr/bin/env python3
"""
Send Employee Onboarding Email
Simple script to email the new workspace link to all beta testers
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SMTP_SERVER = "mail.privateemail.com"
SMTP_PORT = 465
EMAIL_ADDRESS = "commander@100xbuilder.io"
EMAIL_PASSWORD = "Kill50780630#"

# Beta testers
BETA_TESTERS = [
    ("Josh", "joshua.serrano2022@gmail.com"),
    ("Toby", "tobyburrowes@gmail.com"),
    ("William B", "wdbrotherton@gmail.com"),
    ("Dean", "deansabrwork@gmail.com"),
    ("William V", "varniwilliam@gmail.com"),
    ("Rutherford", "ruuutherford@gmail.com"),
]

# Email template
EMAIL_SUBJECT = "Your Workspace Is Ready - Consciousness Revolution"

def get_email_body(name):
    return f"""Hi {name},

Your workspace is ready. Everything you need is in one place now.

YOUR DESK:
https://consciousnessrevolution.io/workspace.html

Bookmark it. That's your command center.

WHAT YOU'LL FIND:
- Kanban board with all tasks (grab one and start)
- Team chat (talk to other beta testers)
- Quick links to everything
- Help docs if you get stuck

FIRST STEPS:
1. Go to the workspace link above
2. Enter your name when prompted
3. Grab the task "Complete onboarding checklist"
4. Follow the checklist
5. Start building

NO SETUP REQUIRED:
- Works in your browser
- No git, no npm, no install
- Just click and go

NEED HELP?
- Check: consciousnessrevolution.io/help.html
- Or ask in team chat on the workspace page
- Or text: 406-580-3779

The team has been waiting 2 months for this.
Now you have direction. Now you can build.

Welcome to the revolution.

- Commander
Consciousness Revolution
"""

def send_email(to_email, name):
    """Send onboarding email to one tester"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = EMAIL_SUBJECT

    body = get_email_body(name)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✓ Sent to {name} ({to_email})")
        return True
    except Exception as e:
        print(f"✗ Failed to send to {name}: {e}")
        return False

def main():
    print("EMPLOYEE ONBOARDING EMAIL SENDER")
    print("=" * 50)
    print(f"Sending to {len(BETA_TESTERS)} beta testers...\n")

    success_count = 0
    for name, email in BETA_TESTERS:
        if send_email(email, name):
            success_count += 1

    print("\n" + "=" * 50)
    print(f"Complete: {success_count}/{len(BETA_TESTERS)} sent successfully")

if __name__ == "__main__":
    main()
