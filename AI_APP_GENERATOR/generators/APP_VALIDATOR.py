"""
APP VALIDATOR - Pattern Theory Application Validation
======================================================
Validates generated applications using Pattern Theory.

Checks: Security, architecture, code quality, documentation

Created: 2025-11-22
Trinity Build: Phase 2
"""

import sys
from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

# Add Pattern Theory Engine to path
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/PATTERN_THEORY_ENGINE")
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/PATTERN_THEORY_ENGINE/core")

try:
    from PATTERN_THEORY_ENGINE import PatternTheoryEngine
    from MANIPULATION_DETECTOR import ManipulationDetector
    PATTERN_THEORY_AVAILABLE = True
except ImportError:
    PATTERN_THEORY_AVAILABLE = False

@dataclass
class ValidationResult:
    """Validation result"""
    category: str
    passed: bool
    score: float
    issues: List[str]
    recommendations: List[str]

@dataclass
class AppValidation:
    """Complete app validation"""
    overall_score: float
    passed: bool
    results: List[ValidationResult]
    pattern_theory_score: float
    golden_ratio_alignment: float

class AppValidator:
    """
    Validates applications using Pattern Theory principles.
    """

    # Security patterns to check
    SECURITY_ISSUES = {
        "eval(": "Dangerous eval() usage - code injection risk",
        "exec(": "Dangerous exec() usage - code injection risk",
        "os.system(": "Shell command injection risk",
        "pickle.loads(": "Pickle deserialization vulnerability",
        "yaml.load(": "YAML deserialization vulnerability (use safe_load)",
        "SELECT * FROM": "SQL injection risk - parameterize queries",
        "innerHTML": "XSS vulnerability - use textContent",
        "dangerouslySetInnerHTML": "React XSS vulnerability"
    }

    # Architecture patterns
    GOOD_PATTERNS = [
        "def test_",  # Has tests
        "try:",  # Error handling
        "@app.route",  # Proper routing
        "import logging",  # Logging
        "class ",  # OOP structure
        "def __init__",  # Constructor
        "return jsonify",  # Proper API responses
    ]

    def __init__(self):
        self.validation_count = 0
        if PATTERN_THEORY_AVAILABLE:
            self.pattern_engine = PatternTheoryEngine()
            self.manipulation_detector = ManipulationDetector()
        else:
            self.pattern_engine = None
            self.manipulation_detector = None

    def validate_security(self, files: Dict[str, str]) -> ValidationResult:
        """Validate security of generated code."""
        issues = []
        recommendations = []

        for filename, content in files.items():
            for pattern, issue in self.SECURITY_ISSUES.items():
                if pattern in content:
                    issues.append(f"{filename}: {issue}")

        if not issues:
            return ValidationResult(
                category="security",
                passed=True,
                score=100,
                issues=[],
                recommendations=["All security checks passed"]
            )

        score = max(0, 100 - (len(issues) * 20))
        recommendations = [
            "Review and fix security issues",
            "Use parameterized queries for database",
            "Sanitize user input",
            "Use environment variables for secrets"
        ]

        return ValidationResult(
            category="security",
            passed=len(issues) == 0,
            score=score,
            issues=issues,
            recommendations=recommendations
        )

    def validate_architecture(self, files: Dict[str, str], spec: Dict[str, Any]) -> ValidationResult:
        """Validate application architecture."""
        issues = []
        good_patterns_found = 0
        all_content = " ".join(files.values())

        # Check for good patterns
        for pattern in self.GOOD_PATTERNS:
            if pattern in all_content:
                good_patterns_found += 1

        # Check file structure
        has_app = "app.py" in files
        has_requirements = "requirements.txt" in files
        has_tests = any("test" in f.lower() for f in files)

        if not has_app:
            issues.append("Missing main app.py file")
        if not has_requirements:
            issues.append("Missing requirements.txt")
        if not has_tests:
            issues.append("No test files found")

        score = min(100, (good_patterns_found / len(self.GOOD_PATTERNS)) * 100)
        if issues:
            score = max(0, score - (len(issues) * 15))

        recommendations = []
        if not has_tests:
            recommendations.append("Add comprehensive test suite")
        if good_patterns_found < 3:
            recommendations.append("Implement logging and error handling")

        return ValidationResult(
            category="architecture",
            passed=len(issues) == 0 and good_patterns_found >= 3,
            score=score,
            issues=issues,
            recommendations=recommendations if recommendations else ["Good architecture patterns detected"]
        )

    def validate_code_quality(self, files: Dict[str, str]) -> ValidationResult:
        """Validate code quality."""
        issues = []
        all_content = " ".join(files.values())

        # Check for documentation
        has_docstrings = '"""' in all_content or "'''" in all_content
        has_comments = "#" in all_content

        # Check for proper structure
        has_functions = "def " in all_content
        has_classes = "class " in all_content

        # Calculate score
        quality_points = sum([
            has_docstrings * 25,
            has_comments * 20,
            has_functions * 25,
            has_classes * 15,
            ("if __name__" in all_content) * 15
        ])

        if not has_docstrings:
            issues.append("Missing docstrings - add documentation to functions/classes")
        if not has_functions:
            issues.append("No functions defined - consider modular structure")

        recommendations = []
        if quality_points < 70:
            recommendations.append("Add docstrings to all functions and classes")
            recommendations.append("Use type hints for better code clarity")

        return ValidationResult(
            category="code_quality",
            passed=quality_points >= 60,
            score=quality_points,
            issues=issues,
            recommendations=recommendations if recommendations else ["Good code quality"]
        )

    def validate_with_pattern_theory(self, spec: Dict[str, Any]) -> ValidationResult:
        """Validate using Pattern Theory Engine."""
        if not PATTERN_THEORY_AVAILABLE:
            return ValidationResult(
                category="pattern_theory",
                passed=True,
                score=75,
                issues=["Pattern Theory Engine not available"],
                recommendations=["Install Pattern Theory Engine for full validation"]
            )

        description = spec.get("description", "")

        # Analyze with Pattern Theory
        pattern_result = self.pattern_engine.analyze(description)

        # Check for manipulation
        manip_result = self.manipulation_detector.detect(description)

        score = pattern_result.truth_score
        passed = pattern_result.algorithm == "Truth" and manip_result.m_score < 50

        issues = []
        if pattern_result.algorithm == "Deceit":
            issues.append(f"Pattern Theory detected deceit patterns (score: {score}%)")
        if manip_result.m_score >= 50:
            issues.append(f"High manipulation score detected: {manip_result.m_score}/100")

        recommendations = []
        if not passed:
            recommendations.append(pattern_result.recommended_action)
            if hasattr(manip_result, 'counter_strategies'):
                recommendations.extend(manip_result.counter_strategies[:2])
            elif hasattr(manip_result, 'counter_strategy'):
                recommendations.append(manip_result.counter_strategy)

        return ValidationResult(
            category="pattern_theory",
            passed=passed,
            score=score,
            issues=issues,
            recommendations=recommendations if recommendations else ["Pattern Theory validation passed"]
        )

    def calculate_golden_ratio_alignment(self, results: List[ValidationResult]) -> float:
        """Calculate Golden Ratio alignment of overall validation."""
        PHI = 1.618033988749895

        # Get scores
        scores = [r.score for r in results]
        if not scores:
            return 0.0

        avg_score = sum(scores) / len(scores)

        # Calculate alignment (how close to Golden Ratio proportions)
        alignment = 100 - abs(avg_score - (100 / PHI)) * PHI

        return max(0, min(100, alignment))

    def validate(self, files: Dict[str, str], spec: Dict[str, Any]) -> AppValidation:
        """
        Validate complete application.

        Args:
            files: Dictionary of filename -> content
            spec: App specification

        Returns:
            AppValidation with all results
        """
        self.validation_count += 1

        results = [
            self.validate_security(files),
            self.validate_architecture(files, spec),
            self.validate_code_quality(files),
            self.validate_with_pattern_theory(spec)
        ]

        # Calculate overall score
        overall_score = sum(r.score for r in results) / len(results)
        passed = all(r.passed for r in results)

        # Pattern Theory score
        pt_result = next((r for r in results if r.category == "pattern_theory"), None)
        pattern_theory_score = pt_result.score if pt_result else 0

        # Golden Ratio alignment
        golden_ratio = self.calculate_golden_ratio_alignment(results)

        return AppValidation(
            overall_score=overall_score,
            passed=passed,
            results=results,
            pattern_theory_score=pattern_theory_score,
            golden_ratio_alignment=golden_ratio
        )

    def to_dict(self, validation: AppValidation) -> Dict[str, Any]:
        """Convert validation to dictionary."""
        return {
            "overall_score": round(validation.overall_score, 2),
            "passed": validation.passed,
            "pattern_theory_score": round(validation.pattern_theory_score, 2),
            "golden_ratio_alignment": round(validation.golden_ratio_alignment, 2),
            "results": [
                {
                    "category": r.category,
                    "passed": r.passed,
                    "score": round(r.score, 2),
                    "issues": r.issues,
                    "recommendations": r.recommendations
                }
                for r in validation.results
            ]
        }


# Testing
if __name__ == "__main__":
    validator = AppValidator()

    print("=" * 60)
    print("APP VALIDATOR - TEST")
    print("=" * 60)

    # Sample files to validate
    files = {
        "app.py": '''"""Main application."""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        return jsonify({"status": "healthy"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
''',
        "requirements.txt": "flask>=2.0.0\n",
        "test_app.py": '''"""Tests."""
def test_health():
    assert True
'''
    }

    spec = {
        "name": "test_app",
        "description": "A test application for validation",
        "features": ["rest_api"]
    }

    validation = validator.validate(files, spec)
    result = validator.to_dict(validation)

    print(f"\nOverall Score: {result['overall_score']}%")
    print(f"Passed: {result['passed']}")
    print(f"Pattern Theory Score: {result['pattern_theory_score']}%")
    print(f"Golden Ratio Alignment: {result['golden_ratio_alignment']}%")

    print("\nResults by category:")
    for r in result['results']:
        status = "" if r['passed'] else ""
        print(f"  {status} {r['category']}: {r['score']}%")
        if r['issues']:
            for issue in r['issues']:
                print(f"     Issue: {issue}")

    print("\n" + "=" * 60)
    print("APP VALIDATOR OPERATIONAL")
    print("=" * 60)
