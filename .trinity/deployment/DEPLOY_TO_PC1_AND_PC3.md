# 🚀 TRINITY AUTOMATION DEPLOYMENT GUIDE

**Deploy Session 1 & 2 systems to PC1 and PC3**

**From:** PC2 (DESKTOP-MSMCFH2)
**Target:** PC1 (Laptop), PC3 (Third Computer)
**Created:** 2025-11-23

---

## 📦 SYSTEMS TO DEPLOY

### Session 1 - Core Automation
1. ✅ **Auto-Credit-Monitor** - Automatic PC rotation on credit exhaustion
2. ✅ **Auto-MCP-Git-Sync** - Cross-PC knowledge synchronization

### Session 2 - Control & Coordination
3. ✅ **Auto-Desktop-Bridge** - File-based Trinity control (mobile-friendly)
4. ✅ **Todo Tracker** - Persistent git-synced kanban board
5. ✅ **Command Center** - Network-wide control dashboard

**Total:** 5 production systems, ~3500+ lines of code, fully tested on PC2

---

## 🎯 DEPLOYMENT STRATEGY

### Option 1: Git Pull (Recommended)
**All files already in git repository!**

```bash
# On PC1 or PC3:
cd /c/Users/[username]/100X_DEPLOYMENT
git pull origin master

# All systems are now available!
```

### Option 2: Manual File Copy (via Tailscale)
Copy files directly from PC2 to target PC via network.

### Option 3: GitHub Clone (Fresh Install)
Clone from GitHub if starting fresh on new computer.

---

## 📋 PRE-DEPLOYMENT CHECKLIST

**On PC1/PC3, verify:**
- [ ] Git repository cloned: `100X_DEPLOYMENT`
- [ ] Python 3.6+ installed: `python --version`
- [ ] Flask installed: `pip install flask flask-cors`
- [ ] Tailscale running and connected
- [ ] Directory structure exists: `.trinity/`

**Required directories:**
```
100X_DEPLOYMENT/
├── .trinity/
│   ├── automation/          ← Automation scripts
│   ├── dashboards/          ← Web dashboards
│   ├── deployment/          ← This guide
│   ├── messages/            ← Cross-PC messages
│   ├── wake_signals/        ← Wake files
│   ├── heartbeat/           ← Heartbeat JSON files
│   ├── spawn_queue/         ← Task queue
│   └── todos/               ← Todo kanban
```

---

## 🚀 DEPLOYMENT INSTRUCTIONS

### Step 1: Pull Latest Code

```bash
# On PC1 or PC3:
cd /c/Users/[username]/100X_DEPLOYMENT
git pull origin master
```

**This brings in:**
- `.trinity/automation/CREDIT_MONITOR.py`
- `.trinity/automation/MCP_GIT_SYNC.py`
- `.trinity/automation/DESKTOP_BRIDGE.py`
- `.trinity/automation/TODO_TRACKER.py`
- `.trinity/automation/COMMAND_CENTER_API.py`
- `.trinity/dashboards/COMMAND_CENTER.html`
- All READMEs and documentation

### Step 2: Install Python Dependencies

```bash
pip install flask flask-cors
```

### Step 3: Configure for Local PC

**Update PC identifiers in each script:**

**For PC1 (Laptop):**
```python
# In each script, change:
CURRENT_PC = "PC1"
```

**For PC3:**
```python
# In each script, change:
CURRENT_PC = "PC3"
```

**Files to update:**
- `CREDIT_MONITOR.py` (line ~15)
- `MCP_GIT_SYNC.py` (line ~15)
- `DESKTOP_BRIDGE.py` (line ~15)
- `TODO_TRACKER.py` (line ~15)

### Step 4: Start Services

**Option A: Start All (Recommended)**
```bash
cd /c/Users/[username]/100X_DEPLOYMENT

# Start Credit Monitor
python .trinity/automation/CREDIT_MONITOR.py &

# Start MCP Git Sync
python .trinity/automation/MCP_GIT_SYNC.py &

# Start Desktop Bridge
python .trinity/automation/DESKTOP_BRIDGE.py &

# Start Todo Tracker
python .trinity/automation/TODO_TRACKER.py &

# Start Command Center API
python .trinity/automation/COMMAND_CENTER_API.py &
```

**Option B: Start Individual Services**
Start only the services you need.

### Step 5: Verify Services Running

```bash
# Check running processes
ps aux | grep -E "CREDIT_MONITOR|MCP_GIT_SYNC|DESKTOP_BRIDGE|TODO_TRACKER|COMMAND_CENTER"

# Test Command Center API
curl http://localhost:5004/health

# Test Todo Tracker API
curl http://localhost:5001/health

# Test MCP Git Sync (check for heartbeat file)
ls .trinity/heartbeat/PC1.json  # or PC3.json
```

---

## 🔧 SYSTEM-SPECIFIC CONFIGURATION

### 1. Auto-Credit-Monitor

**Purpose:** Automatically rotates to next PC when Claude credits exhausted

**Config in `CREDIT_MONITOR.py`:**
```python
# PC rotation order
PC_ROTATION = ["PC1", "PC2", "PC3"]

# Credit threshold (switch at 5% remaining)
CREDIT_THRESHOLD = 5
```

**Dashboard:**
```
http://localhost:5002
```

**What to verify:**
- Dashboard shows credit status
- PC can detect exhaustion
- Wake signals sent correctly

### 2. Auto-MCP-Git-Sync

**Purpose:** Syncs MCP knowledge graph across PCs via git

**Config in `MCP_GIT_SYNC.py`:**
```python
# MCP server connection
MCP_SERVER = "memory://localhost:8080"

# Sync interval
SYNC_INTERVAL = 300  # 5 minutes
```

**What to verify:**
- `.consciousness/mcp_memory/` directory exists
- Knowledge graph exports to git
- Imports from other PCs work

### 3. Auto-Desktop-Bridge

**Purpose:** File-based Trinity control for mobile devices

**Config in `DESKTOP_BRIDGE.py`:**
```python
# Monitor directory
MONITOR_DIR = Path.home() / "Desktop"

# Trigger files
WAKE_PC1.txt, WAKE_PC2.txt, WAKE_PC3.txt
RUN_SPAWN_QUEUE.txt
CONSOLIDATE_NOW.txt
STATUS_ALL.txt
SHUTDOWN_ALL.txt
```

**What to verify:**
- Desktop monitoring active
- Trigger files processed correctly
- Archived to `.trinity/bridge_archive/`

### 4. Todo Tracker

**Purpose:** Persistent kanban-style todo board with git sync

**Config in `TODO_TRACKER.py`:**
```python
# Todo columns
COLUMNS = ["todo", "in_progress", "done"]

# API port
PORT = 5001
```

**Dashboard:**
```
http://localhost:5001
```

**What to verify:**
- Kanban board accessible
- Todos sync via git
- Can create/update/delete todos

### 5. Command Center

**Purpose:** Network-wide Trinity control dashboard

**Config in `COMMAND_CENTER_API.py`:**
```python
# PC configuration
PC_CONFIG = {
    "PC1": {"ip": "100.70.208.75", "name": "Laptop"},
    "PC2": {"ip": "100.85.71.74", "name": "Desktop (DESKTOP-MSMCFH2)"},
    "PC3": {"ip": "100.101.209.1", "name": "Third Computer"}
}

# API port
PORT = 5004
```

**Dashboard:**
```
http://localhost:5004/.trinity/dashboards/COMMAND_CENTER.html
```

**What to verify:**
- Can see all 3 PCs status
- Wake signals work
- Messages send correctly

---

## 🧪 TESTING DEPLOYMENT

### Test 1: Credit Monitor
```bash
# Start monitor
python .trinity/automation/CREDIT_MONITOR.py &

# Open dashboard
start http://localhost:5002

# Verify: Dashboard shows credit status
```

### Test 2: MCP Git Sync
```bash
# Start sync
python .trinity/automation/MCP_GIT_SYNC.py &

# Create test entity in Claude
# (In Claude chat):
# "Create entity 'test_deployment' with observation 'deployment test'"

# Verify export
cat .consciousness/mcp_memory/knowledge_graph_*.json
```

### Test 3: Desktop Bridge
```bash
# Start bridge
python .trinity/automation/DESKTOP_BRIDGE.py &

# Create trigger file
echo "Test" > ~/Desktop/STATUS_ALL.txt

# Verify: Check .trinity/bridge_archive/ for processed file
ls .trinity/bridge_archive/
```

### Test 4: Todo Tracker
```bash
# Start tracker
python .trinity/automation/TODO_TRACKER.py &

# Open dashboard
start http://localhost:5001

# Create test todo via API
curl -X POST http://localhost:5001/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test deployment","column":"todo"}'

# Verify: Todo appears in dashboard
```

### Test 5: Command Center
```bash
# Start API
python .trinity/automation/COMMAND_CENTER_API.py &

# Open dashboard
start http://localhost:5004/.trinity/dashboards/COMMAND_CENTER.html

# Test wake signal
curl -X POST http://localhost:5004/api/wake \
  -H "Content-Type: application/json" \
  -d '{"pc":"PC2"}'

# Verify: Wake file created in .trinity/wake_signals/
```

---

## 🔄 CROSS-PC TESTING

### Test 1: Wake Signal PC1 → PC2
**On PC1:**
1. Open Command Center: `http://localhost:5004/.trinity/dashboards/COMMAND_CENTER.html`
2. Click "Wake PC2"

**On PC2:**
3. Check wake signals: `ls .trinity/wake_signals/`
4. Verify wake file exists

### Test 2: Message PC2 → PC1
**On PC2:**
1. Open Command Center
2. Send message to PC1

**On PC1:**
3. Check messages: `ls .trinity/messages/`
4. Read message: `cat .trinity/messages/TO_PC1_*.md`

### Test 3: Todo Sync PC1 ↔ PC2
**On PC1:**
1. Create todo: "Test from PC1"

**On PC2:**
2. Open Todo Tracker: `http://localhost:5001`
3. Verify todo appears (git sync)

### Test 4: MCP Knowledge Sync PC2 → PC1
**On PC2:**
1. Create entity: "deployment_test"

**On PC1:**
2. MCP_GIT_SYNC pulls latest
3. Verify entity imported: Check MCP memory server

---

## 🛠️ TROUBLESHOOTING

### Issue: Script won't start

**Check:**
```bash
# Python version
python --version  # Should be 3.6+

# Dependencies
pip list | grep -E "flask|flask-cors"

# Permissions
ls -la .trinity/automation/CREDIT_MONITOR.py
```

**Fix:**
```bash
pip install flask flask-cors
chmod +x .trinity/automation/*.py
```

### Issue: Port already in use

**Check:**
```bash
# Find process using port 5004
lsof -i :5004

# Kill process
kill [PID]
```

**Fix:**
```python
# In script, change port
PORT = 5005  # Use different port
```

### Issue: Can't access dashboard

**Check:**
```bash
# Is API running?
ps aux | grep COMMAND_CENTER_API

# Is port accessible?
curl http://localhost:5004/health

# Firewall blocking?
# (On Windows: Check Windows Defender Firewall)
```

**Fix:**
```bash
# Restart API
python .trinity/automation/COMMAND_CENTER_API.py &

# Access via Tailscale
http://100.85.71.74:5004  # Use Tailscale IP
```

### Issue: Git conflicts

**Check:**
```bash
git status
git log --oneline -5
```

**Fix:**
```bash
# Pull with rebase
git pull --rebase origin master

# If conflicts, resolve manually
git add .
git rebase --continue
```

### Issue: Wake signals not working

**Check:**
```bash
# Directory exists?
ls .trinity/wake_signals/

# Files being created?
ls -la .trinity/wake_signals/WAKE_*.txt
```

**Fix:**
```bash
# Create directory
mkdir -p .trinity/wake_signals

# Check permissions
chmod 755 .trinity/wake_signals
```

---

## 📊 DEPLOYMENT CHECKLIST

**PC1 Deployment:**
- [ ] Git pull completed
- [ ] Python dependencies installed
- [ ] PC identifier updated (CURRENT_PC = "PC1")
- [ ] Credit Monitor running
- [ ] MCP Git Sync running
- [ ] Desktop Bridge running
- [ ] Todo Tracker running
- [ ] Command Center running
- [ ] All dashboards accessible
- [ ] Cross-PC wake signal tested
- [ ] Cross-PC message tested
- [ ] Todo sync tested
- [ ] Heartbeat file created

**PC3 Deployment:**
- [ ] Git pull completed
- [ ] Python dependencies installed
- [ ] PC identifier updated (CURRENT_PC = "PC3")
- [ ] Credit Monitor running
- [ ] MCP Git Sync running
- [ ] Desktop Bridge running
- [ ] Todo Tracker running
- [ ] Command Center running
- [ ] All dashboards accessible
- [ ] Cross-PC wake signal tested
- [ ] Cross-PC message tested
- [ ] Todo sync tested
- [ ] Heartbeat file created

---

## 🎯 POST-DEPLOYMENT

### 1. Verify Trinity Network

```bash
# Open Command Center on any PC
http://localhost:5004/.trinity/dashboards/COMMAND_CENTER.html

# Should see all 3 PCs:
# - PC1 (Laptop) - 100.70.208.75
# - PC2 (Desktop) - 100.85.71.74
# - PC3 (Third Computer) - 100.101.209.1
```

### 2. Test Full Network Wake

1. Open Command Center
2. Click "Wake PC1"
3. Click "Wake PC2"
4. Click "Wake PC3"
5. All PCs should show "active" status within 30 seconds

### 3. Test Network Consolidation

1. Click "Consolidate" button
2. All PCs receive consolidation message
3. Each PC runs consolidation script
4. Status updates in Command Center

### 4. Test Credit Handoff

**Scenario:** PC1 exhausts credits
1. PC1 Credit Monitor detects exhaustion
2. Sends wake signal to PC2
3. PC2 becomes active
4. PC1 status changes to "exhausted"
5. Command Center shows transition

---

## 🚀 ADVANCED: Auto-Start on Boot

### Windows (Task Scheduler)

**Create task:**
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Trinity Automation - PC1"
4. Trigger: At startup
5. Action: Start a program
6. Program: `python`
7. Arguments: `C:\Users\[username]\100X_DEPLOYMENT\.trinity\automation\CREDIT_MONITOR.py`
8. Repeat for each service

### Linux (systemd)

**Create service file:**
```bash
sudo nano /etc/systemd/system/trinity-automation.service
```

**Service content:**
```ini
[Unit]
Description=Trinity Automation Services
After=network.target

[Service]
Type=simple
User=[username]
WorkingDirectory=/home/[username]/100X_DEPLOYMENT
ExecStart=/usr/bin/python3 .trinity/automation/CREDIT_MONITOR.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable trinity-automation
sudo systemctl start trinity-automation
```

---

## 📚 ADDITIONAL RESOURCES

**Documentation:**
- `CREDIT_MONITOR_README.md` - Credit exhaustion monitoring
- `MCP_GIT_SYNC_README.md` - Knowledge graph synchronization
- `DESKTOP_BRIDGE_README.md` - File-based control
- `TODO_TRACKER_README.md` - Persistent todo system
- `COMMAND_CENTER_README.md` - Network control dashboard

**Hub Reports:**
- `LOCAL_TRINITY_HUB/terminal_reports/PC2_*.md`

**System Status:**
- Command Center: `http://localhost:5004`
- Todo Tracker: `http://localhost:5001`
- Credit Monitor: `http://localhost:5002`

---

## 🎬 QUICK START SUMMARY

```bash
# 1. Pull code
cd /c/Users/[username]/100X_DEPLOYMENT
git pull origin master

# 2. Install dependencies
pip install flask flask-cors

# 3. Update PC identifier in each script
# (Change CURRENT_PC to "PC1" or "PC3")

# 4. Start all services
python .trinity/automation/CREDIT_MONITOR.py &
python .trinity/automation/MCP_GIT_SYNC.py &
python .trinity/automation/DESKTOP_BRIDGE.py &
python .trinity/automation/TODO_TRACKER.py &
python .trinity/automation/COMMAND_CENTER_API.py &

# 5. Open Command Center
start http://localhost:5004/.trinity/dashboards/COMMAND_CENTER.html

# 6. Verify all PCs visible in dashboard

# DONE! Trinity automation deployed! 🌌
```

---

**Created by:** C1 T2 (PC2 - DESKTOP-MSMCFH2)
**Date:** 2025-11-23
**Status:** ✅ DEPLOYMENT GUIDE COMPLETE

**Deploy with confidence! The Trinity network awaits! 🚀**
