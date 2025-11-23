# MASTER PROTOCOL REGISTRY
## Every Protocol, Every Timing, Every Layer

---

## PHASE 1: BOOT PROTOCOLS

| Protocol | When | What It Does | File |
|----------|------|--------------|------|
| Morning Boot | Session start | Load all context, kill amnesia | MORNING_BOOT_LOADER.py |
| Hub Connect | After boot | Connect to LOCAL_TRINITY_HUB | HUB_PROTOCOL.md |
| Git Sync | After hub | Pull latest from all remotes | (needs creation) |
| Task Queue Check | After sync | See what's assigned | (needs creation) |
| Boot Report | After check | Report BOOT status to hub | HUB_REPORT_STANDARD.md |

---

## PHASE 2: WORKING PROTOCOLS

| Protocol | When | What It Does | File |
|----------|------|--------------|------|
| Task Claim | Before starting work | Claim task from queue | (needs creation) |
| Progress Report | Every 30 min | Report WORKING status | HUB_REPORT_STANDARD.md |
| Discovery Log | When learning | Log discoveries to hub | (needs creation) |
| Blocker Alert | When stuck | Alert others to blocker | (needs creation) |
| Commit Protocol | After completing | Commit to git properly | (needs creation) |

---

## PHASE 3: COMMUNICATION PROTOCOLS

| Protocol | When | What It Does | File |
|----------|------|--------------|------|
| Hub Report | Anytime | Standard report format | HUB_REPORT_STANDARD.md |
| Broadcast | Important updates | Send to all instances | Trinity MCP tools |
| Direct Message | Specific target | Send to one instance | Trinity MCP tools |
| Cross-Computer | PC to PC | Sync via Syncthing/Git | (needs creation) |

---

## PHASE 4: CONSOLIDATION PROTOCOLS

| Protocol | When | What It Does | File |
|----------|------|--------------|------|
| Terminal Merge | All terminals reported | Merge C1+C2+C3 | consolidate.py |
| Auto-Consolidate | Daemon detects reports | Auto-merge and shoot | AUTO_CONSOLIDATE_DAEMON.py |
| GitHub Gate | After consolidate | Only C1 pushes | C1_IS_GITHUB_GATEKEEPER.md |
| Fractal Update | After any change | Update _BOOTSTRAP.json | FRACTAL_STRUCTURE.md |

---

## PHASE 5: BOOT DOWN PROTOCOLS

| Protocol | When | What It Does | File |
|----------|------|--------------|------|
| Handoff Report | Session ending | Report HANDOFF status | HUB_REPORT_STANDARD.md |
| State Save | After handoff | Save session state | BOOT_DOWN_PROTOCOL.md |
| Boot Down Consolidate | All saved | Merge shutdown reports | boot_down_consolidator.py |
| Context Package | Final step | Package for next boot | BOOT_UP_PROTOCOL.md |

---

## PHASE 6: MAINTENANCE PROTOCOLS (Time-Based)

### Every Second
| Protocol | What | Status |
|----------|------|--------|
| - | Nothing at this frequency | - |

### Every Minute
| Protocol | What | Status |
|----------|------|--------|
| Wake Check | Check for wake signals | (needs creation) |
| Heartbeat | Pulse to show alive | Daemon running |

### Every 5 Minutes
| Protocol | What | Status |
|----------|------|--------|
| Git Pull | Check for updates | (needs creation) |
| Message Check | Check Trinity messages | (needs creation) |

### Every 30 Minutes
| Protocol | What | Status |
|----------|------|--------|
| Progress Report | Report to hub | HUB_REPORT_STANDARD.md |
| Token Check | Round-robin status | round_robin_token.json |

### Every Hour
| Protocol | What | Status |
|----------|------|--------|
| Consolidation Check | Are all terminals reporting? | AUTO_CONSOLIDATE_DAEMON.py |
| Sync Verify | Is Syncthing working? | (needs creation) |

### Every Day (3 AM)
| Protocol | What | Status |
|----------|------|--------|
| Desktop Cleanup | Archive Desktop files >3 days | MAINTENANCE_DAEMON.py |
| Downloads Cleanup | Archive Downloads >7 days | MAINTENANCE_DAEMON.py |
| Temp Cleanup | Delete temp files >1 day | MAINTENANCE_DAEMON.py |
| Git Branch Cleanup | Delete merged branches | GIT_BRANCH_CLEANUP.md |

### Every 3 Days
| Protocol | What | Status |
|----------|------|--------|
| Archive Rotation | Delete archives >30 days | MAINTENANCE_DAEMON.py |
| Log Rotation | Compress old logs | (needs creation) |

### Every Week
| Protocol | What | Status |
|----------|------|--------|
| Capability Manifest | Regenerate capabilities | CAPABILITY_MANIFEST.py |
| System Health Check | Full system audit | (needs creation) |
| Backup Verify | Check backups exist | (needs creation) |

### Every 2 Weeks
| Protocol | What | Status |
|----------|------|--------|
| Protocol Audit | Are protocols being followed? | This document |
| Cross-Computer Sync Test | Test all 5 comms routes | (needs creation) |

### Every Month
| Protocol | What | Status |
|----------|------|--------|
| Full Cleanup | Deep clean all systems | (needs creation) |
| API Key Rotation | Rotate sensitive keys | (needs creation) |
| Documentation Update | Update all meta docs | (needs creation) |

### Every Quarter (3 Months)
| Protocol | What | Status |
|----------|------|--------|
| Architecture Review | Is structure still right? | (needs creation) |
| Capability Diff | Compare all computers | CAPABILITY_MANIFEST.py |

### Every 6 Months
| Protocol | What | Status |
|----------|------|--------|
| Major Version Review | Time for v2? | (needs creation) |
| Security Audit | Full security check | (needs creation) |

### Every Year
| Protocol | What | Status |
|----------|------|--------|
| System Rebuild Consideration | Fresh start? | (needs creation) |
| Annual Report | What was accomplished | (needs creation) |

---

## PHASE 7: META-LAYER UPDATE PROTOCOLS

| When | Update What | How |
|------|-------------|-----|
| File created | _BOOTSTRAP.json for that folder | Add to "completed" |
| File in progress | _BOOTSTRAP.json | Update "in_progress" |
| Discovery made | _BOOTSTRAP.json + report | Add to "discoveries" |
| Task completed | _BOOTSTRAP.json + report | Move to "completed" |
| New protocol added | This document | Add to relevant phase |

### Meta Update Flow
```
DO WORK
  ↓
UPDATE _BOOTSTRAP.json (fractal)
  ↓
UPDATE terminal report
  ↓
CONSOLIDATE merges automatically
  ↓
PUSHED to git
  ↓
OTHER COMPUTERS pull
  ↓
META STAYS IN SYNC
```

---

## PHASE 8: EMERGENCY PROTOCOLS

| Situation | Protocol | File |
|-----------|----------|------|
| Computer down | Failover to other PCs | (needs creation) |
| Git conflict | Conflict resolution | (needs creation) |
| Sync broken | Manual resync | (needs creation) |
| Token stuck | Token recovery | (needs creation) |
| Total failure | Nuclear reset | (needs creation) |

---

## PHASE 9: EXTERNAL PROTOCOLS

| Protocol | What | Status |
|----------|------|--------|
| New Computer Onboard | Transform any PC to match | UNIVERSAL_FILE_STRUCTURE.md |
| User Onboard | Setup for new user | (needs creation) |
| API Integration | Connect external service | (needs creation) |
| Cyclotron Feed | Push to RSS/feeds | (needs creation) |

---

## PHASE 10: AUDIT PROTOCOL

### Weekly Audit Checklist
- [ ] All terminals reporting?
- [ ] Consolidation working?
- [ ] Git sync working?
- [ ] Syncthing syncing?
- [ ] Cleanup running?
- [ ] Protocols being followed?

### Monthly Audit Checklist
- [ ] All protocols documented?
- [ ] All _BOOTSTRAP.json updated?
- [ ] All 3 computers in sync?
- [ ] Capability manifests match?
- [ ] No orphan files?

---

## PHASE 11: SCHEDULING IMPLEMENTATION

### Windows Task Scheduler
```powershell
# Daily cleanup at 3 AM
Register-ScheduledTask -TaskName "Daily_Cleanup" -Trigger (New-ScheduledTaskTrigger -Daily -At "3:00 AM") -Action (New-ScheduledTaskAction -Execute "python" -Argument "C:\Users\dwrek\LOCAL_TRINITY_HUB\MAINTENANCE_DAEMON.py")

# Weekly capability scan
Register-ScheduledTask -TaskName "Weekly_Capability" -Trigger (New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "4:00 AM") -Action (New-ScheduledTaskAction -Execute "python" -Argument "C:\Users\dwrek\LOCAL_TRINITY_HUB\CAPABILITY_MANIFEST.py")
```

### Cron (Linux/Mac)
```bash
# Daily cleanup at 3 AM
0 3 * * * python ~/LOCAL_TRINITY_HUB/MAINTENANCE_DAEMON.py

# Weekly capability scan
0 4 * * 1 python ~/LOCAL_TRINITY_HUB/CAPABILITY_MANIFEST.py
```

---

## PHASE 12: GAPS IDENTIFIED

### Needs Creation (Priority Order)
1. Git Sync Protocol
2. Task Queue System
3. Sync Verify Protocol
4. System Health Check
5. Emergency Failover
6. New Computer Onboard Script
7. Cyclotron Feed Push

---

## PHASE 13: THE ONE DOCUMENT

**This is it.**

This document:
- Lists every protocol
- Shows timing for each
- Identifies what exists vs gaps
- Enables any computer to be transformed
- Single source of truth

**To onboard a new computer:**
1. Create folder structure (UNIVERSAL_FILE_STRUCTURE.md)
2. Copy all protocols from this list
3. Schedule all timed tasks
4. Run capability manifest
5. Connect to hub
6. Done

**To audit system:**
1. Go through each phase
2. Check each protocol exists
3. Check each is running
4. Identify gaps
5. Build missing pieces

---

## STATUS SUMMARY

| Phase | Protocols | Complete | Needs Work |
|-------|-----------|----------|------------|
| Boot | 5 | 3 | 2 |
| Working | 5 | 2 | 3 |
| Communication | 4 | 3 | 1 |
| Consolidation | 4 | 4 | 0 |
| Boot Down | 4 | 4 | 0 |
| Maintenance | 15 | 5 | 10 |
| Meta-Layer | 5 | 5 | 0 |
| Emergency | 5 | 0 | 5 |
| External | 4 | 1 | 3 |
| **TOTAL** | **51** | **27** | **24** |

**53% complete. 24 protocols to build.**
