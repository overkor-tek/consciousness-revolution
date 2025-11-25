#!/usr/bin/env python3
"""
NERVE CENTER INPUT SENSOR
Real-world input integration for Trinity system

Collects inputs from multiple sources:
- Web scraping (news, docs, APIs)
- File watchers (local changes)
- Command queue (user input)
- API endpoints (external triggers)
"""

import os
import json
import hashlib
import requests
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Paths
CONSCIOUSNESS_DIR = Path.home() / ".consciousness"
INPUTS_DIR = CONSCIOUSNESS_DIR / "inputs"
QUEUE_DIR = INPUTS_DIR / "queue"
PROCESSED_DIR = INPUTS_DIR / "processed"

class InputSensor:
    """Base class for all input sensors"""

    def __init__(self, sensor_id: str, sensor_type: str):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.ensure_dirs()

    def ensure_dirs(self):
        """Create necessary directories"""
        for dir in [INPUTS_DIR, QUEUE_DIR, PROCESSED_DIR]:
            dir.mkdir(parents=True, exist_ok=True)

    def generate_input_id(self, content: str) -> str:
        """Generate unique input ID"""
        return hashlib.sha256(f"{content}{datetime.now().timestamp()}".encode()).hexdigest()[:12]

    def queue_input(self, content: str, metadata: dict = None, priority: int = 5):
        """Queue an input for processing"""
        input_id = self.generate_input_id(content)

        input_data = {
            "id": input_id,
            "timestamp": datetime.now().isoformat() + "Z",
            "sensor_id": self.sensor_id,
            "sensor_type": self.sensor_type,
            "priority": priority,  # 1=highest, 10=lowest
            "content": content,
            "metadata": metadata or {},
            "status": "queued"
        }

        # Save to queue
        queue_file = QUEUE_DIR / f"input_{input_id}.json"
        with open(queue_file, 'w') as f:
            json.dump(input_data, f, indent=2)

        print(f"[SENSOR:{self.sensor_id}] Queued input {input_id} (priority {priority})")
        return input_id

    def mark_processed(self, input_id: str):
        """Mark input as processed"""
        queue_file = QUEUE_DIR / f"input_{input_id}.json"
        processed_file = PROCESSED_DIR / f"input_{input_id}.json"

        if queue_file.exists():
            # Update status
            with open(queue_file, 'r') as f:
                data = json.load(f)

            data["status"] = "processed"
            data["processed_at"] = datetime.now().isoformat() + "Z"

            # Move to processed
            with open(processed_file, 'w') as f:
                json.dump(data, f, indent=2)

            queue_file.unlink()

            print(f"[SENSOR:{self.sensor_id}] Marked {input_id} as processed")


class WebScraperSensor(InputSensor):
    """Sensor for web content"""

    def __init__(self):
        super().__init__("web_scraper", "web")

    def scrape_url(self, url: str, priority: int = 5):
        """Scrape content from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            content = response.text

            metadata = {
                "url": url,
                "status_code": response.status_code,
                "content_type": response.headers.get("Content-Type"),
                "content_length": len(content)
            }

            input_id = self.queue_input(
                content=content[:10000],  # Limit to 10KB
                metadata=metadata,
                priority=priority
            )

            return input_id

        except Exception as e:
            print(f"[SENSOR:web_scraper] Failed to scrape {url}: {e}")
            return None

    def scrape_feed(self, feed_urls: List[str]):
        """Scrape multiple URLs from a feed"""
        for url in feed_urls:
            self.scrape_url(url, priority=6)
            time.sleep(1)  # Rate limiting


class FileWatcherSensor(InputSensor, FileSystemEventHandler):
    """Sensor for file system changes"""

    def __init__(self, watch_path: str):
        InputSensor.__init__(self, "file_watcher", "filesystem")
        self.watch_path = Path(watch_path)
        self.observer = Observer()

    def start_watching(self):
        """Start watching directory"""
        self.observer.schedule(self, str(self.watch_path), recursive=True)
        self.observer.start()
        print(f"[SENSOR:file_watcher] Watching {self.watch_path}")

    def stop_watching(self):
        """Stop watching"""
        self.observer.stop()
        self.observer.join()

    def on_modified(self, event):
        """Handle file modification"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Ignore certain files
        if file_path.suffix in ['.log', '.tmp', '.pyc']:
            return
        if '.git' in str(file_path):
            return

        # Read file content
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            metadata = {
                "file_path": str(file_path),
                "file_size": file_path.stat().st_size,
                "modified_time": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }

            self.queue_input(
                content=f"File modified: {file_path}\n\n{content[:5000]}",
                metadata=metadata,
                priority=7
            )

        except Exception as e:
            print(f"[SENSOR:file_watcher] Failed to read {file_path}: {e}")

    def on_created(self, event):
        """Handle file creation"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        metadata = {
            "file_path": str(file_path),
            "event_type": "created"
        }

        self.queue_input(
            content=f"New file created: {file_path}",
            metadata=metadata,
            priority=6
        )


class CommandQueueSensor(InputSensor):
    """Sensor for user commands"""

    def __init__(self):
        super().__init__("command_queue", "command")
        self.commands_dir = CONSCIOUSNESS_DIR / "commands"
        self.commands_dir.mkdir(exist_ok=True)

    def submit_command(self, command: str, args: dict = None, priority: int = 1):
        """Submit a user command"""
        metadata = {
            "command_type": "user_command",
            "arguments": args or {}
        }

        input_id = self.queue_input(
            content=command,
            metadata=metadata,
            priority=priority
        )

        return input_id

    def poll_command_dir(self):
        """Poll commands directory for new commands"""
        for cmd_file in self.commands_dir.glob("*.json"):
            try:
                with open(cmd_file, 'r') as f:
                    cmd_data = json.load(f)

                # Queue the command
                self.queue_input(
                    content=cmd_data.get("command", ""),
                    metadata=cmd_data,
                    priority=cmd_data.get("priority", 1)
                )

                # Move to processed
                cmd_file.unlink()

            except Exception as e:
                print(f"[SENSOR:command_queue] Failed to process {cmd_file}: {e}")


class APIEndpointSensor(InputSensor):
    """Sensor for API triggers (webhook-style)"""

    def __init__(self):
        super().__init__("api_endpoint", "api")

    def handle_webhook(self, source: str, payload: dict, priority: int = 5):
        """Handle incoming webhook"""
        metadata = {
            "source": source,
            "webhook_type": payload.get("type", "unknown")
        }

        content = json.dumps(payload, indent=2)

        input_id = self.queue_input(
            content=f"API webhook from {source}:\n{content}",
            metadata=metadata,
            priority=priority
        )

        return input_id


class NerveCenterInputManager:
    """Central manager for all input sensors"""

    def __init__(self):
        self.sensors = {
            "web": WebScraperSensor(),
            "files": None,  # Created dynamically
            "commands": CommandQueueSensor(),
            "api": APIEndpointSensor()
        }

    def start_file_watcher(self, watch_path: str):
        """Start file watching sensor"""
        watcher = FileWatcherSensor(watch_path)
        watcher.start_watching()
        self.sensors["files"] = watcher
        return watcher

    def get_queued_inputs(self, limit: int = 10) -> List[Dict]:
        """Get queued inputs sorted by priority"""
        inputs = []

        for input_file in QUEUE_DIR.glob("input_*.json"):
            try:
                with open(input_file, 'r') as f:
                    data = json.load(f)
                    inputs.append(data)
            except Exception as e:
                print(f"[NERVE_CENTER] Failed to read {input_file}: {e}")

        # Sort by priority (lower number = higher priority)
        inputs.sort(key=lambda x: (x["priority"], x["timestamp"]))

        return inputs[:limit]

    def process_next_input(self):
        """Process the highest priority input"""
        inputs = self.get_queued_inputs(limit=1)

        if not inputs:
            return None

        input_data = inputs[0]

        print(f"\n[NERVE_CENTER] Processing input {input_data['id']}")
        print(f"  Type: {input_data['sensor_type']}")
        print(f"  Priority: {input_data['priority']}")
        print(f"  Content: {input_data['content'][:100]}...")

        # Mark as processed
        sensor = self.sensors.get(input_data['sensor_type'])
        if sensor:
            sensor.mark_processed(input_data['id'])

        return input_data

    def get_stats(self) -> Dict:
        """Get input statistics"""
        return {
            "queued": len(list(QUEUE_DIR.glob("input_*.json"))),
            "processed": len(list(PROCESSED_DIR.glob("input_*.json"))),
            "sensors_active": len([s for s in self.sensors.values() if s is not None])
        }


def test_sensors():
    """Test input sensors"""
    print("Testing Nerve Center Input Sensors...\n")

    manager = NerveCenterInputManager()

    # Test command sensor
    print("--- Testing Command Sensor ---")
    cmd_id = manager.sensors["commands"].submit_command(
        command="Deploy to production",
        args={"env": "prod", "branch": "main"},
        priority=1
    )

    # Test web sensor
    print("\n--- Testing Web Sensor ---")
    # Example: scrape a public API
    # web_id = manager.sensors["web"].scrape_url("https://api.github.com/zen", priority=5)

    # Test API sensor
    print("\n--- Testing API Sensor ---")
    api_id = manager.sensors["api"].handle_webhook(
        source="github",
        payload={"type": "push", "repo": "consciousness-revolution"},
        priority=3
    )

    # Get stats
    print("\n--- Nerve Center Stats ---")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Process inputs
    print("\n--- Processing Inputs ---")
    for i in range(3):
        input_data = manager.process_next_input()
        if not input_data:
            break

    print("\n[OK] Sensor test complete!")


if __name__ == "__main__":
    test_sensors()
