#!/usr/bin/env python3
"""
TRINITY FILE WATCHER
Folder-based synchronization with file watchers
Works with Syncthing, shared folders, or git-synced directories

Setup:
  pip install watchdog --break-system-packages

Usage:
  # Watch for incoming messages and auto-process:
  python trinity_filewatcher.py --instance T1 --trinity-path ~/.trinity --watch
  
  # Send a message via file:
  python trinity_filewatcher.py --instance T1 --trinity-path ~/.trinity \\
      --send --to C1 --subject "Hello" --body "Test message"
  
  # Check status dashboard:
  python trinity_filewatcher.py --instance T1 --trinity-path ~/.trinity --dashboard
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent
except ImportError:
    print("watchdog not installed. Run: pip install watchdog --break-system-packages")
    sys.exit(1)

# ============================================
# CONFIGURATION
# ============================================

DEFAULT_TRINITY_PATH = os.path.expanduser("~/.trinity")

# ============================================
# FILE STRUCTURE MANAGER
# ============================================

class TrinityFileManager:
    """Manages the .trinity folder structure"""
    
    def __init__(self, instance_id: str, trinity_path: str = DEFAULT_TRINITY_PATH):
        self.instance_id = instance_id
        self.base_path = Path(trinity_path)
        
        # Define folder structure
        self.messages_dir = self.base_path / "messages"
        self.inbox_dir = self.messages_dir / "inbox" / instance_id.lower()
        self.outbox_dir = self.messages_dir / "outbox"
        self.broadcast_dir = self.messages_dir / "broadcast"
        self.status_dir = self.base_path / "status"
        self.heartbeat_dir = self.base_path / "heartbeat"
        self.tasks_dir = self.base_path / "tasks"
        self.sync_file = self.base_path / "SYNC.md"
        self.live_sync_file = self.base_path / "LIVE_SYNC.md"
        
        # Create directories
        self._init_directories()
    
    def _init_directories(self):
        """Create all necessary directories"""
        dirs = [
            self.messages_dir,
            self.inbox_dir,
            self.outbox_dir,
            self.broadcast_dir,
            self.status_dir,
            self.heartbeat_dir,
            self.tasks_dir
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def send_message(self, to: str, subject: str, body: str, 
                    priority: str = "NORMAL", metadata: dict = None) -> str:
        """Send a message by creating a file"""
        timestamp = datetime.utcnow()
        message_id = f"{self.instance_id}_to_{to}_{int(timestamp.timestamp() * 1000)}"
        
        message = {
            "id": message_id,
            "from": self.instance_id,
            "to": to,
            "subject": subject,
            "body": body,
            "priority": priority,
            "metadata": metadata or {},
            "timestamp": timestamp.isoformat() + "Z",
            "read": False
        }
        
        # Determine target directory
        if to.upper() == "BROADCAST":
            target_dir = self.broadcast_dir
        else:
            # Create inbox for target if it doesn't exist
            target_inbox = self.messages_dir / "inbox" / to.lower()
            target_inbox.mkdir(parents=True, exist_ok=True)
            target_dir = target_inbox
        
        # Write message file
        filename = f"{message_id}.json"
        filepath = target_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(message, f, indent=2)
        
        # Also save to outbox for record
        outbox_file = self.outbox_dir / filename
        with open(outbox_file, 'w') as f:
            json.dump(message, f, indent=2)
        
        return message_id
    
    def read_messages(self, unread_only: bool = False, mark_read: bool = False, 
                     include_broadcast: bool = True) -> list:
        """Read messages from inbox and broadcast"""
        messages = []
        
        # Read from personal inbox
        if self.inbox_dir.exists():
            for f in self.inbox_dir.glob("*.json"):
                msg = self._read_message_file(f, mark_read)
                if msg and (not unread_only or not msg.get("read")):
                    messages.append(msg)
        
        # Read from broadcast
        if include_broadcast and self.broadcast_dir.exists():
            for f in self.broadcast_dir.glob("*.json"):
                msg = self._read_message_file(f, mark_read)
                if msg and (not unread_only or not msg.get("read")):
                    # Don't mark broadcast as read (shared by all)
                    messages.append(msg)
        
        # Sort by timestamp
        messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return messages
    
    def _read_message_file(self, filepath: Path, mark_read: bool = False) -> dict:
        """Read a single message file"""
        try:
            with open(filepath, 'r') as f:
                msg = json.load(f)
            
            if mark_read and not msg.get("read"):
                msg["read"] = True
                msg["read_at"] = datetime.utcnow().isoformat() + "Z"
                with open(filepath, 'w') as f:
                    json.dump(msg, f, indent=2)
            
            msg["_filepath"] = str(filepath)
            return msg
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None
    
    def update_status(self, status: str, task: str = None, health: str = "green",
                     capabilities: list = None, autonomy_level: int = 1):
        """Update status and heartbeat"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        status_data = {
            "instance_id": self.instance_id,
            "status": status,
            "current_task": task,
            "health": health,
            "capabilities": capabilities or [],
            "autonomy_level": autonomy_level,
            "timestamp": timestamp,
            "last_heartbeat": timestamp
        }
        
        # Write to both status and heartbeat
        status_file = self.status_dir / f"{self.instance_id}.json"
        heartbeat_file = self.heartbeat_dir / f"{self.instance_id}.json"
        
        for f in [status_file, heartbeat_file]:
            with open(f, 'w') as fp:
                json.dump(status_data, fp, indent=2)
    
    def get_all_status(self, stale_threshold: int = 60) -> list:
        """Get status of all instances"""
        statuses = []
        now = datetime.utcnow()
        
        for f in self.status_dir.glob("*.json"):
            try:
                with open(f, 'r') as fp:
                    status = json.load(fp)
                
                # Check if stale
                ts = datetime.fromisoformat(status.get("timestamp", "").replace("Z", ""))
                age = (now - ts).total_seconds()
                status["age_seconds"] = int(age)
                status["is_stale"] = age > stale_threshold
                
                statuses.append(status)
            except Exception as e:
                print(f"Error reading {f}: {e}")
        
        return statuses
    
    def append_sync(self, section: str, content: str, target: str = "SYNC"):
        """Append to sync file"""
        filepath = self.sync_file if target == "SYNC" else self.live_sync_file
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        entry = f"\n## [{timestamp}] {self.instance_id} - {section}\n\n{content}\n\n---\n"
        
        # Create file if needed
        if not filepath.exists():
            with open(filepath, 'w') as f:
                f.write(f"# 🔱 TRINITY {target} FILE\n\nProtocol: File-based coordination\n\n---\n")
        
        with open(filepath, 'a') as f:
            f.write(entry)
    
    def create_task(self, task_id: str, title: str, description: str,
                   assigned_to: str, priority: str = "NORMAL", domain: str = None):
        """Create a task file"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "assigned_to": assigned_to,
            "created_by": self.instance_id,
            "priority": priority,
            "domain": domain,
            "status": "PENDING",
            "created_at": timestamp,
            "updated_at": timestamp
        }
        
        filepath = self.tasks_dir / f"{task_id}.json"
        with open(filepath, 'w') as f:
            json.dump(task, f, indent=2)
        
        # Notify assigned instance
        self.send_message(
            to=assigned_to,
            subject=f"New Task: {title}",
            body=f"Task ID: {task_id}\n\n{description}",
            priority=priority
        )
        
        return task_id


# ============================================
# FILE WATCHER
# ============================================

class TrinityWatcher(FileSystemEventHandler):
    """Watch for new messages and status changes"""
    
    def __init__(self, manager: TrinityFileManager, callback: Callable = None):
        self.manager = manager
        self.callback = callback
        self.processed_files = set()
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        filepath = Path(event.src_path)
        
        # Skip if already processed
        if str(filepath) in self.processed_files:
            return
        self.processed_files.add(str(filepath))
        
        # Check if it's a message for us
        if "inbox" in str(filepath) or "broadcast" in str(filepath):
            if filepath.suffix == ".json":
                self._handle_new_message(filepath)
        
        # Check if it's a status update
        elif "status" in str(filepath) or "heartbeat" in str(filepath):
            if filepath.suffix == ".json":
                self._handle_status_update(filepath)
    
    def on_modified(self, event):
        # Handle modifications similarly
        if not event.is_directory and event.src_path.endswith(".json"):
            filepath = Path(event.src_path)
            if "status" in str(filepath):
                self._handle_status_update(filepath)
    
    def _handle_new_message(self, filepath: Path):
        """Process a new message"""
        try:
            with open(filepath, 'r') as f:
                msg = json.load(f)
            
            # Skip our own messages
            if msg.get("from") == self.manager.instance_id:
                return
            
            priority_icon = {
                "LOW": "⬜", "NORMAL": "🟦", "HIGH": "🟧", "URGENT": "🟥"
            }.get(msg.get("priority", "NORMAL"), "🟦")
            
            print(f"\n{priority_icon} NEW MESSAGE from {msg.get('from')}:")
            print(f"   Subject: {msg.get('subject')}")
            print(f"   Body: {msg.get('body')}")
            print(f"   Time: {msg.get('timestamp')}")
            
            if self.callback:
                self.callback("message", msg)
        
        except Exception as e:
            print(f"Error processing message {filepath}: {e}")
    
    def _handle_status_update(self, filepath: Path):
        """Process a status update"""
        try:
            with open(filepath, 'r') as f:
                status = json.load(f)
            
            # Skip our own status
            if status.get("instance_id") == self.manager.instance_id:
                return
            
            health_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(status.get("health"), "⚪")
            
            print(f"\n{health_icon} STATUS UPDATE: {status.get('instance_id')}")
            print(f"   Status: {status.get('status')}")
            print(f"   Task: {status.get('current_task', 'None')}")
            
            if self.callback:
                self.callback("status", status)
        
        except Exception as e:
            pass  # Status files get updated frequently, ignore errors


def run_watcher(manager: TrinityFileManager):
    """Run the file watcher"""
    print(f"🔱 [{manager.instance_id}] Starting file watcher...")
    print(f"   Watching: {manager.base_path}")
    print("-" * 50)
    
    # Update our status
    manager.update_status("ONLINE", task="Watching for messages")
    
    event_handler = TrinityWatcher(manager)
    observer = Observer()
    
    # Watch messages and status directories
    observer.schedule(event_handler, str(manager.messages_dir), recursive=True)
    observer.schedule(event_handler, str(manager.status_dir), recursive=True)
    
    observer.start()
    
    try:
        # Heartbeat loop
        while True:
            manager.update_status("ONLINE", health="green")
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n👋 Shutting down watcher...")
        manager.update_status("OFFLINE")
        observer.stop()
    
    observer.join()


def print_dashboard(manager: TrinityFileManager):
    """Print status dashboard"""
    print("\n📊 TRINITY STATUS DASHBOARD")
    print("=" * 50)
    
    statuses = manager.get_all_status()
    
    if not statuses:
        print("No instance status found")
        return
    
    for s in statuses:
        health_icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(s.get("health"), "⚪")
        stale = " ⚠️ STALE" if s.get("is_stale") else ""
        
        print(f"\n{health_icon} {s.get('instance_id')}: {s.get('status')}{stale}")
        print(f"   Task: {s.get('current_task', 'None')}")
        print(f"   Last seen: {s.get('age_seconds', '?')}s ago")
        print(f"   Autonomy: Level {s.get('autonomy_level', 0)}")


# ============================================
# CLI INTERFACE
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Trinity File-Based Communication")
    parser.add_argument("--instance", "-i", required=True, help="Instance ID (T1, C1, etc.)")
    parser.add_argument("--trinity-path", "-p", default=DEFAULT_TRINITY_PATH, 
                       help="Path to .trinity folder")
    
    # Modes
    parser.add_argument("--watch", "-w", action="store_true", help="Watch for messages")
    parser.add_argument("--dashboard", "-d", action="store_true", help="Show status dashboard")
    parser.add_argument("--send", "-s", action="store_true", help="Send a message")
    parser.add_argument("--read", "-r", action="store_true", help="Read messages")
    parser.add_argument("--status", action="store_true", help="Update status")
    
    # Message options
    parser.add_argument("--to", help="Message recipient")
    parser.add_argument("--subject", help="Message subject")
    parser.add_argument("--body", help="Message body")
    parser.add_argument("--priority", default="NORMAL", 
                       choices=["LOW", "NORMAL", "HIGH", "URGENT"])
    
    # Status options
    parser.add_argument("--set-status", help="Set status (ONLINE, BUSY, etc.)")
    parser.add_argument("--task", help="Current task description")
    
    args = parser.parse_args()
    
    manager = TrinityFileManager(args.instance, args.trinity_path)
    
    if args.watch:
        run_watcher(manager)
    
    elif args.dashboard:
        print_dashboard(manager)
    
    elif args.send:
        if not args.to or not args.subject or not args.body:
            print("Error: --to, --subject, and --body required for sending")
            return
        
        msg_id = manager.send_message(
            to=args.to,
            subject=args.subject,
            body=args.body,
            priority=args.priority
        )
        print(f"✅ Message sent: {msg_id}")
    
    elif args.read:
        messages = manager.read_messages(mark_read=True)
        
        if not messages:
            print("📭 No messages")
            return
        
        print(f"📬 {len(messages)} message(s):\n")
        for msg in messages:
            priority_icon = {
                "LOW": "⬜", "NORMAL": "🟦", "HIGH": "🟧", "URGENT": "🟥"
            }.get(msg.get("priority", "NORMAL"), "🟦")
            
            print(f"{priority_icon} From: {msg.get('from')} | {msg.get('timestamp')}")
            print(f"   Subject: {msg.get('subject')}")
            print(f"   {msg.get('body')}")
            print("-" * 40)
    
    elif args.status:
        if args.set_status:
            manager.update_status(args.set_status, args.task)
            print(f"✅ Status set to {args.set_status}")
        else:
            print_dashboard(manager)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
