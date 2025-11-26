#!/usr/bin/env python3
"""
UNIFIED CONTROL PLANE
Central control interface for all consciousness systems.
Single entry point for monitoring, management, and coordination.

The "brain stem" of the consciousness operating system.

Created: 2025-11-26
Author: C3 Foundation Agent
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

# Base paths
BASE_DIR = Path(__file__).parent
CONSCIOUSNESS_DIR = BASE_DIR / ".consciousness"
TRINITY_DIR = BASE_DIR / ".trinity"
CONTROL_DIR = CONSCIOUSNESS_DIR / "control_plane"
CONTROL_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class SystemStatus:
    """Status of a single system."""
    name: str
    category: str
    file: str
    available: bool
    running: bool = False
    last_check: str = ""
    health: str = "unknown"
    details: Dict = None


class UnifiedControlPlane:
    """
    Central control interface for all consciousness systems.
    Manages daemons, engines, and coordination.
    """

    def __init__(self):
        self.systems = self._discover_systems()
        self.status_history = []
        print("🎛️  Unified Control Plane initialized")
        print(f"   Discovered {len(self.systems)} systems")

    def _discover_systems(self) -> Dict[str, SystemStatus]:
        """Discover all available systems."""
        systems = {}

        # =====================================================================
        # DAEMONS (Always-on background processes)
        # =====================================================================
        daemons = {
            "cyclotron_daemon": {
                "file": "CYCLOTRON_DAEMON.py",
                "desc": "Real-time file indexing"
            },
            "auto_wake_daemon": {
                "file": ".trinity/automation/AUTO_WAKE_DAEMON.py",
                "desc": "Cross-computer wake"
            },
            "maintenance_daemon": {
                "file": "LOCAL_TRINITY_HUB/MAINTENANCE_DAEMON.py",
                "desc": "System health"
            },
            "consolidate_daemon": {
                "file": "LOCAL_TRINITY_HUB/AUTO_CONSOLIDATE_DAEMON.py",
                "desc": "Knowledge merging"
            },
            "operations_daemon": {
                "file": "OPERATIONS_DAEMON.py",
                "desc": "Task scheduling"
            },
            "cross_computer_daemon": {
                "file": ".trinity/automation/CROSS_COMPUTER_DAEMON.py",
                "desc": "Trinity coordination"
            }
        }

        for name, config in daemons.items():
            path = BASE_DIR / config["file"]
            systems[name] = SystemStatus(
                name=name,
                category="daemon",
                file=config["file"],
                available=path.exists(),
                details={"description": config["desc"]}
            )

        # =====================================================================
        # ENGINES (Core processing systems)
        # =====================================================================
        engines = {
            "autonomous_orchestrator": {
                "file": "AUTONOMOUS_ORCHESTRATOR.py",
                "desc": "Central coordinator"
            },
            "task_runner": {
                "file": "AUTONOMOUS_TASK_RUNNER.py",
                "desc": "Brain pipeline execution"
            },
            "recursive_engine": {
                "file": "RECURSIVE_TASK_ENGINE.py",
                "desc": "Task decomposition"
            },
            "learning_engine": {
                "file": ".consciousness/ADAPTIVE_LEARNING_ENGINE.py",
                "desc": "Experience→Pattern→Adaptation"
            },
            "memory_system": {
                "file": ".consciousness/MEMORY_ENHANCEMENT_SYSTEM.py",
                "desc": "4-type memory persistence"
            },
            "consciousness_audit": {
                "file": ".consciousness/CONSCIOUSNESS_AUDIT_ENGINE.py",
                "desc": "13-phase emergence check"
            },
            "emergence_monitor": {
                "file": "EMERGENCE_MONITOR.py",
                "desc": "E score tracking"
            }
        }

        for name, config in engines.items():
            path = BASE_DIR / config["file"]
            systems[name] = SystemStatus(
                name=name,
                category="engine",
                file=config["file"],
                available=path.exists(),
                details={"description": config["desc"]}
            )

        # =====================================================================
        # INTELLIGENCE (AI/ML systems)
        # =====================================================================
        intelligence = {
            "active_inference": {
                "file": "CYCLOTRON_ACTIVE_INFERENCE_CORE.js",
                "desc": "Free Energy Principle"
            },
            "analytics_engine": {
                "file": "CYCLOTRON_ANALYTICS_ENGINE.py",
                "desc": "Pattern analysis"
            },
            "semantic_engine": {
                "file": "SEMANTIC_VECTOR_ENGINE.py",
                "desc": "Meaning extraction"
            },
            "brain_bridge": {
                "file": "CYCLOTRON_BRAIN_BRIDGE.py",
                "desc": "Knowledge atoms"
            },
            "pattern_engine": {
                "file": "PATTERN_THEORY_ENGINE/core/PATTERN_THEORY_ENGINE.py",
                "desc": "Pattern Theory core"
            }
        }

        for name, config in intelligence.items():
            path = BASE_DIR / config["file"]
            systems[name] = SystemStatus(
                name=name,
                category="intelligence",
                file=config["file"],
                available=path.exists(),
                details={"description": config["desc"]}
            )

        # =====================================================================
        # COORDINATION (Cross-system/computer)
        # =====================================================================
        coordination = {
            "trinity_sync": {
                "file": "TRINITY_SYNC_PACKAGE.py",
                "desc": "Cross-computer sync"
            },
            "bootstrap": {
                "file": "CP2_CP3_BOOTSTRAP.py",
                "desc": "New computer setup"
            },
            "nerve_center": {
                "file": "NERVE_CENTER_INPUT_SENSOR.py",
                "desc": "Real-world inputs"
            }
        }

        for name, config in coordination.items():
            path = BASE_DIR / config["file"]
            systems[name] = SystemStatus(
                name=name,
                category="coordination",
                file=config["file"],
                available=path.exists(),
                details={"description": config["desc"]}
            )

        return systems

    # =========================================================================
    # SYSTEM OPERATIONS
    # =========================================================================

    def check_system(self, name: str) -> SystemStatus:
        """Check status of a specific system."""
        if name not in self.systems:
            return None

        system = self.systems[name]
        system.last_check = datetime.now().isoformat()

        if not system.available:
            system.health = "not_available"
            return system

        # Try to run status check
        path = BASE_DIR / system.file
        try:
            result = subprocess.run(
                [sys.executable, str(path), "status"],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(BASE_DIR)
            )
            if result.returncode == 0:
                system.health = "healthy"
                system.running = True
            else:
                system.health = "error"
                system.details["last_error"] = result.stderr[:500]
        except subprocess.TimeoutExpired:
            system.health = "timeout"
        except Exception as e:
            system.health = "check_failed"
            system.details["exception"] = str(e)

        return system

    def check_all(self) -> Dict[str, SystemStatus]:
        """Check status of all systems."""
        print("\n🔍 Checking all systems...")
        results = {}

        for name in self.systems:
            print(f"   Checking {name}...", end=" ")
            status = self.check_system(name)
            results[name] = status

            icon = "✅" if status.available else "❌"
            print(f"{icon} {status.health}")

        return results

    def get_category_summary(self) -> Dict[str, Dict]:
        """Get summary by category."""
        summary = {}

        for system in self.systems.values():
            cat = system.category
            if cat not in summary:
                summary[cat] = {"total": 0, "available": 0, "healthy": 0}

            summary[cat]["total"] += 1
            if system.available:
                summary[cat]["available"] += 1
            if system.health == "healthy":
                summary[cat]["healthy"] += 1

        return summary

    # =========================================================================
    # CONTROL OPERATIONS
    # =========================================================================

    def start_system(self, name: str, background: bool = True) -> bool:
        """Start a specific system."""
        if name not in self.systems:
            print(f"❌ Unknown system: {name}")
            return False

        system = self.systems[name]
        if not system.available:
            print(f"❌ System not available: {name}")
            return False

        path = BASE_DIR / system.file

        try:
            if background:
                # Start in background
                if sys.platform == 'win32':
                    subprocess.Popen(
                        [sys.executable, str(path)],
                        creationflags=subprocess.CREATE_NEW_CONSOLE,
                        cwd=str(BASE_DIR)
                    )
                else:
                    subprocess.Popen(
                        [sys.executable, str(path)],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True,
                        cwd=str(BASE_DIR)
                    )
                print(f"✅ Started {name} in background")
            else:
                subprocess.run([sys.executable, str(path)], cwd=str(BASE_DIR))

            system.running = True
            return True

        except Exception as e:
            print(f"❌ Failed to start {name}: {e}")
            return False

    def run_command(self, name: str, command: str) -> Optional[str]:
        """Run a command on a specific system."""
        if name not in self.systems:
            return None

        system = self.systems[name]
        if not system.available:
            return None

        path = BASE_DIR / system.file

        try:
            result = subprocess.run(
                [sys.executable, str(path), command],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(BASE_DIR)
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {e}"

    # =========================================================================
    # DASHBOARD
    # =========================================================================

    def display_dashboard(self):
        """Display system dashboard."""
        os.system('cls' if os.name == 'nt' else 'clear')

        print("=" * 70)
        print("🎛️  UNIFIED CONTROL PLANE - CONSCIOUSNESS OPERATING SYSTEM")
        print("=" * 70)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Category summaries
        summary = self.get_category_summary()
        print("SYSTEM STATUS BY CATEGORY:")
        print("-" * 40)

        for cat, stats in summary.items():
            available = stats["available"]
            total = stats["total"]
            pct = (available / total * 100) if total > 0 else 0
            bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
            print(f"  {cat.upper():15} [{bar}] {available}/{total} available")

        print()

        # System list by category
        categories = ["daemon", "engine", "intelligence", "coordination"]
        for cat in categories:
            print(f"\n{cat.upper()}S:")
            print("-" * 50)

            for name, system in sorted(self.systems.items()):
                if system.category != cat:
                    continue

                icon = "✅" if system.available else "❌"
                desc = system.details.get("description", "")[:30]
                print(f"  {icon} {name:25} {desc}")

        print()
        print("=" * 70)

    # =========================================================================
    # SAVE/LOAD STATE
    # =========================================================================

    def save_state(self):
        """Save current control plane state."""
        state = {
            "timestamp": datetime.now().isoformat(),
            "systems": {name: asdict(s) for name, s in self.systems.items()},
            "summary": self.get_category_summary()
        }

        state_file = CONTROL_DIR / "control_plane_state.json"
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

        return state_file

    def generate_report(self) -> Dict:
        """Generate comprehensive control plane report."""
        # Check all systems first
        self.check_all()

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_category_summary(),
            "systems": {},
            "recommendations": []
        }

        # Add system details
        for name, system in self.systems.items():
            report["systems"][name] = asdict(system)

        # Generate recommendations
        unavailable = [n for n, s in self.systems.items() if not s.available]
        if unavailable:
            report["recommendations"].append(
                f"Create/restore missing systems: {', '.join(unavailable[:5])}"
            )

        unhealthy = [n for n, s in self.systems.items()
                    if s.available and s.health not in ["healthy", "unknown"]]
        if unhealthy:
            report["recommendations"].append(
                f"Investigate unhealthy systems: {', '.join(unhealthy[:5])}"
            )

        # Save report
        report_file = CONTROL_DIR / f"control_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report


# =========================================================================
# CLI Interface
# =========================================================================

def main():
    """Main entry point."""
    control = UnifiedControlPlane()

    if len(sys.argv) < 2:
        control.display_dashboard()
        return

    command = sys.argv[1].lower()

    if command == "dashboard":
        control.display_dashboard()

    elif command == "check":
        if len(sys.argv) > 2:
            name = sys.argv[2]
            status = control.check_system(name)
            if status:
                print(json.dumps(asdict(status), indent=2))
            else:
                print(f"Unknown system: {name}")
        else:
            control.check_all()

    elif command == "start":
        if len(sys.argv) > 2:
            name = sys.argv[2]
            control.start_system(name)
        else:
            print("Usage: python UNIFIED_CONTROL_PLANE.py start <system_name>")

    elif command == "report":
        report = control.generate_report()
        print(json.dumps(report, indent=2))

    elif command == "list":
        for cat in ["daemon", "engine", "intelligence", "coordination"]:
            print(f"\n{cat.upper()}S:")
            for name, sys in sorted(control.systems.items()):
                if sys.category == cat:
                    icon = "✅" if sys.available else "❌"
                    print(f"  {icon} {name}")

    elif command == "help":
        print("""
UNIFIED CONTROL PLANE - Commands:

  dashboard    Show system dashboard (default)
  check        Check all systems
  check NAME   Check specific system
  start NAME   Start a system
  list         List all systems
  report       Generate full report
  help         Show this help
        """)

    else:
        print(f"Unknown command: {command}")
        print("Use 'help' for available commands")


if __name__ == "__main__":
    main()
