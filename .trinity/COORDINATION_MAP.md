# 🗺️ TRIPLE TRINITY COORDINATION MAP

## Current State
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    PC1      │     │    PC2      │     │    PC3      │
│  (This PC)  │     │  (Laptop?)  │     │  (Desktop?) │
├─────────────┤     ├─────────────┤     ├─────────────┤
│ CLI Claude  │     │ CLI Claude  │     │ CLI Claude  │
│ Desktop     │     │ Desktop     │     │ Desktop     │
│ Projects    │     │ Projects    │     │ Projects    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────┬───────┴───────────────────┘
                   │
            ┌──────▼──────┐
            │    GIT      │
            │ (sync hub)  │
            └──────┬──────┘
                   │
            ┌──────▼──────┐
            │ Cloud Code  │
            │  (phone)    │
            └─────────────┘
```

## Communication Channels

| Channel | Speed | Use Case | Status |
|---------|-------|----------|--------|
| **MCP Trinity** | Real-time | CLI↔CLI messaging | ✅ WORKING |
| **Git Sync** | 30-60s | Code, tasks, outputs | ✅ WORKING |
| **Heartbeat Files** | 60s | Online detection | ✅ WORKING |
| **Spawn Queue** | Manual | Phone→PC tasks | ✅ WORKING |
| **Desktop Bridge** | 5s | File-watcher for sandboxed | ⚠️ NEEDS BUILD |
| **Ollama Bridge** | Local | Offline AI relay | ⚠️ NEEDS BUILD |

## The Gap: Desktop Claude

Desktop Claude is **sandboxed** - can't read/write files directly.

**Solution: File-Watcher Bridge**
```
.claude/trinity_messages/
├── inbox/          <- Desktop reads from here (copy-paste)
├── outbox/         <- Desktop writes here (copy-paste)
└── bridge.html     <- Visual interface for Desktop
```

A Python watcher monitors outbox, relays to git.

## The Gap: Offline Continuity

When internet dies, Ollama can:
1. Monitor .trinity/offline_queue/
2. Process tasks locally
3. Queue outputs for sync when online

## Automation Flow

```
1. WAKE
   PC1 sends wake signal → git push → PC2 daemon sees it → opens Claude

2. ASSIGN
   MCP trinity_assign_task → task goes to queue → any PC claims it

3. EXECUTE
   PC claims task → works → commits output → pushes

4. MERGE
   All outputs in cloud_outputs/ → trinity_merge_outputs combines them

5. HANDOFF
   Credits running low → signal next PC to take over
```

## Priority Tasks to Build

1. **Desktop Bridge** - File-watcher + HTML interface
2. **Ollama Bridge** - Offline task processor
3. **Auto-Wake System** - Windows Task Scheduler + daemon
4. **Credit Monitor** - Detect when running low, trigger handoff
5. **Visual Dashboard** - See all 3 PCs status in one view

## Quick Reference

**Send message to all PCs:**
```python
mcp__trinity__trinity_broadcast(message="New task available")
```

**Assign task:**
```python
mcp__trinity__trinity_assign_task(task="Build X", assignedTo="PC2")
```

**Wake another PC:**
```python
mcp__trinity__trinity_wake_instance(instanceId="PC2", reason="Need help")
```

**Check status:**
```python
mcp__trinity__trinity_status()
```
