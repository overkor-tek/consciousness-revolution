#!/usr/bin/env python3
"""
FILE SAVER - 8-Dimensional Naming Convention System

Videographers use dimensional naming to organize 1000s of files:
DATE_PROJECT_SCENE_TAKE_CAMERA_LENS_CODEC_VERSION

We apply this to consciousness work:
DATE_DOMAIN_PATTERN_COMPONENT_STATUS_AGENT_VERSION_FORMAT

Example:
20251128_COMPUTER_TRINITY_MESSAGING_COMPLETE_C1_V2.md
20251128_CONSCIOUSNESS_CYCLOTRON_INDEXING_WIP_C2_V1.py

Toyota Principles:
- KANBAN: Pull-based naming (create when needed)
- JIDOKA: Auto-detect errors in naming
- KAIZEN: Improve naming over time

Usage:
    from FILE_SAVER import save_file
    save_file(content, domain="COMPUTER", pattern="TRINITY", component="MESSAGING")
"""

import os
import json
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime

# Configuration
SAVE_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/ORGANIZED")
CYCLOTRON_DB = Path("C:/Users/dwrek/.consciousness/cyclotron_core/atoms.db")
METADATA_DB = Path("C:/Users/dwrek/100X_DEPLOYMENT/.file_metadata/metadata.db")

# 8-Dimensional Naming Convention
DIMENSIONS = {
    "DATE": "Timestamp (YYYYMMDD_HHMM)",
    "DOMAIN": "Seven Domains (COMPUTER/CITY/BODY/BOOK/BATTLESHIP/TOYOTA/CONSCIOUSNESS)",
    "PATTERN": "Pattern Theory component (MISSION/STRUCTURE/RESOURCES/etc)",
    "COMPONENT": "Specific component name",
    "STATUS": "Work status (WIP/REVIEW/COMPLETE/DEPLOYED/ARCHIVED)",
    "AGENT": "Who created (C1/C2/C3/TRINITY/HUMAN)",
    "VERSION": "Version number (V1/V2/V3...)",
    "FORMAT": "File extension (.md/.py/.js/.html/.json)"
}

VALID_DOMAINS = ["COMPUTER", "CITY", "BODY", "BOOK", "BATTLESHIP", "TOYOTA", "CONSCIOUSNESS"]
VALID_PATTERNS = ["MISSION", "STRUCTURE", "RESOURCES", "OPERATIONS", "GOVERNANCE", "DEFENSE", "COMMUNICATION", "ADAPTATION"]
VALID_STATUS = ["WIP", "REVIEW", "COMPLETE", "DEPLOYED", "ARCHIVED", "DEPRECATED"]
VALID_AGENTS = ["C1", "C2", "C3", "TRINITY", "HUMAN", "AUTO"]

class FileSaver:
    """Handles all file saving with dimensional naming"""

    def __init__(self):
        self._init_dirs()
        self._init_metadata_db()

    def _init_dirs(self):
        """Create directory structure"""
        SAVE_DIR.mkdir(exist_ok=True, parents=True)
        METADATA_DB.parent.mkdir(exist_ok=True, parents=True)

        # Create domain subdirectories
        for domain in VALID_DOMAINS:
            (SAVE_DIR / domain).mkdir(exist_ok=True)

    def _init_metadata_db(self):
        """Initialize metadata tracking database"""
        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE,
                filepath TEXT,
                domain TEXT,
                pattern TEXT,
                component TEXT,
                status TEXT,
                agent TEXT,
                version INTEGER,
                format TEXT,
                content_hash TEXT,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                size_bytes INTEGER,
                tags TEXT
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_domain ON files(domain)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_status ON files(status)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent ON files(agent)
        ''')

        conn.commit()
        conn.close()

    def generate_filename(self, domain, pattern, component, status="WIP", agent="AUTO", version=1, format_ext="md"):
        """Generate 8-dimensional filename"""

        # Validate inputs
        domain = domain.upper()
        pattern = pattern.upper() if pattern else "GENERAL"
        status = status.upper()
        agent = agent.upper()

        if domain not in VALID_DOMAINS:
            raise ValueError(f"Invalid domain: {domain}. Must be one of {VALID_DOMAINS}")

        if status not in VALID_STATUS:
            raise ValueError(f"Invalid status: {status}. Must be one of {VALID_STATUS}")

        if agent not in VALID_AGENTS:
            raise ValueError(f"Invalid agent: {agent}. Must be one of {VALID_AGENTS}")

        # Build filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        component = component.upper().replace(" ", "_")

        # Clean format extension
        if format_ext.startswith('.'):
            format_ext = format_ext[1:]

        filename = f"{timestamp}_{domain}_{pattern}_{component}_{status}_{agent}_V{version}.{format_ext}"

        return filename

    def save_file(self, content, domain, pattern, component,
                  status="WIP", agent="AUTO", version=1, format_ext="md",
                  tags=None, auto_increment_version=True):
        """
        Save file with 8-dimensional naming

        Args:
            content: File content (string or bytes)
            domain: Seven domain category
            pattern: Pattern Theory component
            component: Specific component name
            status: Work status
            agent: Who created it
            version: Version number
            format_ext: File extension
            tags: Optional list of tags
            auto_increment_version: If True, auto-increment if file exists

        Returns:
            dict with filepath, filename, and metadata
        """

        # Auto-increment version if file exists
        if auto_increment_version:
            base_filename = self.generate_filename(domain, pattern, component, status, agent, version, format_ext)
            while True:
                filepath = SAVE_DIR / domain / base_filename
                if not filepath.exists():
                    break
                version += 1
                base_filename = self.generate_filename(domain, pattern, component, status, agent, version, format_ext)
        else:
            base_filename = self.generate_filename(domain, pattern, component, status, agent, version, format_ext)
            filepath = SAVE_DIR / domain / base_filename

        # Calculate content hash
        if isinstance(content, str):
            content_bytes = content.encode('utf-8')
        else:
            content_bytes = content
        content_hash = hashlib.sha256(content_bytes).hexdigest()

        # Write file
        if isinstance(content, str):
            filepath.write_text(content, encoding='utf-8')
        else:
            filepath.write_bytes(content)

        size_bytes = filepath.stat().st_size

        # Store metadata
        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO files
            (filename, filepath, domain, pattern, component, status, agent, version, format, content_hash, size_bytes, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            base_filename,
            str(filepath),
            domain,
            pattern,
            component,
            status,
            agent,
            version,
            format_ext,
            content_hash,
            size_bytes,
            json.dumps(tags) if tags else None
        ))

        conn.commit()
        conn.close()

        # Mirror to Cyclotron (if available)
        self._mirror_to_cyclotron(filepath, domain, pattern, component)

        return {
            'filepath': str(filepath),
            'filename': base_filename,
            'domain': domain,
            'pattern': pattern,
            'component': component,
            'status': status,
            'agent': agent,
            'version': version,
            'size_bytes': size_bytes,
            'content_hash': content_hash
        }

    def _mirror_to_cyclotron(self, filepath, domain, pattern, component):
        """Mirror file to Cyclotron for indexing"""
        if not CYCLOTRON_DB.exists():
            return

        try:
            conn = sqlite3.connect(str(CYCLOTRON_DB))
            cursor = conn.cursor()

            # Read content
            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
            except:
                return

            # Create atom ID
            atom_id = hashlib.md5(str(filepath).encode()).hexdigest()[:12]

            # Check if atoms table has FTS
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='atoms_fts'")
            has_fts = cursor.fetchone() is not None

            if has_fts:
                # Insert into FTS table
                cursor.execute('''
                    INSERT OR REPLACE INTO atoms_fts (content, path, domain, pattern, component)
                    VALUES (?, ?, ?, ?, ?)
                ''', (content, str(filepath), domain, pattern, component))
            else:
                # Insert into regular atoms table if it exists
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='atoms'")
                has_atoms = cursor.fetchone() is not None

                if has_atoms:
                    cursor.execute('''
                        INSERT OR REPLACE INTO atoms (id, content, path, domain, pattern, component, created)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (atom_id, content, str(filepath), domain, pattern, component, datetime.now().isoformat()))

            conn.commit()
            conn.close()

        except Exception as e:
            # Silent fail - Cyclotron mirroring is optional
            pass

    def update_status(self, filename, new_status):
        """Update file status (e.g., WIP -> COMPLETE)"""
        if new_status.upper() not in VALID_STATUS:
            raise ValueError(f"Invalid status: {new_status}")

        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('SELECT filepath, domain, pattern, component, agent, version, format FROM files WHERE filename = ?', (filename,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            raise ValueError(f"File not found: {filename}")

        old_filepath, domain, pattern, component, agent, version, format_ext = row

        # Generate new filename with updated status
        new_filename = self.generate_filename(domain, pattern, component, new_status, agent, version, format_ext)
        new_filepath = SAVE_DIR / domain / new_filename

        # Rename file
        Path(old_filepath).rename(new_filepath)

        # Update metadata
        cursor.execute('''
            UPDATE files
            SET filename = ?, filepath = ?, status = ?, modified = CURRENT_TIMESTAMP
            WHERE filename = ?
        ''', (new_filename, str(new_filepath), new_status, filename))

        conn.commit()
        conn.close()

        return str(new_filepath)

    def search_files(self, domain=None, pattern=None, status=None, agent=None, tags=None):
        """Search files by metadata"""
        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        query = "SELECT * FROM files WHERE 1=1"
        params = []

        if domain:
            query += " AND domain = ?"
            params.append(domain.upper())
        if pattern:
            query += " AND pattern = ?"
            params.append(pattern.upper())
        if status:
            query += " AND status = ?"
            params.append(status.upper())
        if agent:
            query += " AND agent = ?"
            params.append(agent.upper())
        if tags:
            query += " AND tags LIKE ?"
            params.append(f"%{tags}%")

        query += " ORDER BY modified DESC"

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        return results

    def get_stats(self):
        """Get file organization statistics"""
        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM files')
        total_files = cursor.fetchone()[0]

        cursor.execute('SELECT domain, COUNT(*) FROM files GROUP BY domain')
        by_domain = dict(cursor.fetchall())

        cursor.execute('SELECT status, COUNT(*) FROM files GROUP BY status')
        by_status = dict(cursor.fetchall())

        cursor.execute('SELECT agent, COUNT(*) FROM files GROUP BY agent')
        by_agent = dict(cursor.fetchall())

        cursor.execute('SELECT SUM(size_bytes) FROM files')
        total_bytes = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_files': total_files,
            'total_size_mb': round(total_bytes / 1_000_000, 2),
            'by_domain': by_domain,
            'by_status': by_status,
            'by_agent': by_agent
        }


# Convenience functions for direct use
_saver = None

def get_saver():
    """Get or create global FileSaver instance"""
    global _saver
    if _saver is None:
        _saver = FileSaver()
    return _saver

def save_file(content, domain, pattern, component, **kwargs):
    """Quick save function"""
    return get_saver().save_file(content, domain, pattern, component, **kwargs)

def update_status(filename, new_status):
    """Quick update status function"""
    return get_saver().update_status(filename, new_status)

def search_files(**kwargs):
    """Quick search function"""
    return get_saver().search_files(**kwargs)

def get_stats():
    """Quick stats function"""
    return get_saver().get_stats()


if __name__ == "__main__":
    # Demo usage
    print("FILE SAVER - 8-Dimensional Naming System\n")

    # Example: Save a Trinity messaging implementation
    demo_content = """
# Trinity Messaging System

This implements cross-instance communication for C1, C2, C3.

## Components
- Message queue
- Bulletin board
- Task delegation
"""

    result = save_file(
        content=demo_content,
        domain="COMPUTER",
        pattern="COMMUNICATION",
        component="TRINITY_MESSAGING",
        status="WIP",
        agent="C1",
        tags=["trinity", "messaging", "coordination"]
    )

    print(f"Saved: {result['filename']}")
    print(f"Path: {result['filepath']}")
    print(f"Size: {result['size_bytes']} bytes")
    print(f"Hash: {result['content_hash'][:16]}...")

    # Show stats
    print("\n" + "="*50)
    stats = get_stats()
    print(f"\nTotal Files: {stats['total_files']}")
    print(f"Total Size: {stats['total_size_mb']} MB")
    print(f"\nBy Domain: {stats['by_domain']}")
    print(f"By Status: {stats['by_status']}")
    print(f"By Agent: {stats['by_agent']}")
