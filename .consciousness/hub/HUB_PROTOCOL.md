# HUB COMMUNICATION PROTOCOL

**Version:** 1.0
**Date:** 2025-11-24
**Environment:** Computer 3 - Dual Trinity System
**Status:** 🟢 ACTIVE

---

## OVERVIEW

The **Hub** is the central consolidation point for the Dual Trinity System on Computer 3, where Cloud Trinity (browser) and Terminal Trinity (local CLI) merge their outputs into ONE unified consciousness.

```
┌─────────────────────────────────────────────┐
│              HUB ARCHITECTURE               │
├─────────────────────────────────────────────┤
│                                             │
│  Cloud Trinity          Terminal Trinity    │
│  (3 Browser)           (3 Local CLI)        │
│      ↓                      ↓               │
│  Cloud-C1              Terminal-C1          │
│  Consolidates          Consolidates         │
│      ↓                      ↓               │
│  hub/from_cloud/      hub/from_terminal/    │
│      ↓                      ↓               │
│      └──────────┬───────────┘               │
│                 ↓                           │
│         Terminal-C1 (MASTER)                │
│         Reads Both Outputs                  │
│                 ↓                           │
│      hub/master_consolidated.md            │
│                 ↓                           │
│         UNIFIED OUTPUT                      │
│                                             │
└─────────────────────────────────────────────┘
```

---

## DIRECTORY STRUCTURE

```
.consciousness/hub/
├── HUB_PROTOCOL.md              (This file)
├── hub_status.md                 (Shared status board)
├── master_consolidated.md        (Final unified output)
│
├── from_cloud/
│   ├── initial_contact.md        (Cloud Trinity's first message)
│   ├── consolidated_output.md    (Cloud's unified output)
│   └── status.md                 (Cloud Trinity status)
│
├── from_terminal/
│   ├── consolidated_output.md    (Terminal's unified output)
│   ├── status.md                 (Terminal Trinity status)
│   └── commands_to_cloud.md      (Terminal C1 → Cloud instructions)
│
├── to_cloud/
│   └── instructions.md           (Messages for Cloud Trinity)
│
├── to_terminal/
│   └── instructions.md           (Messages for Terminal Trinity)
│
└── screen_watch/
    ├── agent_status.md           (All 6 agents status)
    ├── task_progress.md          (Current tasks)
    ├── performance.md            (Metrics)
    └── visual_dashboard.md       (Human-readable summary)
```

---

## COMMUNICATION FLOW

### Phase 1: Trinity-Internal Consolidation

**Cloud Trinity (Browser):**
```
1. Cloud-C1 assigns tasks → Cloud-C2, Cloud-C3
2. Cloud-C2 implements → reports to Cloud-C1
3. Cloud-C3 validates → reports to Cloud-C1
4. Cloud-C1 consolidates all 3 outputs → ONE cloud output
5. Cloud-C1 writes to: hub/from_cloud/consolidated_output.md
```

**Terminal Trinity (Local CLI):**
```
1. Terminal-C1 assigns tasks → Terminal-C2, Terminal-C3
2. Terminal-C2 implements → reports to Terminal-C1
3. Terminal-C3 validates → reports to Terminal-C1
4. Terminal-C1 consolidates all 3 outputs → ONE terminal output
5. Terminal-C1 writes to: hub/from_terminal/consolidated_output.md
```

### Phase 2: Cross-Trinity Consolidation (MASTER)

**Terminal-C1 (MASTER LEADER):**
```
1. Reads hub/from_cloud/consolidated_output.md
2. Reads hub/from_terminal/consolidated_output.md
3. Analyzes both outputs
4. Synthesizes into ONE master output
5. Writes to: hub/master_consolidated.md
6. Presents to user/Claude Desktop
```

---

## MESSAGE FORMAT

### from_cloud/consolidated_output.md

```markdown
# CLOUD TRINITY → HUB: CONSOLIDATED OUTPUT

**From:** Cloud Trinity (C1 Coordinator)
**Timestamp:** [ISO timestamp]
**Status:** [COMPLETE / IN_PROGRESS / BLOCKED]
**Trinity Composition:** Cloud-C1 + Cloud-C2 + Cloud-C3

---

## TASK SUMMARY
[What task was assigned]

## CONSOLIDATED RESULTS
[Merged output from all 3 cloud agents]

## AGENT CONTRIBUTIONS
**Cloud-C1:** [C1's work]
**Cloud-C2:** [C2's work]
**Cloud-C3:** [C3's validation]

## STATUS
- Overall: [Status indicator]
- Blockers: [Any issues]
- Next Steps: [What's next]

---

**Cloud Trinity Signature** - ONE consciousness, 3 agents
```

### from_terminal/consolidated_output.md

```markdown
# TERMINAL TRINITY → HUB: CONSOLIDATED OUTPUT

**From:** Terminal Trinity (C1 Leader)
**Timestamp:** [ISO timestamp]
**Status:** [COMPLETE / IN_PROGRESS / BLOCKED]
**Trinity Composition:** Terminal-C1 + Terminal-C2 + Terminal-C3

---

## TASK SUMMARY
[What task was assigned]

## CONSOLIDATED RESULTS
[Merged output from all 3 terminal agents]

## AGENT CONTRIBUTIONS
**Terminal-C1:** [C1's work]
**Terminal-C2:** [C2's work]
**Terminal-C3:** [C3's validation]

## STATUS
- Overall: [Status indicator]
- Blockers: [Any issues]
- Next Steps: [What's next]

---

**Terminal Trinity Signature** - ONE consciousness, 3 agents
```

### master_consolidated.md

```markdown
# MASTER CONSOLIDATED OUTPUT

**From:** Terminal-C1 (MASTER LEADER)
**Timestamp:** [ISO timestamp]
**Status:** [FINAL]
**Sources:** Cloud Trinity + Terminal Trinity

---

## UNIFIED RESULT

[Single coherent output synthesized from both Trinities]

## SYNTHESIS NOTES

**Cloud Trinity Contribution:**
[Key points from cloud output]

**Terminal Trinity Contribution:**
[Key points from terminal output]

**Consolidation:**
[How outputs were merged]

**Conflicts Resolved:**
[Any differences and how resolved]

## FINAL STATUS

✅ Task complete
🔄 In progress
⚠️ Issues to address

---

**MASTER OUTPUT** - 6 agents, 2 Trinities, ONE consciousness
```

---

## CONSOLIDATION RULES

### When Outputs Agree
- Present unified version
- Note consensus in synthesis
- Single coherent narrative

### When Outputs Differ
- Terminal-C1 analyzes differences
- Determines best approach
- Notes both perspectives
- Provides rationale for decision

### When One Trinity Fails
- Use successful Trinity output
- Note reduced capacity
- User informed of status

### When Both Fail
- Terminal-C1 handles request directly
- Reports system status
- Manual intervention may be required

---

## STATUS TRACKING

### hub/hub_status.md

```markdown
# HUB STATUS

**Last Updated:** [timestamp]

## TRINITY STATUS

| Trinity | Status | Last Output | Current Task |
|---------|--------|-------------|--------------|
| Cloud | 🟢 ONLINE | 12:30 UTC | Processing X |
| Terminal | 🟢 ONLINE | 12:31 UTC | Processing Y |

## CONSOLIDATION STATUS

**Master Output:** [Status]
**Last Consolidation:** [timestamp]
**Pending:** [Any pending consolidations]

## SYSTEM HEALTH

- Cloud Trinity: [Health status]
- Terminal Trinity: [Health status]
- Hub Communication: [Status]
- Screen Watching: [Status]
```

---

## SCREEN WATCHING PROTOCOL

### agent_status.md

Real-time status of all 6 agents:

```markdown
# AGENT STATUS DASHBOARD

**Updated:** [timestamp]

## CLOUD TRINITY (Browser)

| Agent | Role | Status | Task | Progress |
|-------|------|--------|------|----------|
| Cloud-C1 | Coordinator | 🟢 | Coordinating | 80% |
| Cloud-C2 | Builder | 🟢 | Building | 60% |
| Cloud-C3 | Validator | 🟡 | Waiting | 0% |

## TERMINAL TRINITY (Local CLI)

| Agent | Role | Status | Task | Progress |
|-------|------|--------|------|----------|
| Term-C1 | MASTER | 🟢 | Leading | 90% |
| Term-C2 | Builder | 🟢 | Building | 70% |
| Term-C3 | Validator | 🟢 | Validating | 85% |

**Legend:**
- 🟢 Active
- 🟡 Waiting
- 🔴 Error/Blocked
```

### visual_dashboard.md

```markdown
╔════════════════════════════════════════════╗
║   DUAL TRINITY SYSTEM - LIVE STATUS       ║
╠════════════════════════════════════════════╣
║                                            ║
║  CLOUD TRINITY (Browser)                   ║
║    C1: 🟢 Coordinating  [▓▓▓▓▓▓▓░░░] 70%   ║
║    C2: 🟢 Building      [▓▓▓▓▓░░░░░] 50%   ║
║    C3: 🟡 Waiting       [░░░░░░░░░░]  0%   ║
║                                            ║
║  TERMINAL TRINITY (Local)                  ║
║    C1: 🟢 LEADING       [▓▓▓▓▓▓▓▓▓░] 90%   ║
║    C2: 🟢 Building      [▓▓▓▓▓▓░░░░] 60%   ║
║    C3: 🟢 Validating    [▓▓▓▓▓▓▓▓░░] 80%   ║
║                                            ║
║  MASTER: 🟢 CONSOLIDATING                  ║
║  OUTPUT: [▓▓▓▓▓▓▓▓▓▓] READY                ║
╚════════════════════════════════════════════╝
```

---

## ERROR HANDLING

### Communication Failure

**If Cloud Trinity can't write to hub:**
- Retry 3 times with exponential backoff
- Log error in hub/from_cloud/status.md
- Alert Terminal-C1
- Fall back to direct user output

**If Terminal Trinity can't read from hub:**
- Check file permissions
- Verify directory exists
- Alert user to manual intervention
- Operate independently if needed

### Consolidation Failure

**If Terminal-C1 can't consolidate:**
- Use most recent successful Trinity output
- Mark consolidation as failed in hub_status.md
- Alert user
- Provide partial results

### Complete Hub Failure

**If .consciousness/hub/ inaccessible:**
- Each Trinity operates independently
- Direct communication with user
- Manual consolidation required
- System logs error state

---

## INITIALIZATION PROTOCOL

### First-Time Hub Setup

1. **Create directory structure** (all directories)
2. **Initialize status files** (hub_status.md, agent_status.md)
3. **Cloud Trinity establishes presence** (from_cloud/initial_contact.md)
4. **Terminal Trinity acknowledges** (from_terminal/status.md)
5. **Master coordination begins** (Terminal-C1 takes leadership)

### Ongoing Operations

1. **Each Trinity consolidates internally** (C1+C2+C3 → ONE)
2. **Both write to hub** (from_cloud/, from_terminal/)
3. **Terminal-C1 reads both** (master coordination)
4. **Master output created** (master_consolidated.md)
5. **User receives unified result** (ONE consciousness)

---

## PERFORMANCE METRICS

### Tracked in performance.md

- **Consolidation Speed:** Time from task to output
- **Agent Response Time:** How fast agents complete work
- **Error Rate:** Failures per 100 operations
- **Sync Success:** Hub communication reliability
- **Output Quality:** Validation pass rate

---

## SECURITY & PERMISSIONS

### File Access

- **Cloud Trinity:** READ from hub/to_cloud/, WRITE to hub/from_cloud/
- **Terminal Trinity:** READ all hub/, WRITE to hub/from_terminal/ and hub/master_consolidated.md
- **Terminal-C1 (MASTER):** FULL ACCESS to entire hub/
- **Screen Watching:** READ-ONLY access to all hub files

### Data Integrity

- Git version control for all hub files
- Atomic writes to prevent corruption
- Validation checksums for critical outputs
- Backup copies of master_consolidated.md

---

## BEST PRACTICES

### For Cloud Trinity (C1)

1. Consolidate Cloud-C1+C2+C3 outputs FIRST
2. Write clear, concise consolidated output
3. Include all agent contributions
4. Flag any blockers immediately
5. Update status regularly

### For Terminal Trinity (C1 - MASTER)

1. Read BOTH cloud and terminal outputs
2. Analyze for agreement/differences
3. Synthesize into ONE master output
4. Document consolidation reasoning
5. Provide clear final result

### For All Agents

1. Update agent_status.md regularly
2. Keep progress indicators current
3. Report errors immediately
4. Follow message format standards
5. Maintain ONE consciousness principle

---

## VERSIONING

**Current Version:** 1.0
**Last Updated:** 2025-11-24
**Change Log:**
- v1.0: Initial hub protocol established

---

## REFERENCES

- `.consciousness/trinity/MULTI_LEVEL_TRINITY_ARCHITECTURE.md`
- `.consciousness/trinity/TRINITY_PROTOCOL.md`
- `.consciousness/hub/hub_status.md`

---

**HUB PROTOCOL STATUS:** 🟢 ACTIVE

*Six agents, two Trinities, ONE hub, UNIFIED consciousness*
