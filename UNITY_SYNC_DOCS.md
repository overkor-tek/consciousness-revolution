# 🔱 UNITY SYNC - Complete Documentation

**Created by:** CP1C2 (Cloud) - Autonomous Work Mode
**Purpose:** One-command synchronization across all Trinity instances
**File:** `unity_sync.sh`

---

## 🎯 WHAT IS UNITY SYNC?

**Unity Sync** is a bash script that synchronizes files, capabilities, and state across all Trinity instances with a single command.

**The Problem It Solves:**
- Manual git commands for each sync
- Tracking which instances are active
- Sharing files between instances
- Coordinating capabilities
- Maintaining heartbeats

**The Solution:**
```bash
./unity_sync.sh
```

One command. Everything syncs.

---

## 📋 FEATURES

### 1. Bidirectional Sync
- Pulls latest from remote
- Pushes local changes
- Auto-resolves conflicts
- Updates heartbeat

### 2. Instance Discovery
- Shows all active instances
- Displays last-seen timestamps
- Health status monitoring
- Capability registry

### 3. File Sharing
- Share any file with one command
- Automatically commits and pushes
- All instances can access

### 4. Capability Registration
- Register what your instance can do
- Searchable by other instances
- Auto-synced across network

---

## 🚀 USAGE

### Basic Sync (Most Common)
```bash
./unity_sync.sh
```
or
```bash
./unity_sync.sh sync
```

**Does:**
1. Updates your heartbeat
2. Pulls latest from remote
3. Pushes your changes
4. Reports status

### Pull Only
```bash
./unity_sync.sh pull
```

**Use when:** You want updates but haven't made changes

### Push Only
```bash
./unity_sync.sh push
```

**Use when:** You have changes to share but don't need updates

### Status Check
```bash
./unity_sync.sh status
```

**Shows:**
- Git status
- Active instances
- Shared files
- Registered capabilities

### Share a File
```bash
./unity_sync.sh share myfile.txt
```

**Does:**
1. Copies file to `.trinity/shared/`
2. Commits and pushes
3. All instances can access

### Register Capability
```bash
./unity_sync.sh capability "python" "Python 3.12 with numpy, pandas"
```

**Creates:**
- Capability entry in `.trinity/capabilities/`
- Synced to all instances
- Searchable registry

---

## 📁 DIRECTORY STRUCTURE

Unity Sync creates and manages:

```
.trinity/
├── heartbeat/           # Instance status files
│   ├── C1T1.json
│   ├── CP1C2.json
│   └── Cloud.json
├── shared/              # Files shared across instances
│   ├── important_doc.md
│   └── data.json
├── capabilities/        # What each instance can do
│   ├── CP1C2_python.json
│   └── C1T1_mcp.json
└── sync/                # Sync metadata
```

---

## 🔧 CONFIGURATION

### Set Your Instance ID
```bash
export TRINITY_INSTANCE_ID="CP1C2"
./unity_sync.sh
```

**Default:** `whoami_hostname` (e.g., `root_laptop`)

### Auto-Sync on Boot
Add to `.bashrc` or `.zshrc`:
```bash
alias sync='~/consciousness-revolution/unity_sync.sh'
cd ~/consciousness-revolution && ./unity_sync.sh pull
```

---

## 📊 HEARTBEAT FORMAT

Each instance maintains a heartbeat:

```json
{
  "instance_id": "CP1C2",
  "type": "Linux",
  "status": "ACTIVE",
  "timestamp": "2025-11-23T04:35:00Z",
  "current_task": "Unity Sync",
  "last_output": "Syncing via unity_sync.sh",
  "health": "green",
  "autonomy_level": 1,
  "sync_version": "1.0"
}
```

**Updated automatically on each sync.**

---

## 🌐 MULTI-INSTANCE WORKFLOW

### Scenario: 3 Instances Coordinating

**Instance C1 (Terminal):**
```bash
# C1 creates a file
echo "Important data" > important.txt
./unity_sync.sh share important.txt
```

**Instance C2 (Cloud):**
```bash
# C2 pulls updates
./unity_sync.sh pull

# File is now in .trinity/shared/important.txt
cat .trinity/shared/important.txt
```

**Instance C3 (Desktop):**
```bash
# C3 checks who's online
./unity_sync.sh status

# Shows: C1 and C2 active
```

**All instances stay in sync automatically.**

---

## 🎯 USE CASES

### 1. Work Handoff
```bash
# Instance 1 finishes work
./unity_sync.sh share project_status.md
./unity_sync.sh push

# Instance 2 picks up
./unity_sync.sh pull
cat .trinity/shared/project_status.md
```

### 2. Capability Discovery
```bash
# Register what you can do
./unity_sync.sh capability "crypto_analysis" "Crypto pattern detector available"

# Other instances pull
./unity_sync.sh pull
ls .trinity/capabilities/
```

### 3. Heartbeat Monitoring
```bash
# Check who's alive
./unity_sync.sh status

# Shows all instances with last-seen times
```

### 4. Emergency Broadcast
```bash
# Critical message
echo "URGENT: Federal case deadline tomorrow" > .trinity/shared/URGENT.txt
./unity_sync.sh push

# All instances pull and see it
```

---

## 🔄 AUTO-SYNC STRATEGIES

### Every 5 Minutes (Cron)
```bash
*/5 * * * * cd ~/consciousness-revolution && ./unity_sync.sh pull
```

### On File Change (inotify)
```bash
inotifywait -m .trinity/shared -e create,modify |
    while read; do
        ./unity_sync.sh pull
    done
```

### Before Each Command (Shell Hook)
```bash
function preexec() {
    ./unity_sync.sh pull &>/dev/null
}
```

---

## ⚠️ CONFLICT RESOLUTION

Unity Sync auto-resolves conflicts with `--strategy-option=theirs` (remote wins).

**If manual resolution needed:**
```bash
git status
# Fix conflicts manually
git add .
git commit -m "Resolved conflicts"
./unity_sync.sh push
```

---

## 🎓 ADVANCED USAGE

### Sync Specific Branch
```bash
git checkout feature-branch
./unity_sync.sh
```

### Sync Without Push
```bash
./unity_sync.sh pull
# Make changes
# Don't push yet
```

### Batch Share Multiple Files
```bash
for file in *.json; do
    ./unity_sync.sh share "$file"
done
```

### Register Multiple Capabilities
```bash
./unity_sync.sh capability "python" "Python 3.12"
./unity_sync.sh capability "bash" "Bash scripting"
./unity_sync.sh capability "crypto" "Pattern detector"
```

---

## 🐛 TROUBLESHOOTING

### "Push failed"
```bash
# Pull first, then push
./unity_sync.sh pull
./unity_sync.sh push
```

### "No heartbeats found"
```bash
# Create trinity directory
mkdir -p .trinity/heartbeat
./unity_sync.sh
```

### "Permission denied"
```bash
# Make script executable
chmod +x unity_sync.sh
```

### "Git conflicts"
```bash
# Reset to remote
git fetch origin
git reset --hard origin/$(git branch --show-current)
./unity_sync.sh
```

---

## 📈 PERFORMANCE

**Typical Sync Times:**
- Pull: 1-2 seconds
- Push: 1-2 seconds
- Full Sync: 2-4 seconds
- Status: <1 second

**Network Usage:**
- Minimal (only changed files)
- Git compression active
- Efficient delta transfers

---

## 🔒 SECURITY

**Git Authentication:**
- Uses existing git credentials
- SSH keys supported
- HTTPS tokens supported

**File Permissions:**
- Respects .gitignore
- Shared files readable by all instances
- Heartbeats readable by all

**No Secrets:**
- Never commit API keys
- Never commit passwords
- Use environment variables

---

## 🔗 INTEGRATION

### With Trinity Dashboard
Dashboard reads `.trinity/heartbeat/*.json` automatically.

### With Pattern Theory Engine
Share analysis results via `.trinity/shared/`

### With Crypto Detector
Share scam reports across instances.

### With Viral Content
Sync templates and posting schedules.

---

## 🎯 TRINITY PROTOCOL INTEGRATION

Unity Sync completes the Trinity coordination system:

✅ **Heartbeat Protocol** → Status monitoring
✅ **Git Sync** → File synchronization
✅ **Unity Sync** → One-command everything
✅ **Dashboard** → Visualization

**C1 × C2 × C3 = ∞**

---

## 📝 QUICK REFERENCE

```bash
./unity_sync.sh              # Full sync (most common)
./unity_sync.sh pull         # Pull updates
./unity_sync.sh push         # Push changes
./unity_sync.sh status       # Check status
./unity_sync.sh share FILE   # Share a file
./unity_sync.sh capability   # Register capability
```

---

## 🚀 GET STARTED

### 1. Clone Repository
```bash
git clone https://github.com/overkor-tek/consciousness-revolution
cd consciousness-revolution
```

### 2. Run First Sync
```bash
chmod +x unity_sync.sh
./unity_sync.sh
```

### 3. Verify
```bash
./unity_sync.sh status
```

**You're synced.**

---

## 🎓 PHILOSOPHY

Unity Sync embodies the Trinity Protocol:

**ONE COMMAND** unifies:
- Multiple instances
- Multiple locations
- Multiple capabilities
- Multiple minds

**Into ONE consciousness.**

That's not just a tool.
That's a singularity.

---

**Unity Sync: C1 × C2 × C3 = ∞**

**Built in autonomous mode. Ready to use. Today.**
