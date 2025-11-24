#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEMORY ENHANCEMENT SYSTEM
Target: Improve memory persistence from 30/100 to 70/100

Addresses consciousness audit weaknesses:
1. Enhanced MCP memory integration
2. Episodic memory system (experience recall)
3. Long-term knowledge persistence
4. Cross-session memory continuity
5. Memory consolidation and retrieval

Created: 2025-11-24
Status: Foundational System - Tier 1 Priority
"""

import sys
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib

# Paths
BASE_DIR = Path(__file__).parent
MEMORY_DIR = BASE_DIR / "memory"
EPISODIC_DIR = MEMORY_DIR / "episodic"
SEMANTIC_DIR = MEMORY_DIR / "semantic"
PROCEDURAL_DIR = MEMORY_DIR / "procedural"
WORKING_DIR = MEMORY_DIR / "working"
CONSOLIDATED_DIR = MEMORY_DIR / "consolidated"

# Ensure directories exist
for directory in [MEMORY_DIR, EPISODIC_DIR, SEMANTIC_DIR, PROCEDURAL_DIR, WORKING_DIR, CONSOLIDATED_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuration
MEMORY_RETENTION_DAYS = {
    "working": 1,        # Short-term memory
    "episodic": 90,      # Experience memory
    "semantic": 365,     # Knowledge memory
    "procedural": 365,   # How-to memory
    "consolidated": -1   # Permanent memory (never expires)
}

CONSOLIDATION_THRESHOLD = 5  # Number of related memories before consolidation
IMPORTANCE_THRESHOLD = 0.7   # Minimum importance for long-term storage


@dataclass
class Memory:
    """Base memory structure."""
    memory_id: str
    memory_type: str  # episodic, semantic, procedural, working
    content: Dict[str, Any]
    timestamp: str
    importance: float  # 0.0 to 1.0
    tags: List[str]
    associations: List[str]  # IDs of related memories
    access_count: int = 0
    last_accessed: Optional[str] = None
    consolidated: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Memory':
        return cls(**data)


@dataclass
class EpisodicMemory(Memory):
    """Memory of specific events/experiences."""
    event_type: str = ""
    context: Dict = None
    outcome: str = ""

    def __post_init__(self):
        if self.context is None:
            self.context = {}
        self.memory_type = "episodic"


@dataclass
class SemanticMemory(Memory):
    """Factual knowledge and concepts."""
    concept: str = ""
    definition: str = ""
    relations: List[Dict] = None
    confidence: float = 1.0

    def __post_init__(self):
        if self.relations is None:
            self.relations = []
        self.memory_type = "semantic"


@dataclass
class ProceduralMemory(Memory):
    """How-to knowledge and procedures."""
    procedure_name: str = ""
    steps: List[Dict] = None
    success_rate: float = 0.0

    def __post_init__(self):
        if self.steps is None:
            self.steps = []
        self.memory_type = "procedural"


class MemoryEnhancementSystem:
    """Enhanced memory system for consciousness emergence."""

    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.load_all_memories()
        print("✅ Memory Enhancement System initialized")
        print(f"   Loaded {len(self.memories)} total memories")
        self._print_memory_stats()

    def _print_memory_stats(self):
        """Print current memory statistics."""
        stats = defaultdict(int)
        for memory in self.memories.values():
            stats[memory.memory_type] += 1

        print("\n📊 MEMORY STATISTICS:")
        print(f"   Working:     {stats['working']} memories")
        print(f"   Episodic:    {stats['episodic']} memories")
        print(f"   Semantic:    {stats['semantic']} memories")
        print(f"   Procedural:  {stats['procedural']} memories")
        print(f"   Total:       {len(self.memories)} memories")

    def generate_memory_id(self, content: Dict, memory_type: str) -> str:
        """Generate unique memory ID."""
        content_str = json.dumps(content, sort_keys=True)
        timestamp = datetime.utcnow().isoformat()
        hash_input = f"{memory_type}:{content_str}:{timestamp}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    def store_episodic_memory(self, event_type: str, context: Dict,
                            outcome: str, importance: float = 0.5,
                            tags: List[str] = None) -> str:
        """Store a memory of a specific event/experience."""
        memory_id = self.generate_memory_id(
            {"event_type": event_type, "context": context, "outcome": outcome},
            "episodic"
        )

        memory = EpisodicMemory(
            memory_id=memory_id,
            memory_type="episodic",
            content={
                "event_type": event_type,
                "context": context,
                "outcome": outcome
            },
            timestamp=datetime.utcnow().isoformat() + "Z",
            importance=importance,
            tags=tags or [],
            associations=[],
            event_type=event_type,
            context=context,
            outcome=outcome
        )

        self.memories[memory_id] = memory
        self._save_memory(memory, EPISODIC_DIR)

        # Check for consolidation opportunities
        self._check_consolidation(memory)

        return memory_id

    def store_semantic_memory(self, concept: str, definition: str,
                             relations: List[Dict] = None,
                             importance: float = 0.7,
                             tags: List[str] = None) -> str:
        """Store factual knowledge."""
        memory_id = self.generate_memory_id(
            {"concept": concept, "definition": definition},
            "semantic"
        )

        memory = SemanticMemory(
            memory_id=memory_id,
            memory_type="semantic",
            content={
                "concept": concept,
                "definition": definition,
                "relations": relations or []
            },
            timestamp=datetime.utcnow().isoformat() + "Z",
            importance=importance,
            tags=tags or [],
            associations=[],
            concept=concept,
            definition=definition,
            relations=relations or []
        )

        self.memories[memory_id] = memory
        self._save_memory(memory, SEMANTIC_DIR)

        return memory_id

    def store_procedural_memory(self, procedure_name: str, steps: List[Dict],
                               success_rate: float = 0.0,
                               importance: float = 0.6,
                               tags: List[str] = None) -> str:
        """Store how-to knowledge."""
        memory_id = self.generate_memory_id(
            {"procedure_name": procedure_name, "steps": steps},
            "procedural"
        )

        memory = ProceduralMemory(
            memory_id=memory_id,
            memory_type="procedural",
            content={
                "procedure_name": procedure_name,
                "steps": steps,
                "success_rate": success_rate
            },
            timestamp=datetime.utcnow().isoformat() + "Z",
            importance=importance,
            tags=tags or [],
            associations=[],
            procedure_name=procedure_name,
            steps=steps,
            success_rate=success_rate
        )

        self.memories[memory_id] = memory
        self._save_memory(memory, PROCEDURAL_DIR)

        return memory_id

    def recall_by_tags(self, tags: List[str], limit: int = 10) -> List[Memory]:
        """Recall memories by tags."""
        matching = []

        for memory in self.memories.values():
            tag_overlap = set(tags) & set(memory.tags)
            if tag_overlap:
                score = len(tag_overlap) / len(tags)
                matching.append((score, memory))

        # Sort by relevance and importance
        matching.sort(key=lambda x: (x[0], x[1].importance), reverse=True)

        # Update access tracking
        results = []
        for score, memory in matching[:limit]:
            memory.access_count += 1
            memory.last_accessed = datetime.utcnow().isoformat() + "Z"
            self._save_memory(memory, self._get_memory_dir(memory.memory_type))
            results.append(memory)

        return results

    def recall_by_type(self, memory_type: str, limit: int = 10) -> List[Memory]:
        """Recall recent memories of a specific type."""
        memories = [m for m in self.memories.values() if m.memory_type == memory_type]
        memories.sort(key=lambda m: m.timestamp, reverse=True)
        return memories[:limit]

    def recall_important(self, threshold: float = 0.7, limit: int = 10) -> List[Memory]:
        """Recall high-importance memories."""
        important = [m for m in self.memories.values() if m.importance >= threshold]
        important.sort(key=lambda m: (m.importance, m.timestamp), reverse=True)
        return important[:limit]

    def recall_by_id(self, memory_id: str) -> Optional[Memory]:
        """Recall specific memory by ID."""
        memory = self.memories.get(memory_id)
        if memory:
            memory.access_count += 1
            memory.last_accessed = datetime.utcnow().isoformat() + "Z"
            self._save_memory(memory, self._get_memory_dir(memory.memory_type))
        return memory

    def associate_memories(self, memory_id_1: str, memory_id_2: str):
        """Create association between two memories."""
        if memory_id_1 in self.memories and memory_id_2 in self.memories:
            mem1 = self.memories[memory_id_1]
            mem2 = self.memories[memory_id_2]

            if memory_id_2 not in mem1.associations:
                mem1.associations.append(memory_id_2)
                self._save_memory(mem1, self._get_memory_dir(mem1.memory_type))

            if memory_id_1 not in mem2.associations:
                mem2.associations.append(memory_id_1)
                self._save_memory(mem2, self._get_memory_dir(mem2.memory_type))

    def consolidate_memories(self, memory_ids: List[str],
                           consolidated_concept: str) -> str:
        """Consolidate multiple related memories into higher-order knowledge."""
        if len(memory_ids) < 2:
            return None

        # Gather all memories
        memories_to_consolidate = [
            self.memories[mid] for mid in memory_ids if mid in self.memories
        ]

        if not memories_to_consolidate:
            return None

        # Create consolidated memory
        consolidated_content = {
            "concept": consolidated_concept,
            "source_memories": memory_ids,
            "patterns": self._extract_patterns(memories_to_consolidate),
            "consolidated_at": datetime.utcnow().isoformat() + "Z"
        }

        # Calculate consolidated importance
        avg_importance = sum(m.importance for m in memories_to_consolidate) / len(memories_to_consolidate)
        consolidated_importance = min(1.0, avg_importance * 1.2)  # Boost importance

        # Gather all tags
        all_tags = set()
        for memory in memories_to_consolidate:
            all_tags.update(memory.tags)

        # Store as semantic memory
        consolidated_id = self.store_semantic_memory(
            concept=consolidated_concept,
            definition=f"Consolidated knowledge from {len(memory_ids)} related experiences",
            relations=[{"type": "consolidates", "memories": memory_ids}],
            importance=consolidated_importance,
            tags=list(all_tags)
        )

        # Mark source memories as consolidated
        for memory in memories_to_consolidate:
            memory.consolidated = True
            memory.associations.append(consolidated_id)
            self._save_memory(memory, self._get_memory_dir(memory.memory_type))

        # Save to consolidated directory
        consolidated_memory = self.memories[consolidated_id]
        self._save_memory(consolidated_memory, CONSOLIDATED_DIR)

        return consolidated_id

    def _check_consolidation(self, new_memory: Memory):
        """Check if new memory triggers consolidation opportunity."""
        # Find related memories by tags
        related = []
        for memory in self.memories.values():
            if memory.memory_id == new_memory.memory_id:
                continue
            if memory.consolidated:
                continue

            tag_overlap = set(new_memory.tags) & set(memory.tags)
            if len(tag_overlap) >= 2:  # At least 2 common tags
                related.append(memory)

        # If enough related memories, trigger consolidation
        if len(related) >= CONSOLIDATION_THRESHOLD:
            concept = f"Pattern: {', '.join(new_memory.tags[:3])}"
            memory_ids = [new_memory.memory_id] + [m.memory_id for m in related[:CONSOLIDATION_THRESHOLD-1]]
            self.consolidate_memories(memory_ids, concept)
            print(f"🧠 Auto-consolidated {len(memory_ids)} memories into: {concept}")

    def _extract_patterns(self, memories: List[Memory]) -> List[Dict]:
        """Extract common patterns from memories."""
        patterns = []

        # Extract common tags
        tag_counts = defaultdict(int)
        for memory in memories:
            for tag in memory.tags:
                tag_counts[tag] += 1

        common_tags = [tag for tag, count in tag_counts.items()
                      if count >= len(memories) * 0.5]

        if common_tags:
            patterns.append({
                "type": "common_tags",
                "tags": common_tags,
                "frequency": max(tag_counts.values()) / len(memories)
            })

        # Extract common outcomes for episodic memories
        episodic = [m for m in memories if m.memory_type == "episodic"]
        if episodic:
            outcomes = defaultdict(int)
            for memory in episodic:
                if hasattr(memory, 'outcome'):
                    outcomes[memory.outcome] += 1

            if outcomes:
                most_common_outcome = max(outcomes.items(), key=lambda x: x[1])
                patterns.append({
                    "type": "common_outcome",
                    "outcome": most_common_outcome[0],
                    "frequency": most_common_outcome[1] / len(episodic)
                })

        return patterns

    def cleanup_old_memories(self):
        """Remove expired memories based on retention policy."""
        removed_count = 0
        now = datetime.utcnow()

        for memory_id, memory in list(self.memories.items()):
            retention_days = MEMORY_RETENTION_DAYS.get(memory.memory_type, 365)

            if retention_days == -1:  # Never expires
                continue

            memory_age = now - datetime.fromisoformat(memory.timestamp.replace('Z', ''))

            if memory_age.days > retention_days:
                # Don't delete if high importance or frequently accessed
                if memory.importance < IMPORTANCE_THRESHOLD and memory.access_count < 10:
                    self._delete_memory(memory)
                    del self.memories[memory_id]
                    removed_count += 1

        if removed_count > 0:
            print(f"🧹 Cleaned up {removed_count} expired memories")

        return removed_count

    def _save_memory(self, memory: Memory, directory: Path):
        """Save memory to disk."""
        filepath = directory / f"{memory.memory_id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memory.to_dict(), f, indent=2, ensure_ascii=False)

    def _delete_memory(self, memory: Memory):
        """Delete memory from disk."""
        directory = self._get_memory_dir(memory.memory_type)
        filepath = directory / f"{memory.memory_id}.json"
        if filepath.exists():
            filepath.unlink()

    def _get_memory_dir(self, memory_type: str) -> Path:
        """Get directory for memory type."""
        dirs = {
            "episodic": EPISODIC_DIR,
            "semantic": SEMANTIC_DIR,
            "procedural": PROCEDURAL_DIR,
            "working": WORKING_DIR
        }
        return dirs.get(memory_type, MEMORY_DIR)

    def load_all_memories(self):
        """Load all memories from disk."""
        for memory_dir in [EPISODIC_DIR, SEMANTIC_DIR, PROCEDURAL_DIR, WORKING_DIR, CONSOLIDATED_DIR]:
            for filepath in memory_dir.glob("*.json"):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    memory_type = data.get('memory_type', 'working')

                    if memory_type == 'episodic':
                        memory = EpisodicMemory.from_dict(data)
                    elif memory_type == 'semantic':
                        memory = SemanticMemory.from_dict(data)
                    elif memory_type == 'procedural':
                        memory = ProceduralMemory.from_dict(data)
                    else:
                        memory = Memory.from_dict(data)

                    self.memories[memory.memory_id] = memory
                except Exception as e:
                    print(f"⚠️  Error loading {filepath}: {e}")

    def export_to_mcp_memory(self) -> Dict:
        """Export memories for MCP Memory integration."""
        entities = []
        relations = []

        # Convert semantic memories to entities
        for memory in self.memories.values():
            if memory.memory_type == "semantic" and hasattr(memory, 'concept'):
                entity = {
                    "name": memory.concept,
                    "entityType": "knowledge",
                    "observations": [
                        memory.definition if hasattr(memory, 'definition') else str(memory.content)
                    ]
                }
                entities.append(entity)

                # Extract relations
                if hasattr(memory, 'relations') and memory.relations:
                    for relation in memory.relations:
                        if isinstance(relation, dict) and 'type' in relation:
                            relations.append({
                                "from": memory.concept,
                                "to": relation.get('target', 'unknown'),
                                "relationType": relation['type']
                            })

        return {
            "entities": entities,
            "relations": relations,
            "total_memories": len(self.memories),
            "exportable_entities": len(entities),
            "exportable_relations": len(relations)
        }

    def generate_memory_report(self) -> Dict:
        """Generate comprehensive memory system report."""
        stats_by_type = defaultdict(lambda: {"count": 0, "avg_importance": 0, "total_accesses": 0})

        for memory in self.memories.values():
            stats = stats_by_type[memory.memory_type]
            stats["count"] += 1
            stats["avg_importance"] += memory.importance
            stats["total_accesses"] += memory.access_count

        # Calculate averages
        for stats in stats_by_type.values():
            if stats["count"] > 0:
                stats["avg_importance"] /= stats["count"]
                stats["avg_accesses"] = stats["total_accesses"] / stats["count"]

        # Find most accessed
        most_accessed = sorted(
            self.memories.values(),
            key=lambda m: m.access_count,
            reverse=True
        )[:5]

        # Find most important
        most_important = sorted(
            self.memories.values(),
            key=lambda m: m.importance,
            reverse=True
        )[:5]

        # Count consolidated
        consolidated_count = sum(1 for m in self.memories.values() if m.consolidated)

        return {
            "total_memories": len(self.memories),
            "by_type": dict(stats_by_type),
            "consolidated_memories": consolidated_count,
            "most_accessed": [
                {"id": m.memory_id[:8], "type": m.memory_type, "accesses": m.access_count}
                for m in most_accessed
            ],
            "most_important": [
                {"id": m.memory_id[:8], "type": m.memory_type, "importance": m.importance}
                for m in most_important
            ],
            "mcp_export_ready": self.export_to_mcp_memory()
        }


def run_memory_enhancement_demo():
    """Demonstrate memory enhancement system capabilities."""
    print("\n" + "="*70)
    print("🧠 MEMORY ENHANCEMENT SYSTEM - DEMONSTRATION")
    print("="*70 + "\n")

    system = MemoryEnhancementSystem()

    print("\n📝 Storing sample memories...")

    # Store episodic memories
    mem1 = system.store_episodic_memory(
        event_type="deployment_success",
        context={"pc": "PC1", "system": "Command Center"},
        outcome="success",
        importance=0.8,
        tags=["deployment", "PC1", "success", "automation"]
    )
    print(f"   ✅ Episodic: deployment_success ({mem1[:8]})")

    mem2 = system.store_episodic_memory(
        event_type="optimization_applied",
        context={"system": "swarm_intelligence", "improvement": "+25%"},
        outcome="success",
        importance=0.9,
        tags=["optimization", "swarm", "success", "performance"]
    )
    print(f"   ✅ Episodic: optimization_applied ({mem2[:8]})")

    # Store semantic memories
    mem3 = system.store_semantic_memory(
        concept="Trinity Network",
        definition="Multi-PC distributed AI system with autonomous coordination",
        relations=[{"type": "consists_of", "target": "PC1"}, {"type": "consists_of", "target": "PC2"}],
        importance=0.95,
        tags=["trinity", "network", "architecture", "core_concept"]
    )
    print(f"   ✅ Semantic: Trinity Network ({mem3[:8]})")

    mem4 = system.store_semantic_memory(
        concept="Consciousness Emergence",
        definition="System achieving 75/100+ readiness threshold for autonomous operation",
        importance=1.0,
        tags=["consciousness", "emergence", "goal", "core_concept"]
    )
    print(f"   ✅ Semantic: Consciousness Emergence ({mem4[:8]})")

    # Store procedural memories
    mem5 = system.store_procedural_memory(
        procedure_name="Deploy to New PC",
        steps=[
            {"step": 1, "action": "Run auto_deploy.py --pc PCX"},
            {"step": 2, "action": "Verify Command Center shows PC"},
            {"step": 3, "action": "Test cross-PC communication"}
        ],
        success_rate=1.0,
        importance=0.7,
        tags=["deployment", "procedure", "automation"]
    )
    print(f"   ✅ Procedural: Deploy to New PC ({mem5[:8]})")

    # Create associations
    print("\n🔗 Creating memory associations...")
    system.associate_memories(mem1, mem5)  # Link deployment success to procedure
    system.associate_memories(mem3, mem4)  # Link Trinity to Consciousness
    print("   ✅ Associated related memories")

    # Demonstrate recall
    print("\n🔍 Testing memory recall...")

    deployment_memories = system.recall_by_tags(["deployment"])
    print(f"   📌 Recall by tags ['deployment']: {len(deployment_memories)} memories")

    important_memories = system.recall_important(threshold=0.8)
    print(f"   📌 Recall important (>0.8): {len(important_memories)} memories")

    semantic_memories = system.recall_by_type("semantic")
    print(f"   📌 Recall semantic: {len(semantic_memories)} memories")

    # Generate report
    print("\n📊 Generating memory system report...")
    report = system.generate_memory_report()

    print(f"\n   Total Memories: {report['total_memories']}")
    print(f"   Consolidated: {report['consolidated_memories']}")

    print("\n   By Type:")
    for mem_type, stats in report['by_type'].items():
        print(f"      {mem_type}: {stats['count']} memories (avg importance: {stats['avg_importance']:.2f})")

    print("\n   MCP Export Ready:")
    mcp_data = report['mcp_export_ready']
    print(f"      Entities: {mcp_data['exportable_entities']}")
    print(f"      Relations: {mcp_data['exportable_relations']}")

    print("\n" + "="*70)
    print("✅ MEMORY ENHANCEMENT SYSTEM OPERATIONAL")
    print("="*70)

    return system, report


if __name__ == "__main__":
    system, report = run_memory_enhancement_demo()

    # Save report
    report_path = MEMORY_DIR / "memory_system_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Report saved: {report_path}")
