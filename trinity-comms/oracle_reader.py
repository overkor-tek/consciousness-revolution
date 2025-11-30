#!/usr/bin/env python3
"""
ORACLE READER
=============
Reads and processes results from the Trinity network.
Used by Desktop Claude (Oracle) to receive terminal outputs.

Usage:
    python oracle_reader.py                    # List all messages
    python oracle_reader.py --read             # Read all unread messages
    python oracle_reader.py --read C1T1        # Read messages from C1T1
    python oracle_reader.py --clear            # Clear all processed messages
    python oracle_reader.py --watch            # Watch for new messages
"""

import argparse
import json
import os
import time
from datetime import datetime
from pathlib import Path

# Configuration
TRINITY_BASE = Path(os.environ.get("TRINITY_BASE", os.path.expanduser("~/trinity_shared")))
INBOX_DIR = TRINITY_BASE / "oracle_inbox"
OUTBOX_DIR = TRINITY_BASE / "oracle_outbox"
PROCESSED_DIR = TRINITY_BASE / "oracle_processed"

# Ensure directories exist
for d in [INBOX_DIR, OUTBOX_DIR, PROCESSED_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def list_messages(instance_filter: str = None) -> list:
    """List all messages in the inbox."""
    messages = []
    
    for msg_file in sorted(INBOX_DIR.glob("*.json")):
        try:
            with open(msg_file, 'r') as f:
                msg_data = json.load(f)
            
            instance = msg_data.get("instance", "unknown")
            
            if instance_filter and instance != instance_filter:
                continue
                
            messages.append({
                "file": msg_file,
                "instance": instance,
                "task_id": msg_data.get("task_id", "unknown"),
                "timestamp": msg_data.get("timestamp", "unknown"),
                "success": msg_data.get("result", {}).get("success", False),
                "data": msg_data
            })
        except Exception as e:
            print(f"⚠️ Error reading {msg_file}: {e}")
    
    return messages

def read_message(msg: dict) -> str:
    """Format a message for display."""
    data = msg["data"]
    result = data.get("result", {})
    
    output = []
    output.append("=" * 60)
    output.append(f"📬 MESSAGE FROM: {msg['instance']}")
    output.append(f"   Task ID: {msg['task_id']}")
    output.append(f"   Time: {msg['timestamp']}")
    output.append(f"   Success: {'✅' if msg['success'] else '❌'}")
    output.append("-" * 60)
    
    # Original task
    original = data.get("original_task", {})
    if original.get("prompt"):
        output.append(f"📋 ORIGINAL PROMPT:")
        output.append(f"   {original['prompt'][:200]}...")
    
    # Result
    output.append(f"\n📤 RESULT:")
    if result.get("stdout"):
        output.append("   STDOUT:")
        for line in result["stdout"].split("\n")[:20]:
            output.append(f"      {line}")
    if result.get("stderr"):
        output.append("   STDERR:")
        for line in result["stderr"].split("\n")[:10]:
            output.append(f"      {line}")
    if result.get("error"):
        output.append(f"   ERROR: {result['error']}")
    if result.get("message"):
        output.append(f"   MESSAGE: {result['message']}")
    
    output.append("=" * 60)
    
    return "\n".join(output)

def process_messages(instance_filter: str = None, archive: bool = True):
    """Read and optionally archive messages."""
    messages = list_messages(instance_filter)
    
    if not messages:
        print("📭 No messages in inbox")
        return
    
    print(f"\n📬 Found {len(messages)} message(s)\n")
    
    for msg in messages:
        print(read_message(msg))
        
        if archive:
            # Move to processed folder
            archive_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{msg['file'].name}"
            archive_path = PROCESSED_DIR / archive_name
            msg["file"].rename(archive_path)
            print(f"   (archived to {archive_name})")
        
        print()

def send_task(instance_id: str, prompt: str, chain: list = None):
    """Send a task from Oracle to the terminal network."""
    task_file = OUTBOX_DIR / f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    task_data = {
        "target": instance_id,
        "prompt": prompt,
        "from": "oracle",
        "timestamp": datetime.now().isoformat(),
        "chain": chain
    }
    
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    print(f"📤 Task written to outbox: {task_file.name}")
    print(f"   Target: {instance_id}")
    print(f"   Prompt: {prompt[:50]}...")
    
    # Also create the wake file directly for immediate execution
    wake_file = TRINITY_BASE / "wake" / f"{instance_id}.task"
    wake_data = {
        "task_type": "claude",
        "prompt": prompt,
        "triggered_by": "oracle",
        "timestamp": datetime.now().isoformat(),
        "report_to_oracle": True
    }
    
    if chain:
        wake_data["wake_next"] = chain[0] if chain else None
        wake_data["chain_task"] = prompt
    
    with open(wake_file, 'w') as f:
        json.dump(wake_data, f, indent=2)
    
    print(f"⚡ Wake signal sent to {instance_id}")

def watch_inbox(interval: int = 5):
    """Watch inbox for new messages."""
    print(f"👁️ Watching inbox for new messages (interval: {interval}s)")
    print("   Press Ctrl+C to stop\n")
    
    seen_files = set()
    
    # Initial scan
    for f in INBOX_DIR.glob("*.json"):
        seen_files.add(f.name)
    
    try:
        while True:
            time.sleep(interval)
            
            current_files = set(f.name for f in INBOX_DIR.glob("*.json"))
            new_files = current_files - seen_files
            
            if new_files:
                print(f"\n🔔 NEW MESSAGES: {len(new_files)}")
                for fname in new_files:
                    msg_file = INBOX_DIR / fname
                    try:
                        with open(msg_file, 'r') as f:
                            data = json.load(f)
                        print(f"   📬 From {data.get('instance', '?')}: {data.get('task_id', '?')}")
                    except:
                        print(f"   📬 {fname}")
                
                seen_files = current_files
                
    except KeyboardInterrupt:
        print("\n\n👋 Stopped watching")

def clear_inbox():
    """Move all messages to processed folder."""
    messages = list(INBOX_DIR.glob("*.json"))
    
    if not messages:
        print("📭 Inbox already empty")
        return
    
    for msg_file in messages:
        archive_name = f"cleared_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{msg_file.name}"
        archive_path = PROCESSED_DIR / archive_name
        msg_file.rename(archive_path)
    
    print(f"🗑️ Cleared {len(messages)} message(s) to processed folder")

def main():
    parser = argparse.ArgumentParser(description="Oracle Reader - Read Trinity results")
    
    parser.add_argument(
        "instance",
        nargs="?",
        help="Filter messages by instance ID"
    )
    
    parser.add_argument(
        "--read", "-r",
        action="store_true",
        help="Read and archive messages"
    )
    
    parser.add_argument(
        "--watch", "-w",
        action="store_true",
        help="Watch for new messages"
    )
    
    parser.add_argument(
        "--clear", "-c",
        action="store_true",
        help="Clear all messages from inbox"
    )
    
    parser.add_argument(
        "--send", "-s",
        metavar="PROMPT",
        help="Send a task to specified instance"
    )
    
    parser.add_argument(
        "--chain",
        help="Chain instances for task (comma-separated)"
    )
    
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=5,
        help="Watch interval in seconds"
    )
    
    args = parser.parse_args()
    
    if args.clear:
        clear_inbox()
    elif args.watch:
        watch_inbox(args.interval)
    elif args.send:
        if not args.instance:
            print("❌ Must specify instance ID with --send")
            exit(1)
        chain = args.chain.split(",") if args.chain else None
        send_task(args.instance, args.send, chain)
    elif args.read:
        process_messages(args.instance, archive=True)
    else:
        # Just list messages
        messages = list_messages(args.instance)
        if messages:
            print(f"\n📬 {len(messages)} message(s) in inbox:\n")
            for msg in messages:
                status = "✅" if msg["success"] else "❌"
                print(f"  {status} {msg['instance']}: {msg['task_id']} ({msg['timestamp'][:19]})")
        else:
            print("📭 No messages in inbox")

if __name__ == "__main__":
    main()
