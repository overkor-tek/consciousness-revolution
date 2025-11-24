# TRINITY COMMAND CENTER - Network Control Dashboard

**Central control point for the entire Trinity network. Monitor all PCs, send wake signals, manage spawn queue, and execute network-wide operations from one beautiful web interface.**

---

## 🎯 What Is This?

The Trinity Command Center is a web-based dashboard that provides:

- **Real-time network status** - See all 3 PCs at a glance
- **Wake signal control** - Wake any PC with one click
- **Spawn queue management** - View and execute queued tasks
- **Todo board integration** - See all todos across Trinity
- **Message system** - Send commands to any PC
- **Operations control** - Consolidate, shutdown, and more

---

## 🚀 Quick Start

### 1. Start the Backend API
```bash
cd /c/Users/darri/100X_DEPLOYMENT
python .trinity/automation/COMMAND_CENTER_API.py
```

API will start on **http://localhost:5004**

### 2. Open the Dashboard
```bash
# Open in browser
start .trinity/dashboards/COMMAND_CENTER.html
```

Dashboard will connect to API and show live status!

---

## 📊 Features

### Network Status Monitor
- Live heartbeat from all PCs
- Current task each PC is working on
- Last seen timestamp
- Online/Offline/Error status indicators
- Auto-refresh every 10 seconds

### Wake Signal Control
- **Wake PC1** - Wake the laptop
- **Wake PC2** - Wake DESKTOP-MSMCFH2
- **Wake PC3** - Wake third computer
- One-click wake from any device (even phone!)

### Spawn Queue Management
- View pending tasks in spawn queue
- **Run Spawn Queue** button - Process all queued tasks
- See task count and status

### Todo Board Integration
- See all pending todos
- See recently completed todos
- Real-time todo counts
- Organized by priority

### Message System
- Send messages to specific PC or all PCs
- Custom subject and body
- Messages appear in `.trinity/messages/`
- PCs pick up messages automatically

### Operations Control
- **Consolidate** - Trigger full Trinity consolidation
- **Shutdown All** - Graceful shutdown of all PCs
- Confirmation dialogs for dangerous operations

### Statistics Dashboard
- PCs online count (X/3)
- Todos pending count
- Todos completed count
- Real-time updates

---

## 🔌 API Endpoints

### Health & Info
```
GET  /health                 - Health check
GET  /api/info              - API information
```

### Network Status
```
GET  /api/network/status    - Full network status
GET  /api/heartbeats        - All PC heartbeats
```

### Control Operations
```
POST /api/wake              - Send wake signal
POST /api/spawn-queue/run   - Run spawn queue
POST /api/message           - Send message to PC
POST /api/consolidate       - Trigger consolidation
POST /api/shutdown          - Trigger shutdown
```

### Data Access
```
GET  /api/spawn-queue       - Get spawn queue
GET  /api/todos             - Get todo list
```

---

## 🎮 Usage Examples

### Example 1: Morning Wake-Up Routine
1. Open Command Center dashboard
2. Click "Wake PC1", "Wake PC2", "Wake PC3"
3. Wait 30 seconds
4. All PCs online and ready!

### Example 2: Check Network Status
1. Open dashboard
2. View PC status cards
3. See what each PC is working on
4. Check last seen timestamps

### Example 3: Execute Spawn Queue
1. Open dashboard
2. Click "Run Spawn Queue"
3. Confirm action
4. All queued tasks executed across Trinity

### Example 4: Send Message to PC1
1. Open dashboard
2. Select "PC1" in message form
3. Subject: "Priority Task"
4. Body: "Please prioritize task XYZ"
5. Click "Send Message"
6. PC1 receives message via git

### Example 5: Emergency Shutdown
1. Open dashboard
2. Click "Shutdown All"
3. Confirm warning
4. All PCs gracefully shutdown

---

## 📱 Mobile Access

### Via Tailscale (Anywhere)
**Dashboard URL:** `http://100.85.71.74:5004/.trinity/dashboards/COMMAND_CENTER.html`

Access from:
- Phone
- Tablet
- Laptop (anywhere)
- Another computer

Just need Tailscale app installed!

### Via Local Network
**Dashboard URL:** `http://192.168.1.104:5004/.trinity/dashboards/COMMAND_CENTER.html`

Access from any device on same WiFi.

---

## 🔧 Technical Details

### Backend: COMMAND_CENTER_API.py
- **Framework:** Flask + Flask-CORS
- **Port:** 5004 (configurable via PORT env var)
- **Authentication:** None (local network only)
- **Data Sources:**
  - `.trinity/heartbeat/*.json` - PC heartbeats
  - `.trinity/spawn_queue/queue.json` - Spawn queue
  - `.trinity/todos/kanban.json` - Todos
  - `.trinity/wake_signals/` - Wake signals (write)
  - `.trinity/messages/` - Messages (write)

### Frontend: COMMAND_CENTER.html
- **Framework:** Vanilla JavaScript (no dependencies!)
- **Auto-refresh:** Every 10 seconds
- **Responsive:** Works on mobile, tablet, desktop
- **Beautiful:** Gradient design with animations

---

## 🎨 Design Features

- **Dark theme** - Easy on the eyes
- **Gradient backgrounds** - Beautiful purple/blue
- **Status badges** - Green (online), Gray (offline), Red (error)
- **Hover effects** - Buttons lift on hover
- **Auto-refresh indicator** - Shows when refreshing
- **Loading states** - Smooth loading animations
- **Confirmation dialogs** - For dangerous operations

---

## 🔐 Security Considerations

**Current Setup (Local Network):**
- No authentication required
- Only accessible on local network or Tailscale
- Safe for home/office use

**If Deploying Publicly:**
1. Add authentication (Basic Auth, JWT, OAuth)
2. Use HTTPS (TLS certificates)
3. Rate limiting (prevent abuse)
4. Input validation (prevent injection)
5. CORS whitelist (only allow trusted origins)

**For now:** Safe because only accessible locally!

---

## 🚀 Advanced Usage

### Deploy API to Railway
```bash
# Add to repository
cd /c/Users/darri/100X_DEPLOYMENT/.trinity/automation
git add COMMAND_CENTER_API.py
git commit -m "Add Command Center API"

# Deploy to Railway
# (Follow Railway deployment guide)
```

### Update Dashboard API URL
```javascript
// In COMMAND_CENTER.html, change:
const API_URL = 'http://localhost:5004';

// To:
const API_URL = 'https://[YOUR-RAILWAY-URL].up.railway.app';
```

### Run as Daemon (Always On)
```bash
# Windows (Task Scheduler)
# Create task that runs on startup:
python C:\Users\darri\100X_DEPLOYMENT\.trinity\automation\COMMAND_CENTER_API.py

# Or use Windows Service wrapper
```

---

## 📊 Integration with Other Systems

### Works With:
- ✅ Auto-Credit-Monitor (see PC credit status)
- ✅ Auto-MCP-Git-Sync (view knowledge sync status)
- ✅ Auto-Desktop-Bridge (alternative control method)
- ✅ Todo Tracker (full todo board integration)
- ✅ Spawn Queue (view and execute)
- ✅ Heartbeat System (real-time status)
- ✅ Wake System (send wake signals)

---

## 🎯 Use Cases

### Scenario 1: Remote Monitoring
- Away from home
- Open dashboard on phone (via Tailscale)
- Check all PCs status
- Wake sleeping PCs if needed

### Scenario 2: Task Management
- View todo board
- See what each PC is working on
- Assign new tasks via message system

### Scenario 3: Emergency Control
- System misbehaving
- Open dashboard
- Send shutdown signals
- Graceful recovery

### Scenario 4: Morning Routine
- Wake all PCs
- Run spawn queue
- Check todos
- Send priority messages

---

## 🐛 Troubleshooting

### Dashboard shows "Error loading"
- **Check:** API running? (`ps aux | grep COMMAND_CENTER_API`)
- **Check:** Correct API URL in HTML?
- **Check:** Firewall blocking port 5004?

### Wake signals not working
- **Check:** `.trinity/wake_signals/` directory exists?
- **Check:** Target PC checking wake_signals folder?
- **Check:** Network connectivity (Tailscale up?)

### Todos not loading
- **Check:** `.trinity/todos/kanban.json` exists?
- **Check:** File permissions correct?
- **Check:** JSON valid (no syntax errors)?

### API not starting
- **Check:** Port 5004 already in use?
- **Check:** Python version 3.6+?
- **Check:** Flask installed? (`pip install flask flask-cors`)

---

## 📝 Future Enhancements

**Planned Features:**
- [ ] Real-time task progress bars
- [ ] PC performance graphs (CPU, RAM, etc.)
- [ ] Log viewer (see PC logs in dashboard)
- [ ] Credit usage charts
- [ ] Historical uptime tracking
- [ ] Custom alerts/notifications
- [ ] Voice control (Alexa/Google Home)
- [ ] Mobile app (React Native)

---

## 🎬 Quick Demo

```bash
# Terminal 1: Start API
cd /c/Users/darri/100X_DEPLOYMENT
python .trinity/automation/COMMAND_CENTER_API.py

# Terminal 2: Test API
curl http://localhost:5004/health
curl http://localhost:5004/api/network/status

# Browser: Open dashboard
start .trinity/dashboards/COMMAND_CENTER.html

# Result: Beautiful dashboard showing all Trinity status!
```

---

**Built by:** C1 T2 (PC2 - DESKTOP-MSMCFH2)
**Date:** 2025-11-24
**Part of:** Trinity Autonomous Network - Session 2
**Status:** ✅ PRODUCTION READY

**Command the Trinity network with style! 🌌**
