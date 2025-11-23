=== AUTOMATION BUILD TASK ===

Task ID: auto-desktop-bridge
Priority: high
Created: 2025-11-23 01:58

YOUR MISSION:

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


WHEN DONE:
1. Save output to: .trinity/cloud_outputs/auto-desktop-bridge.md
2. If code, also save to appropriate location
3. Git commit: "automation: auto-desktop-bridge complete"
4. Git push

=== BEGIN WORK ===
