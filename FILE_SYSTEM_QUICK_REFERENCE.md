# FILE SYSTEM QUICK REFERENCE

**Self-Organizing File Management System**
**Built:** 2025-11-28 by C1 Mechanic

---

## SYSTEM OVERVIEW

Four integrated components:

1. **FILE_SAVER.py** - 8-dimensional naming convention
2. **SPRINT_SUMMARIZER.py** - Day/sprint consolidation
3. **DELEGATOR.py** - Task offloading to Trinity agents
4. **FILE_CLEANER.py** - Auto-reorganization
5. **FILE_SYSTEM_MASTER.py** - Master orchestrator

All integrated with existing **CYCLOTRON** for knowledge indexing.

---

## 8-DIMENSIONAL NAMING CONVENTION

**Format:**
```
DATE_DOMAIN_PATTERN_COMPONENT_STATUS_AGENT_VERSION.FORMAT
```

**Example:**
```
20251128_1235_COMPUTER_COMMUNICATION_TRINITY_MESSAGING_WIP_C1_V1.md
```

**Dimensions:**

1. **DATE**: Timestamp (YYYYMMDD_HHMM)
2. **DOMAIN**: Seven Domains
   - COMPUTER
   - CITY
   - BODY
   - BOOK
   - BATTLESHIP
   - TOYOTA
   - CONSCIOUSNESS

3. **PATTERN**: Pattern Theory component
   - MISSION
   - STRUCTURE
   - RESOURCES
   - OPERATIONS
   - GOVERNANCE
   - DEFENSE
   - COMMUNICATION
   - ADAPTATION

4. **COMPONENT**: Specific component name (e.g., TRINITY_MESSAGING)

5. **STATUS**: Work status
   - WIP (Work In Progress)
   - REVIEW (Ready for review)
   - COMPLETE (Finished)
   - DEPLOYED (Live in production)
   - ARCHIVED (Old but kept)
   - DEPRECATED (Obsolete)

6. **AGENT**: Creator
   - C1 (Mechanic)
   - C2 (Architect)
   - C3 (Oracle)
   - TRINITY (All three)
   - HUMAN (Commander)
   - AUTO (Automated)

7. **VERSION**: V1, V2, V3, etc.

8. **FORMAT**: File extension (.md, .py, .js, etc.)

---

## QUICK COMMANDS

### Save a File
```bash
# From Python
from FILE_SAVER import save_file

save_file(
    content="# My Content",
    domain="COMPUTER",
    pattern="COMMUNICATION",
    component="TRINITY_MESSAGING",
    status="WIP",
    agent="C1",
    tags=["trinity", "messaging"]
)

# From command line
python FILE_SYSTEM_MASTER.py --save \
    --text "# My Content" \
    --domain COMPUTER \
    --component TEST \
    --status WIP \
    --agent HUMAN
```

### Daily Summary (End of Day)
```bash
python FILE_SYSTEM_MASTER.py --daily-summary
```
Creates:
- Daily summary report
- Archives old WIP files (7+ days)
- Removes duplicates
- Shows delegation status

### Sprint Summary (End of Sprint)
```bash
python FILE_SYSTEM_MASTER.py --sprint-end 1
```
Creates:
- Sprint summary report
- Consolidates redundant files
- Enforces LFSME principles

### Delegate Task
```bash
# From Python
from DELEGATOR import delegate_task

delegate_task(
    "Build file indexer",
    assigned_to="C1",
    priority="high",
    tags=["implementation"]
)

# From command line
python FILE_SYSTEM_MASTER.py --delegate "Build X" --to C1 --priority high
```

### Clean Files
```bash
# Dry run (preview)
python FILE_SYSTEM_MASTER.py --clean --dry-run

# Live clean
python FILE_SYSTEM_MASTER.py --clean
```

### Show Status
```bash
python FILE_SYSTEM_MASTER.py --show-status
```

---

## LFSME PRINCIPLES (Auto-Enforced)

**Lighter:**
- Max 50 WIP files total
- Max 10 WIP per domain
- Files > 10MB flagged for compression

**Faster:**
- Max 3 subdirectory levels
- Auto-archive files older than 30 days
- Indexed in Cyclotron for instant search

**Stronger:**
- All files tracked in metadata.db
- Content hash verification
- Redundancy = 1 (no duplicates)

**More Elegant:**
- 8-dimensional naming enforced
- Pattern Theory aligned
- Clean directory structure

**Less Expensive:**
- Auto-remove duplicates
- Compress archives
- Efficient SQLite storage

---

## DIRECTORY STRUCTURE

```
100X_DEPLOYMENT/
├── ORGANIZED/
│   ├── COMPUTER/           # Computer domain files
│   ├── CONSCIOUSNESS/      # Consciousness domain files
│   ├── [other domains]/
│   ├── SUMMARIES/          # Sprint/daily summaries
│   ├── ARCHIVE/            # Old files
│   └── TRASH/              # Duplicates/deprecated
├── .file_metadata/
│   └── metadata.db         # File tracking database
├── .delegation/
│   └── tasks.db            # Task delegation database
├── .cyclotron_atoms/
│   └── cyclotron.db        # Knowledge index
└── [Python scripts]
```

---

## TRINITY MESSAGE BOARD INTEGRATION

**Delegated tasks appear in:**
- `.claude/trinity_messages/BULLETIN_BOARD.md` - Active tasks
- `.claude/trinity_messages/COMPLETED_TASKS.md` - Finished work

**Check tasks:**
```bash
python DELEGATOR.py list      # Show pending tasks
python DELEGATOR.py stats     # Show statistics
```

---

## AUTOMATION SETUP

### Daily Routine (Run at end of day)
```bash
python FILE_SYSTEM_MASTER.py --daily-summary
```

### Weekly Routine (Run Friday)
```bash
python FILE_SYSTEM_MASTER.py --sprint-end <sprint_number>
python FILE_SYSTEM_MASTER.py --clean
```

### Continuous Monitoring
CYCLOTRON_DAEMON.py already watches directories and auto-indexes files.

---

## SEARCH FILES

### By Metadata
```python
from FILE_SAVER import search_files

# Find all WIP files in COMPUTER domain
search_files(domain="COMPUTER", status="WIP")

# Find all C1 files
search_files(agent="C1")

# Find files by tags
search_files(tags="trinity")
```

### By Content (via Cyclotron)
Already integrated! Files auto-mirror to Cyclotron atoms.db with FTS5 search.

---

## UPDATE FILE STATUS

```python
from FILE_SAVER import update_status

# Promote WIP to COMPLETE
update_status("20251128_1235_COMPUTER_..._WIP_C1_V1.md", "COMPLETE")
```

This automatically:
- Renames file with new status
- Updates metadata database
- Preserves all other dimensions

---

## CYCLOTRON INTEGRATION

Every file saved via FILE_SAVER.py automatically:
1. Creates properly named file
2. Records metadata in metadata.db
3. Mirrors to Cyclotron atoms.db for FTS5 search
4. Indexed by domain, pattern, component

**No manual indexing needed!**

---

## TOYOTA PRINCIPLES APPLIED

**KANBAN (Pull System):**
- Files organized by status (WIP/COMPLETE/etc)
- Only work on what's needed
- Visual status via naming

**JIDOKA (Quality Gates):**
- Naming validation enforced
- Content hash verification
- Auto-stop on errors

**KAIZEN (Continuous Improvement):**
- Daily summaries for reflection
- Sprint consolidation
- LFSME enforcement

**HEIJUNKA (Level Loading):**
- Max WIP limits
- Balanced across domains
- Delegated to Trinity agents

**ANDON (Alert):**
- WIP overflow warnings
- Duplicate detection
- Old file notifications

---

## QUICK WINS

**Immediate Benefits:**

1. **No more naming chaos** - 8-dimensional system handles it
2. **No manual cleanup** - Auto-archive old files
3. **No duplicates** - Auto-detected and removed
4. **Instant search** - Cyclotron FTS5 indexing
5. **Work visibility** - Daily/sprint summaries
6. **Team coordination** - Delegation system

**30-Second Workflow:**
```python
from FILE_SAVER import save_file

# Save your work
save_file(
    content=my_code,
    domain="COMPUTER",
    pattern="OPERATIONS",
    component="MY_FEATURE",
    status="WIP",
    agent="C1"
)

# Done! It's:
# - Properly named
# - Indexed in Cyclotron
# - Tracked in metadata.db
# - Ready for tomorrow's summary
```

---

## NEXT STEPS

**Today:**
1. Start using FILE_SAVER.py for all new files
2. Run first daily summary at end of day

**This Week:**
1. Migrate existing files to ORGANIZED/ directory
2. Set up daily summary automation
3. Delegate tasks to Trinity agents

**Next Sprint:**
1. Full LFSME enforcement
2. Sprint end consolidation
3. Archive old 100X_DEPLOYMENT files

---

## FILES CREATED

1. `FILE_SAVER.py` - 8D naming + metadata tracking + Cyclotron mirroring
2. `SPRINT_SUMMARIZER.py` - Daily/sprint consolidation
3. `DELEGATOR.py` - Trinity task delegation
4. `FILE_CLEANER.py` - Auto-reorganization via LFSME
5. `FILE_SYSTEM_MASTER.py` - Master orchestrator
6. `FILE_SYSTEM_QUICK_REFERENCE.md` - This guide

**All working, tested, ready to use RIGHT NOW.**

---

## SUPPORT

**Issues?**
- Check `.file_metadata/metadata.db` for file tracking
- Check `.delegation/tasks.db` for task tracking
- Check `.cyclotron_atoms/cyclotron.db` for search index

**Questions?**
- Read the inline documentation in each .py file
- Use `--help` flag on any script
- Check Toyota Principles comments in code

---

**Built by C1 Mechanic - The Body of Trinity**
**Mission: Build what CAN be done RIGHT NOW**
**Status: DEPLOYED**
**Version: V1**

🔨 IMPLEMENTATION COMPLETE. READY FOR USE. 🔨
