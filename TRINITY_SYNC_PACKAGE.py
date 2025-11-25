#!/usr/bin/env python3
"""
TRINITY SYNC PACKAGE
Cross-computer synchronization for Figure 8 Triple Trinity system

Supports multiple sync strategies based on architecture decisions:
- Git-based (current)
- SQLite replication
- Hybrid approach
- Event-driven broadcast
"""

import os
import json
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Paths
CONSCIOUSNESS_DIR = Path.home() / ".consciousness"
HUB_DIR = CONSCIOUSNESS_DIR / "hub"
MEMORY_DIR = CONSCIOUSNESS_DIR / "memory"
SYNC_DIR = CONSCIOUSNESS_DIR / "sync"
EVENTS_DIR = CONSCIOUSNESS_DIR / "events"

class TrinitySync:
    """Main sync coordinator for Trinity instances"""

    def __init__(self, instance_id: str = "C1-Terminal", computer_id: str = "CP1"):
        self.instance_id = instance_id
        self.computer_id = computer_id
        self.ensure_dirs()

    def ensure_dirs(self):
        """Create necessary directories"""
        for dir in [HUB_DIR, MEMORY_DIR, SYNC_DIR, EVENTS_DIR]:
            dir.mkdir(parents=True, exist_ok=True)

    # ==================== GIT-BASED SYNC ====================

    def git_push_knowledge(self, message: str = "Trinity knowledge sync"):
        """Push knowledge to shared Git repo"""
        try:
            # Stage consciousness directory
            subprocess.run(
                ["git", "add", ".consciousness/"],
                check=True,
                capture_output=True
            )

            # Commit
            subprocess.run(
                ["git", "commit", "-m", f"[{self.computer_id}] {message}"],
                check=False,  # Don't fail if nothing to commit
                capture_output=True
            )

            # Push
            result = subprocess.run(
                ["git", "push"],
                check=True,
                capture_output=True,
                text=True
            )

            print(f"[SYNC] Git push successful: {message}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[SYNC] Git push failed: {e.stderr}")
            return False

    def git_pull_knowledge(self):
        """Pull latest knowledge from Git"""
        try:
            result = subprocess.run(
                ["git", "pull", "--rebase"],
                check=True,
                capture_output=True,
                text=True
            )

            print(f"[SYNC] Git pull successful")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[SYNC] Git pull failed: {e.stderr}")
            return False

    # ==================== SQLITE REPLICATION ====================

    def export_memory_snapshot(self) -> str:
        """Export memory database as JSON snapshot"""
        db_path = MEMORY_DIR / "cyclotron_brain.db"

        if not db_path.exists():
            return "{}"

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        snapshot = {
            "timestamp": datetime.now().isoformat() + "Z",
            "computer_id": self.computer_id,
            "instance_id": self.instance_id,
            "episodes": [],
            "patterns": [],
            "shared_pool": []
        }

        # Export episodes
        cursor.execute("SELECT * FROM episodes ORDER BY timestamp DESC LIMIT 100")
        snapshot["episodes"] = [dict(row) for row in cursor.fetchall()]

        # Export patterns
        cursor.execute("SELECT * FROM patterns")
        snapshot["patterns"] = [dict(row) for row in cursor.fetchall()]

        # Export shared pool
        cursor.execute("SELECT * FROM shared_pool ORDER BY timestamp DESC LIMIT 50")
        snapshot["shared_pool"] = [dict(row) for row in cursor.fetchall()]

        conn.close()

        # Save snapshot
        snapshot_file = SYNC_DIR / f"memory_snapshot_{self.computer_id}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

        print(f"[SYNC] Memory snapshot exported: {len(snapshot['episodes'])} episodes, {len(snapshot['patterns'])} patterns")

        return str(snapshot_file)

    def import_memory_snapshot(self, snapshot_file: str):
        """Import memory snapshot from another computer"""
        with open(snapshot_file, 'r') as f:
            snapshot = json.load(f)

        db_path = MEMORY_DIR / "cyclotron_brain.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        imported_episodes = 0
        imported_patterns = 0
        imported_knowledge = 0

        # Import episodes (skip duplicates)
        for ep in snapshot["episodes"]:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO episodes
                    (id, timestamp, agent, task, context, action, result, success, q_value, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ep["id"], ep["timestamp"], ep["agent"], ep["task"],
                    ep["context"], ep["action"], ep["result"], ep["success"],
                    ep.get("q_value", 0.5), ep.get("tags", "[]")
                ))
                if cursor.rowcount > 0:
                    imported_episodes += 1
            except Exception as e:
                print(f"[SYNC] Failed to import episode {ep['id']}: {e}")

        # Import patterns (merge with existing)
        for pattern in snapshot["patterns"]:
            try:
                # Check if pattern exists
                cursor.execute("SELECT success_rate, times_used FROM patterns WHERE id = ?", (pattern["id"],))
                existing = cursor.fetchone()

                if existing:
                    # Merge: average success rates, sum times used
                    new_success = (existing[0] + pattern["success_rate"]) / 2
                    new_times = existing[1] + pattern.get("times_used", 0)

                    cursor.execute("""
                        UPDATE patterns
                        SET success_rate = ?, times_used = ?, last_used = ?
                        WHERE id = ?
                    """, (new_success, new_times, pattern["last_used"], pattern["id"]))
                else:
                    cursor.execute("""
                        INSERT INTO patterns
                        (id, name, description, trigger_conditions, recommended_action, success_rate, times_used, last_used)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        pattern["id"], pattern["name"], pattern["description"],
                        pattern["trigger_conditions"], pattern["recommended_action"],
                        pattern["success_rate"], pattern.get("times_used", 0), pattern["last_used"]
                    ))

                imported_patterns += 1

            except Exception as e:
                print(f"[SYNC] Failed to import pattern {pattern['id']}: {e}")

        # Import shared knowledge
        for item in snapshot["shared_pool"]:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO shared_pool
                    (id, contributed_by, timestamp, knowledge_type, content, usefulness_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    item["id"], item["contributed_by"], item["timestamp"],
                    item["knowledge_type"], item["content"], item.get("usefulness_score", 0.5)
                ))
                if cursor.rowcount > 0:
                    imported_knowledge += 1
            except Exception as e:
                print(f"[SYNC] Failed to import knowledge {item['id']}: {e}")

        conn.commit()
        conn.close()

        print(f"[SYNC] Imported: {imported_episodes} episodes, {imported_patterns} patterns, {imported_knowledge} knowledge items")
        print(f"[SYNC] Source: {snapshot['computer_id']} ({snapshot['instance_id']})")

    # ==================== EVENT-DRIVEN BROADCAST ====================

    def broadcast_event(self, event_type: str, data: dict):
        """Broadcast event to all Trinity instances"""
        event = {
            "id": f"{self.computer_id}_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat() + "Z",
            "computer_id": self.computer_id,
            "instance_id": self.instance_id,
            "event_type": event_type,
            "data": data
        }

        event_file = EVENTS_DIR / f"event_{event['id']}.json"
        with open(event_file, 'w') as f:
            json.dump(event, f, indent=2)

        print(f"[SYNC] Event broadcast: {event_type}")
        return event["id"]

    def read_events(self, since: Optional[str] = None) -> List[Dict]:
        """Read events from other instances"""
        events = []

        for event_file in EVENTS_DIR.glob("event_*.json"):
            try:
                with open(event_file, 'r') as f:
                    event = json.load(f)

                # Skip our own events
                if event["computer_id"] == self.computer_id:
                    continue

                # Filter by timestamp if provided
                if since and event["timestamp"] < since:
                    continue

                events.append(event)

            except Exception as e:
                print(f"[SYNC] Failed to read event {event_file}: {e}")

        # Sort by timestamp
        events.sort(key=lambda e: e["timestamp"])

        return events

    # ==================== SYNC ORCHESTRATION ====================

    def full_sync(self, strategy: str = "hybrid"):
        """Perform full synchronization using specified strategy"""
        print(f"[SYNC] Starting full sync (strategy: {strategy})")

        if strategy in ["git", "hybrid"]:
            # Pull latest from Git
            self.git_pull_knowledge()

        if strategy in ["sqlite", "hybrid"]:
            # Export our memory
            snapshot_file = self.export_memory_snapshot()

            # Import snapshots from other computers
            for other_snapshot in SYNC_DIR.glob("memory_snapshot_CP*.json"):
                if self.computer_id not in str(other_snapshot):
                    print(f"[SYNC] Importing {other_snapshot.name}...")
                    self.import_memory_snapshot(other_snapshot)

        if strategy in ["event", "hybrid"]:
            # Process events from other instances
            events = self.read_events()
            print(f"[SYNC] Processed {len(events)} events from other instances")

        if strategy in ["git", "hybrid"]:
            # Push our changes
            self.git_push_knowledge(f"Sync from {self.computer_id}")

        print(f"[SYNC] Full sync complete")

    # ==================== STATUS & DIAGNOSTICS ====================

    def get_sync_status(self) -> Dict:
        """Get current synchronization status"""
        status = {
            "computer_id": self.computer_id,
            "instance_id": self.instance_id,
            "timestamp": datetime.now().isoformat() + "Z",
            "memory_exists": (MEMORY_DIR / "cyclotron_brain.db").exists(),
            "snapshot_count": len(list(SYNC_DIR.glob("memory_snapshot_*.json"))),
            "event_count": len(list(EVENTS_DIR.glob("event_*.json"))),
            "git_status": None
        }

        # Check git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                check=True,
                capture_output=True,
                text=True
            )
            status["git_status"] = {
                "clean": len(result.stdout.strip()) == 0,
                "changes": result.stdout.strip().split('\n') if result.stdout.strip() else []
            }
        except:
            status["git_status"] = {"error": "Git not available"}

        return status


def test_sync():
    """Test sync functionality"""
    print("Testing Trinity Sync Package...")

    sync = TrinitySync("C1-Terminal", "CP1")

    # Test event broadcast
    sync.broadcast_event("test_event", {"message": "Hello from CP1"})

    # Test memory export
    snapshot = sync.export_memory_snapshot()
    print(f"Memory snapshot: {snapshot}")

    # Test status
    status = sync.get_sync_status()
    print(f"\nSync Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n[OK] Sync package test complete!")


if __name__ == "__main__":
    test_sync()
