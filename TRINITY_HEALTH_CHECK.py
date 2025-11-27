#!/usr/bin/env python3
"""
TRINITY HEALTH CHECK & DIAGNOSTICS

Validates all Trinity tools are installed and working correctly.
Runs comprehensive system checks before deployment.

Usage: python3 TRINITY_HEALTH_CHECK.py

Returns: Exit code 0 if all checks pass, 1 if any fail
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

class TrinityHealthCheck:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []

    def check(self, name, condition, fix_hint=None):
        """Run a single check"""
        if condition:
            print(f"  ✅ {name}")
            self.checks_passed += 1
            return True
        else:
            print(f"  ❌ {name}")
            if fix_hint:
                print(f"     Fix: {fix_hint}")
            self.checks_failed += 1
            return False

    def warn(self, name, condition, hint=None):
        """Issue a warning"""
        if not condition:
            print(f"  ⚠️  {name}")
            if hint:
                print(f"     Note: {hint}")
            self.warnings.append(name)

    def check_file_exists(self, filepath, name):
        """Check if a file exists"""
        full_path = self.base_dir / filepath
        return self.check(
            f"{name} exists",
            full_path.exists(),
            f"File not found: {filepath}"
        )

    def check_file_executable(self, filepath, name):
        """Check if a file is executable"""
        full_path = self.base_dir / filepath
        return self.check(
            f"{name} is executable",
            full_path.exists() and os.access(full_path, os.X_OK),
            f"Run: chmod +x {filepath}"
        )

    def check_python_syntax(self, filepath):
        """Check if Python file has valid syntax"""
        full_path = self.base_dir / filepath
        if not full_path.exists():
            return False

        try:
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', str(full_path)],
                capture_output=True,
                text=True
            )
            return self.check(
                f"{filepath} has valid syntax",
                result.returncode == 0,
                f"Syntax error in {filepath}"
            )
        except Exception as e:
            return self.check(
                f"{filepath} syntax check",
                False,
                f"Error checking {filepath}: {e}"
            )

    def check_git_status(self):
        """Check git repository status"""
        try:
            result = subprocess.run(
                ['git', 'status'],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            is_repo = result.returncode == 0
            self.check(
                "Git repository initialized",
                is_repo,
                "Run: git init"
            )

            if is_repo:
                # Check if there are uncommitted changes
                result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=self.base_dir,
                    capture_output=True,
                    text=True
                )
                has_changes = len(result.stdout.strip()) > 0
                self.warn(
                    "Uncommitted changes present",
                    not has_changes,
                    "Consider committing work: git add . && git commit"
                )

            return is_repo
        except Exception:
            return self.check(
                "Git repository initialized",
                False,
                "Git not available or not a repository"
            )

    def check_directory_structure(self):
        """Check if required directories exist"""
        dirs = [
            '.consciousness/sync',
            '.consciousness/trinity',
            '.consciousness/pids'
        ]

        for dir_path in dirs:
            full_path = self.base_dir / dir_path
            self.check(
                f"Directory {dir_path} exists",
                full_path.exists(),
                f"Run: mkdir -p {dir_path}"
            )

    def run_all_checks(self):
        """Run all health checks"""
        print("="*70)
        print("⚡ TRINITY HEALTH CHECK & DIAGNOSTICS")
        print("="*70)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Location: {self.base_dir}")
        print()

        # 1. Core Files Check
        print("📁 CORE FILES:")
        self.check_file_exists("TRINITY_LIVE_DASHBOARD.html", "Dashboard")
        self.check_file_exists("TRINITY_STATUS_READER.py", "Status Reader")
        self.check_file_exists("CP1_OUTPUT_GENERATOR.py", "Output Generator")
        self.check_file_exists("AUTONOMOUS_WORK_MONITOR.py", "Work Monitor")
        self.check_file_exists("TRINITY_MASTER_ORCHESTRATOR.py", "Orchestrator")
        self.check_file_exists("trinity.sh", "Quick Access Script")
        self.check_file_exists("SESSION_SUMMARY_GENERATOR.py", "Summary Generator")
        self.check_file_exists("CP1_C3_TOOLS_README.md", "Documentation")
        print()

        # 2. Executability Check
        print("🔧 EXECUTABILITY:")
        self.check_file_executable("TRINITY_STATUS_READER.py", "Status Reader")
        self.check_file_executable("CP1_OUTPUT_GENERATOR.py", "Output Generator")
        self.check_file_executable("AUTONOMOUS_WORK_MONITOR.py", "Work Monitor")
        self.check_file_executable("TRINITY_MASTER_ORCHESTRATOR.py", "Orchestrator")
        self.check_file_executable("trinity.sh", "Quick Access Script")
        self.check_file_executable("SESSION_SUMMARY_GENERATOR.py", "Summary Generator")
        print()

        # 3. Python Syntax Check
        print("🐍 PYTHON SYNTAX:")
        self.check_python_syntax("TRINITY_STATUS_READER.py")
        self.check_python_syntax("CP1_OUTPUT_GENERATOR.py")
        self.check_python_syntax("AUTONOMOUS_WORK_MONITOR.py")
        self.check_python_syntax("TRINITY_MASTER_ORCHESTRATOR.py")
        self.check_python_syntax("SESSION_SUMMARY_GENERATOR.py")
        self.check_python_syntax("TRINITY_HEALTH_CHECK.py")
        print()

        # 4. Directory Structure
        print("📂 DIRECTORY STRUCTURE:")
        self.check_directory_structure()
        print()

        # 5. Git Repository
        print("📦 GIT REPOSITORY:")
        self.check_git_status()
        print()

        # 6. Dependencies Check
        print("📚 DEPENDENCIES:")
        self.check(
            "Python 3 available",
            sys.version_info >= (3, 6),
            "Upgrade to Python 3.6 or higher"
        )
        print()

        # Final Report
        print("="*70)
        print("📊 HEALTH CHECK SUMMARY")
        print("="*70)
        print(f"✅ Checks Passed: {self.checks_passed}")
        print(f"❌ Checks Failed: {self.checks_failed}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print()

        if self.checks_failed == 0:
            print("🎉 ALL SYSTEMS OPERATIONAL")
            print()
            print("Trinity tools are ready for deployment!")
            print()
            print("Quick Start:")
            print("  ./trinity.sh start      # Start all systems")
            print("  ./trinity.sh dashboard  # Open dashboard")
            print()
            return 0
        else:
            print("⚠️  SOME CHECKS FAILED")
            print()
            print("Please fix the issues above before deployment.")
            print()
            return 1

def main():
    checker = TrinityHealthCheck()
    exit_code = checker.run_all_checks()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
