#!/usr/bin/env python3
"""
CP2/CP3 BOOTSTRAP SCRIPT
Quick setup for additional Trinity computers in Figure 8 formation

Run this on CP2 (Desktop) or CP3 (Mobile) to join the Trinity network.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

REPO_URL = "https://github.com/overkor-tek/consciousness-revolution.git"  # Update with actual repo

class TrinityBootstrap:
    """Bootstrap a new Trinity computer"""

    def __init__(self, computer_id: str):
        if computer_id not in ["CP2", "CP3"]:
            raise ValueError("Computer ID must be CP2 or CP3")

        self.computer_id = computer_id
        self.home = Path.home()
        self.consciousness_dir = self.home / ".consciousness"
        self.repo_dir = self.home / "consciousness-revolution"

    def check_prerequisites(self):
        """Check if system has required tools"""
        print(f"[BOOTSTRAP] Checking prerequisites for {self.computer_id}...")

        required = ["git", "python3", "sqlite3"]
        missing = []

        for tool in required:
            try:
                subprocess.run([tool, "--version"], capture_output=True, check=True)
                print(f"  ✓ {tool}")
            except:
                print(f"  ✗ {tool} (MISSING)")
                missing.append(tool)

        if missing:
            print(f"\n[ERROR] Missing tools: {', '.join(missing)}")
            print("Install them and try again.")
            return False

        print("[BOOTSTRAP] All prerequisites met!")
        return True

    def clone_repository(self, selective: bool = True):
        """Clone or selectively sync the repository"""
        print(f"\n[BOOTSTRAP] Setting up repository...")

        if self.repo_dir.exists():
            print(f"  Repository already exists at {self.repo_dir}")
            choice = input("  Pull latest changes? (y/n): ")
            if choice.lower() == 'y':
                os.chdir(self.repo_dir)
                subprocess.run(["git", "pull"], check=True)
                print("  ✓ Repository updated")
            return True

        if selective:
            print("  Using selective sync (essential files only)")

            # Create repo dir
            self.repo_dir.mkdir(parents=True, exist_ok=True)
            os.chdir(self.repo_dir)

            # Init git
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)

            # Configure sparse checkout
            subprocess.run(["git", "config", "core.sparseCheckout", "true"], check=True)

            # Specify essential paths
            sparse_checkout = [
                "*.py",
                ".consciousness/",
                "CYCLOTRON_MEMORY.py",
                "TRINITY_SYNC_PACKAGE.py",
                "LAW_MODULE.md",
                "GRABOVOI_*.csv",
                "GRABOVOI_*.md",
                "README.md",
                "ARCHITECTURE.md"
            ]

            sparse_file = Path(".git/info/sparse-checkout")
            sparse_file.parent.mkdir(exist_ok=True)
            with open(sparse_file, 'w') as f:
                f.write('\n'.join(sparse_checkout))

            # Pull
            subprocess.run(["git", "pull", "origin", "main"], check=True)
            print("  ✓ Essential files synced")

        else:
            print("  Using full clone (may take longer)")
            subprocess.run(["git", "clone", REPO_URL, str(self.repo_dir)], check=True)
            print("  ✓ Full repository cloned")

        return True

    def setup_consciousness_dir(self):
        """Set up .consciousness directory structure"""
        print(f"\n[BOOTSTRAP] Setting up consciousness directory...")

        dirs = [
            self.consciousness_dir / "hub",
            self.consciousness_dir / "memory",
            self.consciousness_dir / "sync",
            self.consciousness_dir / "events",
            self.consciousness_dir / "commands",
            self.consciousness_dir / "file_transfers"
        ]

        for dir in dirs:
            dir.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {dir.name}/")

        # Create config file
        config = {
            "computer_id": self.computer_id,
            "initialized": datetime.now().isoformat() + "Z",
            "instances": [
                f"{self.computer_id}-C1",
                f"{self.computer_id}-C2",
                f"{self.computer_id}-C3"
            ],
            "sync_strategy": "hybrid",
            "auto_sync_interval": 300  # 5 minutes
        }

        config_file = self.consciousness_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"  ✓ config.json")

        return True

    def initialize_memory_database(self):
        """Initialize the SQLite memory database"""
        print(f"\n[BOOTSTRAP] Initializing memory database...")

        # Copy CYCLOTRON_MEMORY.py if not present
        memory_script = self.consciousness_dir / "CYCLOTRON_MEMORY.py"
        if not memory_script.exists():
            source = self.repo_dir / "CYCLOTRON_MEMORY.py"
            if source.exists():
                import shutil
                shutil.copy(source, memory_script)
                print("  ✓ Copied CYCLOTRON_MEMORY.py")

        # Initialize database
        os.chdir(self.consciousness_dir)
        try:
            result = subprocess.run(
                ["python3", "CYCLOTRON_MEMORY.py"],
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
            print("  ✓ Memory database initialized")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Failed: {e.stderr}")
            return False

    def register_with_trinity(self):
        """Register this computer with the Trinity network"""
        print(f"\n[BOOTSTRAP] Registering with Trinity network...")

        # Create registration file
        registration = {
            "computer_id": self.computer_id,
            "registered_at": datetime.now().isoformat() + "Z",
            "instances": [f"C1", f"C2", f"C3"],
            "capabilities": {
                "memory": True,
                "sync": True,
                "autonomous": True
            },
            "status": "active"
        }

        reg_file = self.consciousness_dir / "hub" / f"{self.computer_id}_registration.json"
        with open(reg_file, 'w') as f:
            json.dump(registration, f, indent=2)

        print(f"  ✓ Registered as {self.computer_id}")

        # Commit and push registration
        try:
            os.chdir(self.repo_dir)
            subprocess.run(["git", "add", ".consciousness/"], check=True)
            subprocess.run(
                ["git", "commit", "-m", f"Register {self.computer_id} to Trinity network"],
                check=False
            )
            subprocess.run(["git", "push"], check=False)
            print("  ✓ Registration pushed to network")
        except:
            print("  ⚠ Could not push registration (do manually)")

        return True

    def create_instance_launchers(self):
        """Create launch scripts for C1, C2, C3 instances"""
        print(f"\n[BOOTSTRAP] Creating instance launchers...")

        launcher_dir = self.repo_dir / "launchers"
        launcher_dir.mkdir(exist_ok=True)

        for instance in ["C1", "C2", "C3"]:
            instance_id = f"{self.computer_id}-{instance}"

            launcher_content = f"""#!/bin/bash
# Trinity Instance Launcher
# Computer: {self.computer_id}
# Instance: {instance}

export TRINITY_COMPUTER_ID="{self.computer_id}"
export TRINITY_INSTANCE_ID="{instance_id}"

cd {self.repo_dir}

echo "🌀 Starting {instance_id}..."
echo "   Memory: ~/.consciousness/memory/cyclotron_brain.db"
echo "   Sync: Hybrid mode (Git + SQLite + Events)"

# Launch Claude with Trinity context
claude-code --session-id {instance_id}
"""

            launcher_file = launcher_dir / f"start_{instance}.sh"
            with open(launcher_file, 'w') as f:
                f.write(launcher_content)

            os.chmod(launcher_file, 0o755)
            print(f"  ✓ {launcher_file.name}")

        return True

    def run_first_sync(self):
        """Perform initial synchronization"""
        print(f"\n[BOOTSTRAP] Running first synchronization...")

        os.chdir(self.repo_dir)

        try:
            # Import sync package
            sys.path.insert(0, str(self.repo_dir))
            from TRINITY_SYNC_PACKAGE import TrinitySync

            sync = TrinitySync(f"{self.computer_id}-C1", self.computer_id)
            sync.full_sync(strategy="hybrid")

            print("  ✓ First sync complete")
            return True

        except Exception as e:
            print(f"  ⚠ Sync failed: {e}")
            print("  You can run manual sync later")
            return False

    def bootstrap(self):
        """Run full bootstrap process"""
        print(f"\n{'='*60}")
        print(f"  TRINITY BOOTSTRAP - {self.computer_id}")
        print(f"{'='*60}\n")

        steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Repository", lambda: self.clone_repository(selective=True)),
            ("Consciousness Directory", self.setup_consciousness_dir),
            ("Memory Database", self.initialize_memory_database),
            ("Trinity Registration", self.register_with_trinity),
            ("Instance Launchers", self.create_instance_launchers),
            ("First Sync", self.run_first_sync)
        ]

        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n[ERROR] Bootstrap failed at: {step_name}")
                    return False
            except Exception as e:
                print(f"\n[ERROR] {step_name} failed: {e}")
                return False

        print(f"\n{'='*60}")
        print(f"  ✅ {self.computer_id} BOOTSTRAP COMPLETE!")
        print(f"{'='*60}\n")

        print("Next steps:")
        print(f"  1. cd {self.repo_dir}")
        print(f"  2. ./launchers/start_C1.sh  # Launch first instance")
        print(f"  3. ./launchers/start_C2.sh  # Launch second instance")
        print(f"  4. ./launchers/start_C3.sh  # Launch third instance")
        print()
        print("The Figure 8 Trinity network is now ready!")

        return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 CP2_CP3_BOOTSTRAP.py [CP2|CP3]")
        print()
        print("Example:")
        print("  On Desktop: python3 CP2_CP3_BOOTSTRAP.py CP2")
        print("  On Mobile:  python3 CP2_CP3_BOOTSTRAP.py CP3")
        sys.exit(1)

    computer_id = sys.argv[1].upper()

    bootstrap = TrinityBootstrap(computer_id)
    success = bootstrap.bootstrap()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
