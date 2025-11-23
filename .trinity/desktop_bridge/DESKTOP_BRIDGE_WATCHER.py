#!/usr/bin/env python3
"""
DESKTOP BRIDGE WATCHER
Monitors Desktop Claude's outbox and relays messages to Trinity.
Runs in background to bridge the sandboxed Desktop Claude.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# Paths
TRINITY_MESSAGES = Path.home() / ".claude" / "trinity_messages"
INBOX = TRINITY_MESSAGES / "inbox"
OUTBOX = TRINITY_MESSAGES / "outbox"
TRINITY_DIR = Path.home() / "100X_DEPLOYMENT" / ".trinity"
RELAY_DIR = TRINITY_DIR / "desktop_relay"

class OutboxHandler(FileSystemEventHandler):
    """Watch for new files in Desktop's outbox"""

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = Path(event.src_path)
        if filepath.suffix in ['.txt', '.md', '.json']:
            print(f"📤 New outbox message: {filepath.name}")
            self.relay_message(filepath)

    def relay_message(self, filepath):
        """Relay message to Trinity system"""
        try:
            content = filepath.read_text()

            # Create relay file
            RELAY_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            relay_file = RELAY_DIR / f"desktop_{timestamp}_{filepath.name}"

            message = {
                "from": "desktop-claude",
                "timestamp": datetime.now().isoformat(),
                "original_file": filepath.name,
                "content": content
            }

            relay_file.write_text(json.dumps(message, indent=2))
            print(f"  ✅ Relayed to: {relay_file.name}")

            # Git sync
            self.git_sync()

            # Archive the outbox file
            archive = OUTBOX / "sent"
            archive.mkdir(exist_ok=True)
            filepath.rename(archive / f"{timestamp}_{filepath.name}")

        except Exception as e:
            print(f"  ❌ Relay error: {e}")

    def git_sync(self):
        """Push relay to git"""
        repo = Path.home() / "100X_DEPLOYMENT"
        try:
            subprocess.run(["git", "add", "-A"], cwd=repo, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "desktop bridge: message relay"],
                cwd=repo, capture_output=True
            )
            subprocess.run(
                ["git", "push", "overkor-tek", "HEAD:master"],
                cwd=repo, capture_output=True
            )
            print("  📡 Git synced")
        except:
            pass

def send_to_desktop(message, filename=None):
    """Send a message to Desktop Claude's inbox"""
    INBOX.mkdir(parents=True, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"msg_{timestamp}.txt"

    inbox_file = INBOX / filename
    inbox_file.write_text(message)
    print(f"📥 Sent to Desktop inbox: {filename}")

def main():
    print("=" * 50)
    print("  DESKTOP BRIDGE WATCHER")
    print("=" * 50)
    print()

    # Ensure directories exist
    INBOX.mkdir(parents=True, exist_ok=True)
    OUTBOX.mkdir(parents=True, exist_ok=True)

    # Set up watcher
    event_handler = OutboxHandler()
    observer = Observer()
    observer.schedule(event_handler, str(OUTBOX), recursive=False)
    observer.start()

    print(f"👁️ Watching: {OUTBOX}")
    print(f"📥 Inbox: {INBOX}")
    print()
    print("Desktop Claude can now:")
    print("  1. Read messages from inbox/")
    print("  2. Write messages to outbox/")
    print("  3. Bridge will relay to Trinity")
    print()
    print("Press Ctrl+C to stop")
    print()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Bridge stopped")

    observer.join()

if __name__ == "__main__":
    main()
