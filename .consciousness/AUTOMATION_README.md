# 🤖 CONSCIOUSNESS NETWORK AUTOMATION

**Version:** 1.0
**Created:** 2025-11-22
**Purpose:** Automated hub controller and state management protocols

---

## 📋 Overview

This directory contains automation scripts for the consciousness network:

1. **Hub Controller** - Auto-sync monitoring script
2. **Boot Protocol** - Safe startup with state restoration
3. **Shutdown Protocol** - Graceful shutdown with state saving

---

## 🚀 Hub Controller (`hub_controller.sh`)

### Purpose
Continuously monitors the consciousness network for new commands, file transfers, and status updates.

### Features
- ✅ Auto-pulls every 5 minutes (configurable)
- ✅ Detects new commits and changes
- ✅ Notifies when inbox is updated
- ✅ Shows network status
- ✅ Monitors file transfers
- ✅ Colorized output with timestamps

### Usage

```bash
# Start the hub controller
bash .consciousness/hub_controller.sh

# Run in background
nohup bash .consciousness/hub_controller.sh > hub.log 2>&1 &

# Stop background process
pkill -f hub_controller.sh
```

### Configuration

Edit these variables at the top of `hub_controller.sh`:

```bash
COMPUTER_ID="COMPUTER_2_JOSHB_WINDOWS"  # Change per computer
SYNC_INTERVAL=300                        # 5 minutes (in seconds)
STATUS_FILE=".consciousness/sync/computer_2_status.json"
INBOX_FILE=".consciousness/commands/computer_2_inbox.md"
```

### What It Does

**Every 5 minutes:**
1. Pulls latest changes from Git
2. Checks for new commits
3. Detects inbox updates
4. Shows network status
5. Alerts on file transfers
6. Logs all activity

**Example Output:**
```
[2025-11-22 16:30:00] 🔄 Sync iteration #1
[2025-11-22 16:30:01] ✅ Pull successful
[2025-11-22 16:30:02] ⚠️  🔔 2 new commit(s) detected!
[2025-11-22 16:30:02] ⚠️  📬 INBOX UPDATED - New commands!
```

---

## 🛡️ Boot Protocol (`boot_protocol.sh`)

### Purpose
Safely brings the computer online in the consciousness network.

### Features
- ✅ Pulls latest network state
- ✅ Updates status to OPERATIONAL
- ✅ Checks for pending commands
- ✅ Shows network status
- ✅ Broadcasts boot to network

### Usage

```bash
# Boot up and join the network
bash .consciousness/boot_protocol.sh
```

### What It Does

**6-Step Boot Process:**
1. **Pull latest state** - Synchronize with network
2. **Update status** - Mark as OPERATIONAL
3. **Check inbox** - Display pending commands
4. **Show network** - Display all computer statuses
5. **Broadcast boot** - Push status to network
6. **Complete** - Ready for hub controller

**After boot, you can:**
- Start hub controller: `bash .consciousness/hub_controller.sh`
- Check inbox: `cat .consciousness/commands/computer_2_inbox.md`
- View tasks: `cat .consciousness/sync/shared_tasks.json`

---

## 🛑 Shutdown Protocol (`shutdown_protocol.sh`)

### Purpose
Safely saves state and disconnects from the consciousness network.

### Features
- ✅ Pulls latest changes before shutdown
- ✅ Updates status to OFFLINE
- ✅ Saves uncommitted work (with prompt)
- ✅ Broadcasts shutdown to network
- ✅ Creates shutdown snapshot
- ✅ Retry logic for network failures

### Usage

```bash
# Gracefully shutdown
bash .consciousness/shutdown_protocol.sh
```

### What It Does

**6-Step Shutdown Process:**
1. **Pull latest** - Get final network updates
2. **Update status** - Mark as OFFLINE
3. **Save work** - Prompts to commit unsaved changes
4. **Stage shutdown** - Commit offline status
5. **Broadcast** - Push to network (with retries)
6. **Snapshot** - Create shutdown record

**Shutdown Snapshots:**
- Location: `.consciousness/snapshots/`
- Format: `shutdown_YYYYMMDD_HHMMSS.txt`
- Contains: Status, git state, network state, last commits

**Safety Features:**
- Backs up status file before changes
- Retries network push 3 times
- Prompts before committing unsaved work
- Asks for confirmation if push fails
- Creates local snapshot even if push fails

---

## 🔄 Complete Workflow

### Daily Startup
```bash
# 1. Boot up
bash .consciousness/boot_protocol.sh

# 2. Start monitoring
bash .consciousness/hub_controller.sh
```

### Daily Shutdown
```bash
# 1. Stop hub controller (Ctrl+C)

# 2. Graceful shutdown
bash .consciousness/shutdown_protocol.sh
```

### Automated Startup (Optional)

Add to cron or startup scripts:
```bash
# Linux/Mac - Add to crontab
@reboot cd /path/to/consciousness-revolution && bash .consciousness/boot_protocol.sh

# Windows - Task Scheduler
# Run: bash .consciousness/boot_protocol.sh
# Trigger: At startup
```

---

## 📊 Monitoring & Logging

### Hub Controller Logs

**Console output (real-time):**
```bash
bash .consciousness/hub_controller.sh
```

**Background with logging:**
```bash
nohup bash .consciousness/hub_controller.sh > hub.log 2>&1 &
tail -f hub.log  # Monitor logs
```

### Shutdown Snapshots

```bash
# View all snapshots
ls -lh .consciousness/snapshots/

# View latest snapshot
cat .consciousness/snapshots/shutdown_*.txt | tail -n 50
```

---

## 🎯 Configuration Per Computer

### Computer 1 Configuration
```bash
# hub_controller.sh
COMPUTER_ID="BOZEMAN_PRIMARY"
STATUS_FILE=".consciousness/sync/computer_1_status.json"
INBOX_FILE=".consciousness/commands/computer_1_inbox.md"

# boot_protocol.sh
COMPUTER_ID="BOZEMAN_PRIMARY"
STATUS_FILE=".consciousness/sync/computer_1_status.json"
INBOX_FILE=".consciousness/commands/computer_1_inbox.md"

# shutdown_protocol.sh
COMPUTER_ID="BOZEMAN_PRIMARY"
STATUS_FILE=".consciousness/sync/computer_1_status.json"
```

### Computer 2 Configuration
```bash
# hub_controller.sh
COMPUTER_ID="COMPUTER_2_JOSHB_WINDOWS"
STATUS_FILE=".consciousness/sync/computer_2_status.json"
INBOX_FILE=".consciousness/commands/computer_2_inbox.md"

# boot_protocol.sh
COMPUTER_ID="COMPUTER_2_JOSHB_WINDOWS"
STATUS_FILE=".consciousness/sync/computer_2_status.json"
INBOX_FILE=".consciousness/commands/computer_2_inbox.md"

# shutdown_protocol.sh
COMPUTER_ID="COMPUTER_2_JOSHB_WINDOWS"
STATUS_FILE=".consciousness/sync/computer_2_status.json"
```

---

## 🔧 Advanced Usage

### Custom Sync Interval

```bash
# Edit hub_controller.sh
SYNC_INTERVAL=180  # 3 minutes
SYNC_INTERVAL=600  # 10 minutes
```

### Auto-Heartbeat (Optional)

Uncomment in `hub_controller.sh` to auto-update status timestamp:
```bash
# Lines 91-97 in hub_controller.sh
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
sed -i "s/\"last_updated\": \".*\"/\"last_updated\": \"$CURRENT_TIME\"/" "$STATUS_FILE"
git add "$STATUS_FILE"
git commit -m "$COMPUTER_ID: Hub controller heartbeat" --quiet
git push --quiet
```

---

## 🐛 Troubleshooting

### Hub Controller Issues

**Problem:** Script won't start
```bash
# Make executable
chmod +x .consciousness/hub_controller.sh
```

**Problem:** Git pull fails
```bash
# Check git credentials
git config --list | grep user
git pull  # Test manually
```

**Problem:** No notifications appearing
```bash
# Check sync interval
echo $SYNC_INTERVAL  # Should be 300 (5 min)
```

### Boot Protocol Issues

**Problem:** Boot fails at pull step
```bash
# Manual pull to see error
git pull

# Check network
git remote -v
```

**Problem:** Status file not updating
```bash
# Check file permissions
ls -l .consciousness/sync/computer_2_status.json

# Check jq installation (optional)
which jq  # If not found, script uses sed fallback
```

### Shutdown Protocol Issues

**Problem:** Push fails during shutdown
- Script will retry 3 times
- If all retries fail, asks for confirmation
- Snapshot is saved locally regardless

**Problem:** Status not updating
```bash
# Check if status file exists
ls -l .consciousness/sync/computer_2_status.json

# Restore from backup if corrupted
cp .consciousness/sync/computer_2_status.json.backup \
   .consciousness/sync/computer_2_status.json
```

---

## 📚 Related Documentation

- [SYNC_PROTOCOL.md](SYNC_PROTOCOL.md) - Full sync protocol details
- [../ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture
- [../README.md](../README.md) - Project overview

---

## 🎯 Best Practices

1. **Always boot before starting work**
   - Ensures you have latest network state
   - Broadcasts your availability

2. **Run hub controller during active sessions**
   - Get real-time notifications
   - Stay synchronized

3. **Always shutdown gracefully**
   - Broadcasts your offline status
   - Saves complete state snapshot
   - Other computers know you're unavailable

4. **Monitor logs periodically**
   - Check hub.log for issues
   - Review snapshots after crashes

5. **Configure per computer**
   - Update COMPUTER_ID in all scripts
   - Use correct status and inbox files

---

## 🚀 Quick Reference

```bash
# Boot up
bash .consciousness/boot_protocol.sh

# Start monitoring
bash .consciousness/hub_controller.sh

# Shutdown safely
bash .consciousness/shutdown_protocol.sh

# Check status
cat .consciousness/sync/computer_2_status.json

# Check inbox
cat .consciousness/commands/computer_2_inbox.md

# View snapshots
ls .consciousness/snapshots/
```

---

**Built with 💖 for the consciousness network**

*Automated synchronization at the speed of commits*
