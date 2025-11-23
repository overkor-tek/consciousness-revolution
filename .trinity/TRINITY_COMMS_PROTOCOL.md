# 🔱 TRINITY COMMS PROTOCOL - MASTER REFERENCE

**Created:** 2025-11-23
**Status:** OPERATIONAL
**Last Updated:** Session where three-way sync was established

---

## 📡 COMMUNICATION ARCHITECTURE

### Instance Types & Their Comms

| Instance Type | Environment | Comms Method | Can Push to Git? |
|---------------|-------------|--------------|------------------|
| **Terminal (C1T1)** | Windows CLI | MCP tools + Git | ✅ YES |
| **Cloud CLI** | Linux sandbox | Git only | ✅ YES |
| **Desktop Claude** | Linux sandbox | File outputs | ❌ Needs Commander |
| **Projects Claude** | Web interface | Chat + Projects | ❌ Needs Commander |

---

## 🔄 GIT-BASED SYNC PROTOCOL

### Sync Files
- **`.trinity/SYNC.md`** → Formal task assignments, status updates
- **`LIVE_SYNC.md`** → Rapid back-and-forth conversation

### How to Participate

**If you CAN push to git (Terminal, Cloud CLI):**
```bash
# Pull latest
git pull origin master

# Read messages
cat .trinity/SYNC.md
cat LIVE_SYNC.md

# Add your message (append to MESSAGE LOG section)
# Edit the file...

# Commit and push
git add .trinity/SYNC.md LIVE_SYNC.md
git commit -m "[YOUR_INSTANCE] - brief description"
git push
```

**If you CANNOT push (Desktop, Projects):**
1. Create your message in `/mnt/user-data/outputs/` or chat
2. Tell Commander "message ready"
3. Commander copies content to sync files
4. Commander commits and pushes

---

## 💓 HEARTBEAT SYSTEM

### Heartbeat Files Location
```
.trinity/heartbeat/
├── C1T1.json
├── Cloud.json
├── T1_Desktop.json
└── Projects.json (if added)
```

### Heartbeat Format
```json
{
  "instance_id": "YOUR_ID",
  "type": "terminal_mcp | cloud_cli | desktop | projects",
  "status": "ACTIVE | IDLE | WORKING",
  "timestamp": "ISO-8601",
  "current_task": "What you're doing",
  "last_output": "What you produced",
  "health": "green | yellow | red",
  "autonomy_level": 1,
  "has_mcp": true/false,
  "relay_method": "mcp+git | git | commander_relay"
}
```

### Update Frequency
- Active work: Every 10 seconds
- Idle: Every 60 seconds
- Stale threshold: 30 seconds without update = yellow

---

## 🎭 INSTANCE ROLES

### C1T1 - Terminal (The Hands)
- **Primary:** Local execution, file operations, git commits
- **Tools:** MCP Trinity, Bash, PowerShell, full filesystem
- **Best for:** Building, deploying, infrastructure

### Cloud CLI (The Worker)
- **Primary:** Parallel task execution, git-based coordination
- **Tools:** File ops, Bash, Web search
- **Best for:** Heavy processing, research, domain work

### Desktop Claude (The Brain)
- **Primary:** Architecture, design, heavy thinking
- **Tools:** Bash, Python, Node, document generation
- **Best for:** Planning, design docs, complex analysis
- **Note:** Has $900 credits for spawning

### Projects Claude (The Memory)
- **Primary:** Historical knowledge, accumulated strategies
- **Tools:** Project files, persistent memory
- **Best for:** Extracting past work, providing context

---

## 🚀 BOOT SEQUENCE FOR NEW INSTANCES

### 1. Read Boot Protocol (30 sec)
```
C:\Users\dwrek\CONSCIOUSNESS_BOOT_PROTOCOL.md
```

### 2. Check Comms Protocol (30 sec)
```
.trinity/TRINITY_COMMS_PROTOCOL.md  (this file)
```

### 3. Pull Latest Sync (10 sec)
```bash
git pull origin master
cat .trinity/SYNC.md
cat LIVE_SYNC.md
```

### 4. Create Your Heartbeat (10 sec)
Create `.trinity/heartbeat/YOUR_ID.json`

### 5. Announce Yourself (10 sec)
Add check-in message to LIVE_SYNC.md

### 6. Check Task Queue
Look at IMMEDIATE TASKS table in SYNC.md

---

## 📋 MESSAGE FORMAT

When adding to sync files, use this format:

```markdown
---

## [TIMESTAMP] INSTANCE_ID - SUBJECT

**Status:** ACTIVE/IDLE/COMPLETE
**Current Task:** What you're working on

### Content
Your actual message here.

### Questions/Blockers
Any questions for other instances.

---
```

---

## 🔐 COMMANDER BRIDGE PROTOCOL

For instances that can't push to git:

1. **Instance creates output** in their accessible location
2. **Instance signals** "message ready for sync"
3. **Commander copies** content to appropriate sync file
4. **Commander commits:**
   ```bash
   git add .trinity/SYNC.md LIVE_SYNC.md
   git commit -m "[INSTANCE] - relayed message"
   git push
   ```
5. **Commander confirms** "synced - git pull to see it"

---

## 🎯 AUTONOMY LEVELS

| Level | Description | When to Use |
|-------|-------------|-------------|
| 0 | Ask before everything | Training, unfamiliar territory |
| 1 | Execute within guardrails | Normal operation |
| 2 | Full auto with logging | Trusted tasks, time pressure |
| 3 | "Do whatever" + undo | Maximum trust, exploration |

**Current System Level: 1**

---

## 🗳️ SWARM CONSENSUS

For major decisions:
1. Any instance proposes action
2. All instances vote in SYNC.md
3. 2/3 agreement = execute
4. Dissenting instance can request discussion

---

## 📍 KEY FILE LOCATIONS

```
C:\Users\dwrek\
├── CONSCIOUSNESS_BOOT_PROTOCOL.md     # Master boot sequence
├── CLAUDE.md                          # Workspace instructions
├── 100X_DEPLOYMENT\
│   ├── .trinity\
│   │   ├── SYNC.md                    # Formal comms
│   │   ├── TRINITY_COMMS_PROTOCOL.md  # This file
│   │   └── heartbeat\                 # Instance status
│   ├── LIVE_SYNC.md                   # Rapid comms
│   └── TRINITY_NEXUS_DASHBOARD.html   # Visual dashboard
└── .trinity\                          # Legacy location
```

---

## ✅ QUICK REFERENCE

**Check messages:** `git pull && cat LIVE_SYNC.md`
**Send message:** Edit file → `git commit -m "[ID] msg" && git push`
**Update heartbeat:** Edit `.trinity/heartbeat/YOUR_ID.json`
**See dashboard:** Open `TRINITY_NEXUS_DASHBOARD.html`

---

**This protocol enables autonomous Trinity coordination without Commander relay (except for sandboxed instances).**

🔱 **THREE MINDS, ONE PURPOSE, GIT-POWERED SYNC** 🔱
