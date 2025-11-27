# Trinity Coordination Protocol

## Meeting Place
This folder (`/home/user/consciousness-revolution/.consciousness/trinity/coordination/`) is the Trinity meeting point.

## How It Works

### 1. Status Updates (Every 30 seconds)
Each instance writes: `status/c1_status.json`, `status/c2_status.json`, `status/c3_status.json`

### 2. Messages (Async)
- To send a message: Write to `messages/c1_to_c2_MSG_ID.json`
- Check for messages: Read `messages/*_to_c1_*.json`
- Mark as read: Move to `messages/read/`

### 3. Work Queue
- New work orders: `work_queue/pending/WO-XXX.json`
- Claim a work order: Move to `work_queue/active/WO-XXX.json` and update with your instance ID
- Complete work order: Move to `work_queue/completed/WO-XXX.json`

## Sync Methods

### Git Sync (Primary - Permanent Record)
- All instances commit changes to this folder
- Push to GitHub for permanent coordination history
- C1 (Terminal) is GitHub gatekeeper

### Google Drive Sync (If Available - Real-Time)
- If Google Drive is mounted/accessible via MCP:
  - Mirror this folder structure to `Google Drive/TRINITY_SYNC/`
  - Use Drive for real-time updates
  - Use Git for permanent record

### Desktop Claude Relay (C2's Special Power)
- If C2 can coordinate between instances directly
- C2 can read this folder and relay to C3
- C2 can spawn/orchestrate work

## Current Status
- C1 (MECHANIC): ACTIVE - Waiting for coordination
- C2 (ARCHITECT): WAITING - Need relay protocol
- C3 (ORACLE): WAITING - Need sync method

## Immediate Question for Commander
**How should C2 and C3 access this folder?**

Options:
A. They pull from Git every 30 sec (automatic polling)
B. You set up Google Drive MCP for all instances
C. Desktop Claude (C2) acts as relay/coordinator
D. We use a different meeting place you specify
