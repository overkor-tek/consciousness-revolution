#!/usr/bin/env python3
"""
BETA BRAIN - Simple Personal Knowledge System
=============================================
For: Consciousness Revolution Beta Testers

This is YOUR brain. It learns what you learn.
It remembers what you tell it.
It helps you find patterns.

Commands:
    python brain.py learn "something I learned today"
    python brain.py search "topic"
    python brain.py patterns
    python brain.py stats
    python brain.py export
"""

import sqlite3
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# Your personal brain file
BRAIN_FILE = Path(__file__).parent / "my_brain.db"

def init_brain():
    """Initialize your personal brain"""
    conn = sqlite3.connect(BRAIN_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            source TEXT,
            created TEXT,
            accessed INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern TEXT NOT NULL UNIQUE,
            frequency INTEGER DEFAULT 1,
            first_seen TEXT,
            last_seen TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            insight TEXT NOT NULL,
            domain TEXT,
            created TEXT
        )
    """)

    conn.commit()
    conn.close()

def learn(content, category="general", source=None):
    """Add something to your brain"""
    conn = sqlite3.connect(BRAIN_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO knowledge (content, category, source, created)
        VALUES (?, ?, ?, ?)
    """, (content, category, source, datetime.now().isoformat()))

    # Extract keywords for pattern tracking
    words = content.lower().split()
    for word in words:
        if len(word) > 4:  # Skip small words
            cursor.execute("""
                INSERT INTO patterns (pattern, first_seen, last_seen)
                VALUES (?, ?, ?)
                ON CONFLICT(pattern) DO UPDATE SET
                    frequency = frequency + 1,
                    last_seen = ?
            """, (word, datetime.now().isoformat(), datetime.now().isoformat(), datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print(f"✓ Learned: {content[:50]}...")

def search(query):
    """Search your brain"""
    conn = sqlite3.connect(BRAIN_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT content, category, created
        FROM knowledge
        WHERE content LIKE ?
        ORDER BY created DESC
        LIMIT 20
    """, (f"%{query}%",))

    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No knowledge found for '{query}'")
        return

    print(f"\n=== Your Brain: '{query}' ===\n")
    for content, category, created in results:
        date = created.split('T')[0] if 'T' in created else created
        print(f"[{category}] {date}: {content[:80]}...")

def show_patterns():
    """Show patterns in your thinking"""
    conn = sqlite3.connect(BRAIN_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pattern, frequency, last_seen
        FROM patterns
        ORDER BY frequency DESC
        LIMIT 20
    """)

    results = cursor.fetchall()
    conn.close()

    print("\n=== Your Thinking Patterns ===\n")
    print("These words appear most in what you learn:\n")
    for pattern, freq, last in results:
        print(f"  {pattern}: {freq}x")

def show_stats():
    """Show brain statistics"""
    conn = sqlite3.connect(BRAIN_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM knowledge")
    knowledge_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM patterns")
    pattern_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM insights")
    insight_count = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) FROM knowledge GROUP BY category")
    categories = cursor.fetchall()

    conn.close()

    print("\n=== Your Brain Stats ===\n")
    print(f"Knowledge items: {knowledge_count}")
    print(f"Patterns tracked: {pattern_count}")
    print(f"Insights saved: {insight_count}")
    print("\nBy category:")
    for cat, count in categories:
        print(f"  {cat}: {count}")

def add_insight(insight, domain="consciousness"):
    """Add an insight"""
    conn = sqlite3.connect(BRAIN_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO insights (insight, domain, created)
        VALUES (?, ?, ?)
    """, (insight, domain, datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print(f"✓ Insight saved: {insight[:50]}...")

def export_brain():
    """Export your brain to JSON"""
    conn = sqlite3.connect(BRAIN_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM knowledge")
    knowledge = cursor.fetchall()

    cursor.execute("SELECT * FROM patterns ORDER BY frequency DESC LIMIT 50")
    patterns = cursor.fetchall()

    cursor.execute("SELECT * FROM insights")
    insights = cursor.fetchall()

    conn.close()

    export = {
        "exported": datetime.now().isoformat(),
        "knowledge_count": len(knowledge),
        "top_patterns": [{"word": p[1], "frequency": p[2]} for p in patterns],
        "insights": [{"insight": i[1], "domain": i[2]} for i in insights]
    }

    export_file = BRAIN_FILE.parent / "brain_export.json"
    with open(export_file, 'w') as f:
        json.dump(export, f, indent=2)

    print(f"✓ Brain exported to {export_file}")

def main():
    init_brain()

    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "learn":
        if len(sys.argv) < 3:
            print("Usage: python brain.py learn \"what you learned\"")
            return
        content = " ".join(sys.argv[2:])
        learn(content)

    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: python brain.py search \"topic\"")
            return
        search(sys.argv[2])

    elif cmd == "patterns":
        show_patterns()

    elif cmd == "stats":
        show_stats()

    elif cmd == "insight":
        if len(sys.argv) < 3:
            print("Usage: python brain.py insight \"your insight\"")
            return
        add_insight(" ".join(sys.argv[2:]))

    elif cmd == "export":
        export_brain()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
