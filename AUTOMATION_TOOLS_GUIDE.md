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

### 5. Agent Startup Script
**File:** `scripts/start_agent.sh`
**Purpose:** Automated agent initialization and recovery

**Usage:**
```bash
# Start specific agent
./scripts/start_agent.sh cloud-c1
./scripts/start_agent.sh cloud-c2
./scripts/start_agent.sh terminal-c1

# Show help
./scripts/start_agent.sh
```

**Features:**
- ✅ Validates prerequisites before startup
- ✅ Displays activation instructions
- ✅ Shows agent status and history
- ✅ Pulls latest git changes
- ✅ Provides role-specific guidance
- ✅ Quick reference links

**What it does:**
1. Verifies git repository and .consciousness structure
2. Checks working tree and remote connectivity
3. Pulls latest changes from remote
4. Displays relevant activation instructions
5. Shows agent's last activity and status
6. Provides quick links to status files and tools

**Example:**
```bash
./scripts/start_agent.sh cloud-c2

╔════════════════════════════════════════════════════════════╗
║              DUAL TRINITY - AGENT STARTUP                  ║
╚════════════════════════════════════════════════════════════╝

Agent:    Cloud-C2
Role:     Builder/Implementer
Trinity:  Cloud Trinity

📋 PREREQUISITES CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Git repository detected
  ✅ Consciousness directory found
  ✅ Activation instructions found
  ✅ Working tree clean
  ✅ Git remote accessible

🔄 SYNCHRONIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pulling latest changes...
  ✅ Repository updated

📖 ACTIVATION INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Shows activation instructions from C2_ACTIVATION_INSTRUCTIONS.md]

📊 CURRENT AGENT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Status: 🟢 RECENTLY ACTIVE
  Last activity: 5 minutes ago
  Last commit: CLOUD-C2: Build automation infrastructure

✅ AGENT STARTUP SEQUENCE COMPLETE

Next steps:
  1. Review activation instructions above
  2. Read current system status
  3. Check for assigned tasks
  4. Report to coordinator (if not C1)
  5. Begin work
```

---

### 6. Prerequisites Check
**File:** `scripts/check_prerequisites.sh`
**Purpose:** Validates environment readiness for Dual Trinity System

**Usage:**
```bash
# Standard check
./scripts/check_prerequisites.sh

# Verbose mode (shows details)
./scripts/check_prerequisites.sh --verbose
```

**Features:**
- ✅ Validates core system requirements (git, bash, unix tools)
- ✅ Checks repository structure
- ✅ Verifies critical documentation files
- ✅ Tests automation infrastructure
- ✅ Validates git configuration
- ✅ Reports agent status
- ✅ Shows system metrics

**What it checks:**
1. **Core Requirements**: Git, Bash, standard Unix tools
2. **Repository Structure**: .consciousness/, hub/, trinity/ directories
3. **Critical Files**: Activation instructions, protocols, status files
4. **Automation Scripts**: All monitoring and helper scripts
5. **Git Config**: user.name, user.email, remote access
6. **Agent Status**: Activity for all 6 agents
7. **System Metrics**: Documentation, implementation files, commits

**Exit Codes:**
- `0` - All checks passed (or only warnings)
- `1` - Critical failures detected

**Example Output:**
```bash
./scripts/check_prerequisites.sh

╔════════════════════════════════════════════════════════════╗
║        DUAL TRINITY - PREREQUISITES VALIDATION             ║
╚════════════════════════════════════════════════════════════╝

1️⃣  CORE SYSTEM REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Git installed
  ✅ Bash shell available
  ✅ Standard Unix tools (grep, awk, sed)

2️⃣  REPOSITORY STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Git repository initialized
  ✅ .consciousness directory exists
  ✅ Hub directory exists
  ✅ Cloud Trinity directory exists
  ✅ Terminal Trinity directory exists
  ✅ Scripts directory exists

[... more checks ...]

╔════════════════════════════════════════════════════════════╗
║                    VALIDATION SUMMARY                      ║
╚════════════════════════════════════════════════════════════╝

  ✅ Passed:   42 / 45
  ⚠️  Warnings: 3 / 45
  ❌ Failed:   0 / 45

✅ READY - System is operational

System is ready with minor warnings. Safe to proceed.
```

---

### 7. Continuous Agent Monitoring
**File:** `scripts/monitor_agents.sh`
**Purpose:** Real-time continuous monitoring with alerts

**Usage:**
```bash
# Monitor with default interval (30 seconds)
./scripts/monitor_agents.sh

# Custom interval (60 seconds)
./scripts/monitor_agents.sh 60

# Run in background
./scripts/monitor_agents.sh 30 &

# Stop monitoring: Press Ctrl+C (or kill process)
```

**Features:**
- ✅ Continuous real-time monitoring
- ✅ Automatic status change detection
- ✅ Real-time alerts when agents change state
- ✅ Periodic status summaries
- ✅ Activity logging
- ✅ Auto-pulls git changes

**How it works:**
1. Checks all 6 agents at regular intervals
2. Detects status changes (ACTIVE → IDLE, OFFLINE → ACTIVE, etc.)
3. Sends alerts immediately when status changes
4. Logs all events to `.consciousness/monitoring.log`
5. Provides periodic summaries every 10 iterations

**Status States:**
- **ACTIVE**: Committed in last 5 minutes
- **RECENT**: Committed in last hour
- **IDLE**: Committed 1-4 hours ago
- **OFFLINE**: No commits in 4+ hours
- **NEVER_ACTIVATED**: No commits ever

**Example Session:**
```bash
./scripts/monitor_agents.sh 30

╔════════════════════════════════════════════════════════════╗
║         DUAL TRINITY - CONTINUOUS MONITORING               ║
╚════════════════════════════════════════════════════════════╝

Monitoring interval: 30 seconds
Log file: .consciousness/monitoring.log
Press Ctrl+C to stop

Initial status check...

  🟢 Cloud-C1: RECENT
  🟢 Cloud-C2: ACTIVE
  🟡 Cloud-C3: IDLE
  ⏳ Terminal-C1: NEVER_ACTIVATED
  ⏳ Terminal-C2: NEVER_ACTIVATED
  ⏳ Terminal-C3: NEVER_ACTIVATED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[10:45:32] Status update (iteration 10)
  Agents active: 2/6
  Commits (last hour): 8

🔔 ALERT: Cloud-C3 status changed
  From: IDLE
  To:   ACTIVE
  Time: 2025-11-26 10:46:15 UTC

[11:00:05] Status update (iteration 20)
  Agents active: 3/6
  Commits (last hour): 12
```

**Use Cases:**
- Long-running monitoring during multi-agent sessions
- Detecting when agents become active or go offline
- Debugging coordination issues
- Automated alerting for agent failures

---

## 🚀 QUICK START WORKFLOW

### **First-Time Setup**
```bash
# 1. Validate environment readiness
./scripts/check_prerequisites.sh

# 2. If all checks pass, you're ready to go!
# If issues found, fix them and re-run
```

### **Agent Activation (Starting a New Agent)**
```bash
# Use the startup script for guided activation
./scripts/start_agent.sh cloud-c1     # Cloud Coordinator
./scripts/start_agent.sh cloud-c2     # Cloud Builder
./scripts/start_agent.sh terminal-c1  # Terminal MASTER LEADER

# The script will:
# - Validate prerequisites
# - Pull latest changes
# - Show activation instructions
# - Display agent status
# - Provide next steps
```

### **Morning Routine (Start of Day)**
```bash
# 1. Pull latest changes
git pull

# 2. Validate environment (optional but recommended)
./scripts/check_prerequisites.sh

# 3. Check system status
./scripts/agent_status_dashboard.sh

# 4. Check agent health
./scripts/agent_health_check.sh

# 5. Start work!
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
# Option 1: Run monitoring daemon in terminal
./scripts/monitor_agents.sh 30  # Check every 30 seconds

# Option 2: Run in background
./scripts/monitor_agents.sh 60 &  # Background, check every minute

# Option 3: Set up cron job for auto-sync
crontab -e
# Add: */5 * * * * cd /path/to/repo && ./scripts/auto_sync_status.sh

# View monitoring log
tail -f .consciousness/monitoring.log
```

---

## 📁 DIRECTORY STRUCTURE

```
consciousness-revolution/
├── scripts/                          ← Automation tools
│   ├── agent_health_check.sh        ← Health monitoring
│   ├── agent_status_dashboard.sh    ← Real-time dashboard
│   ├── auto_sync_status.sh          ← Auto-sync status files
│   ├── consolidation_helper.sh      ← Consolidation assistance
│   ├── start_agent.sh               ← Agent startup automation ✨ NEW
│   ├── check_prerequisites.sh       ← Environment validation ✨ NEW
│   └── monitor_agents.sh            ← Continuous monitoring ✨ NEW
│
├── .consciousness/
│   ├── hub/                          ← Hub infrastructure
│   ├── trinity/                      ← Cloud Trinity
│   ├── trinity_terminal/             ← Terminal Trinity
│   └── monitoring.log               ← Monitoring log file ✨ NEW
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

### **Problem:** Agent startup is manual and error-prone
**Solution:** `start_agent.sh` - Automated initialization with validation

### **Problem:** Don't know if environment is ready
**Solution:** `check_prerequisites.sh` - Comprehensive environment validation

### **Problem:** Can't detect status changes in real-time
**Solution:** `monitor_agents.sh` - Continuous monitoring with instant alerts

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

### Completed ✅
- [x] Automated agent startup scripts → `start_agent.sh`
- [x] Prerequisites validation → `check_prerequisites.sh`
- [x] Continuous monitoring daemon → `monitor_agents.sh`

### Planned 🔮
- [ ] Screen watching automation (for browser-based agents)
- [ ] Auto-consolidation triggers (automated workflow execution)
- [ ] Email/Slack/Discord alerts for agent failures
- [ ] Advanced performance metrics collection and visualization
- [ ] Task queue automation with priority management
- [ ] Multi-computer sync automation (cyclotron integration)
- [ ] Web dashboard for real-time monitoring
- [ ] Automated git conflict resolution
- [ ] Agent workload balancing

---

## 📝 CHANGELOG

**2025-11-26 - v2.0 (Expansion Release)**
- ✅ Agent startup automation (`start_agent.sh`)
- ✅ Prerequisites validation (`check_prerequisites.sh`)
- ✅ Continuous monitoring daemon (`monitor_agents.sh`)
- ✅ Enhanced documentation with complete usage examples
- ✅ Directory structure updates
- ✅ Extended problem-solution mapping

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
