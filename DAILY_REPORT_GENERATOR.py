#!/usr/bin/env python3
"""
DAILY REPORT GENERATOR
Generates comprehensive daily status reports.
Aggregates all system data into readable format.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
REPORTS_PATH = CONSCIOUSNESS / "daily_reports"
REPORTS_PATH.mkdir(parents=True, exist_ok=True)


class DailyReportGenerator:
    """Generate daily status reports."""

    def __init__(self):
        self.sections = []

    def generate(self) -> str:
        """Generate complete daily report."""
        report = []

        # Header
        report.append("=" * 60)
        report.append("CONSCIOUSNESS REVOLUTION - DAILY STATUS REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # System Health
        report.append(self._section_health())

        # Cyclotron Status
        report.append(self._section_cyclotron())

        # Activity Summary
        report.append(self._section_activity())

        # API Usage
        report.append(self._section_api())

        # Backup Status
        report.append(self._section_backup())

        # Alerts
        report.append(self._section_alerts())

        # Recommendations
        report.append(self._section_recommendations())

        # Footer
        report.append("")
        report.append("=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)

        return "\n".join(report)

    def _section_health(self) -> str:
        """Health section."""
        lines = ["", "📊 SYSTEM HEALTH", "-" * 40]

        metrics = CONSCIOUSNESS / "monitoring" / "metrics.json"
        if metrics.exists():
            with open(metrics) as f:
                data = json.load(f)

            current = data.get("current", {})
            lines.append(f"Health Score: {current.get('health_score', 0):.1f}%")

            for component in ["cyclotron", "brain", "disk", "api"]:
                comp_data = current.get(component, {})
                status = "✅" if comp_data.get("healthy") else "❌"
                lines.append(f"  {status} {component.capitalize()}")
        else:
            lines.append("No metrics available")

        return "\n".join(lines)

    def _section_cyclotron(self) -> str:
        """Cyclotron section."""
        lines = ["", "🔄 CYCLOTRON KNOWLEDGE BASE", "-" * 40]

        index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
        if index.exists():
            with open(index) as f:
                data = json.load(f)

            stats = data.get("stats", {})
            lines.append(f"Total Atoms: {stats.get('total', 0)}")

            by_type = stats.get("by_type", {})
            if by_type:
                lines.append("By Type:")
                for t, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:5]:
                    lines.append(f"  • {t}: {count}")

            tags = data.get("tags", {})
            top_tags = sorted(tags.items(), key=lambda x: len(x[1]), reverse=True)[:5]
            if top_tags:
                lines.append("Top Tags:")
                for tag, atoms in top_tags:
                    lines.append(f"  • {tag}: {len(atoms)}")
        else:
            lines.append("Cyclotron not initialized")

        return "\n".join(lines)

    def _section_activity(self) -> str:
        """Activity section."""
        lines = ["", "📈 ACTIVITY SUMMARY", "-" * 40]

        # Task results
        results_path = CONSCIOUSNESS / "task_results"
        if results_path.exists():
            today = datetime.now().strftime("%Y%m%d")
            today_results = list(results_path.glob(f"result_{today}*.json"))
            lines.append(f"Tasks completed today: {len(today_results)}")
        else:
            lines.append("Tasks completed today: 0")

        # Agent states
        agents_path = CONSCIOUSNESS / "agents"
        if agents_path.exists():
            states = list(agents_path.glob("state_*.json"))
            lines.append(f"Agent executions (all time): {len(states)}")

        # Session count
        sessions_path = CONSCIOUSNESS / "sessions"
        if sessions_path.exists():
            sessions = list(sessions_path.glob("*/session_*.json"))
            lines.append(f"Sessions recorded: {len(sessions)}")

        return "\n".join(lines)

    def _section_api(self) -> str:
        """API usage section."""
        lines = ["", "💰 API USAGE", "-" * 40]

        usage = CONSCIOUSNESS / "monitoring" / "api_usage.json"
        if usage.exists():
            with open(usage) as f:
                data = json.load(f)

            today = datetime.now().strftime("%Y-%m-%d")
            today_data = data.get("daily", {}).get(today, {})

            lines.append(f"Today's cost: ${today_data.get('cost', 0):.4f}")
            lines.append(f"Today's calls: {today_data.get('calls', 0)}")
            lines.append(f"Total cost: ${data.get('total_cost', 0):.4f}")
        else:
            lines.append("No API usage data")

        return "\n".join(lines)

    def _section_backup(self) -> str:
        """Backup section."""
        lines = ["", "💾 BACKUP STATUS", "-" * 40]

        manifest = HOME / ".backups" / "manifest.json"
        if manifest.exists():
            with open(manifest) as f:
                data = json.load(f)

            lines.append(f"Total backups: {len(data.get('backups', []))}")
            lines.append(f"Last backup: {data.get('last_backup', 'Never')}")

            total_size = data.get('total_size', 0)
            lines.append(f"Total size: {total_size / (1024*1024):.2f} MB")
        else:
            lines.append("No backups configured")

        return "\n".join(lines)

    def _section_alerts(self) -> str:
        """Alerts section."""
        lines = ["", "⚠️ ALERTS", "-" * 40]

        alerts = CONSCIOUSNESS / "monitoring" / "alerts.json"
        if alerts.exists():
            with open(alerts) as f:
                data = json.load(f)

            active = data.get("active", [])
            if active:
                lines.append(f"Active alerts: {len(active)}")
                for alert in active[-5:]:
                    lines.append(f"  • [{alert['severity']}] {alert['message']}")
            else:
                lines.append("No active alerts ✅")
        else:
            lines.append("No alerts data")

        return "\n".join(lines)

    def _section_recommendations(self) -> str:
        """Recommendations section."""
        lines = ["", "💡 RECOMMENDATIONS", "-" * 40]

        recommendations = []

        # Check backup freshness
        manifest = HOME / ".backups" / "manifest.json"
        if manifest.exists():
            with open(manifest) as f:
                data = json.load(f)
            last = data.get("last_backup")
            if last:
                last_dt = datetime.strptime(last, "%Y%m%d_%H%M%S")
                if datetime.now() - last_dt > timedelta(days=1):
                    recommendations.append("Run backup: python AUTOMATED_BACKUP_SYSTEM.py backup")

        # Check cyclotron
        index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
        if index.exists():
            with open(index) as f:
                data = json.load(f)
            if data.get("stats", {}).get("total", 0) < 100:
                recommendations.append("Unify knowledge: python KNOWLEDGE_UNIFIER.py unify")

        if not recommendations:
            lines.append("All systems optimal ✅")
        else:
            for rec in recommendations:
                lines.append(f"• {rec}")

        return "\n".join(lines)

    def save_report(self) -> Path:
        """Generate and save report."""
        report = self.generate()

        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = REPORTS_PATH / filename

        with open(filepath, 'w') as f:
            f.write(report)

        # Also save as latest
        latest = REPORTS_PATH / "latest.txt"
        with open(latest, 'w') as f:
            f.write(report)

        return filepath


def main():
    """CLI for report generator."""
    import sys

    generator = DailyReportGenerator()

    if len(sys.argv) < 2:
        # Default: generate and print
        print(generator.generate())
        return

    command = sys.argv[1]

    if command == "generate":
        print(generator.generate())

    elif command == "save":
        path = generator.save_report()
        print(f"Report saved to: {path}")

    elif command == "latest":
        latest = REPORTS_PATH / "latest.txt"
        if latest.exists():
            print(latest.read_text())
        else:
            print("No saved report. Run 'save' first.")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
