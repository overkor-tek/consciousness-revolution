#!/usr/bin/env python3
"""
TRINITY WAKE MONITOR v1.0
=========================
Production-ready wake system for Trinity orchestration.

Each terminal instance runs this monitor. When a .task file appears
with this instance's ID, it wakes up, executes the task, and optionally
wakes the next instance in the chain.

Usage:
    INSTANCE_ID=C1T1 python trinity_wake_monitor.py
    
Or edit INSTANCE_ID below.
"""

import time
import os
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ watchdog not installed. Run: pip install watchdog")
    exit(1)

# =============================================================================
# CONFIGURATION
# =============================================================================

# Instance ID - change this per terminal or set via environment variable
INSTANCE_ID = os.environ.get("INSTANCE_ID", "C1T1")

# Base directory for Trinity shared folder
TRINITY_BASE = Path(os.environ.get("TRINITY_BASE", os.path.expanduser("~/trinity_shared")))

# Subdirectories
WAKE_DIR = TRINITY_BASE / "wake"
INBOX_DIR = TRINITY_BASE / "oracle_inbox"
OUTBOX_DIR = TRINITY_BASE / "oracle_outbox"
WORKSPACE_DIR = TRINITY_BASE / f"{INSTANCE_ID}_workspace"
LOGS_DIR = TRINITY_BASE / "logs"

# Create directories if they don't exist
for d in [WAKE_DIR, INBOX_DIR, OUTBOX_DIR, WORKSPACE_DIR, LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format=f'[{INSTANCE_ID}] %(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / f"{INSTANCE_ID}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# TASK EXECUTION
# =============================================================================

def execute_claude_task(prompt: str, allowed_tools: str = "Bash,Read,Write") -> dict:
    """Execute a Claude Code task in headless mode."""
    logger.info(f"Executing prompt: {prompt[:100]}...")
    
    try:
        result = subprocess.run(
            [
                "claude", "-p", prompt,
                "--allowedTools", allowed_tools,
                "--output-format", "text"
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        logger.error("Task timed out after 5 minutes")
        return {"success": False, "error": "timeout"}
    except FileNotFoundError:
        logger.error("Claude CLI not found. Is Claude Code installed?")
        return {"success": False, "error": "claude_not_found"}
    except Exception as e:
        logger.error(f"Execution error: {e}")
        return {"success": False, "error": str(e)}

def execute_bash_task(command: str) -> dict:
    """Execute a direct bash command."""
    logger.info(f"Executing bash: {command[:100]}...")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        logger.error(f"Bash error: {e}")
        return {"success": False, "error": str(e)}

def execute_python_task(script_path: str) -> dict:
    """Execute a Python script."""
    logger.info(f"Executing Python: {script_path}")
    
    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        logger.error(f"Python error: {e}")
        return {"success": False, "error": str(e)}

# =============================================================================
# WAKE SYSTEM
# =============================================================================

def wake_next_instance(next_id: str, task_data: dict):
    """Create a wake file for the next instance in the chain."""
    wake_file = WAKE_DIR / f"{next_id}.task"
    
    wake_data = {
        "prompt": task_data.get("chain_task", task_data.get("prompt", "")),
        "task_type": task_data.get("task_type", "claude"),
        "triggered_by": INSTANCE_ID,
        "timestamp": datetime.now().isoformat(),
        "chain_context": task_data.get("chain_context", {}),
        "wake_next": task_data.get("chain_next")  # Continue the chain
    }
    
    with open(wake_file, 'w') as f:
        json.dump(wake_data, f, indent=2)
    
    logger.info(f"⭐ Woke next instance: {next_id}")

def write_result(task_id: str, result: dict, task_data: dict):
    """Write task result to workspace and optionally to oracle inbox."""
    # Write to own workspace
    result_file = WORKSPACE_DIR / f"result_{task_id}.json"
    result_data = {
        "task_id": task_id,
        "instance": INSTANCE_ID,
        "timestamp": datetime.now().isoformat(),
        "original_task": task_data,
        "result": result
    }
    
    with open(result_file, 'w') as f:
        json.dump(result_data, f, indent=2)
    
    logger.info(f"📝 Result written to {result_file}")
    
    # If this is the final task in chain, write to oracle inbox
    if task_data.get("report_to_oracle", False) or not task_data.get("wake_next"):
        oracle_file = INBOX_DIR / f"result_{INSTANCE_ID}_{task_id}.json"
        with open(oracle_file, 'w') as f:
            json.dump(result_data, f, indent=2)
        logger.info(f"📬 Result sent to Oracle inbox")

def process_task(task_file: Path):
    """Process an incoming task file."""
    task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        with open(task_file, 'r') as f:
            task_data = json.load(f)
        
        logger.info(f"📋 Processing task from: {task_data.get('triggered_by', 'unknown')}")
        
        # Determine task type and execute
        task_type = task_data.get("task_type", "claude")
        
        if task_type == "claude":
            prompt = task_data.get("prompt", "")
            if prompt:
                result = execute_claude_task(
                    prompt, 
                    task_data.get("allowed_tools", "Bash,Read,Write")
                )
            else:
                result = {"success": False, "error": "no_prompt"}
                
        elif task_type == "bash":
            command = task_data.get("command", "")
            result = execute_bash_task(command)
            
        elif task_type == "python":
            script = task_data.get("script", "")
            result = execute_python_task(script)
            
        elif task_type == "echo":
            # Simple test task
            message = task_data.get("message", "Hello from Trinity!")
            logger.info(f"📢 ECHO: {message}")
            result = {"success": True, "message": message}
            
        else:
            result = {"success": False, "error": f"unknown_task_type: {task_type}"}
        
        # Write result
        write_result(task_id, result, task_data)
        
        # Remove processed task file
        task_file.unlink()
        logger.info(f"✅ Task complete, file removed")
        
        # Wake next instance if specified
        next_instance = task_data.get("wake_next")
        if next_instance:
            wake_next_instance(next_instance, task_data)
        
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in task file: {e}")
        # Move bad file to error location
        error_file = WORKSPACE_DIR / f"error_{task_file.name}"
        task_file.rename(error_file)
        return {"success": False, "error": "invalid_json"}
        
    except Exception as e:
        logger.error(f"Task processing error: {e}")
        return {"success": False, "error": str(e)}

# =============================================================================
# WATCHDOG EVENT HANDLER
# =============================================================================

class TrinityWakeHandler(FileSystemEventHandler):
    """Handles file system events for Trinity wake system."""
    
    def on_created(self, event):
        """Called when a file is created in the wake directory."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Check if this is our task file
        expected_name = f"{INSTANCE_ID}.task"
        if file_path.name == expected_name:
            logger.info(f"🔥 WAKE SIGNAL DETECTED!")
            
            # Small delay to ensure file is fully written
            time.sleep(0.5)
            
            # Process the task
            process_task(file_path)

# =============================================================================
# MAIN MONITOR LOOP
# =============================================================================

def run_monitor():
    """Main monitoring loop."""
    logger.info("=" * 60)
    logger.info(f"🔱 TRINITY WAKE MONITOR STARTING")
    logger.info(f"   Instance: {INSTANCE_ID}")
    logger.info(f"   Watching: {WAKE_DIR}")
    logger.info(f"   Workspace: {WORKSPACE_DIR}")
    logger.info("=" * 60)
    
    # Write status file
    status_file = WORKSPACE_DIR / "STATUS.json"
    with open(status_file, 'w') as f:
        json.dump({
            "instance": INSTANCE_ID,
            "status": "monitoring",
            "started": datetime.now().isoformat(),
            "wake_dir": str(WAKE_DIR),
            "workspace": str(WORKSPACE_DIR)
        }, f, indent=2)
    
    # Setup watchdog
    event_handler = TrinityWakeHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WAKE_DIR), recursive=False)
    observer.start()
    
    logger.info("👁️ Watchdog active. Waiting for tasks...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Shutdown signal received")
        observer.stop()
        
        # Update status
        with open(status_file, 'w') as f:
            json.dump({
                "instance": INSTANCE_ID,
                "status": "stopped",
                "stopped": datetime.now().isoformat()
            }, f, indent=2)
    
    observer.join()
    logger.info("👋 Monitor stopped")

# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_monitor()
