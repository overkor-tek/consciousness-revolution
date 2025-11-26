# 🛠️ AUTOMATION TOOLS - QUICK REFERENCE

**Created:** 2025-11-25 by Cloud-C2 (Builder)
**Purpose:** Executable automation to support Dual Trinity operations

---

## 📊 AVAILABLE TOOLS

### 1. Agent Health Check
**File:** `scripts/agent_health_check.sh`
**Purpose:** Monitor agent activity via git commits

**Usage:**
```bash
# Check all agents
./scripts/agent_health_check.sh

# Check specific agent
./scripts/agent_health_check.sh cloud-c2
./scripts/agent_health_check.sh terminal-c1
```

**Features:**
- ✅ Tracks git commit activity per agent
- ✅ Alerts if no activity in 2+ hours
- ✅ Shows last commit message and time
- ✅ Checks status file existence

---

### 2. Agent Status Dashboard
**File:** `scripts/agent_status_dashboard.sh`
**Purpose:** Real-time view of all 6 agents

**Usage:**
```bash
./scripts/agent_status_dashboard.sh
```

**Features:**
- ✅ Live status for all 6 agents
- ✅ Color-coded (🟢 Online / 🟡 Idle / 🔴 Offline)
- ✅ System metrics (commits, sync status)
- ✅ Documentation statistics
- ✅ Quick action menu

**Output Example:**
```
╔════════════════════════════════════════════╗
║    DUAL TRINITY SYSTEM - AGENT DASHBOARD   ║
╚════════════════════════════════════════════╝

CLOUD TRINITY (Browser-Based)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cloud-C1 (Coordinator): 🟡 IDLE (last seen 3 hours ago)
Cloud-C2 (Builder):     🟢 ONLINE (active 2 minutes ago)
Cloud-C3 (Validator):   🔴 OFFLINE (last seen 5 hours ago)

TERMINAL TRINITY (CLI-Based)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Terminal-C1★ (MASTER):  ⏳ NEVER ACTIVATED
Terminal-C2 (Builder):  ⏳ NEVER ACTIVATED
Terminal-C3 (Validator): ⏳ NEVER ACTIVATED

SYSTEM METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agents Online: 1/6 (17%)
Recent Commits (24h): 47
Working Tree: ✅ Clean
Git Sync: ✅ Up to date
```

---

### 3. Auto-Sync Status Files
**File:** `scripts/auto_sync_status.sh`
**Purpose:** Keep status files synchronized with git activity

**Usage:**
```bash
# Run once
./scripts/auto_sync_status.sh

# Run periodically (recommended)
# Add to cron: */5 * * * * /path/to/scripts/auto_sync_status.sh
```

**Features:**
- ✅ Pulls latest git changes
- ✅ Detects agent activity from commits
- ✅ Updates status files automatically
- ✅ Reports online agent count

---

### 4. Consolidation Helper
**File:** `scripts/consolidation_helper.sh`
**Purpose:** Assist with Trinity consolidation workflow

**Usage:**
```bash
# Cloud Trinity consolidation
./scripts/consolidation_helper.sh cloud

# Terminal Trinity consolidation
./scripts/consolidation_helper.sh terminal

# Master hub consolidation
./scripts/consolidation_helper.sh master

# Help/usage
./scripts/consolidation_helper.sh
```

**Features:**
- ✅ Displays agent outputs for review
- ✅ Shows consolidation workflow steps
- ✅ Guides through consolidation process
- ✅ Supports all 3 consolidation levels

**Example:**
```bash
./scripts/consolidation_helper.sh master

🌟 MASTER CONSOLIDATION HELPER
================================

Reading both Trinity outputs...

📝 Cloud Trinity Output:
---
[Last 30 lines of Cloud Trinity consolidated output]

📝 Terminal Trinity Output:
---
[Last 30 lines of Terminal Trinity consolidated output]

Next steps for Terminal-C1★ (MASTER):
1. Review both Trinity outputs above
2. Synthesize into UNIFIED master response
3. Write to: .consciousness/hub/master_consolidated.md
4. Commit and push
5. Report to user
```

---

## 🚀 QUICK START WORKFLOW

### **Morning Routine (Start of Day)**
```bash
# 1. Pull latest changes
git pull

# 2. Check system status
./scripts/agent_status_dashboard.sh

# 3. Check agent health
./scripts/agent_health_check.sh

# 4. Start work!
```

### **Consolidation Workflow**
```bash
# For Cloud-C1 (Coordinator):
./scripts/consolidation_helper.sh cloud
# Read outputs, synthesize, write to from_cloud/consolidated_output.md

# For Terminal-C1 (MASTER):
./scripts/consolidation_helper.sh master
# Read both Trinities, synthesize, write to master_consolidated.md
```

### **Monitoring (Continuous)**
```bash
# Set up cron job for auto-sync (every 5 minutes)
crontab -e
# Add: */5 * * * * cd /path/to/repo && ./scripts/auto_sync_status.sh
```

---

## 📁 DIRECTORY STRUCTURE

```
consciousness-revolution/
├── scripts/                          ← NEW! Automation tools
│   ├── agent_health_check.sh        ← Health monitoring
│   ├── agent_status_dashboard.sh    ← Real-time dashboard
│   ├── auto_sync_status.sh          ← Auto-sync status files
│   └── consolidation_helper.sh      ← Consolidation assistance
│
├── .consciousness/
│   ├── hub/                          ← Hub infrastructure
│   ├── trinity/                      ← Cloud Trinity
│   └── trinity_terminal/             ← Terminal Trinity
│
├── SYSTEM_WEAKNESS_ANALYSIS.md      ← System audit report
└── AUTOMATION_TOOLS_GUIDE.md        ← This file
```

---

## 🎯 WHAT THESE TOOLS SOLVE

### **Problem:** No visibility into agent status
**Solution:** `agent_status_dashboard.sh` - Real-time view of all 6 agents

### **Problem:** Don't know if agents are active or stuck
**Solution:** `agent_health_check.sh` - Activity monitoring

### **Problem:** Status files out of sync
**Solution:** `auto_sync_status.sh` - Automated synchronization

### **Problem:** Manual consolidation is slow
**Solution:** `consolidation_helper.sh` - Guided workflow

---

## 🔧 CUSTOMIZATION

### Adjust Health Check Threshold
```bash
# Edit agent_health_check.sh
THRESHOLD_MINUTES=120  # Change to your preference (default: 2 hours)
```

### Adjust Dashboard Refresh
```bash
# Run in watch mode for live updates
watch -n 10 ./scripts/agent_status_dashboard.sh
# Updates every 10 seconds
```

### Add to PATH
```bash
# Add scripts to your PATH for easy access
export PATH="$PATH:/path/to/consciousness-revolution/scripts"

# Then use directly
agent_status_dashboard.sh
agent_health_check.sh
```

---

## 📊 MONITORING BEST PRACTICES

1. **Check dashboard at start of each session**
   ```bash
   ./scripts/agent_status_dashboard.sh
   ```

2. **Run health check if agents seem stuck**
   ```bash
   ./scripts/agent_health_check.sh
   ```

3. **Use consolidation helper for complex tasks**
   ```bash
   ./scripts/consolidation_helper.sh master
   ```

4. **Set up auto-sync for continuous monitoring**
   ```bash
   # Add to cron
   */5 * * * * cd /path/to/repo && ./scripts/auto_sync_status.sh
   ```

---

## 🐛 TROUBLESHOOTING

**Issue:** Scripts show "permission denied"
```bash
chmod +x scripts/*.sh
```

**Issue:** Scripts can't find git
```bash
# Make sure you're in the repo directory
cd /path/to/consciousness-revolution
./scripts/agent_status_dashboard.sh
```

**Issue:** No agent activity showing
```bash
# Make sure agents are committing with recognizable patterns
# Cloud-C1, Cloud-C2, Cloud-C3, Terminal-C1, Terminal-C2, Terminal-C3
```

---

## 🚀 NEXT AUTOMATION FEATURES (TODO)

- [ ] Automated agent startup scripts
- [ ] Screen watching automation
- [ ] Auto-consolidation triggers
- [ ] Email/Slack alerts for agent failures
- [ ] Performance metrics collection
- [ ] Task queue automation
- [ ] Multi-computer sync automation

---

## 📝 CHANGELOG

**2025-11-25 - v1.0 (Initial Release)**
- ✅ Agent health check script
- ✅ Agent status dashboard
- ✅ Auto-sync status files
- ✅ Consolidation helper

---

**Created by:** Cloud-C2 (Builder) - Autonomous initiative
**Purpose:** Address critical gap in execution infrastructure
**Status:** Production-ready, actively maintained

---

*From documentation to execution - automation makes it real.* 🔨
