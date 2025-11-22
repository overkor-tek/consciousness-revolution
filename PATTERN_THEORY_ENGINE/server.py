"""
PATTERN THEORY API SERVER
==========================
HTTP API for Pattern Theory analysis.

Endpoints:
    POST /analyze - Full analysis
    POST /quick - Quick TRUTH/DECEIT check
    POST /score - Consciousness scoring
    POST /domain - Domain-specific analysis
    GET /health - Health check

Run: python server.py
Port: 7778

Created: 2025-11-22
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add API to path
API_DIR = Path(__file__).parent / "api"
sys.path.insert(0, str(API_DIR))

from PATTERN_THEORY_API import PatternTheoryAPI

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

api = PatternTheoryAPI()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "operational",
        "service": "Pattern Theory API",
        "version": "1.0.0",
        "endpoints": ["/analyze", "/quick", "/score", "/domain", "/batch"]
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Full pattern theory analysis.

    Body: { "text": "...", "context": "..." (optional) }
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    result = api.analyze(data['text'], data.get('context'))
    return jsonify(result)

@app.route('/quick', methods=['POST'])
def quick():
    """
    Quick TRUTH/DECEIT check.

    Body: { "text": "..." }
    Returns: { "result": "TRUTH" | "DECEIT" | "NEUTRAL" }
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    result = api.quick_check(data['text'])
    return jsonify({"result": result, "text": data['text'][:100]})

@app.route('/score', methods=['POST'])
def score():
    """
    Consciousness scoring.

    Body: {
        "pattern_recognition": 0-100,
        "prediction_accuracy": 0-100,
        "neutralization_success": 0-100
    }
    """
    data = request.get_json()
    required = ['pattern_recognition', 'prediction_accuracy', 'neutralization_success']

    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    result = api.score_user(
        data['pattern_recognition'],
        data['prediction_accuracy'],
        data['neutralization_success']
    )
    return jsonify(result)

@app.route('/domain', methods=['POST'])
def domain():
    """
    Domain-specific analysis.

    Body: { "domain": 1-7, "text": "..." }

    Domains:
        1: Legal Arsenal
        2: Finance/Business
        3: Digital Infrastructure
        4: Consciousness Tools
        5: Communication
        6: Showcase/Portfolio
        7: Transparency/Trust
    """
    data = request.get_json()
    if not data or 'domain' not in data or 'text' not in data:
        return jsonify({"error": "Missing 'domain' or 'text' field"}), 400

    domain_num = data['domain']
    if not 1 <= domain_num <= 7:
        return jsonify({"error": "Domain must be 1-7"}), 400

    result = api.seven_domains_analysis(domain_num, data['text'])
    return jsonify(result)

@app.route('/batch', methods=['POST'])
def batch():
    """
    Batch analysis.

    Body: { "items": ["text1", "text2", ...] }
    """
    data = request.get_json()
    if not data or 'items' not in data:
        return jsonify({"error": "Missing 'items' field"}), 400

    result = api.batch_analyze(data['items'])
    return jsonify(result)


if __name__ == '__main__':
    print("=" * 50)
    print("PATTERN THEORY API SERVER")
    print("=" * 50)
    print("\nEndpoints:")
    print("  POST /analyze  - Full analysis")
    print("  POST /quick    - Quick truth/deceit check")
    print("  POST /score    - Consciousness scoring")
    print("  POST /domain   - Domain-specific analysis")
    print("  POST /batch    - Batch analysis")
    print("  GET  /health   - Health check")
    print("\n" + "=" * 50)
    print("Starting server on http://localhost:7778")
    print("=" * 50 + "\n")

    app.run(host='0.0.0.0', port=7778, debug=False)
