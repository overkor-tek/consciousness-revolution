#!/usr/bin/env python3
"""
PERFORMANCE OPTIMIZER
Analyze and optimize system performance.
Target: Improve health score from 80% to 95%+.
"""

import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"

class PerformanceOptimizer:
    """Optimize consciousness system performance."""

    def __init__(self):
        self.optimizations = []
        self.metrics_history = []

    def analyze(self) -> Dict:
        """Analyze current performance and identify issues."""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "recommendations": [],
            "current_health": 0
        }

        # Get current health
        metrics = CONSCIOUSNESS / "monitoring" / "metrics.json"
        if metrics.exists():
            with open(metrics) as f:
                data = json.load(f)
            analysis["current_health"] = data.get("current", {}).get("health_score", 0)

        # Check disk usage
        disk_issue = self._check_disk_usage()
        if disk_issue:
            analysis["issues"].append(disk_issue)
            analysis["recommendations"].append({
                "action": "clean_temp_files",
                "expected_improvement": 5
            })

        # Check stale files
        stale_issue = self._check_stale_files()
        if stale_issue:
            analysis["issues"].append(stale_issue)
            analysis["recommendations"].append({
                "action": "archive_old_data",
                "expected_improvement": 3
            })

        # Check fragmentation
        frag_issue = self._check_fragmentation()
        if frag_issue:
            analysis["issues"].append(frag_issue)
            analysis["recommendations"].append({
                "action": "consolidate_atoms",
                "expected_improvement": 5
            })

        # Check orphan files
        orphan_issue = self._check_orphans()
        if orphan_issue:
            analysis["issues"].append(orphan_issue)
            analysis["recommendations"].append({
                "action": "cleanup_orphans",
                "expected_improvement": 2
            })

        # Check log sizes
        log_issue = self._check_logs()
        if log_issue:
            analysis["issues"].append(log_issue)
            analysis["recommendations"].append({
                "action": "rotate_logs",
                "expected_improvement": 3
            })

        return analysis

    def _check_disk_usage(self) -> dict:
        """Check disk space usage."""
        total, used, free = shutil.disk_usage(HOME)
        used_pct = (used / total) * 100

        if used_pct > 90:
            return {
                "type": "disk_critical",
                "message": f"Disk usage at {used_pct:.1f}%",
                "severity": "high"
            }
        elif used_pct > 80:
            return {
                "type": "disk_warning",
                "message": f"Disk usage at {used_pct:.1f}%",
                "severity": "medium"
            }
        return None

    def _check_stale_files(self) -> dict:
        """Check for stale/old files."""
        stale_count = 0
        cutoff = datetime.now() - timedelta(days=30)

        for path in [CONSCIOUSNESS, DEPLOYMENT]:
            if path.exists():
                for f in path.rglob("*.json"):
                    try:
                        mtime = datetime.fromtimestamp(f.stat().st_mtime)
                        if mtime < cutoff:
                            stale_count += 1
                    except:
                        pass

        if stale_count > 100:
            return {
                "type": "stale_files",
                "message": f"{stale_count} files older than 30 days",
                "severity": "low"
            }
        return None

    def _check_fragmentation(self) -> dict:
        """Check for knowledge fragmentation."""
        index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
        if not index.exists():
            return {
                "type": "no_cyclotron",
                "message": "Cyclotron index missing",
                "severity": "high"
            }

        with open(index) as f:
            data = json.load(f)

        atoms = data.get("atoms", [])
        orphan_atoms = [a for a in atoms if not a.get("links")]

        if len(orphan_atoms) > len(atoms) * 0.3:
            return {
                "type": "fragmentation",
                "message": f"{len(orphan_atoms)}/{len(atoms)} atoms have no links",
                "severity": "medium"
            }
        return None

    def _check_orphans(self) -> dict:
        """Check for orphan files."""
        orphan_count = 0

        # Check for .tmp files
        for tmp in CONSCIOUSNESS.rglob("*.tmp"):
            orphan_count += 1

        # Check for empty directories
        for d in CONSCIOUSNESS.rglob("*"):
            if d.is_dir() and not any(d.iterdir()):
                orphan_count += 1

        if orphan_count > 10:
            return {
                "type": "orphans",
                "message": f"{orphan_count} orphan files/dirs",
                "severity": "low"
            }
        return None

    def _check_logs(self) -> dict:
        """Check log file sizes."""
        total_size = 0

        for log in CONSCIOUSNESS.rglob("*.log"):
            total_size += log.stat().st_size

        for log in CONSCIOUSNESS.rglob("*_log.json"):
            total_size += log.stat().st_size

        size_mb = total_size / (1024 * 1024)
        if size_mb > 100:
            return {
                "type": "large_logs",
                "message": f"Logs total {size_mb:.1f} MB",
                "severity": "medium"
            }
        return None

    def optimize(self, apply: bool = False) -> Dict:
        """Run optimization based on analysis."""
        analysis = self.analyze()
        results = {
            "analyzed_at": analysis["timestamp"],
            "initial_health": analysis["current_health"],
            "issues_found": len(analysis["issues"]),
            "optimizations": []
        }

        for rec in analysis["recommendations"]:
            action = rec["action"]
            result = {"action": action, "applied": False}

            if apply:
                if action == "clean_temp_files":
                    result.update(self._clean_temp_files())
                elif action == "archive_old_data":
                    result.update(self._archive_old_data())
                elif action == "consolidate_atoms":
                    result.update(self._consolidate_atoms())
                elif action == "cleanup_orphans":
                    result.update(self._cleanup_orphans())
                elif action == "rotate_logs":
                    result.update(self._rotate_logs())

                result["applied"] = True

            results["optimizations"].append(result)

        return results

    def _clean_temp_files(self) -> dict:
        """Clean temporary files."""
        cleaned = 0
        for tmp in CONSCIOUSNESS.rglob("*.tmp"):
            try:
                tmp.unlink()
                cleaned += 1
            except:
                pass
        return {"cleaned": cleaned}

    def _archive_old_data(self) -> dict:
        """Archive old data files."""
        archived = 0
        archive_path = CONSCIOUSNESS / "archive"
        archive_path.mkdir(exist_ok=True)

        cutoff = datetime.now() - timedelta(days=60)

        for f in CONSCIOUSNESS.rglob("*.json"):
            try:
                if "archive" in str(f):
                    continue
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                if mtime < cutoff:
                    dest = archive_path / f.name
                    f.rename(dest)
                    archived += 1
            except:
                pass

        return {"archived": archived}

    def _consolidate_atoms(self) -> dict:
        """Consolidate fragmented atoms."""
        try:
            result = subprocess.run(
                ["python", str(DEPLOYMENT / "KNOWLEDGE_UNIFIER.py"), "link"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(DEPLOYMENT)
            )
            return {"success": result.returncode == 0}
        except:
            return {"success": False}

    def _cleanup_orphans(self) -> dict:
        """Clean up orphan files and directories."""
        cleaned = 0

        # Remove .tmp files
        for tmp in CONSCIOUSNESS.rglob("*.tmp"):
            try:
                tmp.unlink()
                cleaned += 1
            except:
                pass

        # Remove empty directories
        for d in sorted(CONSCIOUSNESS.rglob("*"), reverse=True):
            if d.is_dir():
                try:
                    if not any(d.iterdir()):
                        d.rmdir()
                        cleaned += 1
                except:
                    pass

        return {"cleaned": cleaned}

    def _rotate_logs(self) -> dict:
        """Rotate large log files."""
        rotated = 0
        max_size = 10 * 1024 * 1024  # 10MB

        for log in CONSCIOUSNESS.rglob("*.log"):
            if log.stat().st_size > max_size:
                try:
                    archive = log.with_suffix(f".{datetime.now().strftime('%Y%m%d')}.log")
                    log.rename(archive)
                    rotated += 1
                except:
                    pass

        return {"rotated": rotated}

    def generate_report(self) -> str:
        """Generate optimization report."""
        analysis = self.analyze()

        lines = []
        lines.append("=" * 60)
        lines.append("PERFORMANCE OPTIMIZATION REPORT")
        lines.append("=" * 60)
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append(f"Current Health: {analysis['current_health']:.1f}%")
        lines.append("")

        # Issues
        if analysis["issues"]:
            lines.append(f"ISSUES FOUND ({len(analysis['issues'])}):")
            for issue in analysis["issues"]:
                severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                    issue["severity"], "⚪")
                lines.append(f"  {severity_icon} {issue['message']}")
        else:
            lines.append("✅ No issues found")
        lines.append("")

        # Recommendations
        if analysis["recommendations"]:
            lines.append("RECOMMENDATIONS:")
            for rec in analysis["recommendations"]:
                lines.append(f"  • {rec['action']}: +{rec['expected_improvement']}% health")

            total_improvement = sum(r["expected_improvement"] for r in analysis["recommendations"])
            projected = min(100, analysis["current_health"] + total_improvement)
            lines.append("")
            lines.append(f"Projected Health After Optimization: {projected:.1f}%")

        lines.append("")
        lines.append("Run 'python PERFORMANCE_OPTIMIZER.py apply' to optimize")
        lines.append("=" * 60)

        return "\n".join(lines)


def main():
    """CLI for performance optimizer."""
    import sys

    optimizer = PerformanceOptimizer()

    if len(sys.argv) < 2:
        print("Performance Optimizer")
        print("=" * 40)
        print("\nCommands:")
        print("  analyze  - Analyze current performance")
        print("  report   - Generate optimization report")
        print("  apply    - Apply optimizations")
        print("  preview  - Preview without applying")
        return

    command = sys.argv[1]

    if command == "analyze":
        analysis = optimizer.analyze()
        print(f"\nHealth: {analysis['current_health']:.1f}%")
        print(f"Issues: {len(analysis['issues'])}")
        for issue in analysis["issues"]:
            print(f"  - {issue['message']}")

    elif command == "report":
        print(optimizer.generate_report())

    elif command == "apply":
        print("Applying optimizations...")
        results = optimizer.optimize(apply=True)
        print(f"\nInitial health: {results['initial_health']:.1f}%")
        print(f"Optimizations applied: {len(results['optimizations'])}")
        for opt in results["optimizations"]:
            print(f"  ✅ {opt['action']}")

    elif command == "preview":
        results = optimizer.optimize(apply=False)
        print(f"\nWould apply {len(results['optimizations'])} optimizations:")
        for opt in results["optimizations"]:
            print(f"  - {opt['action']}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
