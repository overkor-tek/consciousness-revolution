#!/usr/bin/env python3
"""
Grabovoi Codes Cyclotron Indexer
Breaks down Grabovoi's number sequences into searchable, analyzable data chunks
Part of the consciousness-revolution cyclotron system
"""

import csv
import json
import hashlib
from datetime import datetime
from pathlib import Path

class GrabovoiIndexer:
    """Indexes Grabovoi codes for cyclotron ingestion"""

    def __init__(self):
        self.codes_file = "GRABOVOI_CODES_DATABASE.csv"
        self.output_dir = Path(".cyclotron_atoms")
        self.output_dir.mkdir(exist_ok=True)

    def load_codes(self):
        """Load codes from CSV database"""
        codes = []
        with open(self.codes_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                codes.append(row)
        return codes

    def create_atom(self, code_data):
        """Create a cyclotron atom from a Grabovoi code"""
        atom_id = hashlib.md5(
            f"{code_data['Code']}_{code_data['Purpose']}".encode()
        ).hexdigest()[:16]

        atom = {
            "id": atom_id,
            "type": "grabovoi_code",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "code": code_data['Code'],
                "category": code_data['Category'],
                "subcategory": code_data['Subcategory'],
                "purpose": code_data['Purpose'],
                "instructions": code_data['Instructions'],
                "frequency_type": code_data['Frequency_Type'],
                "searchable_text": f"{code_data['Purpose']} {code_data['Category']} {code_data['Subcategory']}",
                "code_length": len(code_data['Code'].replace(' ', '')),
                "digit_sum": sum(int(d) for d in code_data['Code'] if d.isdigit())
            },
            "metadata": {
                "source": "Grigory Grabovoi System",
                "indexed_by": "GRABOVOI_CYCLOTRON_INDEXER",
                "version": "1.0"
            }
        }
        return atom

    def generate_pattern_analysis(self, codes):
        """Analyze patterns in the number sequences"""
        analysis = {
            "total_codes": len(codes),
            "categories": {},
            "code_length_distribution": {},
            "frequency_types": {},
            "common_digits": {},
            "digit_sum_stats": {
                "min": float('inf'),
                "max": 0,
                "average": 0
            }
        }

        digit_sums = []
        all_digits = []

        for code in codes:
            # Category distribution
            cat = code['Category']
            analysis['categories'][cat] = analysis['categories'].get(cat, 0) + 1

            # Code length
            clean_code = code['Code'].replace(' ', '')
            length = len(clean_code)
            analysis['code_length_distribution'][length] = \
                analysis['code_length_distribution'].get(length, 0) + 1

            # Frequency types
            freq = code['Frequency_Type']
            analysis['frequency_types'][freq] = \
                analysis['frequency_types'].get(freq, 0) + 1

            # Digit analysis
            digits = [int(d) for d in clean_code if d.isdigit()]
            all_digits.extend(digits)
            digit_sum = sum(digits)
            digit_sums.append(digit_sum)

        # Digit statistics
        analysis['digit_sum_stats']['min'] = min(digit_sums)
        analysis['digit_sum_stats']['max'] = max(digit_sums)
        analysis['digit_sum_stats']['average'] = sum(digit_sums) / len(digit_sums)

        # Most common digits
        for digit in range(10):
            analysis['common_digits'][digit] = all_digits.count(digit)

        return analysis

    def index_all(self):
        """Main indexing function"""
        print("🌀 Grabovoi Cyclotron Indexer Starting...")

        # Load codes
        codes = self.load_codes()
        print(f"📊 Loaded {len(codes)} Grabovoi codes")

        # Create atoms
        atoms = []
        for code_data in codes:
            atom = self.create_atom(code_data)
            atoms.append(atom)

            # Save individual atom file
            atom_file = self.output_dir / f"grabovoi_{atom['id']}.json"
            with open(atom_file, 'w') as f:
                json.dump(atom, f, indent=2)

        print(f"⚛️  Created {len(atoms)} cyclotron atoms")

        # Create master index
        master_index = {
            "indexer": "GRABOVOI_CYCLOTRON_INDEXER",
            "timestamp": datetime.now().isoformat(),
            "total_atoms": len(atoms),
            "atoms": atoms
        }

        index_file = self.output_dir / "grabovoi_master_index.json"
        with open(index_file, 'w') as f:
            json.dump(master_index, f, indent=2)

        print(f"📝 Created master index: {index_file}")

        # Generate pattern analysis
        analysis = self.generate_pattern_analysis(codes)
        analysis_file = self.output_dir / "grabovoi_pattern_analysis.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"🔍 Pattern analysis saved: {analysis_file}")

        # Create searchable text file for grep
        search_file = Path("GRABOVOI_SEARCHABLE.txt")
        with open(search_file, 'w') as f:
            f.write("GRABOVOI CODES - SEARCHABLE INDEX\n")
            f.write("=" * 80 + "\n\n")
            for code in codes:
                f.write(f"CODE: {code['Code']}\n")
                f.write(f"CATEGORY: {code['Category']} > {code['Subcategory']}\n")
                f.write(f"PURPOSE: {code['Purpose']}\n")
                f.write(f"FREQUENCY: {code['Frequency_Type']}\n")
                f.write(f"INSTRUCTIONS: {code['Instructions']}\n")
                f.write("-" * 80 + "\n")

        print(f"🔎 Searchable text file: {search_file}")

        # Summary
        print("\n✨ INDEXING COMPLETE ✨")
        print(f"\nPattern Analysis Summary:")
        print(f"  Categories: {len(analysis['categories'])}")
        print(f"  Frequency Types: {len(analysis['frequency_types'])}")
        print(f"  Avg Digit Sum: {analysis['digit_sum_stats']['average']:.2f}")
        print(f"  Most Common Digit: {max(analysis['common_digits'], key=analysis['common_digits'].get)}")

        return atoms, analysis

def main():
    indexer = GrabovoiIndexer()
    atoms, analysis = indexer.index_all()

    print("\n🌀 Ready for cyclotron integration")
    print("📂 Atoms stored in: .cyclotron_atoms/")
    print("🔍 Search with: grep -i 'keyword' GRABOVOI_SEARCHABLE.txt")

if __name__ == "__main__":
    main()
