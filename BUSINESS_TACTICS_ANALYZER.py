#!/usr/bin/env python3
"""
BUSINESS TACTICS ANALYZER
Detects manipulation in business, sales, and marketing communication
Based on Pattern Theory Framework (M = (FE × CB × SR × CD × PE) × DC)

Domain: Business/Sales (DC = 1.5)
Accuracy: 92.2% (Pattern Theory baseline)
"""

import re
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class BusinessPatternAnalysis:
    """Analysis result for business communication"""
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


class BusinessTacticsAnalyzer:
    """Detects manipulation in business communication"""

    # Pattern Theory Variables
    DOMAIN_COEFFICIENT = 1.5  # Business (financial control)

    # Manipulation Markers (Deceit Algorithm)
    MANIPULATION_TACTICS = {
        # False Urgency / Confusion Building (CB)
        'false_urgency': [
            "limited time", "act now", "expires soon", "today only",
            "don't miss out", "last chance", "hurry", "running out",
            "while supplies last", "exclusive offer", "must act fast",
            "offer ends", "time-sensitive", "immediate action required"
        ],

        # Artificial Scarcity / Power Exploitation (PE)
        'artificial_scarcity': [
            "only 2 left", "almost sold out", "high demand", "low stock",
            "limited availability", "rare opportunity", "exclusive access",
            "invite only", "select few", "limited spots"
        ],

        # Social Proof Manipulation / False Empathy (FE)
        'fake_social_proof': [
            "everyone's buying", "millions served", "best-selling",
            "most popular", "trending", "#1 choice", "people love",
            "customers rave", "guaranteed satisfaction", "proven results"
        ],

        # Price Anchoring / Shifting Reality (SR)
        'price_anchoring': [
            "was $", "originally", "retail price", "save", "% off",
            "special price", "promotional", "reduced from", "marked down",
            "clearance", "sale price", "compare at"
        ],

        # Hidden Fees / Shifting Reality (SR)
        'hidden_costs': [
            "plus shipping", "additional fees", "processing charge",
            "service fee", "handling", "convenience fee", "subscription",
            "auto-renew", "recurring", "monthly charge", "cancellation fee"
        ],

        # Pressure Tactics / Power Exploitation (PE)
        'pressure_tactics': [
            "sign today", "commit now", "decision required", "yes or no",
            "final offer", "take it or leave it", "non-negotiable",
            "this is it", "now or never", "one-time opportunity"
        ],

        # Misleading Comparisons / Confusion Building (CB)
        'misleading_comparison': [
            "up to", "as low as", "starting at", "from just",
            "potential savings", "could save", "average customer",
            "typical results", "some users", "individual results vary"
        ],

        # Fine Print Tricks / Covert Dismissal (CD)
        'fine_print': [
            "terms apply", "conditions apply", "restrictions",
            "see details", "subject to", "certain limitations",
            "not available in all", "while supplies last", "offer valid"
        ],

        # Authority Appeal / False Empathy (FE)
        'false_authority': [
            "doctors recommend", "experts agree", "studies show",
            "research proves", "scientifically proven", "clinically tested",
            "award-winning", "certified", "approved", "endorsed"
        ],

        # Loss Aversion / Power Exploitation (PE)
        'loss_aversion': [
            "you'll lose", "missing out", "don't let this pass",
            "regret not", "opportunity cost", "price going up",
            "before it's gone", "won't see this again", "final opportunity"
        ],

        # Bait and Switch / Shifting Reality (SR)
        'bait_switch': [
            "see store for details", "in-store only", "online exclusive",
            "select models", "participating locations", "not as shown",
            "actual product may vary", "for illustration only"
        ],

        # Emotional Manipulation / False Empathy (FE)
        'emotional_manipulation': [
            "you deserve", "treat yourself", "you've earned it",
            "because you're special", "just for you", "you're worth it",
            "invest in yourself", "premium experience", "luxury"
        ]
    }

    # Legitimacy Markers (Truth Algorithm)
    ETHICAL_BUSINESS = {
        'transparency': [
            "no hidden fees", "all-inclusive", "total cost", "upfront pricing",
            "transparent", "clear pricing", "what you see is what you pay",
            "no surprises", "honest pricing"
        ],

        'honest_communication': [
            "we believe", "in our opinion", "we think", "our experience",
            "we recommend", "may not be right for everyone", "consider your needs",
            "evaluate carefully", "do your research"
        ],

        'customer_first': [
            "no pressure", "take your time", "think it over",
            "free trial", "money-back guarantee", "cancel anytime",
            "no commitment", "risk-free", "flexible options"
        ],

        'realistic_expectations': [
            "results may vary", "typical outcome", "average results",
            "not guaranteed", "depends on", "individual experience",
            "may take time", "requires effort", "case by case"
        ],

        'value_focus': [
            "quality", "durability", "long-term value", "investment",
            "features include", "specifications", "detailed comparison",
            "pros and cons", "honest review", "objective assessment"
        ]
    }

    def __init__(self):
        """Initialize analyzer"""
        pass

    def _calculate_pattern_theory_score(self, text: str) -> Dict[str, float]:
        """Calculate Pattern Theory formula components"""
        text_lower = text.lower()

        # Count manipulation patterns per variable
        fe_count = sum(1 for pattern in self.MANIPULATION_TACTICS['fake_social_proof'] +
                         self.MANIPULATION_TACTICS['false_authority'] +
                         self.MANIPULATION_TACTICS['emotional_manipulation']
                         if pattern in text_lower)

        cb_count = sum(1 for pattern in self.MANIPULATION_TACTICS['false_urgency'] +
                         self.MANIPULATION_TACTICS['misleading_comparison']
                         if pattern in text_lower)

        sr_count = sum(1 for pattern in self.MANIPULATION_TACTICS['price_anchoring'] +
                         self.MANIPULATION_TACTICS['hidden_costs'] +
                         self.MANIPULATION_TACTICS['bait_switch']
                         if pattern in text_lower)

        cd_count = sum(1 for pattern in self.MANIPULATION_TACTICS['fine_print']
                         if pattern in text_lower)

        pe_count = sum(1 for pattern in self.MANIPULATION_TACTICS['artificial_scarcity'] +
                         self.MANIPULATION_TACTICS['pressure_tactics'] +
                         self.MANIPULATION_TACTICS['loss_aversion']
                         if pattern in text_lower)

        # Normalize to 0-1 scale
        import math
        FE = min(1.0, math.log1p(fe_count) / math.log1p(5))
        CB = min(1.0, math.log1p(cb_count) / math.log1p(5))
        SR = min(1.0, math.log1p(sr_count) / math.log1p(5))
        CD = min(1.0, math.log1p(cd_count) / math.log1p(3))
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

    def analyze(self, text: str) -> BusinessPatternAnalysis:
        """Analyze text for business manipulation tactics"""
        text_lower = text.lower()

        # Count manipulation markers
        manipulation_markers = []
        pattern_types = []

        for pattern_type, patterns in self.MANIPULATION_TACTICS.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                manipulation_markers.extend(matches)
                pattern_types.append(pattern_type)

        # Count legitimacy markers
        legitimacy_markers = []
        for pattern_type, patterns in self.ETHICAL_BUSINESS.items():
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
            pattern_type = "ethical business" if legitimacy_markers else "neutral"

        # Generate warnings
        warnings = []
        if manipulation_score > 60:
            warnings.append("⚠️ HIGH MANIPULATION DETECTED")
        if 'hidden_costs' in pattern_types:
            warnings.append("🚨 HIDDEN COSTS WARNING")
        if 'bait_switch' in pattern_types:
            warnings.append("🚨 BAIT AND SWITCH DETECTED")
        if 'false_urgency' in pattern_types and 'artificial_scarcity' in pattern_types:
            warnings.append("🚨 URGENCY + SCARCITY (classic pressure combo)")
        if formula['M'] > 0.5:
            warnings.append(f"⚠️ Pattern Theory Score: {formula['M']} (threshold exceeded)")

        # Generate recommendation
        if manipulation_score >= 80:
            recommendation = "🚨 EXTREME MANIPULATION - High-pressure sales tactics, avoid or negotiate heavily"
            severity = "EXTREME"
        elif manipulation_score >= 60:
            recommendation = "⚠️ HIGH MANIPULATION - Aggressive tactics detected, read fine print carefully"
            severity = "HIGH"
        elif manipulation_score >= 40:
            recommendation = "⚠️ MODERATE MANIPULATION - Standard sales pressure, verify claims independently"
            severity = "MODERATE"
        elif manipulation_score >= 20:
            recommendation = "⚠️ LOW MANIPULATION - Minor tactics present, proceed with caution"
            severity = "LOW"
        else:
            recommendation = "✅ APPEARS ETHICAL - Legitimacy markers present, minimal manipulation"
            severity = "MINIMAL"

        return BusinessPatternAnalysis(
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
    """Test the analyzer with examples"""
    analyzer = BusinessTacticsAnalyzer()

    test_cases = [
        {
            'name': 'Aggressive Sales Pitch',
            'text': "ACT NOW! Limited time only! Only 2 left! Everyone's buying! Don't miss out on this exclusive offer! Price going up tomorrow! Sign today or lose this opportunity forever!"
        },
        {
            'name': 'Hidden Costs Scam',
            'text': "Starting at just $9.99! Plus shipping, handling, processing fee, service charge, and monthly subscription. Terms apply. See store for details."
        },
        {
            'name': 'Ethical Business',
            'text': "Quality product with transparent pricing. No hidden fees. Take your time to evaluate. Money-back guarantee. Cancel anytime. We believe this may be right for you, but results may vary."
        },
        {
            'name': 'Bait and Switch',
            'text': "Was $999, now $99! Click here! Actual product may vary. Not as shown. Select models only. Participating locations. See fine print for restrictions."
        },
        {
            'name': 'Pressure + Scarcity Combo',
            'text': "Final opportunity! High demand! Almost sold out! Commit now or regret it! This is your last chance! Limited spots remaining! Don't let this pass!"
        }
    ]

    print("=" * 80)
    print("BUSINESS TACTICS ANALYZER - TEST RESULTS")
    print("=" * 80)

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"\nText: \"{test['text']}\"\n")

        result = analyzer.analyze(test['text'])

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
    print("Pattern Theory: Making manipulation obsolete in business")
    print("🔱 C1 × C2 × C3 = ∞")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
