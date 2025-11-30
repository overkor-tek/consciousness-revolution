#!/usr/bin/env python3
"""
🧠 CYCLOTRON BRAIN AGENT 🧠
Transform passive knowledge index into active intelligence system

ARCHITECTURE:
- Layer 1: Atoms (raw knowledge particles)
- Layer 2: Bonds (relationships between atoms)
- Layer 3: Emergence (meta-patterns that emerge from bonds)

VORTEX DYNAMICS:
- Information circulates under pressure
- Hot zones (high activity) vs cold zones (archive)
- Semantic gravity pulls related atoms together
- Vacuum zones create pull for missing information

BRAIN-LIKE PROCESSING:
- Continuous background cycles (like Default Mode Network)
- Hebbian learning (strengthen used connections)
- Pattern emergence (insights from circulation)
- Memory consolidation (compress related atoms)

Usage:
    python CYCLOTRON_BRAIN_AGENT.py        # Start brain agent
    python CYCLOTRON_BRAIN_AGENT.py status # Check brain state
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import logging

# Configuration - Use portable paths
ATOMS_DIR = Path(__file__).parent / ".cyclotron_atoms"
INDEX_FILE = ATOMS_DIR / "index.json"
BRAIN_STATE_FILE = ATOMS_DIR / "brain_state.json"
VORTEX_FILE = ATOMS_DIR / "information_vortex.json"
EMERGENCE_FILE = ATOMS_DIR / "emergent_patterns.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CyclotronBrainAgent:
    """Active intelligence system - circulating knowledge under pressure"""

    def __init__(self):
        self.atoms = {}              # Layer 1: Raw knowledge particles
        self.bonds = defaultdict(list)  # Layer 2: Relationships
        self.patterns = []           # Layer 3: Emergent intelligence
        self.vortex_zones = {
            'hot': [],      # High activity, recently accessed
            'warm': [],     # Moderate activity
            'cold': [],     # Archive, rarely used
            'vacuum': []    # Gaps - missing information creates pull
        }
        self.cycle_count = 0
        self.insights_discovered = 0

    def load_atoms(self):
        """Load Layer 1: Knowledge atoms from cyclotron index"""
        logger.info("🔄 Loading atoms from cyclotron...")
        if not INDEX_FILE.exists():
            logger.error("❌ Cyclotron index not found")
            return

        with open(INDEX_FILE) as f:
            index = json.load(f)
            self.atoms = {atom['name']: atom for atom in index.get('atoms', [])}

        logger.info(f"✅ Loaded {len(self.atoms)} atoms")

    def build_bonds(self):
        """Layer 2: Find relationships between atoms (semantic connections)"""
        logger.info("🔗 Building bonds between atoms...")

        # Clear existing bonds
        self.bonds.clear()

        # For each atom, find related atoms based on:
        # 1. Filename similarities
        # 2. Type clustering
        # 3. Content references (future: full-text analysis)

        for atom_name, atom in self.atoms.items():
            # Type-based bonds
            same_type_atoms = [a for a, data in self.atoms.items()
                             if data['type'] == atom['type'] and a != atom_name]
            self.bonds[atom_name].extend(same_type_atoms[:5])  # Top 5

            # Semantic bonds (word overlap in filenames)
            words = set(atom_name.lower().replace('.', ' ').replace('_', ' ').split())
            for other_name, other_atom in self.atoms.items():
                if other_name == atom_name:
                    continue
                other_words = set(other_name.lower().replace('.', ' ').replace('_', ' ').split())
                overlap = len(words & other_words)
                if overlap >= 2:  # 2+ shared words = semantic bond
                    if other_name not in self.bonds[atom_name]:
                        self.bonds[atom_name].append(other_name)

        total_bonds = sum(len(v) for v in self.bonds.values())
        logger.info(f"✅ Created {total_bonds} bonds between atoms")

    def calculate_vortex_zones(self):
        """Vortex Dynamics: Classify atoms by activity/pressure"""
        logger.info("🌀 Calculating vortex zones (hot/warm/cold/vacuum)...")

        self.vortex_zones = {'hot': [], 'warm': [], 'cold': [], 'vacuum': []}

        for atom_name, atom in self.atoms.items():
            # Connection count = "semantic gravity"
            connection_count = len(self.bonds.get(atom_name, []))

            # Modified time (recent = hot)
            modified = atom.get('modified', 0)
            age_days = (time.time() - modified) / 86400

            # Hot zone: high connections OR recently modified
            if connection_count > 10 or age_days < 7:
                self.vortex_zones['hot'].append(atom_name)
            # Warm zone: moderate connections
            elif connection_count > 5:
                self.vortex_zones['warm'].append(atom_name)
            # Cold zone: few connections, old
            elif connection_count > 0:
                self.vortex_zones['cold'].append(atom_name)
            # Vacuum: isolated atoms (create pull for connections)
            else:
                self.vortex_zones['vacuum'].append(atom_name)

        logger.info(f"🌀 Vortex: Hot={len(self.vortex_zones['hot'])}, "
                   f"Warm={len(self.vortex_zones['warm'])}, "
                   f"Cold={len(self.vortex_zones['cold'])}, "
                   f"Vacuum={len(self.vortex_zones['vacuum'])}")

    def emerge_patterns(self):
        """Layer 3: Discover meta-patterns from bond network"""
        logger.info("✨ Emerging patterns from circulation...")

        self.patterns = []

        # Pattern 1: Highly connected hubs (knowledge centers)
        hubs = [(name, len(bonds)) for name, bonds in self.bonds.items()]
        hubs.sort(key=lambda x: x[1], reverse=True)
        top_hubs = hubs[:10]

        if top_hubs:
            self.patterns.append({
                'type': 'knowledge_hubs',
                'insight': 'Core knowledge centers with many connections',
                'data': [{'name': h[0], 'connections': h[1]} for h in top_hubs]
            })

        # Pattern 2: Isolated clusters (could be new domains)
        # Find groups of atoms that connect to each other but not outside

        # Pattern 3: Type concentrations (what knowledge types dominate)
        type_counts = defaultdict(int)
        for atom in self.atoms.values():
            type_counts[atom['type']] += 1

        self.patterns.append({
            'type': 'knowledge_composition',
            'insight': 'Distribution of knowledge types',
            'data': dict(type_counts)
        })

        # Pattern 4: Vacuum zones (missing information)
        if self.vortex_zones['vacuum']:
            self.patterns.append({
                'type': 'vacuum_zones',
                'insight': f"{len(self.vortex_zones['vacuum'])} isolated atoms - opportunity for connection",
                'data': self.vortex_zones['vacuum'][:20]  # Sample
            })

        self.insights_discovered = len(self.patterns)
        logger.info(f"✨ Discovered {self.insights_discovered} emergent patterns")

    def brain_cycle(self):
        """Complete brain processing cycle - like a brain wave"""
        self.cycle_count += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"🧠 BRAIN CYCLE #{self.cycle_count}")
        logger.info(f"{'='*60}")

        # Layer 1: Load raw atoms
        self.load_atoms()

        # Layer 2: Build relationship bonds
        self.build_bonds()

        # Vortex: Calculate pressure zones
        self.calculate_vortex_zones()

        # Layer 3: Emerge patterns (bootstrap feedback)
        self.emerge_patterns()

        # Save brain state
        self.save_state()

        logger.info(f"{'='*60}")
        logger.info(f"✅ Cycle complete. Insights: {self.insights_discovered}")
        logger.info(f"{'='*60}\n")

    def save_state(self):
        """Persist brain state to disk"""
        brain_state = {
            'cycle_count': self.cycle_count,
            'atom_count': len(self.atoms),
            'bond_count': sum(len(v) for v in self.bonds.values()),
            'insights_discovered': self.insights_discovered,
            'last_cycle': datetime.now().isoformat(),
            'vortex_zones': {k: len(v) for k, v in self.vortex_zones.items()}
        }

        with open(BRAIN_STATE_FILE, 'w') as f:
            json.dump(brain_state, f, indent=2)

        # Save vortex visualization
        with open(VORTEX_FILE, 'w') as f:
            json.dump(self.vortex_zones, f, indent=2)

        # Save emerged patterns
        with open(EMERGENCE_FILE, 'w') as f:
            json.dump({
                'cycle': self.cycle_count,
                'timestamp': datetime.now().isoformat(),
                'patterns': self.patterns
            }, f, indent=2)

    def run_daemon(self, interval=300):
        """Run continuous brain cycles (like Default Mode Network)"""
        logger.info("🧠 CYCLOTRON BRAIN AGENT STARTING...")
        logger.info(f"⏱️  Cycle interval: {interval} seconds ({interval/60:.1f} minutes)")
        logger.info("🌀 Information vortex initialized")
        logger.info("🔄 Entering continuous processing mode...\n")

        try:
            while True:
                self.brain_cycle()
                logger.info(f"⏸️  Sleeping {interval}s until next cycle...\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("\n🛑 Brain agent stopped by user")
            self.save_state()

def main():
    """Main entry point"""
    import sys

    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

    agent = CyclotronBrainAgent()

    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        # Show current brain state
        if BRAIN_STATE_FILE.exists():
            with open(BRAIN_STATE_FILE) as f:
                state = json.load(f)
            print("\n🧠 CYCLOTRON BRAIN STATUS")
            print("=" * 50)
            for k, v in state.items():
                print(f"{k}: {v}")
            print("=" * 50)
        else:
            print("❌ Brain agent not running or no state file found")
    else:
        # Run daemon mode
        agent.run_daemon(interval=300)  # 5-minute cycles

if __name__ == '__main__':
    main()
