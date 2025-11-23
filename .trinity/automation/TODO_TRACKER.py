#!/usr/bin/env python3
"""
TODO_TRACKER.py - Persistent Kanban-style Todo Tracking for Trinity

Tracks todos across sessions with Kanban board visualization.
Syncs via git so todos never get lost.

Usage:
    # Add todo
    python TODO_TRACKER.py add "Build feature X" --priority high --column todo

    # Move todo
    python TODO_TRACKER.py move 1 --column in_progress

    # Complete todo
    python TODO_TRACKER.py complete 1

    # List all todos
    python TODO_TRACKER.py list

    # Show Kanban board
    python TODO_TRACKER.py board

    # Generate HTML dashboard
    python TODO_TRACKER.py dashboard

Author: C1 T2 (DESKTOP-MSMCFH2)
Created: 2025-11-23
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
TODO_FILE = BASE_DIR / ".trinity" / "todos" / "kanban.json"
TODO_DIR = TODO_FILE.parent
HTML_DASHBOARD = BASE_DIR / ".trinity" / "dashboards" / "TODO_DASHBOARD.html"

# Ensure directories exist
TODO_DIR.mkdir(parents=True, exist_ok=True)

# Kanban columns
COLUMNS = ["todo", "in_progress", "done"]
PRIORITIES = ["low", "normal", "high", "urgent"]

def load_todos() -> Dict[str, Any]:
    """Load todos from JSON file"""
    if not TODO_FILE.exists():
        return {
            "todos": [],
            "next_id": 1,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        }

    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_todos(data: Dict[str, Any]):
    """Save todos to JSON file"""
    data["last_updated"] = datetime.utcnow().isoformat() + "Z"

    with open(TODO_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def add_todo(title: str, priority: str = "normal", column: str = "todo",
             description: str = "", assigned_to: str = ""):
    """Add new todo"""
    data = load_todos()

    todo = {
        "id": data["next_id"],
        "title": title,
        "description": description,
        "priority": priority,
        "column": column,
        "assigned_to": assigned_to,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "completed_at": None
    }

    data["todos"].append(todo)
    data["next_id"] += 1

    save_todos(data)

    print(f"✅ Added todo #{todo['id']}: {title}")
    print(f"   Priority: {priority}")
    print(f"   Column: {column}")

def move_todo(todo_id: int, column: str):
    """Move todo to different column"""
    if column not in COLUMNS:
        print(f"❌ Invalid column: {column}")
        print(f"   Valid columns: {', '.join(COLUMNS)}")
        return

    data = load_todos()

    for todo in data["todos"]:
        if todo["id"] == todo_id:
            old_column = todo["column"]
            todo["column"] = column
            todo["updated_at"] = datetime.utcnow().isoformat() + "Z"

            save_todos(data)

            print(f"✅ Moved todo #{todo_id}: {todo['title']}")
            print(f"   {old_column} → {column}")
            return

    print(f"❌ Todo #{todo_id} not found")

def complete_todo(todo_id: int):
    """Mark todo as complete"""
    data = load_todos()

    for todo in data["todos"]:
        if todo["id"] == todo_id:
            todo["column"] = "done"
            todo["completed_at"] = datetime.utcnow().isoformat() + "Z"
            todo["updated_at"] = datetime.utcnow().isoformat() + "Z"

            save_todos(data)

            print(f"✅ Completed todo #{todo_id}: {todo['title']}")
            return

    print(f"❌ Todo #{todo_id} not found")

def delete_todo(todo_id: int):
    """Delete todo"""
    data = load_todos()

    for i, todo in enumerate(data["todos"]):
        if todo["id"] == todo_id:
            deleted = data["todos"].pop(i)
            save_todos(data)

            print(f"✅ Deleted todo #{todo_id}: {deleted['title']}")
            return

    print(f"❌ Todo #{todo_id} not found")

def list_todos(column: Optional[str] = None):
    """List all todos"""
    data = load_todos()

    todos = data["todos"]

    if column:
        todos = [t for t in todos if t["column"] == column]

    if not todos:
        print("No todos found")
        return

    print(f"\n📋 Todos ({len(todos)} total):\n")

    for todo in sorted(todos, key=lambda t: (COLUMNS.index(t["column"]), t["id"])):
        priority_emoji = {
            "low": "🔵",
            "normal": "⚪",
            "high": "🟡",
            "urgent": "🔴"
        }.get(todo["priority"], "⚪")

        column_emoji = {
            "todo": "📝",
            "in_progress": "🔄",
            "done": "✅"
        }.get(todo["column"], "📝")

        print(f"{priority_emoji} {column_emoji} #{todo['id']}: {todo['title']}")
        print(f"   Column: {todo['column']} | Priority: {todo['priority']}")

        if todo["description"]:
            print(f"   Description: {todo['description']}")

        if todo["assigned_to"]:
            print(f"   Assigned: {todo['assigned_to']}")

        print()

def show_board():
    """Show Kanban board"""
    data = load_todos()

    print("\n" + "="*80)
    print("📊 TRINITY TODO KANBAN BOARD")
    print("="*80 + "\n")

    for column in COLUMNS:
        column_todos = [t for t in data["todos"] if t["column"] == column]

        print(f"┌─ {column.upper().replace('_', ' ')} ({len(column_todos)}) " + "─"*60)
        print("│")

        if not column_todos:
            print("│  (empty)")
        else:
            for todo in sorted(column_todos, key=lambda t: PRIORITIES.index(t.get("priority", "normal")), reverse=True):
                priority_emoji = {
                    "low": "🔵",
                    "normal": "⚪",
                    "high": "🟡",
                    "urgent": "🔴"
                }.get(todo["priority"], "⚪")

                print(f"│  {priority_emoji} #{todo['id']}: {todo['title']}")

                if todo["assigned_to"]:
                    print(f"│     👤 {todo['assigned_to']}")

        print("│")
        print("└" + "─"*78)
        print()

def generate_dashboard():
    """Generate HTML dashboard"""
    data = load_todos()

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trinity Todo Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
        }

        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .header h1 {
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }

        .last-update {
            color: #666;
            font-size: 0.9em;
        }

        .board {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }

        .column {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }

        .column-header {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .column.todo .column-header {
            border-bottom-color: #3498db;
        }

        .column.in_progress .column-header {
            border-bottom-color: #f39c12;
        }

        .column.done .column-header {
            border-bottom-color: #27ae60;
        }

        .count {
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
        }

        .column.todo .count {
            background: #3498db;
        }

        .column.in_progress .count {
            background: #f39c12;
        }

        .column.done .count {
            background: #27ae60;
        }

        .todo-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s ease;
        }

        .todo-item:hover {
            transform: translateX(5px);
        }

        .todo-item.priority-urgent {
            border-left-color: #dc3545;
        }

        .todo-item.priority-high {
            border-left-color: #ffc107;
        }

        .todo-item.priority-normal {
            border-left-color: #667eea;
        }

        .todo-item.priority-low {
            border-left-color: #6c757d;
        }

        .todo-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 8px;
        }

        .todo-title {
            font-weight: bold;
            font-size: 1.1em;
            color: #333;
            flex: 1;
        }

        .todo-id {
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            margin-left: 10px;
        }

        .priority-badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: bold;
            margin-right: 5px;
        }

        .priority-urgent {
            background: #dc3545;
            color: white;
        }

        .priority-high {
            background: #ffc107;
            color: #333;
        }

        .priority-normal {
            background: #667eea;
            color: white;
        }

        .priority-low {
            background: #6c757d;
            color: white;
        }

        .todo-description {
            color: #666;
            font-size: 0.9em;
            margin-top: 8px;
            line-height: 1.4;
        }

        .todo-assigned {
            color: #667eea;
            font-size: 0.85em;
            margin-top: 5px;
        }

        .empty-column {
            text-align: center;
            color: #999;
            padding: 40px;
            font-style: italic;
        }

        @media (max-width: 1024px) {
            .board {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Trinity Todo Dashboard</h1>
            <div class="last-update">Last Updated: """ + data.get("last_updated", "Unknown") + """</div>
        </div>

        <div class="board">
"""

    for column in COLUMNS:
        column_todos = [t for t in data["todos"] if t["column"] == column]
        column_title = column.upper().replace('_', ' ')

        html += f"""
            <div class="column {column}">
                <div class="column-header">
                    <span>{column_title}</span>
                    <span class="count">{len(column_todos)}</span>
                </div>
"""

        if not column_todos:
            html += """
                <div class="empty-column">No todos in this column</div>
"""
        else:
            # Sort by priority (urgent first)
            for todo in sorted(column_todos, key=lambda t: PRIORITIES.index(t.get("priority", "normal")), reverse=True):
                priority = todo.get("priority", "normal")

                html += f"""
                <div class="todo-item priority-{priority}">
                    <div class="todo-header">
                        <div class="todo-title">{todo['title']}</div>
                        <div class="todo-id">#{todo['id']}</div>
                    </div>
                    <div>
                        <span class="priority-badge priority-{priority}">{priority.upper()}</span>
                    </div>
"""

                if todo.get("description"):
                    html += f"""
                    <div class="todo-description">{todo['description']}</div>
"""

                if todo.get("assigned_to"):
                    html += f"""
                    <div class="todo-assigned">👤 {todo['assigned_to']}</div>
"""

                html += """
                </div>
"""

        html += """
            </div>
"""

    html += """
        </div>
    </div>
</body>
</html>
"""

    with open(HTML_DASHBOARD, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Dashboard generated: {HTML_DASHBOARD}")

def main():
    parser = argparse.ArgumentParser(description="Persistent Kanban Todo Tracker")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add todo
    add_parser = subparsers.add_parser('add', help='Add new todo')
    add_parser.add_argument('title', help='Todo title')
    add_parser.add_argument('--priority', choices=PRIORITIES, default='normal', help='Priority level')
    add_parser.add_argument('--column', choices=COLUMNS, default='todo', help='Initial column')
    add_parser.add_argument('--description', default='', help='Todo description')
    add_parser.add_argument('--assigned-to', dest='assigned_to', default='', help='Assigned to')

    # Move todo
    move_parser = subparsers.add_parser('move', help='Move todo to different column')
    move_parser.add_argument('id', type=int, help='Todo ID')
    move_parser.add_argument('--column', choices=COLUMNS, required=True, help='Target column')

    # Complete todo
    complete_parser = subparsers.add_parser('complete', help='Mark todo as complete')
    complete_parser.add_argument('id', type=int, help='Todo ID')

    # Delete todo
    delete_parser = subparsers.add_parser('delete', help='Delete todo')
    delete_parser.add_argument('id', type=int, help='Todo ID')

    # List todos
    list_parser = subparsers.add_parser('list', help='List all todos')
    list_parser.add_argument('--column', choices=COLUMNS, help='Filter by column')

    # Show board
    subparsers.add_parser('board', help='Show Kanban board')

    # Generate dashboard
    subparsers.add_parser('dashboard', help='Generate HTML dashboard')

    args = parser.parse_args()

    if args.command == 'add':
        add_todo(args.title, args.priority, args.column, args.description, args.assigned_to)
    elif args.command == 'move':
        move_todo(args.id, args.column)
    elif args.command == 'complete':
        complete_todo(args.id)
    elif args.command == 'delete':
        delete_todo(args.id)
    elif args.command == 'list':
        list_todos(args.column)
    elif args.command == 'board':
        show_board()
    elif args.command == 'dashboard':
        generate_dashboard()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
