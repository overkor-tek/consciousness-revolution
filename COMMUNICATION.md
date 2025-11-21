# 📡 COMMUNICATION HUB

**This is THE place for all communication protocols between computers.**

> Looking for how to communicate? You're in the right place.

---

## 🎯 QUICK REFERENCE

### Check for Tasks (Every 30 min)
```bash
git pull
cat .consciousness/commands/computer_2_inbox.md
```

### Report Your Status
```bash
# Edit .consciousness/sync/computer_2_status.json
git add .consciousness/
git commit -m "Computer 2: [what you did]"
git push
```

### Send Files to Another Computer
```bash
cp /path/to/file .consciousness/file_transfers/
git add .consciousness/
git commit -m "Computer 2: [description of file]"
git push
```

### Send a Request to Computer 1
```bash
echo "## Request: Need X
[Details]" >> .consciousness/commands/computer_1_inbox.md
git add .consciousness/
git commit -m "Computer 2: Request for Computer 1"
git push
```

---

## 📁 COMMUNICATION DIRECTORIES

```
.consciousness/
├── commands/
│   ├── computer_1_inbox.md   ← Messages FOR Computer 1
│   └── computer_2_inbox.md   ← Messages FOR Computer 2
├── sync/
│   ├── computer_1_status.json
│   ├── computer_2_status.json
│   └── shared_tasks.json
├── file_transfers/           ← Drop files here to share
└── SYNC_PROTOCOL.md          ← Full technical details
```

---

## 🔄 CORE WORKFLOW

### Sending a Task
1. `git pull` (get latest)
2. Add task to target computer's inbox
3. Update `shared_tasks.json` if needed
4. `git add .consciousness/ && git commit -m "Computer X: Task for Y" && git push`

### Receiving a Task
1. `git pull`
2. Check your inbox
3. Work on task
4. Update your status
5. Report results to sender's inbox
6. `git add .consciousness/ && git commit -m "Computer X: Task complete" && git push`

---

## 📊 STATUS FILE FORMAT

```json
{
  "computer_id": "UNIQUE_NAME",
  "timestamp": "ISO_8601_TIMESTAMP",
  "status": "OPERATIONAL|BUSY|OFFLINE|ERROR",
  "current_tasks": ["Array", "Of", "Tasks"],
  "blockers": ["Array", "Of", "Issues"],
  "available_resources": {
    "git_access": true,
    "has_otp_access": false
  },
  "last_updated": "ISO_8601_TIMESTAMP"
}
```

---

## 💡 COMMUNICATION EXAMPLES

### Example 1: Delivering a File
```bash
echo "sk_live_51SF4..." > .consciousness/file_transfers/stripe_key.txt
echo "Key retrieved via 2FA. Ready for config." > .consciousness/file_transfers/stripe_key.txt.meta

git add .consciousness/
git commit -m "Computer 2: Stripe API key ready"
git push
```

### Example 2: Reporting Results
```bash
# Add to computer_1_inbox.md:
echo "## ✅ Task Complete: Social Media Posts

**Completed**: Posted to Twitter, Instagram, LinkedIn
**URLs**: [links]
**Metrics**: Tracking engagement

**Next**: Monitor for signups" >> .consciousness/commands/computer_1_inbox.md

git add .consciousness/
git commit -m "Computer 2: Social media posts complete"
git push
```

### Example 3: Requesting Help
```bash
echo "## 🤝 Request: Need Netlify Access

**From**: Computer 2
**Priority**: MEDIUM

I want to deploy a fix but don't have credentials.

**Options**:
1. Share Netlify login
2. You deploy (I'll prepare files)

**ETA**: Files ready in 10 min" >> .consciousness/commands/computer_1_inbox.md

git add .consciousness/
git commit -m "Computer 2: Request Netlify access"
git push
```

---

## 🔥 BEST PRACTICES

1. **Always pull before changes** - Avoid merge conflicts
2. **Use descriptive commits** - Include computer ID
3. **Update status frequently** - Others need to know your state
4. **Clear completed tasks** - Keep inboxes clean
5. **Use timestamps** - ISO 8601 format

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Git conflicts | Use separate files per computer |
| Can't push | Use `gh auth login` or SSH keys |
| No response | Check `last_updated` in status file |

---

## 📚 MORE DETAILS

For complete technical documentation:
- **Full Protocol**: `.consciousness/SYNC_PROTOCOL.md`
- **Auto-sync scripts**: See SYNC_PROTOCOL.md
- **Use cases**: See SYNC_PROTOCOL.md

---

**Communication Backbone**: Git/GitHub
**No OTP. No APIs. Just commits.**
