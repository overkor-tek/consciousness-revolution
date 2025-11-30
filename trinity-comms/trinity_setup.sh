#!/bin/bash
#
# TRINITY SETUP SCRIPT
# ====================
# Sets up a computer to participate in the Trinity network.
#
# Usage:
#   ./trinity_setup.sh                    # Interactive setup
#   ./trinity_setup.sh C1T1               # Setup as C1T1
#   ./trinity_setup.sh C1T1 --minimal     # Skip optional components
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   🔱 TRINITY SETUP                           ║"
echo "║              Multi-Computer AI Orchestration                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Parse arguments
INSTANCE_ID=${1:-""}
MINIMAL=${2:-""}

# Get instance ID if not provided
if [ -z "$INSTANCE_ID" ]; then
    echo -e "${YELLOW}Available instance IDs:${NC}"
    echo "  Computer 1: C1T1 (lead), C2T1, C3T1"
    echo "  Computer 2: C1T2 (lead), C2T2, C3T2"
    echo "  Computer 3: C1T3 (lead), C2T3, C3T3"
    echo ""
    read -p "Enter your instance ID: " INSTANCE_ID
fi

echo -e "\n${GREEN}Setting up as: $INSTANCE_ID${NC}\n"

# Base directory
TRINITY_BASE="$HOME/trinity_shared"

# Create directory structure
echo -e "${BLUE}Creating directory structure...${NC}"
mkdir -p "$TRINITY_BASE/wake"
mkdir -p "$TRINITY_BASE/oracle_inbox"
mkdir -p "$TRINITY_BASE/oracle_outbox"
mkdir -p "$TRINITY_BASE/logs"
mkdir -p "$TRINITY_BASE/${INSTANCE_ID}_workspace"
mkdir -p "$TRINITY_BASE/C1_workspace"
mkdir -p "$TRINITY_BASE/C2_workspace"
mkdir -p "$TRINITY_BASE/C3_workspace"
mkdir -p "$TRINITY_BASE/scripts"
echo -e "${GREEN}✓ Directories created${NC}"

# Check for Python
echo -e "\n${BLUE}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python3 not found. Please install Python 3.9+${NC}"
    exit 1
fi

# Install watchdog
echo -e "\n${BLUE}Installing watchdog...${NC}"
pip3 install watchdog --quiet 2>/dev/null || pip install watchdog --quiet
echo -e "${GREEN}✓ Watchdog installed${NC}"

# Check for Claude Code
echo -e "\n${BLUE}Checking Claude Code...${NC}"
if command -v claude &> /dev/null; then
    echo -e "${GREEN}✓ Claude Code found${NC}"
    
    # Test headless mode
    echo -e "${BLUE}Testing headless mode...${NC}"
    if claude -p "echo test" --output-format text &>/dev/null; then
        echo -e "${GREEN}✓ Headless mode works${NC}"
    else
        echo -e "${YELLOW}⚠ Headless mode test failed (may need authentication)${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Claude Code not found. Install from Anthropic to enable AI execution.${NC}"
fi

# Copy scripts
echo -e "\n${BLUE}Installing Trinity scripts...${NC}"

# Create the wake monitor script
cat > "$TRINITY_BASE/scripts/trinity_wake_monitor.py" << 'SCRIPT'
#!/usr/bin/env python3
import time, os, json, subprocess, logging
from datetime import datetime
from pathlib import Path
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Run: pip install watchdog")
    exit(1)

INSTANCE_ID = os.environ.get("INSTANCE_ID", "C1T1")
TRINITY_BASE = Path(os.path.expanduser("~/trinity_shared"))
WAKE_DIR = TRINITY_BASE / "wake"
WORKSPACE = TRINITY_BASE / f"{INSTANCE_ID}_workspace"
LOGS = TRINITY_BASE / "logs"
INBOX = TRINITY_BASE / "oracle_inbox"

for d in [WAKE_DIR, WORKSPACE, LOGS, INBOX]:
    d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=f'[{INSTANCE_ID}] %(asctime)s - %(message)s',
    handlers=[logging.FileHandler(LOGS / f"{INSTANCE_ID}.log"), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory: return
        f = Path(event.src_path)
        if f.name == f"{INSTANCE_ID}.task":
            log.info("🔥 WAKE!")
            time.sleep(0.5)
            try:
                with open(f) as tf: task = json.load(tf)
                log.info(f"Task: {task.get('task_type', 'claude')}")
                
                result = {"success": False}
                if task.get("task_type") == "echo":
                    log.info(f"ECHO: {task.get('message')}")
                    result = {"success": True, "message": task.get("message")}
                elif task.get("prompt"):
                    r = subprocess.run(
                        ["claude", "-p", task["prompt"], "--allowedTools", task.get("allowed_tools", "Bash,Read,Write")],
                        capture_output=True, text=True, timeout=300
                    )
                    result = {"success": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr}
                
                # Save result
                tid = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(WORKSPACE / f"result_{tid}.json", 'w') as rf:
                    json.dump({"task_id": tid, "instance": INSTANCE_ID, "result": result, "task": task}, rf, indent=2)
                
                if task.get("report_to_oracle"):
                    with open(INBOX / f"result_{INSTANCE_ID}_{tid}.json", 'w') as rf:
                        json.dump({"task_id": tid, "instance": INSTANCE_ID, "timestamp": datetime.now().isoformat(), "result": result}, rf, indent=2)
                
                f.unlink()
                log.info("✅ Done")
                
                if task.get("wake_next"):
                    with open(WAKE_DIR / f"{task['wake_next']}.task", 'w') as nf:
                        json.dump({"prompt": task.get("chain_task", task.get("prompt")), "triggered_by": INSTANCE_ID, "task_type": task.get("task_type", "claude")}, nf)
                    log.info(f"⭐ Woke: {task['wake_next']}")
            except Exception as e:
                log.error(f"Error: {e}")

if __name__ == "__main__":
    log.info(f"🔱 TRINITY MONITOR - {INSTANCE_ID}")
    log.info(f"Watching: {WAKE_DIR}")
    with open(WORKSPACE / "STATUS.json", 'w') as sf:
        json.dump({"instance": INSTANCE_ID, "status": "monitoring", "started": datetime.now().isoformat()}, sf, indent=2)
    observer = Observer()
    observer.schedule(Handler(), str(WAKE_DIR))
    observer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Stopped")
    observer.join()
SCRIPT

# Create trigger script
cat > "$TRINITY_BASE/scripts/trinity_trigger.py" << 'SCRIPT'
#!/usr/bin/env python3
import sys, json, os
from datetime import datetime
from pathlib import Path

WAKE_DIR = Path(os.path.expanduser("~/trinity_shared/wake"))
WAKE_DIR.mkdir(parents=True, exist_ok=True)

if len(sys.argv) < 2:
    print("Usage: python trinity_trigger.py INSTANCE [PROMPT] [--echo MSG] [--chain NEXT]")
    sys.exit(1)

instance = sys.argv[1]
prompt = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
task = {"triggered_by": "manual", "timestamp": datetime.now().isoformat(), "task_type": "claude"}

for i, arg in enumerate(sys.argv):
    if arg == "--echo" and i+1 < len(sys.argv):
        task["task_type"] = "echo"
        task["message"] = sys.argv[i+1]
    elif arg == "--chain" and i+1 < len(sys.argv):
        task["wake_next"] = sys.argv[i+1]
    elif arg == "--oracle":
        task["report_to_oracle"] = True

if prompt: task["prompt"] = prompt

with open(WAKE_DIR / f"{instance}.task", 'w') as f:
    json.dump(task, f, indent=2)
print(f"✅ Wake sent to {instance}")
SCRIPT

chmod +x "$TRINITY_BASE/scripts/trinity_wake_monitor.py"
chmod +x "$TRINITY_BASE/scripts/trinity_trigger.py"

echo -e "${GREEN}✓ Scripts installed${NC}"

# Check/Install Syncthing
if [ "$MINIMAL" != "--minimal" ]; then
    echo -e "\n${BLUE}Checking Syncthing...${NC}"
    if command -v syncthing &> /dev/null; then
        echo -e "${GREEN}✓ Syncthing found${NC}"
    else
        echo -e "${YELLOW}⚠ Syncthing not installed${NC}"
        read -p "Install Syncthing? (y/n) " install_syncthing
        if [ "$install_syncthing" = "y" ]; then
            if command -v brew &> /dev/null; then
                brew install syncthing
            elif command -v apt &> /dev/null; then
                sudo apt install syncthing -y
            else
                echo -e "${RED}Please install Syncthing manually: https://syncthing.net${NC}"
            fi
        fi
    fi
fi

# Create environment file
echo -e "\n${BLUE}Creating environment file...${NC}"
cat > "$TRINITY_BASE/.env" << EOF
# Trinity Environment Configuration
export INSTANCE_ID="$INSTANCE_ID"
export TRINITY_BASE="$TRINITY_BASE"
EOF
echo -e "${GREEN}✓ Environment file created${NC}"

# Create convenience aliases
echo -e "\n${BLUE}Creating convenience commands...${NC}"
cat > "$TRINITY_BASE/scripts/trinity.sh" << EOF
#!/bin/bash
# Trinity convenience commands
export INSTANCE_ID="$INSTANCE_ID"
export TRINITY_BASE="$TRINITY_BASE"

case "\$1" in
    start)
        echo "Starting Trinity monitor..."
        cd "\$TRINITY_BASE/scripts"
        python3 trinity_wake_monitor.py
        ;;
    wake)
        python3 "\$TRINITY_BASE/scripts/trinity_trigger.py" "\$2" "\$3" "\$4" "\$5"
        ;;
    status)
        cat "\$TRINITY_BASE/${INSTANCE_ID}_workspace/STATUS.json" 2>/dev/null || echo "Not running"
        ;;
    logs)
        tail -f "\$TRINITY_BASE/logs/${INSTANCE_ID}.log"
        ;;
    *)
        echo "Trinity Commands:"
        echo "  trinity start  - Start the wake monitor"
        echo "  trinity wake INSTANCE PROMPT - Wake an instance"
        echo "  trinity status - Show current status"
        echo "  trinity logs   - Follow log file"
        ;;
esac
EOF
chmod +x "$TRINITY_BASE/scripts/trinity.sh"
echo -e "${GREEN}✓ Commands created${NC}"

# Summary
echo -e "\n${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETE                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo -e "Instance: ${GREEN}$INSTANCE_ID${NC}"
echo -e "Base dir: ${BLUE}$TRINITY_BASE${NC}"
echo ""
echo "Quick start:"
echo -e "  ${YELLOW}source $TRINITY_BASE/.env${NC}"
echo -e "  ${YELLOW}$TRINITY_BASE/scripts/trinity.sh start${NC}"
echo ""
echo "Or manually:"
echo -e "  ${YELLOW}INSTANCE_ID=$INSTANCE_ID python3 $TRINITY_BASE/scripts/trinity_wake_monitor.py${NC}"
echo ""
echo "Test wake:"
echo -e "  ${YELLOW}python3 $TRINITY_BASE/scripts/trinity_trigger.py $INSTANCE_ID --echo 'Hello Trinity!'${NC}"
echo ""

if command -v syncthing &> /dev/null; then
    echo -e "Syncthing: Run ${YELLOW}syncthing${NC} and share ${BLUE}$TRINITY_BASE${NC} with other computers"
fi

echo ""
echo -e "🔱 ${GREEN}Trinity is ready.${NC}"
