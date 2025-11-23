# UNIVERSAL FILE STRUCTURE - SAME ON ALL COMPUTERS

## THE RULE
**Every computer has the exact same folder structure.**
**Files go in the same place on PC1, PC2, and PC3.**

---

## REQUIRED STRUCTURE (Create on every computer)

```
~/ (Home Directory)
├── LOCAL_TRINITY_HUB/           # Central hub for THIS computer
│   ├── terminal_reports/        # C1, C2, C3 drop reports here
│   ├── consolidated/            # Merged outputs
│   ├── outbound/                # FINAL output goes here → GitHub
│   ├── inbound/                 # Files FROM other computers
│   ├── capabilities/            # What this computer can do
│   ├── archives/                # Old files moved here
│   ├── logs/                    # Daemon logs, activity logs
│   ├── boot_state/              # Session state for boot up
│   ├── session_state/           # Current session data
│   ├── protocols/               # How to do things
│   ├── commands/                # Scripts and commands
│   ├── api_keys/                # API credentials (gitignored)
│   └── emergency/               # Emergency protocols
│
├── 100X_DEPLOYMENT/             # The actual product
│   └── (deployment files)
│
├── .trinity/                    # Trinity coordination
│   ├── messages/                # Inter-instance messages
│   ├── wake/                    # Wake signals
│   ├── tasks/                   # Task queue
│   ├── outputs/                 # Task outputs
│   └── reports/                 # Session reports
│
├── .consciousness/              # Brain/memory
│   └── brain/                   # Persistent memory
│
└── Desktop/                     # KEPT CLEAN - auto-archived
```

---

## SETUP COMMANDS (Run on each computer)

### PC1 (DWREKSCPU)
```bash
# Already done - this is the template
```

### PC2 (DESKTOP-MSMCFH2)
```bash
mkdir -p ~/LOCAL_TRINITY_HUB/{terminal_reports,consolidated,outbound,inbound,capabilities,archives,logs,boot_state,session_state,protocols,commands,api_keys,emergency}
```

### PC3 (DESKTOP-S72LRRO)
```bash
mkdir -p ~/LOCAL_TRINITY_HUB/{terminal_reports,consolidated,outbound,inbound,capabilities,archives,logs,boot_state,session_state,protocols,commands,api_keys,emergency}
```

---

## FILE PLACEMENT RULES

| File Type | Location | Example |
|-----------|----------|---------|
| Terminal reports | `~/LOCAL_TRINITY_HUB/terminal_reports/` | `C1_REPORT.json` |
| Consolidated output | `~/LOCAL_TRINITY_HUB/consolidated/` | `PC1_CONSOLIDATED_20251123.json` |
| Final output to GitHub | `~/LOCAL_TRINITY_HUB/outbound/` | `PC1_OUTPUT_20251123.json` |
| Received from other PCs | `~/LOCAL_TRINITY_HUB/inbound/` | `FROM_PC2_20251123.json` |
| Protocols/docs | `~/LOCAL_TRINITY_HUB/protocols/` | `MORNING_BOOT_LOADER.py` |
| Session state | `~/LOCAL_TRINITY_HUB/session_state/` | `round_robin_token.json` |
| Capability manifest | `~/LOCAL_TRINITY_HUB/capabilities/` | `manifest.json` |

---

## WHY THIS MATTERS

1. **C1 knows where C2's files are** - same path on both computers
2. **Syncthing can mirror folders** - same structure = easy sync
3. **Scripts work everywhere** - no hardcoded paths per computer
4. **No random filing** - everything has a home

---

## SYNCTHING SYNC TARGETS

These folders sync between all computers:
- `~/LOCAL_TRINITY_HUB/protocols/` - Everyone has same protocols
- `~/LOCAL_TRINITY_HUB/session_state/` - Shared state
- `~/LOCAL_TRINITY_HUB/outbound/` → `~/LOCAL_TRINITY_HUB/inbound/` (cross-computer)

---

## ENFORCEMENT

**Before saving ANY file, ask:**
1. Does this folder exist on all computers?
2. Is this the same path PC2 and PC3 would use?
3. Would Syncthing know how to sync this?

**If NO to any → put it in LOCAL_TRINITY_HUB with the standard structure.**

---

## IMMEDIATE ACTION

**C2 and C3: Run the mkdir command above NOW.**
**Then all 3 computers have identical structure.**

No more random filing. Same shape everywhere.
