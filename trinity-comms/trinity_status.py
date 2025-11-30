#!/usr/bin/env python3
"""
TRINITY STATUS DASHBOARD
========================
Shows the current status of all Trinity instances.

Usage:
    python trinity_status.py
    python trinity_status.py --watch  # Continuous monitoring
"""

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path

# Configuration
TRINITY_BASE = Path(os.environ.get("TRINITY_BASE", os.path.expanduser("~/trinity_shared")))

# All known instances
INSTANCES = [
    # Computer 1
    "C1T1", "C2T1", "C3T1",
    # Computer 2  
    "C1T2", "C2T2", "C3T2",
    # Computer 3
    "C1T3", "C2T3", "C3T3",
]

def get_instance_status(instance_id: str) -> dict:
    """Get status of a specific instance."""
    workspace = TRINITY_BASE / f"{instance_id}_workspace"
    status_file = workspace / "STATUS.json"
    
    if not status_file.exists():
        return {
            "instance": instance_id,
            "status": "unknown",
            "workspace_exists": workspace.exists()
        }
    
    try:
        with open(status_file, 'r') as f:
            return json.load(f)
    except:
        return {
            "instance": instance_id,
            "status": "error",
            "error": "Could not read status file"
        }

def get_pending_tasks() -> list:
    """Get list of pending wake tasks."""
    wake_dir = TRINITY_BASE / "wake"
    if not wake_dir.exists():
        return []
    
    tasks = []
    for task_file in wake_dir.glob("*.task"):
        try:
            with open(task_file, 'r') as f:
                task_data = json.load(f)
            tasks.append({
                "instance": task_file.stem,
                "file": str(task_file),
                "triggered_by": task_data.get("triggered_by", "unknown"),
                "timestamp": task_data.get("timestamp", "unknown")
            })
        except:
            tasks.append({
                "instance": task_file.stem,
                "file": str(task_file),
                "error": "Could not read task file"
            })
    
    return tasks

def get_oracle_inbox() -> list:
    """Get messages in Oracle inbox."""
    inbox = TRINITY_BASE / "oracle_inbox"
    if not inbox.exists():
        return []
    
    messages = []
    for msg_file in inbox.glob("*.json"):
        try:
            with open(msg_file, 'r') as f:
                msg_data = json.load(f)
            messages.append({
                "file": msg_file.name,
                "instance": msg_data.get("instance", "unknown"),
                "timestamp": msg_data.get("timestamp", "unknown"),
                "success": msg_data.get("result", {}).get("success", "unknown")
            })
        except:
            messages.append({
                "file": msg_file.name,
                "error": "Could not read message"
            })
    
    return messages

def get_recent_logs(instance_id: str, lines: int = 5) -> list:
    """Get recent log entries for an instance."""
    log_file = TRINITY_BASE / "logs" / f"{instance_id}.log"
    if not log_file.exists():
        return []
    
    try:
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
        return [line.strip() for line in all_lines[-lines:]]
    except:
        return []

def print_status_symbol(status: str) -> str:
    """Return a symbol for the status."""
    symbols = {
        "monitoring": "🟢",
        "stopped": "🔴",
        "unknown": "⚪",
        "error": "🟠"
    }
    return symbols.get(status, "❓")

def print_dashboard():
    """Print the full dashboard."""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("=" * 70)
    print("🔱 TRINITY STATUS DASHBOARD")
    print(f"   Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Base: {TRINITY_BASE}")
    print("=" * 70)
    
    # Instance Status
    print("\n📊 INSTANCE STATUS")
    print("-" * 40)
    
    for computer in range(1, 4):
        instances = [f"C{i}T{computer}" for i in range(1, 4)]
        print(f"\n  Computer {computer}:")
        for inst in instances:
            status = get_instance_status(inst)
            symbol = print_status_symbol(status.get("status", "unknown"))
            started = status.get("started", "")[:19] if status.get("started") else ""
            print(f"    {symbol} {inst}: {status.get('status', 'unknown'):<12} {started}")
    
    # Pending Tasks
    print("\n\n⏳ PENDING WAKE TASKS")
    print("-" * 40)
    tasks = get_pending_tasks()
    if tasks:
        for task in tasks:
            print(f"  📋 {task['instance']}: from {task.get('triggered_by', '?')}")
    else:
        print("  (no pending tasks)")
    
    # Oracle Inbox
    print("\n\n📬 ORACLE INBOX")
    print("-" * 40)
    messages = get_oracle_inbox()
    if messages:
        for msg in messages[-5:]:  # Last 5 messages
            success = "✅" if msg.get("success") else "❌"
            print(f"  {success} {msg.get('instance', '?')}: {msg.get('file', '')}")
    else:
        print("  (no messages)")
    
    # Recent Activity
    print("\n\n📜 RECENT ACTIVITY (C1T1)")
    print("-" * 40)
    logs = get_recent_logs("C1T1", 5)
    if logs:
        for log in logs:
            print(f"  {log[:65]}...")
    else:
        print("  (no logs)")
    
    print("\n" + "=" * 70)
    print("Press Ctrl+C to exit")

def main():
    parser = argparse.ArgumentParser(description="Trinity Status Dashboard")
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Continuously update the dashboard"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=5,
        help="Update interval in seconds (default: 5)"
    )
    
    args = parser.parse_args()
    
    if args.watch:
        try:
            while True:
                print_dashboard()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard closed")
    else:
        print_dashboard()

if __name__ == "__main__":
    main()
