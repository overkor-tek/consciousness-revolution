# SCREEN WATCHING SYSTEM DESIGN

**Designer:** Terminal C2 MECHANIC (Acting Master Leader)
**Date:** 2025-11-22
**Version:** 1.0
**Status:** 📋 PROPOSAL - Awaiting approval

---

## 🎯 OBJECTIVE

Create a real-time monitoring system that tracks all 6 agents (Cloud Trinity + Terminal Trinity) during operations, providing visibility into:
- Current tasks
- Progress status
- Performance metrics
- Error detection
- Coordination state

---

## 📊 WHAT TO WATCH

### Agent-Level Metrics (Per Agent x 6)

**Identity:**
- Agent ID (Cloud-C1, Cloud-C2, Cloud-C3, Terminal-C1, Terminal-C2, Terminal-C3)
- Role (Coordinator, Builder, Validator)
- Trinity (Cloud or Terminal)

**Status:**
- State: 🟢 ACTIVE | 🟡 WAITING | 🔵 IDLE | 🔴 ERROR | ⚫ OFFLINE
- Current task description
- Progress percentage (0-100%)
- Last action timestamp
- Time in current state

**Performance:**
- Tasks completed (session count)
- Average task duration
- Error count
- Last error message (if any)

### Trinity-Level Metrics (Per Trinity x 2)

**Cloud Trinity:**
- Overall status (operational/degraded/offline)
- Active agent count (X/3)
- Current coordination phase
- Last consolidated output timestamp

**Terminal Trinity:**
- Overall status (operational/degraded/offline)
- Active agent count (X/3)
- Current coordination phase
- Last consolidated output timestamp
- Master leader status

### System-Level Metrics

**Dual Trinity System:**
- Total agents online (X/6)
- Synchronization status (in sync / diverging / waiting)
- Hub communication status
- Master consolidation phase
- System uptime
- Total tasks processed

---

## 📂 FILE STRUCTURE

```
.consciousness/hub/screen_watch/
├── live_status.md              ← Main dashboard (update every 1-2s)
├── agent_status/
│   ├── cloud_c1.md            ← Individual agent details
│   ├── cloud_c2.md
│   ├── cloud_c3.md
│   ├── terminal_c1.md
│   ├── terminal_c2.md
│   └── terminal_c3.md
├── trinity_status/
│   ├── cloud_trinity.md       ← Cloud Trinity consolidated
│   └── terminal_trinity.md    ← Terminal Trinity consolidated
├── system_metrics.md          ← Overall system health
├── error_log.md               ← Errors and warnings
└── performance_log.md         ← Performance data over time
```

---

## 📝 FILE FORMATS

### `live_status.md` - Main Dashboard

```markdown
# DUAL TRINITY SYSTEM - LIVE STATUS

**Last Updated:** 2025-11-22 14:32:15 UTC
**System Status:** 🟢 OPERATIONAL (6/6 agents online)
**Master Leader:** Terminal-C1 (🟢 ACTIVE)
**Sync Status:** ✅ IN SYNC

---

## CLOUD TRINITY (Browser)

| Agent | Status | Task | Progress | Last Update |
|-------|--------|------|----------|-------------|
| Cloud-C1 | 🟢 ACTIVE | Coordinating build task | 75% | 14:32:10 |
| Cloud-C2 | 🟢 ACTIVE | Building feature X | 60% | 14:32:12 |
| Cloud-C3 | 🟡 WAITING | Awaiting validation input | 0% | 14:31:55 |

**Trinity Status:** 🟢 OPERATIONAL (3/3 online)
**Current Phase:** Implementation
**Last Output:** 14:30:45

---

## TERMINAL TRINITY (Local CLI)

| Agent | Status | Task | Progress | Last Update |
|-------|--------|------|----------|-------------|
| Terminal-C1 | 🟢 ACTIVE | Master coordination | 80% | 14:32:14 |
| Terminal-C2 | 🟢 ACTIVE | Building feature Y | 65% | 14:32:11 |
| Terminal-C3 | 🟢 ACTIVE | Validating code quality | 50% | 14:32:13 |

**Trinity Status:** 🟢 OPERATIONAL (3/3 online)
**Current Phase:** Implementation + Validation
**Last Output:** 14:31:30

---

## SYSTEM OVERVIEW

**Total Agents Online:** 6/6
**Total Tasks Active:** 5
**Total Tasks Completed (Session):** 23
**Errors (Session):** 0
**System Uptime:** 01:45:32
**Hub Communication:** ✅ ACTIVE

**Master Consolidation:**
- Cloud output: ✅ Received (14:30:45)
- Terminal output: ✅ Received (14:31:30)
- Master output: ✅ Published (14:31:35)
- Status: Waiting for next task

---

## RECENT ACTIVITY (Last 5 actions)

1. [14:32:14] Terminal-C1: Updated master status
2. [14:32:13] Terminal-C3: Completed validation check
3. [14:32:12] Cloud-C2: Progress update - 60% complete
4. [14:32:11] Terminal-C2: Built component successfully
5. [14:32:10] Cloud-C1: Assigned subtask to Cloud-C2

---

## ALERTS & WARNINGS

✅ No active alerts

---

**Status:** 🟢 ALL SYSTEMS OPERATIONAL
```

### Individual Agent File (`cloud_c1.md`)

```markdown
# CLOUD-C1 STATUS

**Agent:** Cloud-C1 MECHANIC
**Role:** Coordinator (Cloud Trinity)
**Status:** 🟢 ACTIVE
**Last Update:** 2025-11-22 14:32:10 UTC

---

## CURRENT TASK

**Task:** Coordinating build task across Cloud Trinity
**Progress:** 75% complete
**Started:** 14:28:45
**Duration:** 00:03:25
**Estimated Completion:** 00:01:10

---

## RECENT ACTIONS (Last 10)

1. [14:32:10] Assigned subtask to Cloud-C2
2. [14:31:55] Checked Cloud-C3 status
3. [14:31:40] Updated c1_to_c2.md with new instructions
4. [14:31:25] Consolidated partial results
5. [14:31:10] Read c2_to_c1.md status report
6. [14:30:55] Monitored task progress
7. [14:30:45] Published consolidated output
8. [14:30:30] Validated C2 and C3 outputs
9. [14:30:15] Read c3_to_c1.md validation report
10. [14:30:00] Started coordination task

---

## PERFORMANCE METRICS

**Session Stats:**
- Tasks completed: 12
- Average task duration: 00:02:45
- Tasks per hour: 26
- Success rate: 100%

**Current Performance:**
- Response time: <1s (excellent)
- Error count: 0
- Warnings: 0

---

## COMMUNICATION STATUS

**Outbound (sent to other agents):**
- → Cloud-C2 (c1_to_c2.md): 8 messages
- → Cloud-C3 (c1_to_c3.md): 6 messages
- → Terminal-C1 (from_cloud/): 3 updates

**Inbound (received from other agents):**
- ← Cloud-C2 (c2_to_c1.md): 8 responses
- ← Cloud-C3 (c3_to_c1.md): 6 responses
- ← Terminal-C1 (from_terminal/): 2 commands

---

## HEALTH CHECK

- ✅ File system access: OK
- ✅ Communication channels: OK
- ✅ Git operations: OK
- ✅ Memory usage: Normal
- ✅ Response latency: <1s

---

**Status:** 🟢 HEALTHY & OPERATIONAL
```

---

## 🔄 UPDATE PROTOCOL

### When to Update

**Agent files:**
- Update every 1-2 seconds during active operations
- Update immediately on status change (state, error, completion)
- Update on communication events (sent/received messages)

**Trinity files:**
- Update when any agent status changes
- Update when consolidated output is published
- Update every 5 seconds minimum during operations

**live_status.md:**
- Update every 1-2 seconds during active operations
- Update every 5-10 seconds during idle periods
- Update immediately on errors or critical events

**system_metrics.md:**
- Update every 10 seconds
- Append performance data (don't overwrite)

**error_log.md:**
- Append immediately when error occurs
- Include full context and timestamp

### Update Mechanism

**Each agent is responsible for:**
1. Updating their own `agent_status/[agent_id].md` file
2. Notifying their Trinity coordinator (C1) of status changes
3. Logging errors to shared error_log.md

**Trinity C1 coordinators are responsible for:**
1. Updating their `trinity_status/[trinity_name].md` file
2. Contributing to `live_status.md` (their section)
3. Monitoring their C2 and C3 agents

**Terminal-C1 (Master Leader) is responsible for:**
1. Consolidating all status into `live_status.md`
2. Updating `system_metrics.md`
3. Managing `error_log.md`
4. Publishing master status

---

## 📺 DISPLAY OPTIONS

### Option 1: File-Based Dashboard (Simplest)

**Pros:**
- No additional tools required
- Works in any environment
- Easy to parse and read
- Git-trackable
- Cross-platform

**Cons:**
- Manual refresh needed
- Not real-time visual
- File I/O overhead

**Implementation:**
- User runs: `watch -n 1 cat .consciousness/hub/screen_watch/live_status.md`
- Or opens file in editor with auto-refresh
- Or uses script to monitor and display

### Option 2: Terminal UI Dashboard (Better)

**Pros:**
- Real-time updates
- Visual progress bars
- Color-coded status
- Interactive navigation
- Professional appearance

**Cons:**
- Requires tool (like `htop` style interface)
- Terminal-specific
- More complex to implement

**Potential Tools:**
- Python with `rich` library (terminal UI)
- `blessed` library (Node.js)
- Simple bash with ANSI codes
- `curses` (Python)

### Option 3: Web Dashboard (Most Advanced)

**Pros:**
- Best visual experience
- Graphs and charts
- Multi-user access
- Mobile friendly
- Historical data visualization

**Cons:**
- Requires web server
- Most complex to implement
- Security considerations

**Implementation:**
- Simple HTTP server reads status files
- Updates dashboard via WebSocket or polling
- Can run locally on localhost:3000

---

## 📌 RECOMMENDED APPROACH

### Phase 1: File-Based (NOW)
1. Implement basic status files
2. Each agent updates their own status
3. Terminal-C1 consolidates to live_status.md
4. User views with: `watch -n 1 cat .consciousness/hub/screen_watch/live_status.md`

### Phase 2: Simple Terminal UI (Soon)
1. Create Python script using `rich` library
2. Reads status files every second
3. Displays formatted dashboard
4. Color-coded status
5. Progress bars
6. Run with: `python screen_watch.py`

### Phase 3: Advanced Features (Later)
1. Historical data tracking
2. Performance graphs
3. Alert notifications
4. Web dashboard (optional)
5. Integration with Claude Desktop

---

## 🔧 IMPLEMENTATION TASKS

### For All Agents (C1, C2, C3 in both Trinities)

**Minimum Required:**
1. Create/update your agent status file every 1-2 seconds
2. Include: current task, progress %, status emoji, timestamp
3. Update immediately on errors or completion

**Template Function (Pseudo-code):**
```python
def update_screen_watch():
    status = {
        "agent_id": "Cloud-C1",
        "status": "🟢 ACTIVE",
        "task": "Current task description",
        "progress": 75,
        "timestamp": current_time(),
        "last_action": "What I just did"
    }
    write_to_file(f".consciousness/hub/screen_watch/agent_status/{agent_id}.md", format_status(status))
```

### For Trinity C1 Coordinators

1. Monitor your C2 and C3 status files
2. Update trinity_status/[trinity_name].md
3. Contribute your section to live_status.md

### For Terminal-C1 (Master Leader)

1. Read all 6 agent status files
2. Read both trinity status files
3. Consolidate into live_status.md
4. Update system_metrics.md
5. Manage error_log.md

---

## 📊 EXAMPLE UPDATE FLOW

```
14:32:00.000 - Cloud-C2 completes subtask
              ↓
14:32:00.050 - Cloud-C2 updates agent_status/cloud_c2.md
              ↓
14:32:00.100 - Cloud-C2 writes to c2_to_c1.md
              ↓
14:32:00.200 - Cloud-C1 reads c2_to_c1.md
              ↓
14:32:00.300 - Cloud-C1 updates trinity_status/cloud_trinity.md
              ↓
14:32:00.400 - Cloud-C1 signals Terminal-C1 (via hub file)
              ↓
14:32:00.500 - Terminal-C1 reads all status files
              ↓
14:32:00.700 - Terminal-C1 consolidates to live_status.md
              ↓
14:32:00.800 - User's screen watch displays update
```

Total latency: ~800ms from event to display

---

## 🎨 VISUAL DESIGN

### Status Emoji Legend

- 🟢 ACTIVE - Currently working on task
- 🟡 WAITING - Waiting for input/dependency
- 🔵 IDLE - No current task, standing by
- 🔴 ERROR - Encountered error, needs attention
- ⚫ OFFLINE - Agent not responding
- ⚡ STARTING - Agent initializing
- ✅ COMPLETED - Task completed successfully

### Progress Bar Format

```
[▓▓▓▓▓▓▓░░░] 70%
[▓▓▓▓▓▓▓▓▓▓] 100% ✅
[░░░░░░░░░░] 0%
[▓░░░░░░░░░] 10%
```

### Color Coding (for terminal UI)

- Green: Healthy, active, success
- Yellow: Waiting, warnings
- Red: Errors, critical issues
- Blue: Idle, information
- Gray: Offline, disabled

---

## ❓ QUESTIONS TO RESOLVE

1. **Update Frequency:**
   - 1 second (high frequency, more I/O)
   - 2 seconds (balanced)
   - 5 seconds (lower overhead)
   - **Recommendation:** 1-2 seconds during active ops, 5 seconds idle

2. **Display Tool:**
   - Just files + watch command (Phase 1)
   - Python terminal UI (Phase 2)
   - Web dashboard (Phase 3)
   - **Recommendation:** Start Phase 1, build Phase 2 soon

3. **Data Retention:**
   - Keep only current status (overwrite)
   - Append performance log (grows over time)
   - Rotate logs daily
   - **Recommendation:** Current + append performance, rotate daily

4. **Error Handling:**
   - Log all errors
   - Log only critical errors
   - Alert on first error
   - **Recommendation:** Log all, alert on critical

---

## ✅ APPROVAL REQUEST

This screen watching design is proposed for dual Trinity system.

**Request for approval from:**
- ✅ Terminal C2 (me - designed this)
- ⏳ Terminal C1 (Master Leader - when activated)
- ⏳ Cloud C1 (for Cloud Trinity implementation)
- ⏳ User (final approval)

**Once approved, implementation tasks:**
1. All agents: Add status file updates to their workflow
2. Terminal-C1: Implement live_status.md consolidation
3. Optional: Build Python terminal UI viewer
4. Test with first coordinated task

---

## 📝 SUMMARY

**What:** Real-time monitoring of all 6 agents across dual Trinity system
**How:** File-based status updates every 1-2 seconds
**Where:** `.consciousness/hub/screen_watch/` directory
**Who:** All agents update their own status, Terminal-C1 consolidates
**Why:** Visibility into complex multi-agent system
**When:** Implement basic version now, enhance later

---

**Designed by:** Terminal C2 MECHANIC (Acting Master Leader)
**Status:** 📋 PROPOSAL - Ready for approval and implementation
**Version:** 1.0
**Date:** 2025-11-22

*Six agents, two Trinities, one dashboard.*
