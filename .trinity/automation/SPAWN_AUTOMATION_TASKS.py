#!/usr/bin/env python3
"""
SPAWN AUTOMATION BUILD TASKS
Creates tasks to build the Triple Trinity coordination system itself.
"""

import json
from datetime import datetime
from pathlib import Path
import subprocess

TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
SPAWN_QUEUE = TRINITY_DIR / "spawn_queue"

def create_task(task_id, description, priority="high"):
    """Create a spawn task file"""
    SPAWN_QUEUE.mkdir(parents=True, exist_ok=True)

    task = {
        "id": task_id,
        "type": "automation_build",
        "description": description,
        "priority": priority,
        "created_at": datetime.now().isoformat() + "Z",
        "status": "pending"
    }

    instructions = f"""=== AUTOMATION BUILD TASK ===

Task ID: {task_id}
Priority: {priority}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}

YOUR MISSION:
{description}

WHEN DONE:
1. Save output to: .trinity/cloud_outputs/{task_id}.md
2. If code, also save to appropriate location
3. Git commit: "automation: {task_id} complete"
4. Git push

=== BEGIN WORK ===
"""

    task_file = SPAWN_QUEUE / f"{task_id}.json"
    task_file.write_text(json.dumps(task, indent=2))

    md_file = SPAWN_QUEUE / f"{task_id}.md"
    md_file.write_text(instructions)

    print(f"✅ Created: {task_id} [{priority}]")
    return task_id

def main():
    print("=== SPAWNING AUTOMATION BUILD TASKS ===\n")

    # Task 1: Desktop Bridge
    create_task("auto-desktop-bridge", """
BUILD: Desktop Claude File-Watcher Bridge

Desktop Claude is sandboxed - can't access filesystem directly.
Build a bridge system:

1. Python file-watcher script that monitors:
   - .claude/trinity_messages/outbox/ for new files
   - Relays content to .trinity/messages/

2. HTML interface (bridge.html) that Desktop can open:
   - Shows inbox messages
   - Has textarea to write outbox messages
   - Copy-paste friendly for sandboxed environment

3. Instructions for Desktop Claude to use the bridge

Output:
- DESKTOP_BRIDGE_WATCHER.py
- DESKTOP_BRIDGE_UI.html
- DESKTOP_BRIDGE_INSTRUCTIONS.md
""", "high")

    # Task 2: Ollama Offline Bridge
    create_task("auto-ollama-bridge", """
BUILD: Ollama Offline Task Processor

When internet goes down, Ollama should keep working:

1. Python script that:
   - Monitors .trinity/offline_queue/ for tasks
   - Processes with local Ollama model
   - Saves outputs to .trinity/offline_outputs/
   - Queues for git sync when online

2. Task format spec for offline processing

3. Auto-detect online/offline status

Output:
- OLLAMA_OFFLINE_BRIDGE.py
- OFFLINE_TASK_SPEC.md
""", "high")

    # Task 3: Auto-Wake System
    create_task("auto-wake-system", """
BUILD: Cross-Computer Auto-Wake System

Make computers wake each other automatically:

1. Enhanced daemon that can:
   - Detect wake signals in git
   - Actually open Claude Code (not just notify)
   - Use Windows Task Scheduler for reliability

2. Wake methods:
   - Git signal file
   - Tailscale direct ping
   - Windows scheduled task trigger

3. Test protocol for PC1→PC2→PC3 chain

Output:
- AUTO_WAKE_DAEMON.py
- WAKE_TEST_PROTOCOL.md
- Windows .bat scripts for each method
""", "high")

    # Task 4: Credit Monitor
    create_task("auto-credit-monitor", """
BUILD: Credit Exhaustion Monitor & Handoff

Detect when credits running low and trigger handoff:

1. Monitor patterns that indicate credit exhaustion:
   - Rate limit errors
   - Slower responses
   - Usage API if available

2. Automatic handoff protocol:
   - Save current state
   - Signal next PC
   - Queue remaining work

3. Dashboard showing credit status across all PCs

Output:
- CREDIT_MONITOR.py
- HANDOFF_PROTOCOL.md
- CREDIT_DASHBOARD.html
""", "normal")

    # Task 5: Visual Command Center
    create_task("auto-command-center", """
BUILD: Triple Trinity Visual Command Center

Single dashboard showing all 3 PCs:

1. HTML dashboard that displays:
   - All PC heartbeats (online/offline)
   - Current tasks on each PC
   - Message queue
   - Spawn queue status
   - Recent outputs

2. Auto-refresh from git-synced JSON files

3. Mobile-friendly for phone monitoring

Output:
- COMMAND_CENTER.html
- COMMAND_CENTER_DATA.py (generates JSON for dashboard)
""", "normal")

    # Task 6: MCP-Git Sync
    create_task("auto-mcp-git-sync", """
BUILD: MCP Trinity → Git Synchronizer

Bridge MCP real-time messages to git for persistence:

1. Script that:
   - Polls MCP trinity_receive_messages
   - Saves to .trinity/messages/archive/
   - Commits periodically

2. Reverse: git messages → MCP broadcast

3. Ensures no messages lost between sessions

Output:
- MCP_GIT_SYNC.py
- MESSAGE_ARCHIVE_SPEC.md
""", "normal")

    print("\n=== 6 AUTOMATION TASKS CREATED ===")
    print("\nThese tasks BUILD the coordination system itself.")
    print("Assign to different PCs for parallel execution:")
    print("  PC1: auto-desktop-bridge, auto-credit-monitor")
    print("  PC2: auto-ollama-bridge, auto-mcp-git-sync")
    print("  PC3: auto-wake-system, auto-command-center")

    # Git sync
    print("\nSyncing to git...")
    repo = Path.home() / "100X_DEPLOYMENT"
    subprocess.run(["git", "add", "-A"], cwd=repo)
    subprocess.run(["git", "commit", "-m", "automation: spawn build tasks"], cwd=repo)
    subprocess.run(["git", "push", "overkor-tek", "HEAD:master"], cwd=repo)
    print("✅ Spawn queue synced")

if __name__ == "__main__":
    main()
