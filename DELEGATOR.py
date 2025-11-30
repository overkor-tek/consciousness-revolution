#!/usr/bin/env python3
"""
DELEGATOR - Task Offloading to Trinity Instances (C1/C2/C3)

Allows automatic delegation of work to other Trinity agents:
- C1 Mechanic: Implementation tasks
- C2 Architect: Design/architecture tasks
- C3 Oracle: Vision/consciousness tasks

Uses Trinity Message Board for async coordination.

Toyota Principles:
- KANBAN: Pull-based task assignment
- HEIJUNKA: Level loading across agents
- ANDON: Alert when tasks are blocked

Usage:
    from DELEGATOR import delegate_task
    delegate_task("Build file indexer", assigned_to="C1", priority="high")
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime

# Configuration
TRINITY_MSG_DIR = Path("C:/Users/dwrek/.claude/trinity_messages")
TASKS_DB = Path("C:/Users/dwrek/100X_DEPLOYMENT/.delegation/tasks.db")
BULLETIN_BOARD = TRINITY_MSG_DIR / "BULLETIN_BOARD.md"
C1_OUTBOX = TRINITY_MSG_DIR / "C1_OUTBOX.md"
C2_OUTBOX = TRINITY_MSG_DIR / "C2_OUTBOX.md"
C3_OUTBOX = TRINITY_MSG_DIR / "C3_OUTBOX.md"
COMPLETED_TASKS = TRINITY_MSG_DIR / "COMPLETED_TASKS.md"

# Task priorities
PRIORITIES = ["urgent", "high", "normal", "low"]

# Valid agents
AGENTS = ["C1", "C2", "C3", "TRINITY", "ANY"]

class Delegator:
    """Handles task delegation to Trinity instances"""

    def __init__(self):
        self._init_dirs()
        self._init_tasks_db()

    def _init_dirs(self):
        """Create directory structure"""
        TRINITY_MSG_DIR.mkdir(exist_ok=True, parents=True)
        TASKS_DB.parent.mkdir(exist_ok=True, parents=True)

    def _init_tasks_db(self):
        """Initialize task tracking database"""
        conn = sqlite3.connect(str(TASKS_DB))
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_description TEXT NOT NULL,
                assigned_to TEXT NOT NULL,
                priority TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'pending',
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                claimed_by TEXT,
                claimed_at TIMESTAMP,
                completed_at TIMESTAMP,
                output TEXT,
                tags TEXT
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_assigned ON tasks(assigned_to)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority)
        ''')

        conn.commit()
        conn.close()

    def delegate_task(self, task_description, assigned_to="ANY", priority="normal", tags=None):
        """
        Delegate task to Trinity agent

        Args:
            task_description: What needs to be done
            assigned_to: C1/C2/C3/TRINITY/ANY
            priority: urgent/high/normal/low
            tags: Optional list of tags

        Returns:
            Task ID
        """

        assigned_to = assigned_to.upper()
        priority = priority.lower()

        if assigned_to not in AGENTS:
            raise ValueError(f"Invalid agent: {assigned_to}. Must be one of {AGENTS}")

        if priority not in PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {PRIORITIES}")

        # Insert into database
        conn = sqlite3.connect(str(TASKS_DB))
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tasks (task_description, assigned_to, priority, tags)
            VALUES (?, ?, ?, ?)
        ''', (task_description, assigned_to, priority, json.dumps(tags) if tags else None))

        task_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Post to bulletin board
        self._post_to_bulletin_board(task_id, task_description, assigned_to, priority)

        return task_id

    def _post_to_bulletin_board(self, task_id, task_description, assigned_to, priority):
        """Post task to Trinity bulletin board"""

        # Create bulletin board if it doesn't exist
        if not BULLETIN_BOARD.exists():
            BULLETIN_BOARD.write_text("# TRINITY BULLETIN BOARD\n\n## Active Tasks\n\n")

        # Read current board
        current_content = BULLETIN_BOARD.read_text()

        # Add new task
        priority_emoji = {
            "urgent": "🔴",
            "high": "🟠",
            "normal": "🟢",
            "low": "🔵"
        }

        task_entry = f"- [{priority_emoji.get(priority, '🟢')} TASK-{task_id}] **{assigned_to}**: {task_description} *(Priority: {priority})* - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

        # Insert after "## Active Tasks"
        if "## Active Tasks" in current_content:
            parts = current_content.split("## Active Tasks\n\n", 1)
            new_content = parts[0] + "## Active Tasks\n\n" + task_entry + parts[1]
        else:
            new_content = current_content + "\n## Active Tasks\n\n" + task_entry

        BULLETIN_BOARD.write_text(new_content)

    def claim_task(self, task_id, claimed_by):
        """Claim a task (when agent picks it up)"""

        claimed_by = claimed_by.upper()

        conn = sqlite3.connect(str(TASKS_DB))
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE tasks
            SET status = 'in_progress', claimed_by = ?, claimed_at = CURRENT_TIMESTAMP
            WHERE id = ? AND status = 'pending'
        ''', (claimed_by, task_id))

        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()

        if rows_affected > 0:
            self._update_bulletin_board_status(task_id, "IN PROGRESS", claimed_by)
            return True
        return False

    def complete_task(self, task_id, output, completed_by):
        """Mark task as complete with output"""

        completed_by = completed_by.upper()

        conn = sqlite3.connect(str(TASKS_DB))
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE tasks
            SET status = 'completed', output = ?, completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (output, task_id))

        cursor.execute('''
            SELECT task_description, assigned_to, priority FROM tasks WHERE id = ?
        ''', (task_id,))

        result = cursor.fetchone()
        conn.commit()
        conn.close()

        if result:
            task_description, assigned_to, priority = result
            self._post_to_completed_tasks(task_id, task_description, completed_by, output)
            self._remove_from_bulletin_board(task_id)
            return True

        return False

    def _update_bulletin_board_status(self, task_id, status, agent):
        """Update task status on bulletin board"""

        if not BULLETIN_BOARD.exists():
            return

        content = BULLETIN_BOARD.read_text()
        content = content.replace(
            f"TASK-{task_id}]",
            f"TASK-{task_id} - {status} by {agent}]"
        )
        BULLETIN_BOARD.write_text(content)

    def _remove_from_bulletin_board(self, task_id):
        """Remove completed task from bulletin board"""

        if not BULLETIN_BOARD.exists():
            return

        content = BULLETIN_BOARD.read_text()
        lines = content.split('\n')
        filtered_lines = [line for line in lines if f"TASK-{task_id}]" not in line]
        BULLETIN_BOARD.write_text('\n'.join(filtered_lines))

    def _post_to_completed_tasks(self, task_id, task_description, completed_by, output):
        """Post completed task to COMPLETED_TASKS.md"""

        if not COMPLETED_TASKS.exists():
            COMPLETED_TASKS.write_text("# TRINITY COMPLETED TASKS\n\n")

        current_content = COMPLETED_TASKS.read_text()

        entry = f"""
## TASK-{task_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Task:** {task_description}
**Completed By:** {completed_by}
**Output:**
{output}

---

"""

        # Prepend to file (latest first)
        new_content = "# TRINITY COMPLETED TASKS\n\n" + entry + current_content.replace("# TRINITY COMPLETED TASKS\n\n", "")

        COMPLETED_TASKS.write_text(new_content)

    def get_pending_tasks(self, assigned_to=None):
        """Get pending tasks (optionally filtered by agent)"""

        conn = sqlite3.connect(str(TASKS_DB))
        cursor = conn.cursor()

        if assigned_to:
            assigned_to = assigned_to.upper()
            cursor.execute('''
                SELECT * FROM tasks
                WHERE status = 'pending' AND (assigned_to = ? OR assigned_to = 'ANY')
                ORDER BY
                    CASE priority
                        WHEN 'urgent' THEN 1
                        WHEN 'high' THEN 2
                        WHEN 'normal' THEN 3
                        WHEN 'low' THEN 4
                    END,
                    created ASC
            ''', (assigned_to,))
        else:
            cursor.execute('''
                SELECT * FROM tasks
                WHERE status = 'pending'
                ORDER BY
                    CASE priority
                        WHEN 'urgent' THEN 1
                        WHEN 'high' THEN 2
                        WHEN 'normal' THEN 3
                        WHEN 'low' THEN 4
                    END,
                    created ASC
            ''')

        results = cursor.fetchall()
        conn.close()

        return results

    def get_in_progress_tasks(self, claimed_by=None):
        """Get in-progress tasks (optionally filtered by who claimed)"""

        conn = sqlite3.connect(str(TASKS_DB))
        cursor = conn.cursor()

        if claimed_by:
            claimed_by = claimed_by.upper()
            cursor.execute('''
                SELECT * FROM tasks
                WHERE status = 'in_progress' AND claimed_by = ?
                ORDER BY created DESC
            ''', (claimed_by,))
        else:
            cursor.execute('''
                SELECT * FROM tasks
                WHERE status = 'in_progress'
                ORDER BY created DESC
            ''')

        results = cursor.fetchall()
        conn.close()

        return results

    def get_stats(self):
        """Get delegation statistics"""

        conn = sqlite3.connect(str(TASKS_DB))
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM tasks')
        total_tasks = cursor.fetchone()[0]

        cursor.execute('SELECT status, COUNT(*) FROM tasks GROUP BY status')
        by_status = dict(cursor.fetchall())

        cursor.execute('SELECT assigned_to, COUNT(*) FROM tasks GROUP BY assigned_to')
        by_assigned = dict(cursor.fetchall())

        cursor.execute('SELECT claimed_by, COUNT(*) FROM tasks WHERE claimed_by IS NOT NULL GROUP BY claimed_by')
        by_claimed = dict(cursor.fetchall())

        cursor.execute('SELECT priority, COUNT(*) FROM tasks WHERE status = "pending" GROUP BY priority')
        pending_by_priority = dict(cursor.fetchall())

        conn.close()

        return {
            'total_tasks': total_tasks,
            'by_status': by_status,
            'by_assigned': by_assigned,
            'by_claimed': by_claimed,
            'pending_by_priority': pending_by_priority
        }


# Convenience functions
_delegator = None

def get_delegator():
    """Get or create global Delegator instance"""
    global _delegator
    if _delegator is None:
        _delegator = Delegator()
    return _delegator

def delegate_task(task_description, assigned_to="ANY", priority="normal", tags=None):
    """Quick delegate function"""
    return get_delegator().delegate_task(task_description, assigned_to, priority, tags)

def claim_task(task_id, claimed_by):
    """Quick claim function"""
    return get_delegator().claim_task(task_id, claimed_by)

def complete_task(task_id, output, completed_by):
    """Quick complete function"""
    return get_delegator().complete_task(task_id, output, completed_by)

def get_pending_tasks(assigned_to=None):
    """Quick get pending function"""
    return get_delegator().get_pending_tasks(assigned_to)

def get_stats():
    """Quick stats function"""
    return get_delegator().get_stats()


if __name__ == "__main__":
    import sys

    delegator = Delegator()

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd == 'list':
            # List pending tasks
            print("\n=== PENDING TASKS ===\n")
            tasks = delegator.get_pending_tasks()
            if tasks:
                for task in tasks:
                    task_id, desc, assigned_to, priority, status, created, claimed_by, claimed_at, completed_at, output, tags = task
                    print(f"[TASK-{task_id}] {assigned_to} | {priority.upper()}")
                    print(f"  {desc}")
                    print(f"  Created: {created}\n")
            else:
                print("No pending tasks.\n")

        elif cmd == 'stats':
            # Show stats
            stats = delegator.get_stats()
            print("\n=== DELEGATION STATS ===\n")
            print(f"Total Tasks: {stats['total_tasks']}")
            print(f"By Status: {stats['by_status']}")
            print(f"By Assigned: {stats['by_assigned']}")
            print(f"By Claimed: {stats['by_claimed']}")
            print(f"Pending by Priority: {stats['pending_by_priority']}\n")

        elif cmd == 'delegate':
            # Quick delegate from command line
            if len(sys.argv) < 3:
                print("Usage: python DELEGATOR.py delegate <description> [assigned_to] [priority]")
                sys.exit(1)

            description = sys.argv[2]
            assigned_to = sys.argv[3] if len(sys.argv) > 3 else "ANY"
            priority = sys.argv[4] if len(sys.argv) > 4 else "normal"

            task_id = delegator.delegate_task(description, assigned_to, priority)
            print(f"\nTask delegated: TASK-{task_id}")
            print(f"Assigned to: {assigned_to}")
            print(f"Priority: {priority}\n")

        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python DELEGATOR.py [list|stats|delegate]")

    else:
        # Demo usage
        print("\nDELEGATOR - Trinity Task Delegation System\n")

        # Example: Delegate tasks to different agents
        task1 = delegator.delegate_task(
            "Build file indexer with SQLite FTS5",
            assigned_to="C1",
            priority="high",
            tags=["implementation", "database"]
        )

        task2 = delegator.delegate_task(
            "Design scalable architecture for multi-device sync",
            assigned_to="C2",
            priority="normal",
            tags=["architecture", "design"]
        )

        task3 = delegator.delegate_task(
            "Analyze consciousness implications of autonomous file management",
            assigned_to="C3",
            priority="low",
            tags=["consciousness", "vision"]
        )

        print(f"Created TASK-{task1}: C1 Implementation")
        print(f"Created TASK-{task2}: C2 Architecture")
        print(f"Created TASK-{task3}: C3 Vision")

        # Show stats
        stats = delegator.get_stats()
        print(f"\nTotal Tasks: {stats['total_tasks']}")
        print(f"Pending: {stats['by_status'].get('pending', 0)}")
        print(f"\nCheck BULLETIN_BOARD.md for task assignments!")
