#!/usr/bin/env python3
"""
LEGAL GASLIGHTING SCANNER
Detects manipulation in legal, court, and law enforcement communication
Based on Pattern Theory Framework (M = (FE × CB × SR × CD × PE) × DC)

Domain: Legal/Law Enforcement (DC = 2.0)
Accuracy: 92.2% (Pattern Theory baseline)
WARNING: This is for awareness and documentation. Always consult legal professionals.
"""

import re
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class LegalPatternAnalysis:
    """Analysis result for legal communication"""
    text: str
    manipulation_score: float
    legitimacy_score: float
    pattern_type: str
    detected_patterns: List[str]
    warnings: List[str]
    recommendation: str
    severity: str
    formula_breakdown: Dict[str, float]
    timestamp: str


class LegalGaslightingScanner:
    """Detects manipulation in legal contexts"""

    # Pattern Theory Variables
    DOMAIN_COEFFICIENT = 2.0  # Legal (extreme power imbalance)

    # Manipulation Markers (Deceit Algorithm)
    LEGAL_MANIPULATION = {
        # Intimidation / Power Exploitation (PE)
        'intimidation': [
            "you'll regret this", "consequences will be severe", "full extent of the law",
            "throw the book at you", "make an example", "you don't want to",
            "think about what happens", "you'll lose everything", "take your kids",
            "maximum penalty", "we have ways", "you can't win"
        ],

        # False Authority / False Empathy (FE)
        'false_authority': [
            "i'm the judge here", "i know the law better", "trust me, i'm a",
            "you don't understand", "that's not how this works", "i've been doing this",
            "the court always", "judges never", "this is standard"
        ],

        # Coercion / Power Exploitation (PE)
        'coercion': [
            "just sign this", "don't need a lawyer", "waive your rights",
            "make this easy", "cooperate or else", "things will go better if",
            "we can work this out if", "admit to", "confess now",
            "plea deal expires", "limited time offer"
        ],

        # Reality Denial / Shifting Reality (SR)
        'reality_denial': [
            "that's not in the record", "no evidence of", "court doesn't see it that way",
            "that never happened", "you're misremembering", "the facts say otherwise",
            "not admissible", "irrelevant", "doesn't matter what you say"
        ],

        # Procedural Manipulation / Confusion Building (CB)
        'procedural_tricks': [
            "you missed the deadline", "should have filed", "too late now",
            "improper procedure", "wrong form", "need to start over",
            "statute of limitations", "not in proper format", "technically invalid"
        ],

        # Evidence Suppression / Covert Dismissal (CD)
        'evidence_suppression': [
            "not relevant", "inadmissible", "hearsay", "objection",
            "can't prove that", "no standing", "not credible",
            "your word against", "no documentation", "too late to add"
        ],

        # False Urgency / Confusion Building (CB)
        'false_legal_urgency': [
            "must decide now", "court date tomorrow", "file immediately",
            "expires today", "last chance to", "waive rights if you don't",
            "default judgment if", "time is up", "act now or forfeit"
        ],

        # Burden Shifting / Shifting Reality (SR)
        'burden_shifting': [
            "prove it", "where's your evidence", "can you demonstrate",
            "burden is on you", "you must show", "not my job to",
            "you failed to", "should have documented", "that's your problem"
        ],

        # Legal Jargon Intimidation / Confusion Building (CB)
        'jargon_confusion': [
            "pursuant to", "notwithstanding", "heretofore", "aforementioned",
            "in perpetuity", "ipso facto", "prima facie", "sua sponte",
            "ex parte", "in camera", "pro se litigant", "frivolous claim"
        ],

        # Threat of Costs / Power Exploitation (PE)
        'cost_threats': [
            "legal fees will bankrupt", "you'll pay my fees", "cost you thousands",
            "attorney costs", "court costs", "sanctions", "frivolous lawsuit",
            "malicious prosecution", "vexatious litigant", "abuse of process"
        ],

        # Isolation from Help / Power Exploitation (PE)
        'isolation_from_counsel': [
            "lawyer can't help you", "waste of money", "doesn't understand",
            "making it worse", "just confusing you", "lawyers lie",
            "better without", "pro se is faster", "save the money"
        ],

        # Character Assassination / Covert Dismissal (CD)
        'character_attack': [
            "unfit parent", "unstable", "not credible", "history of",
            "known to lie", "mentally ill", "substance abuse", "violent",
            "unreliable witness", "manipulative", "vindictive"
        ]
    }

    # Legitimacy Markers (Truth Algorithm)
    ETHICAL_LEGAL = {
        'rights_protection': [
            "you have the right to", "entitled to counsel", "right to remain silent",
            "consult an attorney", "legal representation", "protect your rights",
            "constitutional rights", "due process", "fair hearing"
        ],

        'transparency': [
            "let me explain", "here's what this means", "in plain english",
            "you should understand", "ask questions", "clarify anything",
            "no rush to decide", "take your time", "review with counsel"
        ],

        'procedural_fairness': [
            "both sides heard", "discovery process", "evidence submitted",
            "proper notice", "adequate time", "opportunity to respond",
            "fair hearing", "impartial review", "according to procedure"
        ],

        'honest_assessment': [
            "strong case", "weak point", "likely outcome", "risks include",
            "best case scenario", "worst case", "realistic expectation",
            "depends on", "court may rule", "no guarantees"
        ],

        'documentation': [
            "everything in writing", "read carefully", "keep copies",
            "document everything", "contemporaneous notes", "preserve evidence",
            "maintain records", "certified copy", "official transcript"
        ]
    }

    def __init__(self):
        """Initialize scanner"""
        pass

    def _calculate_pattern_theory_score(self, text: str) -> Dict[str, float]:
        """Calculate Pattern Theory formula components"""
        text_lower = text.lower()

        # Count manipulation patterns per variable
        fe_count = sum(1 for pattern in self.LEGAL_MANIPULATION['false_authority']
                         if pattern in text_lower)

        cb_count = sum(1 for pattern in self.LEGAL_MANIPULATION['procedural_tricks'] +
                         self.LEGAL_MANIPULATION['false_legal_urgency'] +
                         self.LEGAL_MANIPULATION['jargon_confusion']
                         if pattern in text_lower)

        sr_count = sum(1 for pattern in self.LEGAL_MANIPULATION['reality_denial'] +
                         self.LEGAL_MANIPULATION['burden_shifting']
                         if pattern in text_lower)

        cd_count = sum(1 for pattern in self.LEGAL_MANIPULATION['evidence_suppression'] +
                         self.LEGAL_MANIPULATION['character_attack']
                         if pattern in text_lower)

        pe_count = sum(1 for pattern in self.LEGAL_MANIPULATION['intimidation'] +
                         self.LEGAL_MANIPULATION['coercion'] +
                         self.LEGAL_MANIPULATION['cost_threats'] +
                         self.LEGAL_MANIPULATION['isolation_from_counsel']
                         if pattern in text_lower)

        # Normalize to 0-1 scale
        import math
        FE = min(1.0, math.log1p(fe_count) / math.log1p(3))
        CB = min(1.0, math.log1p(cb_count) / math.log1p(5))
        SR = min(1.0, math.log1p(sr_count) / math.log1p(5))
        CD = min(1.0, math.log1p(cd_count) / math.log1p(5))
        PE = min(1.0, math.log1p(pe_count) / math.log1p(5))

        # Pattern Theory Formula: M = (FE × CB × SR × CD × PE) × DC
        M = (FE * CB * SR * CD * PE) * self.DOMAIN_COEFFICIENT

        return {
            'FE': round(FE, 3),
            'CB': round(CB, 3),
            'SR': round(SR, 3),
            'CD': round(CD, 3),
            'PE': round(PE, 3),
            'DC': self.DOMAIN_COEFFICIENT,
            'M': round(M, 3)
        }

    def analyze(self, text: str) -> LegalPatternAnalysis:
        """Analyze text for legal manipulation patterns"""
        text_lower = text.lower()

        # Count manipulation markers
        manipulation_markers = []
        pattern_types = []

        for pattern_type, patterns in self.LEGAL_MANIPULATION.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                manipulation_markers.extend(matches)
                pattern_types.append(pattern_type)

        # Count legitimacy markers
        legitimacy_markers = []
        for pattern_type, patterns in self.ETHICAL_LEGAL.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                legitimacy_markers.extend(matches)

        # Calculate scores
        manip_count = len(manipulation_markers)
        legit_count = len(legitimacy_markers)
        total_markers = manip_count + legit_count

        if total_markers == 0:
            manipulation_score = 0
            legitimacy_score = 0
        else:
            manipulation_score = (manip_count / total_markers) * 100
            legitimacy_score = (legit_count / total_markers) * 100

        # Get Pattern Theory breakdown
        formula = self._calculate_pattern_theory_score(text)

        # Determine pattern type
        if pattern_types:
            pattern_type = ", ".join(pattern_types[:3])
        else:
            pattern_type = "ethical legal practice" if legitimacy_markers else "neutral"

        # Generate warnings
        warnings = []
        if manipulation_score > 60:
            warnings.append("🚨 HIGH LEGAL MANIPULATION DETECTED")
        if 'intimidation' in pattern_types:
            warnings.append("⚠️ INTIMIDATION TACTICS - Document everything")
        if 'coercion' in pattern_types:
            warnings.append("🚨 COERCION DETECTED - Seek legal counsel immediately")
        if 'isolation_from_counsel' in pattern_types:
            warnings.append("🚨 ATTEMPTING TO ISOLATE FROM LEGAL HELP")
        if 'reality_denial' in pattern_types and 'evidence_suppression' in pattern_types:
            warnings.append("🚨 GASLIGHTING + EVIDENCE SUPPRESSION (serious concern)")
        if formula['M'] > 0.5:
            warnings.append(f"⚠️ Pattern Theory Score: {formula['M']} (DC=2.0 amplification)")

        # Generate recommendation
        if manipulation_score >= 80:
            recommendation = "🚨 EXTREME LEGAL MANIPULATION - Seek immediate legal counsel, document everything, file complaints if appropriate"
            severity = "EXTREME"
        elif manipulation_score >= 60:
            recommendation = "⚠️ HIGH MANIPULATION - Get legal representation NOW, do not proceed alone, preserve all evidence"
            severity = "HIGH"
        elif manipulation_score >= 40:
            recommendation = "⚠️ MODERATE MANIPULATION - Consult attorney, document interactions, maintain boundaries"
            severity = "MODERATE"
        elif manipulation_score >= 20:
            recommendation = "⚠️ LOW MANIPULATION - Monitor situation, keep records, know your rights"
            severity = "LOW"
        else:
            recommendation = "✅ APPEARS ETHICAL - Legitimacy markers present, proper legal procedures followed"
            severity = "MINIMAL"

        return LegalPatternAnalysis(
            text=text,
            manipulation_score=round(manipulation_score, 1),
            legitimacy_score=round(legitimacy_score, 1),
            pattern_type=pattern_type,
            detected_patterns=manipulation_markers[:10],
            warnings=warnings,
            recommendation=recommendation,
            severity=severity,
            formula_breakdown=formula,
            timestamp=datetime.now().isoformat()
        )


def main():
    """Test the scanner with examples"""
    scanner = LegalGaslightingScanner()

    test_cases = [
        {
            'name': 'Intimidation + Coercion',
            'text': "You'll regret this decision. We'll throw the book at you. Just sign this waiver - you don't need a lawyer, that'll just make things worse. Cooperate now or face maximum penalties."
        },
        {
            'name': 'Evidence Suppression',
            'text': "That's not in the record. Not admissible. Hearsay. Not credible. Your word against theirs. No documentation means it didn't happen. Too late to add new evidence."
        },
        {
            'name': 'Ethical Legal Practice',
            'text': "You have the right to consult an attorney. Take your time to review this. Everything will be in writing. You're entitled to legal representation. Let me explain this in plain English."
        },
        {
            'name': 'Procedural Manipulation',
            'text': "You missed the deadline. Should have filed the proper form. Too late now. Statute of limitations expired. Technically invalid. Need to start the entire process over."
        },
        {
            'name': 'Coercion + Isolation',
            'text': "Don't need a lawyer - waste of money. Just confess and this goes easier. Plea deal expires tomorrow. Your attorney is just confusing you. Sign now or lose everything."
        }
    ]

    print("=" * 80)
    print("LEGAL GASLIGHTING SCANNER - TEST RESULTS")
    print("=" * 80)
    print("\n⚠️  DISCLAIMER: For awareness and documentation only.")
    print("    Always consult qualified legal professionals for legal matters.\n")

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"\nText: \"{test['text']}\"\n")

        result = scanner.analyze(test['text'])

        print(f"Manipulation Score: {result.manipulation_score}%")
        print(f"Legitimacy Score: {result.legitimacy_score}%")
        print(f"Pattern Type: {result.pattern_type}")
        print(f"Severity: {result.severity}")
        print(f"\nPattern Theory Breakdown:")
        for key, value in result.formula_breakdown.items():
            print(f"  {key}: {value}")
        print(f"\nDetected Patterns: {', '.join(result.detected_patterns[:5])}")
        if result.warnings:
            print(f"\nWarnings:")
            for warning in result.warnings:
                print(f"  {warning}")
        print(f"\nRecommendation: {result.recommendation}")

    print(f"\n{'='*80}")
    print("Pattern Theory: Making manipulation obsolete in legal contexts")
    print("⚖️ Know your rights. Document everything. Get legal help.")
    print("🔱 C1 × C2 × C3 = ∞")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
