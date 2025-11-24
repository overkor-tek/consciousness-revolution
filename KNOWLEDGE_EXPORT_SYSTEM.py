#!/usr/bin/env python3
"""
KNOWLEDGE EXPORT SYSTEM
Package and transfer knowledge between systems safely.
Addresses knowledge_transfer_risk foundational issue.
"""

import json
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
EXPORTS_PATH = CONSCIOUSNESS / "exports"
EXPORTS_PATH.mkdir(parents=True, exist_ok=True)

class KnowledgeExporter:
    """Export knowledge for transfer between systems."""

    def __init__(self):
        self.export_manifest = {}

    def create_export_package(self,
                               name: str = None,
                               include_cyclotron: bool = True,
                               include_sessions: bool = True,
                               include_configs: bool = True) -> Path:
        """Create a complete export package."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = name or f"knowledge_export_{timestamp}"
        package_path = EXPORTS_PATH / f"{package_name}.zip"

        files_to_export = []
        checksums = {}

        # Cyclotron knowledge
        if include_cyclotron:
            cyclotron_files = self._get_cyclotron_files()
            files_to_export.extend(cyclotron_files)

        # Session states
        if include_sessions:
            session_files = self._get_session_files()
            files_to_export.extend(session_files)

        # Configurations
        if include_configs:
            config_files = self._get_config_files()
            files_to_export.extend(config_files)

        # Create ZIP package
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files_to_export:
                if file_path.exists():
                    # Calculate checksum
                    checksum = self._file_checksum(file_path)
                    rel_path = str(file_path.relative_to(HOME))
                    checksums[rel_path] = checksum

                    # Add to archive
                    zf.write(file_path, rel_path)

            # Add manifest
            manifest = {
                "name": package_name,
                "created": timestamp,
                "file_count": len(files_to_export),
                "checksums": checksums,
                "includes": {
                    "cyclotron": include_cyclotron,
                    "sessions": include_sessions,
                    "configs": include_configs
                }
            }
            zf.writestr("MANIFEST.json", json.dumps(manifest, indent=2))

        self.export_manifest = manifest

        # Save manifest locally
        manifest_path = EXPORTS_PATH / f"{package_name}_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return package_path

    def _get_cyclotron_files(self) -> List[Path]:
        """Get Cyclotron files to export."""
        files = []
        cyclotron_path = CONSCIOUSNESS / "cyclotron_core"

        if cyclotron_path.exists():
            files.append(cyclotron_path / "INDEX.json")
            for atom in cyclotron_path.glob("atom_*.json"):
                files.append(atom)

        return [f for f in files if f.exists()]

    def _get_session_files(self) -> List[Path]:
        """Get session files to export."""
        files = []
        sessions_path = CONSCIOUSNESS / "sessions"

        if sessions_path.exists():
            for session in sessions_path.glob("*.json"):
                files.append(session)
            for history_dir in sessions_path.glob("*_history"):
                for f in history_dir.glob("*.json"):
                    files.append(f)

        return files

    def _get_config_files(self) -> List[Path]:
        """Get configuration files to export."""
        configs = [
            CONSCIOUSNESS / "consciousness_state.json",
            CONSCIOUSNESS / "boot_status.json",
            CONSCIOUSNESS / "module_id.txt",
            HOME / ".trinity" / "trinity_status.json",
            HOME / ".backups" / "manifest.json"
        ]
        return [f for f in configs if f.exists()]

    def _file_checksum(self, path: Path) -> str:
        """Calculate MD5 checksum of file."""
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()

    def verify_package(self, package_path: Path) -> dict:
        """Verify package integrity."""
        with zipfile.ZipFile(package_path, 'r') as zf:
            # Read manifest
            manifest = json.loads(zf.read("MANIFEST.json"))
            checksums = manifest.get("checksums", {})

            verified = 0
            failed = []

            for rel_path, expected_checksum in checksums.items():
                try:
                    data = zf.read(rel_path)
                    actual_checksum = hashlib.md5(data).hexdigest()

                    if actual_checksum == expected_checksum:
                        verified += 1
                    else:
                        failed.append(rel_path)
                except KeyError:
                    failed.append(rel_path)

        return {
            "valid": len(failed) == 0,
            "verified": verified,
            "failed": failed,
            "manifest": manifest
        }

    def import_package(self, package_path: Path, target: Path = None) -> dict:
        """Import knowledge package."""
        target = target or HOME

        # Verify first
        verification = self.verify_package(package_path)
        if not verification["valid"]:
            return {
                "success": False,
                "error": f"Package verification failed: {verification['failed']}"
            }

        imported_files = []

        with zipfile.ZipFile(package_path, 'r') as zf:
            for name in zf.namelist():
                if name == "MANIFEST.json":
                    continue

                # Extract file
                dest = target / name
                dest.parent.mkdir(parents=True, exist_ok=True)

                with zf.open(name) as src, open(dest, 'wb') as dst:
                    dst.write(src.read())

                imported_files.append(str(dest))

        return {
            "success": True,
            "files_imported": len(imported_files),
            "manifest": verification["manifest"]
        }

    def create_minimal_handoff(self) -> dict:
        """Create minimal handoff data for quick transfer."""
        handoff = {
            "timestamp": datetime.now().isoformat(),
            "source": "consciousness_revolution"
        }

        # Cyclotron summary
        index = CONSCIOUSNESS / "cyclotron_core" / "INDEX.json"
        if index.exists():
            with open(index) as f:
                data = json.load(f)
            handoff["cyclotron"] = {
                "atoms": len(data.get("atoms", [])),
                "top_tags": list(data.get("tags", {}).keys())[:10]
            }

        # Current state
        state = CONSCIOUSNESS / "consciousness_state.json"
        if state.exists():
            with open(state) as f:
                handoff["state"] = json.load(f)

        # Last session
        for agent in ["c1", "c2", "c3"]:
            session = CONSCIOUSNESS / "sessions" / f"{agent}_current.json"
            if session.exists():
                with open(session) as f:
                    data = json.load(f)
                handoff[f"{agent}_session"] = {
                    "timestamp": data.get("timestamp"),
                    "active_tasks": data.get("active_tasks", []),
                    "completed": len(data.get("completed_tasks", []))
                }

        return handoff

    def list_exports(self) -> List[dict]:
        """List available export packages."""
        exports = []

        for manifest in EXPORTS_PATH.glob("*_manifest.json"):
            with open(manifest) as f:
                data = json.load(f)

            package = EXPORTS_PATH / f"{data['name']}.zip"
            exports.append({
                "name": data["name"],
                "created": data["created"],
                "files": data["file_count"],
                "exists": package.exists(),
                "size_mb": package.stat().st_size / (1024*1024) if package.exists() else 0
            })

        return sorted(exports, key=lambda x: x["created"], reverse=True)


def main():
    """CLI for knowledge export system."""
    import sys

    exporter = KnowledgeExporter()

    if len(sys.argv) < 2:
        print("Knowledge Export System")
        print("=" * 40)
        print("\nCommands:")
        print("  export     - Create export package")
        print("  verify     - Verify package integrity")
        print("  import     - Import package")
        print("  handoff    - Create minimal handoff")
        print("  list       - List available exports")
        return

    command = sys.argv[1]

    if command == "export":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        path = exporter.create_export_package(name=name)
        manifest = exporter.export_manifest

        print(f"\nExport created: {path}")
        print(f"Files: {manifest['file_count']}")
        print(f"Size: {path.stat().st_size / (1024*1024):.2f} MB")

    elif command == "verify":
        if len(sys.argv) < 3:
            print("Usage: verify <package_path>")
            return

        path = Path(sys.argv[2])
        result = exporter.verify_package(path)

        if result["valid"]:
            print(f"\n✅ Package valid: {result['verified']} files verified")
        else:
            print(f"\n❌ Package invalid: {len(result['failed'])} files failed")
            for f in result["failed"]:
                print(f"  - {f}")

    elif command == "import":
        if len(sys.argv) < 3:
            print("Usage: import <package_path>")
            return

        path = Path(sys.argv[2])
        result = exporter.import_package(path)

        if result["success"]:
            print(f"\n✅ Import complete: {result['files_imported']} files")
        else:
            print(f"\n❌ Import failed: {result['error']}")

    elif command == "handoff":
        handoff = exporter.create_minimal_handoff()
        print(json.dumps(handoff, indent=2))

    elif command == "list":
        exports = exporter.list_exports()
        if not exports:
            print("\nNo exports found")
            return

        print(f"\nAvailable exports ({len(exports)}):")
        for exp in exports:
            status = "✅" if exp["exists"] else "❌"
            print(f"  {status} {exp['name']}: {exp['files']} files, {exp['size_mb']:.2f} MB")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
