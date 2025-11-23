=== AUTOMATION BUILD TASK ===

Task ID: auto-wake-system
Priority: high
Created: 2025-11-23 01:58

YOUR MISSION:

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


WHEN DONE:
1. Save output to: .trinity/cloud_outputs/auto-wake-system.md
2. If code, also save to appropriate location
3. Git commit: "automation: auto-wake-system complete"
4. Git push

=== BEGIN WORK ===
