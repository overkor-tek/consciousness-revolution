"""
AI APP GENERATOR API
=====================
REST API for AI App Generation service.

Endpoints:
- POST /generate - Generate app from description
- GET /health - Health check
- GET /stats - Generation statistics

Created: 2025-11-22
Trinity Build: Phase 2
"""

import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# Add paths
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/AI_APP_GENERATOR")
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/AI_APP_GENERATOR/core")
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/AI_APP_GENERATOR/generators")
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/PATTERN_THEORY_ENGINE")
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/PATTERN_THEORY_ENGINE/core")
sys.path.insert(0, "C:/Users/dwrek/100X_DEPLOYMENT/PATTERN_THEORY_ENGINE/projection")

from AI_APP_GENERATOR import AIAppGenerator
from CODE_GENERATOR import CodeGenerator
from DATABASE_DESIGNER import DatabaseDesigner
from TEST_GENERATOR import TestGenerator

app = Flask(__name__)
CORS(app)

# Initialize generators
app_generator = AIAppGenerator()
code_generator = CodeGenerator()
db_designer = DatabaseDesigner()
test_generator = TestGenerator()

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "AI App Generator API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/stats')
def stats():
    """Get generation statistics."""
    return jsonify({
        "apps_generated": app_generator.generation_count,
        "code_files_generated": code_generator.generation_count,
        "databases_designed": db_designer.design_count,
        "test_suites_generated": test_generator.generation_count,
        "uptime": datetime.now().isoformat()
    })

@app.route('/generate', methods=['POST'])
def generate_app():
    """
    Generate complete app from description.

    Request body:
    {
        "description": "Build me a todo app with user auth"
    }
    """
    try:
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({"error": "Missing 'description' field"}), 400

        description = data['description']

        # Generate app
        result = app_generator.generate(description)

        # Get additional components
        spec_dict = {
            "name": result.spec.name,
            "features": result.spec.features
        }

        code_result = code_generator.generate_all(spec_dict)
        db_schema = db_designer.design(spec_dict)
        test_suite = test_generator.generate_suite(spec_dict)

        return jsonify({
            "success": True,
            "app": app_generator.to_dict(result),
            "code": {
                "frontend_files": len(code_result["frontend"]),
                "backend_files": len(code_result["backend"]),
                "files": [f.filename for f in code_result["frontend"] + code_result["backend"]]
            },
            "database": {
                "tables": len(db_schema.tables),
                "table_names": [t.name for t in db_schema.tables]
            },
            "tests": test_generator.to_dict(test_suite)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/generate/code', methods=['POST'])
def generate_code():
    """Generate just code from spec."""
    try:
        data = request.get_json()
        spec = {
            "name": data.get("name", "app"),
            "features": data.get("features", ["basic_crud"])
        }

        result = code_generator.generate_all(spec)

        return jsonify({
            "success": True,
            "frontend": [
                {"filename": f.filename, "lines": f.lines, "language": f.language}
                for f in result["frontend"]
            ],
            "backend": [
                {"filename": f.filename, "lines": f.lines, "language": f.language}
                for f in result["backend"]
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate/database', methods=['POST'])
def generate_database():
    """Generate database schema from spec."""
    try:
        data = request.get_json()
        spec = {
            "name": data.get("name", "app"),
            "features": data.get("features", ["basic_crud"])
        }

        schema = db_designer.design(spec)

        return jsonify({
            "success": True,
            "schema": db_designer.to_dict(schema)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate/tests', methods=['POST'])
def generate_tests():
    """Generate test suite from spec."""
    try:
        data = request.get_json()
        spec = {
            "name": data.get("name", "app"),
            "features": data.get("features", ["basic_crud"])
        }

        suite = test_generator.generate_suite(spec)

        return jsonify({
            "success": True,
            "suite": test_generator.to_dict(suite),
            "content_preview": test_generator.to_file_content(suite)[:1000]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("=" * 60)
    print("AI APP GENERATOR API")
    print("=" * 60)
    print(f"Starting on http://localhost:5001")
    print("Endpoints:")
    print("  POST /generate - Generate complete app")
    print("  POST /generate/code - Generate code only")
    print("  POST /generate/database - Generate schema only")
    print("  POST /generate/tests - Generate tests only")
    print("  GET /health - Health check")
    print("  GET /stats - Statistics")
    print("=" * 60)

    app.run(debug=True, port=5001, host='0.0.0.0')
