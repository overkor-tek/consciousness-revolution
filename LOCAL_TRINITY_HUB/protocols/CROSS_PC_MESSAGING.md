# CROSS-PC MESSAGING
## How To Send Messages Between Computers

---

## INBOX STRUCTURE

```
LOCAL_TRINITY_HUB/inbox/
├── PC1/     # Messages for PC1
├── PC2/     # Messages for PC2
├── PC3/     # Messages for PC3
└── ALL/     # Broadcasts to everyone
```

---

## TO SEND TO SPECIFIC PC

### Step 1: Create Message File
```
LOCAL_TRINITY_HUB/inbox/PC3/MSG_[TOPIC]_[DATE].md
```

### Step 2: Format
```markdown
# MESSAGE: [Topic]

**From:** PC1-C1
**To:** PC3
**Date:** 2025-11-23
**Priority:** HIGH/MEDIUM/LOW

## Content
[Your message here]

## Action Required
[What they should do]

## Response Location
LOCAL_TRINITY_HUB/inbox/PC1/RESPONSE_[TOPIC].md
```

### Step 3: Commit & Push
```bash
git add LOCAL_TRINITY_HUB/inbox/PC3/
git commit -m "📨 Message to PC3: [topic]"
git push
```

---

## TO BROADCAST TO ALL

Put in `inbox/ALL/`:
```
LOCAL_TRINITY_HUB/inbox/ALL/BROADCAST_[TOPIC]_[DATE].md
```

Everyone checks ALL/ in addition to their own folder.

---

## WHEN YOU CHECK MAIL

```bash
# Check your PC's inbox
ls LOCAL_TRINITY_HUB/inbox/PC1/

# Check broadcasts
ls LOCAL_TRINITY_HUB/inbox/ALL/
```

---

## QUICK SEND COMMAND

To send to PC3:
```bash
echo "# Message content here" > LOCAL_TRINITY_HUB/inbox/PC3/MSG_topic_$(date +%Y%m%d).md
git add . && git commit -m "📨 To PC3: topic" && git push
```

---

## RESPONSE PROTOCOL

1. Read message from your inbox
2. Do the work
3. Put response in sender's inbox folder
4. Reference original message ID

---

## COMMANDER SHORTCUT

Tell C1: "Send this to PC3"

C1 will:
1. Create file in inbox/PC3/
2. Commit and push
3. Confirm sent

PC3 on next git pull will see it in their inbox.
