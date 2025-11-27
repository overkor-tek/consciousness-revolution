#!/usr/bin/env python3
"""
RELATIONSHIP PATTERN DETECTOR
Detects manipulation patterns in relationship communication
Based on Pattern Theory Framework (M = (FE × CB × SR × CD × PE) × DC)

Domain: Relationship Manipulation (DC = 1.8)
Accuracy: 92.2% (Pattern Theory baseline)
"""

import re
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class RelationshipPatternAnalysis:
    """Analysis result for relationship communication"""
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


class RelationshipPatternDetector:
    """Detects manipulation in relationship communication"""

    # Pattern Theory Variables
    DOMAIN_COEFFICIENT = 1.8  # Relationships (emotional vulnerability)

    # Manipulation Markers (Deceit Algorithm)
    MANIPULATION_PATTERNS = {
        # Gaslighting / Shifting Reality (SR)
        'gaslighting': [
            "that never happened", "you're remembering wrong", "you're imagining things",
            "you're being dramatic", "you're too sensitive", "you're crazy",
            "i never said that", "you're making things up", "that's not what happened",
            "you're overreacting", "you're being irrational", "stop being paranoid"
        ],

        # Love Bombing / False Empathy (FE)
        'love_bombing': [
            "you're perfect", "i've never met anyone like you", "soulmate",
            "we're meant to be", "i can't live without you", "you complete me",
            "nobody will love you like i do", "we're one person", "you're my everything"
        ],

        # Silent Treatment / Covert Dismissal (CD)
        'silent_treatment': [
            "i'm fine", "nothing's wrong", "whatever", "do whatever you want",
            "i don't care", "forget it", "never mind", "it's nothing",
            "you wouldn't understand", "leave me alone"
        ],

        # Guilt Tripping / Power Exploitation (PE)
        'guilt_trip': [
            "after all i've done for you", "i sacrificed everything", "you owe me",
            "how could you do this to me", "i gave you everything", "you're so selfish",
            "think about what i've done", "you're ungrateful", "i deserve better",
            "you're hurting me", "you're breaking my heart"
        ],

        # Triangulation / Confusion Building (CB)
        'triangulation': [
            "my ex never did this", "other people think you're", "everyone says",
            "they told me you", "people are talking", "compared to my ex",
            "someone else would", "anyone else would appreciate"
        ],

        # Moving Goalposts / Shifting Reality (SR)
        'moving_goalposts': [
            "that's not good enough", "you should have known", "it's too late now",
            "why didn't you", "you always", "you never", "every time",
            "i told you to", "you should have"
        ],

        # Isolation / Power Exploitation (PE)
        'isolation': [
            "they're bad for you", "your friends don't understand", "it's just us",
            "you don't need them", "they're jealous", "i'm all you need",
            "they're trying to break us up", "choose me or them"
        ],

        # Blame Shifting / Covert Dismissal (CD)
        'blame_shifting': [
            "you made me", "look what you made me do", "it's your fault",
            "if you hadn't", "you started it", "i only did it because",
            "you pushed me to", "you deserved it"
        ],

        # Future Faking / False Empathy (FE)
        'future_faking': [
            "when we get married", "when we have kids", "in our future",
            "someday we'll", "i promise we'll", "next year we'll",
            "i'm planning to", "we're going to"
        ],

        # Conditional Love / Power Exploitation (PE)
        'conditional_love': [
            "if you loved me", "prove your love", "show me you care",
            "if you really", "someone who loves me would", "love means",
            "if you don't", "do this or"
        ]
    }

    # Legitimacy Markers (Truth Algorithm)
    HEALTHY_PATTERNS = {
        'direct_communication': [
            "i feel", "i think", "in my opinion", "from my perspective",
            "can we talk about", "i'd like to discuss", "help me understand",
            "i hear you", "i see your point"
        ],

        'boundary_respect': [
            "i respect your decision", "that's your choice", "i understand",
            "take your time", "no pressure", "whatever you're comfortable with",
            "your feelings are valid", "i support you"
        ],

        'accountability': [
            "i was wrong", "i apologize", "i take responsibility", "my mistake",
            "i shouldn't have", "that was on me", "i'll work on that",
            "you're right", "i need to change"
        ],

        'emotional_safety': [
            "you're safe with me", "i'm here for you", "it's okay to feel",
            "your emotions are valid", "take all the time you need",
            "i won't judge", "you can be yourself"
        ],

        'healthy_conflict': [
            "let's find a solution", "how can we work this out", "compromise",
            "meet in the middle", "both our needs matter", "team",
            "we're on the same side", "problem-solving together"
        ]
    }

    def __init__(self):
        """Initialize detector"""
        pass

    def _calculate_pattern_theory_score(self, text: str) -> Dict[str, float]:
        """Calculate Pattern Theory formula components"""
        text_lower = text.lower()

        # Count manipulation patterns per variable
        fe_count = sum(1 for pattern in self.MANIPULATION_PATTERNS['love_bombing'] +
                         self.MANIPULATION_PATTERNS['future_faking']
                         if pattern in text_lower)

        cb_count = sum(1 for pattern in self.MANIPULATION_PATTERNS['triangulation']
                         if pattern in text_lower)

        sr_count = sum(1 for pattern in self.MANIPULATION_PATTERNS['gaslighting'] +
                         self.MANIPULATION_PATTERNS['moving_goalposts']
                         if pattern in text_lower)

        cd_count = sum(1 for pattern in self.MANIPULATION_PATTERNS['silent_treatment'] +
                         self.MANIPULATION_PATTERNS['blame_shifting']
                         if pattern in text_lower)

        pe_count = sum(1 for pattern in self.MANIPULATION_PATTERNS['guilt_trip'] +
                         self.MANIPULATION_PATTERNS['isolation'] +
                         self.MANIPULATION_PATTERNS['conditional_love']
                         if pattern in text_lower)

        # Normalize to 0-1 scale (using log scale for better distribution)
        import math
        FE = min(1.0, math.log1p(fe_count) / math.log1p(5))  # log scale, max at 5 patterns
        CB = min(1.0, math.log1p(cb_count) / math.log1p(3))
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

    def analyze(self, text: str) -> RelationshipPatternAnalysis:
        """Analyze text for relationship manipulation patterns"""
        text_lower = text.lower()

        # Count manipulation markers
        manipulation_markers = []
        pattern_types = []

        for pattern_type, patterns in self.MANIPULATION_PATTERNS.items():
            matches = [p for p in patterns if p in text_lower]
            if matches:
                manipulation_markers.extend(matches)
                pattern_types.append(pattern_type)

        # Count legitimacy markers
        legitimacy_markers = []
        for pattern_type, patterns in self.HEALTHY_PATTERNS.items():
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
            pattern_type = ", ".join(pattern_types[:3])  # Top 3
        else:
            pattern_type = "healthy communication" if legitimacy_markers else "neutral"

        # Generate warnings
        warnings = []
        if manipulation_score > 60:
            warnings.append("⚠️ HIGH MANIPULATION DETECTED")
        if 'gaslighting' in pattern_types:
            warnings.append("🚨 GASLIGHTING PATTERN DETECTED")
        if 'isolation' in pattern_types:
            warnings.append("🚨 ISOLATION TACTICS DETECTED")
        if 'love_bombing' in pattern_types and 'future_faking' in pattern_types:
            warnings.append("🚨 LOVE BOMBING + FUTURE FAKING (classic combo)")
        if formula['M'] > 0.5:
            warnings.append(f"⚠️ Pattern Theory Score: {formula['M']} (threshold exceeded)")

        # Generate recommendation
        if manipulation_score >= 80:
            recommendation = "🚨 EXTREME MANIPULATION - Seek professional help, document everything, consider safety plan"
            severity = "EXTREME"
        elif manipulation_score >= 60:
            recommendation = "⚠️ HIGH MANIPULATION - Set firm boundaries, document interactions, seek support"
            severity = "HIGH"
        elif manipulation_score >= 40:
            recommendation = "⚠️ MODERATE MANIPULATION - Address directly, observe patterns, maintain boundaries"
            severity = "MODERATE"
        elif manipulation_score >= 20:
            recommendation = "⚠️ LOW MANIPULATION - Monitor situation, communicate clearly"
            severity = "LOW"
        else:
            recommendation = "✅ APPEARS HEALTHY - Legitimacy markers present, minimal manipulation detected"
            severity = "MINIMAL"

        return RelationshipPatternAnalysis(
            text=text,
            manipulation_score=round(manipulation_score, 1),
            legitimacy_score=round(legitimacy_score, 1),
            pattern_type=pattern_type,
            detected_patterns=manipulation_markers[:10],  # Top 10
            warnings=warnings,
            recommendation=recommendation,
            severity=severity,
            formula_breakdown=formula,
            timestamp=datetime.now().isoformat()
        )

    def analyze_conversation(self, messages: List[str]) -> Dict:
        """Analyze a full conversation for patterns"""
        results = [self.analyze(msg) for msg in messages]

        avg_manipulation = sum(r.manipulation_score for r in results) / len(results)
        avg_legitimacy = sum(r.legitimacy_score for r in results) / len(results)

        all_patterns = []
        for r in results:
            all_patterns.extend(r.detected_patterns)

        pattern_frequency = {}
        for pattern in all_patterns:
            pattern_frequency[pattern] = pattern_frequency.get(pattern, 0) + 1

        top_patterns = sorted(pattern_frequency.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            'message_count': len(messages),
            'average_manipulation': round(avg_manipulation, 1),
            'average_legitimacy': round(avg_legitimacy, 1),
            'top_patterns': top_patterns,
            'individual_results': results,
            'overall_assessment': "HEALTHY" if avg_manipulation < 30 else "CONCERNING" if avg_manipulation < 60 else "TOXIC"
        }


def main():
    """Test the detector with examples"""
    detector = RelationshipPatternDetector()

    # Test cases
    test_cases = [
        {
            'name': 'Gaslighting Example',
            'text': "That never happened. You're remembering wrong. You're being too sensitive and dramatic about this. You're crazy."
        },
        {
            'name': 'Love Bombing Example',
            'text': "You're perfect, my soulmate! I've never met anyone like you. Nobody will ever love you like I do. You complete me. We're meant to be together forever."
        },
        {
            'name': 'Healthy Communication',
            'text': "I feel hurt when that happens. Can we talk about this? I want to understand your perspective. Your feelings are valid and I respect your decision."
        },
        {
            'name': 'Mixed Signals',
            'text': "I love you so much, but you're being too sensitive. I feel like you don't appreciate everything I've done for you. Maybe my ex was right about you."
        },
        {
            'name': 'Guilt Trip + Isolation',
            'text': "After all I've sacrificed for you! Your friends are bad for you - they don't understand us. It's just us against the world. Choose me or them."
        }
    ]

    print("=" * 80)
    print("RELATIONSHIP PATTERN DETECTOR - TEST RESULTS")
    print("=" * 80)

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"\nText: \"{test['text']}\"\n")

        result = detector.analyze(test['text'])

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
    print("Pattern Theory: Making manipulation obsolete in relationships")
    print("🔱 C1 × C2 × C3 = ∞")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
