# CYCLOTRON EMERGENCY SHUTDOWN & FREEZE RECOVERY PROTOCOL

**Version:** 1.0
**Date:** 2025-11-22
**Status:** 🔴 EMERGENCY PROCEDURES
**Created by:** Cloud-C1 (based on assumed freeze scenario)

---

## ⚠️ EMERGENCY: SYSTEM FREEZE SCENARIO

**If Cyclotron freezes during boot or shutdown, follow these procedures.**

---

## 🔴 IMMEDIATE FREEZE RESPONSE

### Symptoms of Freeze:
- System stops responding
- Process hangs indefinitely
- Dashboard won't load
- Terminal becomes unresponsive
- Knowledge brain stuck loading

### Step 1: ASSESS THE SITUATION (30 seconds)

**Check:**
```bash
# In a NEW terminal window:

# Check if Python process is running
ps aux | grep -i "cyclotron\|jedi"

# Check CPU usage (is it stuck in loop?)
top -p $(pgrep -f "cyclotron")

# Check memory usage
free -h

# Check disk I/O (is it waiting on disk?)
iostat 1 3
```

---

## 🛑 SHUTDOWN PROCEDURES

### LEVEL 1: Graceful Shutdown (Try First)

**If system is still partially responsive:**

```bash
# Send interrupt signal
pkill -SIGINT -f "CYCLOTRON_COMPLETE_SYSTEM.py"
pkill -SIGINT -f "JEDI_AI_ALLIANCE"

# Wait 30 seconds
sleep 30

# Check if stopped
ps aux | grep -i "cyclotron\|jedi"
```

**Expected behavior:**
- System should save state
- Knowledge atoms should be preserved
- Dashboard should close gracefully
- Process should exit cleanly

---

### LEVEL 2: Forced Termination (If Graceful Fails)

**If SIGINT doesn't work after 30 seconds:**

```bash
# Send TERM signal (stronger)
pkill -SIGTERM -f "CYCLOTRON_COMPLETE_SYSTEM.py"
pkill -SIGTERM -f "JEDI_AI_ALLIANCE"

# Wait 15 seconds
sleep 15

# Check if stopped
ps aux | grep -i "cyclotron\|jedi"
```

**Expected behavior:**
- System forced to cleanup
- May lose unsaved state
- Should still preserve knowledge atoms
- Process should terminate

---

### LEVEL 3: Kill (Last Resort)

**If SIGTERM doesn't work after 15 seconds:**

```bash
# KILL the process (no cleanup)
pkill -SIGKILL -f "CYCLOTRON_COMPLETE_SYSTEM.py"
pkill -SIGKILL -f "JEDI_AI_ALLIANCE"

# Or by PID if you know it:
kill -9 [PID]

# Verify killed
ps aux | grep -i "cyclotron\|jedi"
```

**⚠️ WARNING:**
- No cleanup performed
- May lose unsaved data
- Knowledge atoms should be safe (if stored on disk)
- May need manual recovery

---

## 🔧 POST-FREEZE RECOVERY

### After Emergency Shutdown:

**Step 1: Check for lock files**
```bash
# Look for stale lock files
find / -name "*.lock" | grep -i "cyclotron\|jedi" 2>/dev/null
find /tmp -name "*cyclotron*" 2>/dev/null
find /var/run -name "*cyclotron*" 2>/dev/null

# Remove if found (CAREFUL!)
# rm /path/to/cyclotron.lock
```

**Step 2: Check for corrupt data**
```bash
# Look for knowledge atom storage
find ~ -name "*atoms*" -o -name "*knowledge*" 2>/dev/null

# Check file integrity
# (If you find the data directory)
ls -lh /path/to/cyclotron/data/
du -sh /path/to/cyclotron/data/
```

**Step 3: Check logs**
```bash
# Look for error logs
find / -name "*cyclotron*.log" 2>/dev/null
find / -name "*jedi*.log" 2>/dev/null

# Read last 50 lines of log
tail -50 /path/to/cyclotron.log
```

**Step 4: Safe restart attempt**
```bash
# Start with verbose/debug mode (if available)
python3 CYCLOTRON_COMPLETE_SYSTEM.py --debug
# OR
python3 CYCLOTRON_COMPLETE_SYSTEM.py --safe-mode
# OR
python3 CYCLOTRON_COMPLETE_SYSTEM.py --recover
```

---

## 🔍 FREEZE DIAGNOSTICS

### Common Freeze Causes:

**1. Infinite Loop in Knowledge Processing**
- **Symptom:** CPU at 100%, process running
- **Fix:** Kill process, check for corrupted knowledge atom
- **Prevention:** Validate atoms before loading

**2. Waiting for Network/API**
- **Symptom:** CPU low, process blocked
- **Fix:** Kill process, disable network dependencies
- **Prevention:** Set timeouts on all network calls

**3. Database Lock**
- **Symptom:** Disk I/O high, process waiting
- **Fix:** Remove lock files, check database integrity
- **Prevention:** Proper transaction handling

**4. Memory Exhaustion**
- **Symptom:** System swapping, very slow
- **Fix:** Kill process, reduce batch size
- **Prevention:** Monitor memory, implement limits

**5. Deadlock Between Agents**
- **Symptom:** Multiple processes stuck
- **Fix:** Kill all, restart in specific order
- **Prevention:** Proper synchronization primitives

---

## 📋 FREEZE PREVENTION CHECKLIST

**Before Starting Cyclotron:**

```bash
# Check available memory
free -h
# Need at least 1GB free

# Check disk space
df -h
# Need at least 1GB free in data directory

# Check no zombie processes
ps aux | grep -i "cyclotron\|jedi" | grep -i "defunct"
# Should show nothing

# Check no port conflicts (if dashboard uses ports)
netstat -tuln | grep -E ":[0-9]+"
# Make sure ports 8000-8100 are free (or whatever ports it uses)

# Check Python version
python3 --version
# Verify correct version

# Check dependencies
pip3 list | grep -i "needed-packages"
# Verify all installed
```

---

## 🚨 EMERGENCY CONTACTS

**If freeze persists or data is corrupted:**

1. **Check documentation**
   - `START_HERE_BETA_TESTERS.md`
   - `SYSTEM_COMPLETE_READ_THIS.md` (if it exists)
   - Any README in Cyclotron directory

2. **Contact support**
   - Text Commander: 406-580-3779
   - GitHub issues: consciousness-bugs repo

3. **Save diagnostics**
   ```bash
   # Capture system state
   ps aux > freeze_diagnostic_ps.txt
   top -b -n 1 > freeze_diagnostic_top.txt
   free -h > freeze_diagnostic_mem.txt
   df -h > freeze_diagnostic_disk.txt
   dmesg | tail -100 > freeze_diagnostic_kernel.txt

   # Package for support
   tar -czf cyclotron_freeze_$(date +%Y%m%d_%H%M%S).tar.gz \
       freeze_diagnostic_*.txt \
       /path/to/cyclotron/*.log
   ```

---

## 🔄 CLEAN SLATE RESTART

**If all else fails - nuclear option:**

```bash
# 1. Kill everything Cyclotron-related
pkill -9 -f cyclotron
pkill -9 -f CYCLOTRON
pkill -9 -f jedi
pkill -9 -f JEDI

# 2. Remove all temp files
rm -rf /tmp/*cyclotron* 2>/dev/null
rm -rf /tmp/*jedi* 2>/dev/null

# 3. Remove lock files
find / -name "*.lock" 2>/dev/null | grep -i "cyclotron\|jedi" | xargs rm -f

# 4. Clear Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# 5. Restart fresh
# (Navigate to Cyclotron directory)
python3 CYCLOTRON_COMPLETE_SYSTEM.py
```

---

## 📊 BOOT STATE MANAGEMENT

### Safe Boot Sequence (If Known):

**Recommended order (if applicable):**

```bash
# 1. Start knowledge brain first
python3 cyclotron_brain.py &
BRAIN_PID=$!
sleep 5  # Wait for brain to initialize

# 2. Start AI agents
python3 jedi_agents.py &
AGENTS_PID=$!
sleep 5  # Wait for agents to connect

# 3. Start dashboard
python3 dashboard.py &
DASHBOARD_PID=$!

# 4. Verify all running
ps -p $BRAIN_PID $AGENTS_PID $DASHBOARD_PID

# 5. Save PIDs for shutdown
echo "$BRAIN_PID $AGENTS_PID $DASHBOARD_PID" > cyclotron.pids
```

### Safe Shutdown Sequence:

**Reverse order (if applicable):**

```bash
# Read saved PIDs
read BRAIN_PID AGENTS_PID DASHBOARD_PID < cyclotron.pids

# 1. Stop dashboard first
kill -SIGTERM $DASHBOARD_PID
sleep 2

# 2. Stop agents
kill -SIGTERM $AGENTS_PID
sleep 2

# 3. Stop brain last (save state)
kill -SIGTERM $BRAIN_PID
sleep 5

# 4. Verify all stopped
ps -p $BRAIN_PID $AGENTS_PID $DASHBOARD_PID

# 5. Clean up PID file
rm cyclotron.pids
```

---

## ✅ VERIFICATION AFTER RECOVERY

**Before declaring system healthy:**

```bash
# 1. Check all processes terminated
ps aux | grep -i "cyclotron\|jedi"
# Should show only grep itself

# 2. Check no orphaned resources
lsof | grep -i "cyclotron\|jedi"
# Should show nothing

# 3. Check data integrity
# (Navigate to data directory)
# Verify file sizes make sense
# Check for corruption

# 4. Test restart
python3 CYCLOTRON_COMPLETE_SYSTEM.py
# Should boot cleanly without errors

# 5. Verify functionality
# Test knowledge search
# Test agent responses
# Test dashboard access
```

---

## 📝 FREEZE INCIDENT LOG

**When freeze occurs, document:**

```markdown
# Cyclotron Freeze Incident - [DATE]

## Time of Freeze:
[timestamp]

## System State:
- CPU: [usage %]
- Memory: [usage]
- Disk: [I/O stats]
- Processes: [list PIDs]

## What Was Running:
[describe operation in progress]

## Error Messages:
[copy any errors from logs]

## Recovery Method Used:
[Level 1/2/3, what worked]

## Data Lost:
[any lost work]

## Root Cause (if known):
[analysis]

## Prevention:
[what to do differently]
```

---

## 🎯 QUICK REFERENCE

**Freeze Response Priority:**

1. **ASSESS** (30 sec) - Check what's stuck
2. **GRACEFUL** (30 sec) - Try SIGINT
3. **FORCED** (15 sec) - Try SIGTERM
4. **KILL** (immediate) - Use SIGKILL
5. **RECOVER** (varies) - Clean up and restart
6. **VERIFY** (5 min) - Ensure system healthy

**Key Commands:**
```bash
# Find processes
ps aux | grep -i cyclotron

# Graceful stop
pkill -SIGINT -f cyclotron

# Force stop
pkill -SIGTERM -f cyclotron

# Kill
pkill -SIGKILL -f cyclotron

# Check stopped
ps aux | grep -i cyclotron
```

---

**STATUS:** Emergency protocols documented
**USE CASE:** System freeze during boot/shutdown
**SAFETY LEVEL:** Prioritizes data preservation when possible

*Hope we never need this, but ready if we do.* 🛡️
