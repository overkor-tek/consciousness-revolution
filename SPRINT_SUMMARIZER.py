#!/usr/bin/env python3
"""
SPRINT SUMMARIZER - End-of-Day/Sprint Consolidation System

Consolidates work at sprint/day boundaries:
- Collects all WIP files from the day
- Generates summary report
- Updates status to COMPLETE/REVIEW
- Creates consolidated artifact
- Cleans up redundant files
- Mirrors to Cyclotron

Toyota Principles:
- KAIZEN: Daily improvement cycle
- KANBAN: Pull system for work completion
- JIDOKA: Quality gates before completion

Usage:
    python SPRINT_SUMMARIZER.py                    # Summarize today
    python SPRINT_SUMMARIZER.py --sprint=1         # Summarize sprint 1
    python SPRINT_SUMMARIZER.py --days=7           # Last 7 days
    python SPRINT_SUMMARIZER.py --auto-clean       # Auto-archive old WIP
"""

import os
import sys
import json
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Import our file saver
try:
    from FILE_SAVER import FileSaver, save_file, update_status, search_files
except ImportError:
    print("ERROR: FILE_SAVER.py not found. Run from 100X_DEPLOYMENT directory.")
    sys.exit(1)

# Configuration
METADATA_DB = Path("C:/Users/dwrek/100X_DEPLOYMENT/.file_metadata/metadata.db")
SUMMARY_DIR = Path("C:/Users/dwrek/100X_DEPLOYMENT/ORGANIZED/SUMMARIES")

class SprintSummarizer:
    """Handles sprint/day-end consolidation"""

    def __init__(self):
        self.saver = FileSaver()
        SUMMARY_DIR.mkdir(exist_ok=True, parents=True)

    def get_files_by_date_range(self, start_date, end_date=None):
        """Get all files modified within date range"""
        if end_date is None:
            end_date = datetime.now()

        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM files
            WHERE modified >= ? AND modified <= ?
            ORDER BY modified DESC
        ''', (start_date.isoformat(), end_date.isoformat()))

        results = cursor.fetchall()
        conn.close()

        return results

    def get_today_files(self):
        """Get all files from today"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.get_files_by_date_range(today_start)

    def get_sprint_files(self, sprint_number):
        """Get files from specific sprint (assuming 2-week sprints)"""
        # Calculate sprint dates (2 weeks each, starting from project start)
        project_start = datetime(2025, 10, 1)  # Adjust to your project start
        sprint_start = project_start + timedelta(weeks=2 * (sprint_number - 1))
        sprint_end = sprint_start + timedelta(weeks=2)

        return self.get_files_by_date_range(sprint_start, sprint_end)

    def categorize_files(self, files):
        """Categorize files by domain, status, agent"""
        categorized = {
            'by_domain': defaultdict(list),
            'by_status': defaultdict(list),
            'by_agent': defaultdict(list),
            'by_pattern': defaultdict(list)
        }

        for file_row in files:
            # File row: id, filename, filepath, domain, pattern, component, status, agent, version, format, content_hash, created, modified, size_bytes, tags
            domain = file_row[3]
            pattern = file_row[4]
            status = file_row[6]
            agent = file_row[7]

            categorized['by_domain'][domain].append(file_row)
            categorized['by_status'][status].append(file_row)
            categorized['by_agent'][agent].append(file_row)
            categorized['by_pattern'][pattern].append(file_row)

        return categorized

    def generate_summary_report(self, files, title="Sprint Summary"):
        """Generate markdown summary report"""
        if not files:
            return f"# {title}\n\nNo files found for this period.\n"

        categorized = self.categorize_files(files)

        # Build report
        report = f"# {title}\n\n"
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report += f"**Total Files:** {len(files)}\n\n"

        # Summary statistics
        report += "## Summary Statistics\n\n"

        total_size = sum(f[13] for f in files)  # size_bytes column
        report += f"- Total Size: {total_size / 1_000_000:.2f} MB\n"
        report += f"- Files by Domain: {dict((k, len(v)) for k, v in categorized['by_domain'].items())}\n"
        report += f"- Files by Status: {dict((k, len(v)) for k, v in categorized['by_status'].items())}\n"
        report += f"- Files by Agent: {dict((k, len(v)) for k, v in categorized['by_agent'].items())}\n\n"

        # Breakdown by domain
        report += "## Breakdown by Domain\n\n"
        for domain, domain_files in sorted(categorized['by_domain'].items()):
            report += f"### {domain} ({len(domain_files)} files)\n\n"

            for file_row in domain_files[:10]:  # Show first 10
                filename = file_row[1]
                status = file_row[6]
                size = file_row[13]
                report += f"- `{filename}` [{status}] ({size} bytes)\n"

            if len(domain_files) > 10:
                report += f"- ... and {len(domain_files) - 10} more\n"

            report += "\n"

        # WIP Items (need attention)
        wip_files = categorized['by_status'].get('WIP', [])
        if wip_files:
            report += f"## WIP Items Requiring Attention ({len(wip_files)})\n\n"
            for file_row in wip_files:
                filename = file_row[1]
                component = file_row[5]
                modified = file_row[12]
                report += f"- `{filename}` - {component} (last modified: {modified})\n"
            report += "\n"

        # Completed items
        complete_files = categorized['by_status'].get('COMPLETE', [])
        if complete_files:
            report += f"## Completed Items ({len(complete_files)})\n\n"
            for file_row in complete_files[:20]:  # Show first 20
                filename = file_row[1]
                component = file_row[5]
                report += f"- {component}: `{filename}`\n"
            if len(complete_files) > 20:
                report += f"- ... and {len(complete_files) - 20} more\n"
            report += "\n"

        # Pattern Theory breakdown
        report += "## Pattern Theory Breakdown\n\n"
        for pattern, pattern_files in sorted(categorized['by_pattern'].items()):
            if pattern and pattern != "GENERAL":
                report += f"- **{pattern}**: {len(pattern_files)} files\n"
        report += "\n"

        # Next steps
        report += "## Recommended Next Steps\n\n"
        if wip_files:
            report += f"1. Review {len(wip_files)} WIP items - promote to COMPLETE or continue work\n"
        report += "2. Archive old COMPLETE items to free up working space\n"
        report += "3. Plan next sprint based on incomplete components\n"
        report += "4. Run FILE_CLEANER.py to reorganize if needed\n\n"

        # Footer
        report += "---\n"
        report += f"*Generated by SPRINT_SUMMARIZER.py - {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"

        return report

    def save_summary(self, report, summary_type="DAILY"):
        """Save summary report with proper naming"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"SUMMARY_{summary_type}_{timestamp}.md"
        filepath = SUMMARY_DIR / filename

        filepath.write_text(report, encoding='utf-8')

        # Also save via FileSaver for tracking
        save_file(
            content=report,
            domain="CONSCIOUSNESS",
            pattern="COMMUNICATION",
            component=f"SPRINT_SUMMARY_{summary_type}",
            status="COMPLETE",
            agent="AUTO",
            tags=["summary", "sprint", summary_type.lower()]
        )

        return str(filepath)

    def auto_clean_old_wip(self, days_threshold=7):
        """Auto-archive WIP items older than threshold"""
        cutoff_date = datetime.now() - timedelta(days=days_threshold)

        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        cursor.execute('''
            SELECT filename FROM files
            WHERE status = 'WIP' AND modified < ?
        ''', (cutoff_date.isoformat(),))

        old_wip = cursor.fetchall()
        conn.close()

        archived_count = 0
        for (filename,) in old_wip:
            try:
                update_status(filename, "ARCHIVED")
                archived_count += 1
            except:
                pass

        return archived_count

    def consolidate_redundant_files(self):
        """Find and mark redundant files (same content hash, different versions)"""
        conn = sqlite3.connect(str(METADATA_DB))
        cursor = conn.cursor()

        # Find duplicate hashes
        cursor.execute('''
            SELECT content_hash, COUNT(*) as cnt
            FROM files
            GROUP BY content_hash
            HAVING cnt > 1
        ''')

        duplicates = cursor.fetchall()

        redundant = []
        for content_hash, count in duplicates:
            cursor.execute('''
                SELECT filename, version, modified FROM files
                WHERE content_hash = ?
                ORDER BY version DESC, modified DESC
            ''', (content_hash,))

            files_with_hash = cursor.fetchall()

            # Keep the latest version, mark others as redundant
            for filename, version, modified in files_with_hash[1:]:
                redundant.append(filename)

        conn.close()

        # Mark redundant files as ARCHIVED
        archived_count = 0
        for filename in redundant:
            try:
                update_status(filename, "ARCHIVED")
                archived_count += 1
            except:
                pass

        return archived_count


def main():
    parser = argparse.ArgumentParser(description="Sprint/Day-end consolidation system")
    parser.add_argument('--sprint', type=int, help="Sprint number to summarize")
    parser.add_argument('--days', type=int, help="Number of days to summarize")
    parser.add_argument('--auto-clean', action='store_true', help="Auto-archive old WIP files")
    parser.add_argument('--consolidate', action='store_true', help="Consolidate redundant files")

    args = parser.parse_args()

    summarizer = SprintSummarizer()

    # Determine which files to summarize
    if args.sprint:
        files = summarizer.get_sprint_files(args.sprint)
        title = f"Sprint {args.sprint} Summary"
        summary_type = f"SPRINT_{args.sprint}"
    elif args.days:
        start_date = datetime.now() - timedelta(days=args.days)
        files = summarizer.get_files_by_date_range(start_date)
        title = f"Last {args.days} Days Summary"
        summary_type = f"LAST_{args.days}_DAYS"
    else:
        files = summarizer.get_today_files()
        title = f"Daily Summary - {datetime.now().strftime('%Y-%m-%d')}"
        summary_type = "DAILY"

    # Generate summary report
    print(f"Generating {title}...")
    report = summarizer.generate_summary_report(files, title)

    # Save summary
    summary_path = summarizer.save_summary(report, summary_type)
    print(f"\nSummary saved to: {summary_path}")

    # Print to console
    print("\n" + "="*60)
    print(report)
    print("="*60)

    # Auto-clean if requested
    if args.auto_clean:
        print("\nAuto-cleaning old WIP files...")
        archived = summarizer.auto_clean_old_wip(days_threshold=7)
        print(f"Archived {archived} old WIP files")

    # Consolidate if requested
    if args.consolidate:
        print("\nConsolidating redundant files...")
        archived = summarizer.consolidate_redundant_files()
        print(f"Archived {archived} redundant files")


if __name__ == "__main__":
    main()
