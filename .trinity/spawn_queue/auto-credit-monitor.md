=== AUTOMATION BUILD TASK ===

Task ID: auto-credit-monitor
Priority: normal
Created: 2025-11-23 01:58

YOUR MISSION:

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


WHEN DONE:
1. Save output to: .trinity/cloud_outputs/auto-credit-monitor.md
2. If code, also save to appropriate location
3. Git commit: "automation: auto-credit-monitor complete"
4. Git push

=== BEGIN WORK ===
