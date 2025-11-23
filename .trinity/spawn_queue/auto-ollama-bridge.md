=== AUTOMATION BUILD TASK ===

Task ID: auto-ollama-bridge
Priority: high
Created: 2025-11-23 01:58

YOUR MISSION:

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


WHEN DONE:
1. Save output to: .trinity/cloud_outputs/auto-ollama-bridge.md
2. If code, also save to appropriate location
3. Git commit: "automation: auto-ollama-bridge complete"
4. Git push

=== BEGIN WORK ===
