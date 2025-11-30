#!/usr/bin/env python3
"""
FILE SYSTEM MASTER - Self-Organizing File Management Orchestrator

Combines all file management systems:
- FILE_SAVER: 8-dimensional naming
- SPRINT_SUMMARIZER: Day/sprint consolidation
- DELEGATOR: Task offloading
- FILE_CLEANER: Auto-reorganization
- CYCLOTRON: Knowledge indexing

Usage:
    python FILE_SYSTEM_MASTER.py --save <content> --domain COMPUTER --component TEST
    python FILE_SYSTEM_MASTER.py --daily-summary
    python FILE_SYSTEM_MASTER.py --delegate "Build X" --to C1
    python FILE_SYSTEM_MASTER.py --clean
    python FILE_SYSTEM_MASTER.py --status
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Import all subsystems
try:
    from FILE_SAVER import FileSaver, save_file, update_status, search_files, get_stats as get_file_stats
    from SPRINT_SUMMARIZER import SprintSummarizer
    from DELEGATOR import Delegator, delegate_task, get_pending_tasks, get_stats as get_delegation_stats
    from FILE_CLEANER import FileCleaner
except ImportError as e:
    print(f"ERROR: Missing required module: {e}")
    print("Ensure all components are in the same directory.")
    sys.exit(1)

class FileSystemMaster:
    """Master orchestrator for self-organizing file system"""

    def __init__(self):
        self.file_saver = FileSaver()
        self.summarizer = SprintSummarizer()
        self.delegator = Delegator()
        self.cleaner = FileCleaner()

    def save_work(self, content, domain, pattern, component, status="WIP", agent="AUTO", tags=None):
        """Save work with proper naming and indexing"""
        result = save_file(
            content=content,
            domain=domain,
            pattern=pattern,
            component=component,
            status=status,
            agent=agent,
            tags=tags
        )

        print(f"✅ Saved: {result['filename']}")
        print(f"📁 Path: {result['filepath']}")
        print(f"📊 Size: {result['size_bytes']} bytes")

        return result

    def end_of_day_routine(self):
        """Run end-of-day consolidation"""
        print("\n🌙 END OF DAY ROUTINE\n")
        print("="*60)

        # 1. Generate daily summary
        print("\n1. Generating daily summary...")
        files = self.summarizer.get_today_files()
        report = self.summarizer.generate_summary_report(
            files,
            title=f"Daily Summary - {datetime.now().strftime('%Y-%m-%d')}"
        )
        summary_path = self.summarizer.save_summary(report, "DAILY")
        print(f"   ✅ Summary saved: {summary_path}")

        # 2. Clean up old WIP
        print("\n2. Cleaning old WIP files...")
        archived = self.summarizer.auto_clean_old_wip(days_threshold=7)
        print(f"   ✅ Archived {archived} old WIP files")

        # 3. Remove duplicates
        print("\n3. Removing duplicate files...")
        self.cleaner.dry_run = False
        removed = self.cleaner.remove_duplicates()
        print(f"   ✅ Removed {removed} duplicate files")

        # 4. Show delegation status
        print("\n4. Delegation status...")
        pending = get_pending_tasks()
        print(f"   📋 Pending tasks: {len(pending)}")

        print("\n" + "="*60)
        print("✨ End of day routine complete!")

        return {
            'summary_path': summary_path,
            'archived_wip': archived,
            'removed_duplicates': removed,
            'pending_tasks': len(pending)
        }

    def sprint_end_routine(self, sprint_number):
        """Run end-of-sprint consolidation"""
        print(f"\n🏁 SPRINT {sprint_number} END ROUTINE\n")
        print("="*60)

        # 1. Generate sprint summary
        print("\n1. Generating sprint summary...")
        files = self.summarizer.get_sprint_files(sprint_number)
        report = self.summarizer.generate_summary_report(
            files,
            title=f"Sprint {sprint_number} Summary"
        )
        summary_path = self.summarizer.save_summary(report, f"SPRINT_{sprint_number}")
        print(f"   ✅ Summary saved: {summary_path}")

        # 2. Consolidate redundant files
        print("\n2. Consolidating redundant files...")
        archived = self.summarizer.consolidate_redundant_files()
        print(f"   ✅ Archived {archived} redundant files")

        # 3. Enforce LFSME principles
        print("\n3. Enforcing LFSME principles...")
        self.cleaner.dry_run = False
        self.cleaner.enforce_lfsme()
        print(f"   ✅ LFSME enforcement complete")

        print("\n" + "="*60)
        print(f"✨ Sprint {sprint_number} consolidation complete!")

        return {
            'summary_path': summary_path,
            'archived_redundant': archived
        }

    def delegate_work(self, task_description, assigned_to="ANY", priority="normal", tags=None):
        """Delegate work to Trinity agents"""
        task_id = delegate_task(task_description, assigned_to, priority, tags)

        print(f"✅ Task delegated: TASK-{task_id}")
        print(f"📋 Assigned to: {assigned_to}")
        print(f"🎯 Priority: {priority}")
        print(f"📢 Posted to BULLETIN_BOARD.md")

        return task_id

    def show_status(self):
        """Show comprehensive system status"""
        print("\n" + "="*60)
        print("📊 FILE SYSTEM STATUS")
        print("="*60)

        # File stats
        print("\n📁 FILE ORGANIZATION:")
        file_stats = get_file_stats()
        print(f"   Total Files: {file_stats['total_files']}")
        print(f"   Total Size: {file_stats['total_size_mb']} MB")
        print(f"   By Domain: {file_stats['by_domain']}")
        print(f"   By Status: {file_stats['by_status']}")
        print(f"   By Agent: {file_stats['by_agent']}")

        # Delegation stats
        print("\n📋 DELEGATION STATUS:")
        delegation_stats = get_delegation_stats()
        print(f"   Total Tasks: {delegation_stats['total_tasks']}")
        print(f"   By Status: {delegation_stats['by_status']}")
        print(f"   By Assigned: {delegation_stats['by_assigned']}")
        print(f"   Pending Priority: {delegation_stats['pending_by_priority']}")

        # Today's activity
        print("\n📆 TODAY'S ACTIVITY:")
        today_files = self.summarizer.get_today_files()
        print(f"   Files Created/Modified: {len(today_files)}")

        categorized = self.summarizer.categorize_files(today_files)
        print(f"   By Status: {dict((k, len(v)) for k, v in categorized['by_status'].items())}")

        print("\n" + "="*60)

    def quick_save(self, content_file=None, content_text=None, domain="COMPUTER",
                   pattern="GENERAL", component="WORK", status="WIP", agent="HUMAN"):
        """Quick save from file or text"""

        if content_file:
            content = Path(content_file).read_text(encoding='utf-8')
        elif content_text:
            content = content_text
        else:
            print("ERROR: Must provide either --file or --text")
            return None

        return self.save_work(content, domain, pattern, component, status, agent)


def main():
    parser = argparse.ArgumentParser(description="Self-organizing file system master controller")

    # Save operations
    parser.add_argument('--save', action='store_true', help="Save new file")
    parser.add_argument('--file', help="Content from file")
    parser.add_argument('--text', help="Content as text")
    parser.add_argument('--domain', default="COMPUTER", help="Domain (COMPUTER/CONSCIOUSNESS/etc)")
    parser.add_argument('--pattern', default="GENERAL", help="Pattern component")
    parser.add_argument('--component', default="WORK", help="Component name")
    parser.add_argument('--status', default="WIP", help="Status (WIP/COMPLETE/etc)")
    parser.add_argument('--agent', default="HUMAN", help="Agent (C1/C2/C3/HUMAN/etc)")

    # Routine operations
    parser.add_argument('--daily-summary', action='store_true', help="Run end-of-day routine")
    parser.add_argument('--sprint-end', type=int, help="Run end-of-sprint routine (sprint number)")

    # Delegation
    parser.add_argument('--delegate', help="Delegate task")
    parser.add_argument('--to', default="ANY", help="Assign to (C1/C2/C3/ANY)")
    parser.add_argument('--priority', default="normal", help="Priority (urgent/high/normal/low)")

    # Cleaning
    parser.add_argument('--clean', action='store_true', help="Run file cleaner")
    parser.add_argument('--dry-run', action='store_true', help="Dry run mode")

    # Status
    parser.add_argument('--show-status', action='store_true', help="Show system status")

    args = parser.parse_args()

    master = FileSystemMaster()

    # Execute requested operation
    if args.save:
        master.quick_save(
            content_file=args.file,
            content_text=args.text,
            domain=args.domain,
            pattern=args.pattern,
            component=args.component,
            status=args.status,
            agent=args.agent
        )

    elif args.daily_summary:
        master.end_of_day_routine()

    elif args.sprint_end:
        master.sprint_end_routine(args.sprint_end)

    elif args.delegate:
        master.delegate_work(args.delegate, args.to, args.priority)

    elif args.clean:
        cleaner = FileCleaner(dry_run=args.dry_run)
        cleaner.enforce_lfsme()

    elif args.show_status:
        master.show_status()

    else:
        # Show help if no args
        parser.print_help()


if __name__ == "__main__":
    main()
