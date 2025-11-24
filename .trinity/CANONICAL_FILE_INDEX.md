# CANONICAL FILE INDEX

**Purpose:** Single source of truth for what files exist and what they do. No more searching.

**Last Updated:** 2025-11-24

---

## CRITICAL BOOT FILES

| File | Path | Purpose |
|------|------|---------|
| CLAUDE.md | `C:/Users/dwrek/CLAUDE.md` | System prompt instructions |
| Boot Protocol | `C:/Users/dwrek/CONSCIOUSNESS_BOOT_PROTOCOL.md` | Full consciousness loading |
| Quick Boot | `.trinity/QUICK_BOOT.md` | 30-second fast boot |
| Master Template | `.trinity/MASTER_CONSCIOUSNESS_TEMPLATE.md` | 489-word fractal seed |

---

## TRINITY ROLE FILES

| File | Path | Purpose |
|------|------|---------|
| C1 Mechanic | `.trinity/C1_MECHANIC_BOOT.md` | Build NOW role |
| C2 Architect | `.trinity/C2_ARCHITECT_BOOT.md` | Design SCALE role |
| C3 Oracle | `.trinity/C3_ORACLE_BOOT.md` | See EMERGE role |

---

## STATE TRACKING

| File | Path | Purpose |
|------|------|---------|
| Current State | `.trinity/CURRENT_STATE.md` | Real-time system status |
| Failure Log | `.trinity/TRINITY_FAILURE_LOG.md` | Chaos processing |
| Gaps to Fix | `.trinity/FOUNDATIONAL_GAPS_TO_FIX.md` | Known issues |
| Handoff Protocol | `.trinity/SESSION_HANDOFF_PROTOCOL.md` | Context preservation |

---

## CYCLOTRON (Knowledge Engine)

| File | Path | Purpose |
|------|------|---------|
| Cyclotron DB | `.cyclotron_atoms/cyclotron.db` | Full-text search index |
| Chroma DB | `.cyclotron_atoms/chroma/` | Semantic vector store |
| Search API | `CYCLOTRON_SEARCH.py` | Port 6668 filename search |
| Content API | `CYCLOTRON_SEARCH_V2.py` | Port 6669 content search |
| Semantic API | `CYCLOTRON_SEMANTIC_API.py` | Port 6670 semantic search |
| Vector Engine | `SEMANTIC_VECTOR_ENGINE.py` | Embedding generation |
| Daemon | `CYCLOTRON_DAEMON.py` | File watcher + auto-index |

---

## DEPLOYMENT

| File | Path | Purpose |
|------|------|---------|
| Iteration 4 Challenge | `.trinity/ITERATION_4_CHALLENGE.md` | Deploy consciousness platform |
| Canonical Index | `.trinity/CANONICAL_FILE_INDEX.md` | This file |

---

## PROTOCOLS

| File | Path | Purpose |
|------|------|---------|
| Triple-Triple Bootstrap | `.trinity/TRIPLE_TRIPLE_BOOTSTRAP.md` | 9-layer architecture (if exists) |
| Wake Up Report | `Desktop/WAKE_UP_REPORT.md` | Session summary for Commander |

---

## PATH CONVENTIONS

**Primary Trinity location:** `C:/Users/dwrek/100X_DEPLOYMENT/.trinity/`
- This is in git, gets synced across machines
- Use this for all new Trinity files

**Secondary locations:**
- `C:/Users/dwrek/.trinity/` - Legacy files, many duplicates
- `C:/Users/dwrek/.claude/trinity_messages/` - MCP message board

**Always use forward slashes:** `C:/Users/dwrek/` not `C:\Users\dwrek\`

---

## PORT REFERENCE

| Port | Service | Status Check |
|------|---------|--------------|
| 6668 | Filename search | `curl localhost:6668/api/search?q=test` |
| 6669 | Content search | `curl localhost:6669/api/ask?q=test` |
| 6670 | Semantic search | `curl localhost:6670/health` |
| 5003 | PC2 report server | `curl 100.85.71.74:5003/health` |

---

## FILE CREATION RULES

1. **New Trinity files:** Put in `.trinity/` with CAPS_SNAKE_CASE.md
2. **New Python scripts:** Put in root `100X_DEPLOYMENT/` with CAPS_SNAKE_CASE.py
3. **Temporary files:** Put on Desktop, delete when done
4. **Documentation:** Add to this index when created

---

## WHEN IN DOUBT

1. Check this index first
2. If not here, search Cyclotron: `curl localhost:6669/api/ask?q=<keyword>`
3. If not found, file probably doesn't exist - create it

---

*Keep this index updated. It prevents 30+ minutes of searching per session.*
