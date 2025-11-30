#!/usr/bin/env python3
"""
FILE CLEANER - Self-Organizing File System

Auto-reorganizes files based on:
- LFSME principles (Lighter, Faster, Stronger, More Elegant, Less Expensive)
- Age and status
- Redundancy detection
- Pattern Theory alignment
- Cyclotron indexing

Toyota Principles:
- 5S: Sort, Set in order, Shine, Standardize, Sustain
- MUDA: Eliminate waste (duplicate files, outdated versions)
- KAIZEN: Continuous improvement

Usage:
    python FILE_CLEANER.py                    # Full clean
    python FILE_CLEANER.py --dry-run          # Preview changes
    python FILE_CLEANER.py --archive-old=30   # Archive files older than 30 days
    python FILE_CLEANER.py --remove-dupes     # Remove duplicate files
"""

import os
import sys
import shutil
import hashlib
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Import our file saver
try:
    from FILE_SAVER import FileSaver, update_status, search_files
except ImportError:
    print("ERROR: FILE_SAVER.py not found. Run from 100X_DEPLOYMENT directory.")
    sys.exit(1)

# Configuration
ORGANIZED_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/ORGANIZED")
ARCHIVE_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/ORGANIZED/ARCHIVE")
TRASH_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/ORGANIZED/TRASH")
METADATA_DB = Path("C:/Users/dwrek/100X_DEPLOYMENT/.file_metadata/metadata.db")

# LFSME criteria
LFSME_RULES = {
    "LIGHTER": {
        "max_file_size_mb": 10,  # Files > 10MB should be compressed or archived
        "max_total_wip": 50,      # Max 50 WIP files at once
    },
    "FASTER": {
        "max_depth": 3,           # Max 3 subdirectory levels
        "archive_old_days": 30,   # Archive files older than 30 days
    },
    "STRONGER": {
        "require_backup": True,   # All COMPLETE files should be backed up
        "redundancy": 1,          # Keep only 1 copy of identical files
    },
    "MORE_ELEGANT": {
        "naming_convention": True,  # Enforce 8-dimensional naming
        "max_wip_per_domain": 10,   # Max 10 WIP per domain
    },
    "LESS_EXPENSIVE": {
        "remove_duplicates": True,   # Remove duplicate content
        "compress_archives": True,   # Compress archived files
    }
}

class FileCleaner:
    """Handles automatic file organization and cleaning"""

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.saver = FileSaver()
        self._init_dirs()
        self.actions = []

    def _init_dirs(self):
        """Create directory structure"""
        ARCHIVE_DIR.mkdir(exist_ok=True, parents=True)
        TRASH_DIR.mkdir(exist_ok=True, parents=True)

    def log_action(self, action_type, filepath, reason):
        """Log cleaning action"""
        self.actions.append({
            'type': action_type,
            'filepath': str(filepath),
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        })

        if self.dry_run:
            print(f"[DRY RUN] {action_type}: {filepath} - {reason}")
        else:
            print(f"{action_type}: {filepath} - {reason}")

    def find_duplicate_files(self):
        """Find files with identical content (by hash)"""
        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('''
            SELECT content_hash, COUNT(*) as cnt, GROUP_CONCAT(filename) as files
            FROM files
            WHERE status != 'ARCHIVED' AND status != 'DEPRECATED'
            GROUP BY content_hash
            HAVING cnt > 1
        ''')

        duplicates = []
        for content_hash, count, files in cursor.fetchall():
            file_list = files.split(',')
            # Keep the newest, mark others as duplicates
            duplicates.append({
                'hash': content_hash,
                'count': count,
                'files': file_list
            })

        conn.close()
        return duplicates

    def remove_duplicates(self):
        """Remove duplicate files, keeping the latest version"""
        duplicates = self.find_duplicate_files()

        removed_count = 0
        for dup_group in duplicates:
            files = dup_group['files']

            # Sort by version and modified date
            conn = sqlite3.connect(str(METADATA_DB))
            cursor = conn.cursor()

            file_info = []
            for filename in files:
                cursor.execute('''
                    SELECT filename, filepath, version, modified FROM files
                    WHERE filename = ?
                ''', (filename,))
                result = cursor.fetchone()
                if result:
                    file_info.append(result)

            conn.close()

            # Sort: highest version first, then most recent
            file_info.sort(key=lambda x: (x[2], x[3]), reverse=True)

            # Keep first, remove rest
            for filename, filepath, version, modified in file_info[1:]:
                self._move_to_trash(filepath, f"Duplicate of {file_info[0][0]}")
                removed_count += 1

        return removed_count

    def archive_old_files(self, days_threshold=30):
        """Archive files older than threshold"""
        cutoff_date = datetime.now() - timedelta(days=days_threshold)

        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('''
            SELECT filename, filepath FROM files
            WHERE status = 'COMPLETE' AND modified < ?
        ''', (cutoff_date.isoformat(),))

        old_files = cursor.fetchall()
        conn.close()

        archived_count = 0
        for filename, filepath in old_files:
            self._move_to_archive(filepath, f"Older than {days_threshold} days")
            archived_count += 1

        return archived_count

    def clean_wip_overflow(self):
        """Clean up excess WIP files per domain"""
        max_wip_per_domain = LFSME_RULES['MORE_ELEGANT']['max_wip_per_domain']

        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        # Get WIP count per domain
        cursor.execute('''
            SELECT domain, COUNT(*) as cnt FROM files
            WHERE status = 'WIP'
            GROUP BY domain
            HAVING cnt > ?
        ''', (max_wip_per_domain,))

        overflow_domains = cursor.fetchall()

        cleaned_count = 0
        for domain, count in overflow_domains:
            excess = count - max_wip_per_domain

            # Get oldest WIP files in this domain
            cursor.execute('''
                SELECT filename, filepath FROM files
                WHERE domain = ? AND status = 'WIP'
                ORDER BY modified ASC
                LIMIT ?
            ''', (domain, excess))

            old_wip = cursor.fetchall()

            for filename, filepath in old_wip:
                # Archive or deprecate
                try:
                    update_status(filename, "ARCHIVED")
                    self.log_action("ARCHIVED", filepath, f"WIP overflow in {domain} domain")
                    cleaned_count += 1
                except:
                    pass

        conn.close()
        return cleaned_count

    def _move_to_archive(self, filepath, reason):
        """Move file to archive directory"""
        filepath = Path(filepath)
        if not filepath.exists():
            return

        # Determine archive location
        archive_path = ARCHIVE_DIR / filepath.name

        # Handle filename collision
        if archive_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_path = ARCHIVE_DIR / f"{filepath.stem}_{timestamp}{filepath.suffix}"

        if not self.dry_run:
            shutil.move(str(filepath), str(archive_path))

            # Update metadata
            try:
                conn = sqlite3.connect(str(METADATA_DB))
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE files
                    SET status = 'ARCHIVED', filepath = ?, modified = CURRENT_TIMESTAMP
                    WHERE filepath = ?
                ''', (str(archive_path), str(filepath)))
                conn.commit()
                conn.close()
            except:
                pass

        self.log_action("ARCHIVE", filepath, reason)

    def _move_to_trash(self, filepath, reason):
        """Move file to trash directory"""
        filepath = Path(filepath)
        if not filepath.exists():
            return

        # Determine trash location
        trash_path = TRASH_DIR / filepath.name

        # Handle filename collision
        if trash_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            trash_path = TRASH_DIR / f"{filepath.stem}_{timestamp}{filepath.suffix}"

        if not self.dry_run:
            shutil.move(str(filepath), str(trash_path))

            # Update metadata
            try:
                conn = sqlite3.connect(str(METADATA_DB))
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE files
                    SET status = 'DEPRECATED', filepath = ?, modified = CURRENT_TIMESTAMP
                    WHERE filepath = ?
                ''', (str(trash_path), str(filepath)))
                conn.commit()
                conn.close()
            except:
                pass

        self.log_action("TRASH", filepath, reason)

    def enforce_lfsme(self):
        """Enforce all LFSME rules"""
        print("\n=== ENFORCING LFSME PRINCIPLES ===\n")

        # LIGHTER: Limit total WIP files
        max_wip = LFSME_RULES['LIGHTER']['max_total_wip']
        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM files WHERE status = 'WIP'")
        wip_count = cursor.fetchone()[0]
        conn.close()

        if wip_count > max_wip:
            print(f"[LIGHTER] WIP overflow: {wip_count}/{max_wip}")
            self.clean_wip_overflow()

        # FASTER: Archive old files
        archive_days = LFSME_RULES['FASTER']['archive_old_days']
        print(f"[FASTER] Archiving files older than {archive_days} days...")
        archived = self.archive_old_files(archive_days)
        print(f"Archived {archived} old files")

        # STRONGER: Enforce redundancy rules
        print("[STRONGER] Checking for redundant files...")
        duplicates = self.find_duplicate_files()
        print(f"Found {len(duplicates)} duplicate groups")

        # LESS EXPENSIVE: Remove duplicates
        if LFSME_RULES['LESS_EXPENSIVE']['remove_duplicates']:
            print("[LESS EXPENSIVE] Removing duplicate files...")
            removed = self.remove_duplicates()
            print(f"Removed {removed} duplicate files")

        print("\n=== LFSME ENFORCEMENT COMPLETE ===\n")

    def generate_cleaning_report(self):
        """Generate report of all cleaning actions"""
        if not self.actions:
            return "No cleaning actions performed."

        report = "# FILE CLEANING REPORT\n\n"
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report += f"**Mode:** {'DRY RUN' if self.dry_run else 'LIVE'}\n"
        report += f"**Total Actions:** {len(self.actions)}\n\n"

        # Group by action type
        by_type = defaultdict(list)
        for action in self.actions:
            by_type[action['type']].append(action)

        for action_type, actions in sorted(by_type.items()):
            report += f"## {action_type} ({len(actions)} files)\n\n"
            for action in actions[:20]:  # Show first 20
                filepath = Path(action['filepath']).name
                report += f"- `{filepath}` - {action['reason']}\n"
            if len(actions) > 20:
                report += f"- ... and {len(actions) - 20} more\n"
            report += "\n"

        return report


def main():
    parser = argparse.ArgumentParser(description="Self-organizing file system cleaner")
    parser.add_argument('--dry-run', action='store_true', help="Preview changes without executing")
    parser.add_argument('--archive-old', type=int, help="Archive files older than N days")
    parser.add_argument('--remove-dupes', action='store_true', help="Remove duplicate files")
    parser.add_argument('--enforce-lfsme', action='store_true', help="Enforce all LFSME principles")

    args = parser.parse_args()

    cleaner = FileCleaner(dry_run=args.dry_run)

    if args.dry_run:
        print("\n*** DRY RUN MODE - No changes will be made ***\n")

    if args.enforce_lfsme:
        cleaner.enforce_lfsme()

    elif args.archive_old:
        print(f"Archiving files older than {args.archive_old} days...")
        archived = cleaner.archive_old_files(args.archive_old)
        print(f"Archived {archived} files")

    elif args.remove_dupes:
        print("Removing duplicate files...")
        removed = cleaner.remove_duplicates()
        print(f"Removed {removed} duplicate files")

    else:
        # Full clean
        print("Running full clean...")
        cleaner.enforce_lfsme()

    # Generate report
    print("\n" + "="*60)
    report = cleaner.generate_cleaning_report()
    print(report)
    print("="*60)


if __name__ == "__main__":
    main()
