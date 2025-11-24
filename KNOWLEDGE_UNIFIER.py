#!/usr/bin/env python3
"""
KNOWLEDGE UNIFIER
Consolidates scattered knowledge into unified Cyclotron graph.
Resolves foundational issue: knowledge_fragmentation
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
from glob import glob

from CYCLOTRON_BRAIN_BRIDGE import CyclotronBridge, KnowledgeAtom

# Paths
HOME = Path.home()
CONSCIOUSNESS = HOME / ".consciousness"
PLANNING = HOME / ".planning"
DEPLOYMENT = HOME / "100X_DEPLOYMENT"
TRINITY = HOME / ".trinity"


class KnowledgeUnifier:
    """Unifies scattered knowledge sources into Cyclotron."""

    def __init__(self):
        self.cyclotron = CyclotronBridge()
        self.sources_scanned = 0
        self.atoms_created = 0
        self.duplicates_skipped = 0

    def scan_all_sources(self) -> dict:
        """Scan and ingest all knowledge sources."""
        print("=" * 60)
        print("KNOWLEDGE UNIFIER")
        print("=" * 60)

        results = {}

        # 1. Consciousness brain files
        print("\n1. Scanning .consciousness/brain...")
        results["brain"] = self._scan_brain_files()

        # 2. Planning/Traction files
        print("\n2. Scanning .planning/traction...")
        results["planning"] = self._scan_planning_files()

        # 3. Trinity messages
        print("\n3. Scanning .trinity messages...")
        results["trinity"] = self._scan_trinity_messages()

        # 4. Deployment docs
        print("\n4. Scanning deployment docs...")
        results["deployment"] = self._scan_deployment_docs()

        # 5. Session summaries
        print("\n5. Scanning session summaries...")
        results["sessions"] = self._scan_session_summaries()

        # 6. Build relationships
        print("\n6. Building relationships...")
        relationships = self._build_relationships()

        # Summary
        print("\n" + "=" * 60)
        print("UNIFICATION COMPLETE")
        print("=" * 60)
        print(f"Sources scanned: {self.sources_scanned}")
        print(f"Atoms created: {self.atoms_created}")
        print(f"Duplicates skipped: {self.duplicates_skipped}")
        print(f"Relationships created: {relationships}")

        status = self.cyclotron.get_status()
        print(f"\nCyclotron now has: {status['total_atoms']} atoms")

        return {
            "results": results,
            "atoms_created": self.atoms_created,
            "relationships": relationships,
            "total_atoms": status["total_atoms"]
        }

    def _scan_brain_files(self) -> dict:
        """Scan brain directory for knowledge."""
        brain_path = CONSCIOUSNESS / "brain"
        if not brain_path.exists():
            return {"scanned": 0}

        count = 0
        for json_file in brain_path.glob("*.json"):
            self.sources_scanned += 1

            try:
                with open(json_file) as f:
                    data = json.load(f)

                # Extract based on file type
                if "metrics" in data:
                    for metric in data["metrics"]:
                        self._create_atom_if_new(
                            f"Metric: {metric.get('name')} = {metric.get('actual')} (goal: {metric.get('goal')})",
                            "fact",
                            "brain_metrics",
                            ["metric", "scorecard"]
                        )
                        count += 1

                elif "rocks" in data:
                    for rock in data["rocks"]:
                        self._create_atom_if_new(
                            f"Rock: {rock.get('rock')} - Status: {rock.get('status')} - Owner: {rock.get('owner')}",
                            "action",
                            "brain_rocks",
                            ["rock", "quarterly"]
                        )
                        count += 1

                elif "issues" in data:
                    for issue in data["issues"]:
                        self._create_atom_if_new(
                            f"Issue: {issue.get('issue')} - Priority: {issue.get('priority')}",
                            "pattern",
                            "brain_issues",
                            ["issue", "problem"]
                        )
                        count += 1

            except (json.JSONDecodeError, KeyError):
                continue

        print(f"   Found {count} items")
        return {"scanned": count}

    def _scan_planning_files(self) -> dict:
        """Scan planning/traction files."""
        traction_path = PLANNING / "traction"
        if not traction_path.exists():
            return {"scanned": 0}

        count = 0
        for json_file in traction_path.glob("*.json"):
            self.sources_scanned += 1

            try:
                with open(json_file) as f:
                    data = json.load(f)

                # Vision/values
                if "core_values" in data:
                    for value in data.get("core_values", []):
                        self._create_atom_if_new(
                            f"Core Value: {value.get('value')} - {value.get('description', '')}",
                            "concept",
                            "traction_vision",
                            ["value", "vision", "culture"]
                        )
                        count += 1

                # Goals
                if "ten_year_target" in data:
                    self._create_atom_if_new(
                        f"10-Year Target: {data['ten_year_target']}",
                        "concept",
                        "traction_vision",
                        ["goal", "vision", "long-term"]
                    )
                    count += 1

            except (json.JSONDecodeError, KeyError):
                continue

        print(f"   Found {count} items")
        return {"scanned": count}

    def _scan_trinity_messages(self) -> dict:
        """Scan Trinity message files."""
        if not TRINITY.exists():
            return {"scanned": 0}

        count = 0

        # Scan various Trinity sources
        message_patterns = [
            TRINITY / "messages" / "*.json",
            TRINITY / "reports" / "*.md",
            TRINITY / "*.md"
        ]

        for pattern in message_patterns:
            for file_path in Path(pattern.parent).glob(pattern.name) if pattern.parent.exists() else []:
                self.sources_scanned += 1

                if file_path.suffix == ".json":
                    try:
                        with open(file_path) as f:
                            data = json.load(f)

                        if isinstance(data, dict) and "message" in data:
                            self._create_atom_if_new(
                                f"Trinity: {data['message'][:200]}",
                                "insight",
                                "trinity_message",
                                ["trinity", "communication"]
                            )
                            count += 1

                    except (json.JSONDecodeError, KeyError):
                        continue

                elif file_path.suffix == ".md":
                    # Extract title from markdown
                    content = file_path.read_text(errors='ignore')[:500]
                    lines = content.split('\n')
                    title = lines[0].replace('#', '').strip() if lines else file_path.stem

                    self._create_atom_if_new(
                        f"Trinity Doc: {title}",
                        "insight",
                        "trinity_doc",
                        ["trinity", "documentation"]
                    )
                    count += 1

        print(f"   Found {count} items")
        return {"scanned": count}

    def _scan_deployment_docs(self) -> dict:
        """Scan deployment for documentation."""
        count = 0

        # Scan markdown files
        for md_file in DEPLOYMENT.glob("*.md"):
            self.sources_scanned += 1

            # Skip very large files
            if md_file.stat().st_size > 50000:
                continue

            content = md_file.read_text(errors='ignore')[:1000]
            lines = content.split('\n')
            title = lines[0].replace('#', '').strip() if lines else md_file.stem

            # Determine type from filename
            name_lower = md_file.stem.lower()
            if "complete" in name_lower or "delivery" in name_lower:
                atom_type = "action"
                tags = ["delivery", "complete"]
            elif "architecture" in name_lower or "spec" in name_lower:
                atom_type = "concept"
                tags = ["architecture", "design"]
            elif "guide" in name_lower or "start" in name_lower:
                atom_type = "insight"
                tags = ["guide", "documentation"]
            else:
                atom_type = "insight"
                tags = ["documentation"]

            self._create_atom_if_new(
                f"Doc: {title}",
                atom_type,
                "deployment_doc",
                tags
            )
            count += 1

        print(f"   Found {count} items")
        return {"scanned": count}

    def _scan_session_summaries(self) -> dict:
        """Scan session summary files."""
        count = 0

        # Look for session files
        patterns = [
            CONSCIOUSNESS / "session_state.json",
            TRINITY / "*SESSION*.md",
            DEPLOYMENT / "*SESSION*.md"
        ]

        for pattern in patterns:
            if pattern.suffix:
                files = [pattern] if pattern.exists() else []
            else:
                files = list(pattern.parent.glob(pattern.name)) if pattern.parent.exists() else []

            for file_path in files:
                self.sources_scanned += 1

                if file_path.suffix == ".json":
                    try:
                        with open(file_path) as f:
                            data = json.load(f)

                        if "task" in data or "summary" in data:
                            summary = data.get("summary", data.get("task", "Unknown"))[:200]
                            self._create_atom_if_new(
                                f"Session: {summary}",
                                "action",
                                "session",
                                ["session", "work"]
                            )
                            count += 1

                    except (json.JSONDecodeError, KeyError):
                        continue

        print(f"   Found {count} items")
        return {"scanned": count}

    def _create_atom_if_new(self, content: str, atom_type: str, source: str, tags: List[str]) -> bool:
        """Create atom only if not duplicate."""
        # Check for existing similar atoms
        existing = self.cyclotron.search(content[:50])

        for atom in existing:
            if atom.content == content or content in atom.content:
                self.duplicates_skipped += 1
                return False

        # Create new atom
        self.cyclotron.create_atom(content, atom_type, source, tags)
        self.atoms_created += 1
        return True

    def _build_relationships(self) -> int:
        """Build relationships between related atoms."""
        relationships = 0

        # Get all atoms by type
        concepts = self.cyclotron.search_by_type("concept")
        actions = self.cyclotron.search_by_type("action")
        insights = self.cyclotron.search_by_type("insight")

        # Link concepts to related actions
        for concept in concepts:
            concept_words = set(concept.content.lower().split())

            for action in actions:
                action_words = set(action.content.lower().split())
                overlap = concept_words & action_words

                if len(overlap) >= 3 and concept.id not in action.links:
                    self.cyclotron.link_atoms(concept.id, action.id)
                    relationships += 1

        # Link insights to related concepts
        for insight in insights[:50]:  # Limit for performance
            insight_words = set(insight.content.lower().split())

            for concept in concepts:
                concept_words = set(concept.content.lower().split())
                overlap = insight_words & concept_words

                if len(overlap) >= 2 and insight.id not in concept.links:
                    self.cyclotron.link_atoms(insight.id, concept.id)
                    relationships += 1

        return relationships

    def get_unification_status(self) -> dict:
        """Get current unification status."""
        status = self.cyclotron.get_status()

        return {
            "total_atoms": status["total_atoms"],
            "types": status["types"],
            "sources": status["sources"],
            "top_tags": status["top_tags"][:10],
            "fragmentation_resolved": status["total_atoms"] > 50
        }


def main():
    """CLI for knowledge unifier."""
    import sys

    unifier = KnowledgeUnifier()

    if len(sys.argv) < 2:
        print("Knowledge Unifier")
        print("=" * 40)
        print("\nCommands:")
        print("  unify    - Scan and unify all sources")
        print("  status   - Show unification status")
        return

    command = sys.argv[1]

    if command == "unify":
        unifier.scan_all_sources()

    elif command == "status":
        status = unifier.get_unification_status()
        print(f"\nUnification Status:")
        print(f"  Total atoms: {status['total_atoms']}")
        print(f"  Types: {status['types']}")
        print(f"  Fragmentation resolved: {status['fragmentation_resolved']}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
