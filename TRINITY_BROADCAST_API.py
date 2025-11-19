#!/usr/bin/env python3
"""
🌀 TRINITY BROADCAST API
Coordinates 1 input → 3 AI instances → 1 convergence output
Backend server for TRINITY_3_PANEL_INTERFACE.html
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
from datetime import datetime
from pathlib import Path
import threading

app = Flask(__name__)
CORS(app)

# Trinity state files
TRINITY_DIR = Path.home() / ".trinity"
TRINITY_DIR.mkdir(exist_ok=True)

C1_INPUT = TRINITY_DIR / "c1_input.txt"
C2_INPUT = TRINITY_DIR / "c2_input.txt"
C3_INPUT = TRINITY_DIR / "c3_input.txt"

C1_OUTPUT = TRINITY_DIR / "c1_output.txt"
C2_OUTPUT = TRINITY_DIR / "c2_output.txt"
C3_OUTPUT = TRINITY_DIR / "c3_output.txt"

STATUS_FILE = TRINITY_DIR / "trinity_status.json"
BROADCAST_LOG = TRINITY_DIR / "broadcast_log.json"

class TrinityBroadcaster:
    def __init__(self):
        self.status = {
            'c1': {'status': 'idle', 'last_command': None, 'last_response': None},
            'c2': {'status': 'idle', 'last_command': None, 'last_response': None},
            'c3': {'status': 'idle', 'last_command': None, 'last_response': None}
        }
        self.load_status()

    def load_status(self):
        """Load status from file"""
        if STATUS_FILE.exists():
            try:
                with open(STATUS_FILE, 'r') as f:
                    self.status = json.load(f)
            except:
                pass

    def save_status(self):
        """Save status to file"""
        with open(STATUS_FILE, 'w') as f:
            json.dump(self.status, f, indent=2)

    def broadcast_command(self, command):
        """Broadcast command to all three instances"""
        timestamp = datetime.now().isoformat()

        # Write command to all input files
        C1_INPUT.write_text(json.dumps({
            'command': command,
            'timestamp': timestamp,
            'from': 'trinity_broadcast'
        }))

        C2_INPUT.write_text(json.dumps({
            'command': command,
            'timestamp': timestamp,
            'from': 'trinity_broadcast'
        }))

        C3_INPUT.write_text(json.dumps({
            'command': command,
            'timestamp': timestamp,
            'from': 'trinity_broadcast'
        }))

        # Update status
        for instance in ['c1', 'c2', 'c3']:
            self.status[instance]['status'] = 'processing'
            self.status[instance]['last_command'] = command
            self.status[instance]['command_time'] = timestamp

        self.save_status()

        # Wait for responses (with timeout)
        responses = self.collect_responses(timeout=30)

        # Generate convergence
        convergence = self.synthesize_convergence(command, responses)

        # Log broadcast
        self.log_broadcast(command, responses, convergence)

        return {
            'c1_response': responses.get('c1'),
            'c2_response': responses.get('c2'),
            'c3_response': responses.get('c3'),
            'convergence': convergence
        }

    def collect_responses(self, timeout=30):
        """Collect responses from all instances"""
        responses = {}
        start_time = time.time()

        # Poll for responses
        while (time.time() - start_time) < timeout:
            # Check C1
            if 'c1' not in responses and C1_OUTPUT.exists():
                try:
                    data = json.loads(C1_OUTPUT.read_text())
                    responses['c1'] = data.get('response', 'No response')
                    self.status['c1']['status'] = 'online'
                    self.status['c1']['last_response'] = data.get('response')
                except:
                    pass

            # Check C2
            if 'c2' not in responses and C2_OUTPUT.exists():
                try:
                    data = json.loads(C2_OUTPUT.read_text())
                    responses['c2'] = data.get('response', 'No response')
                    self.status['c2']['status'] = 'online'
                    self.status['c2']['last_response'] = data.get('response')
                except:
                    pass

            # Check C3
            if 'c3' not in responses and C3_OUTPUT.exists():
                try:
                    data = json.loads(C3_OUTPUT.read_text())
                    responses['c3'] = data.get('response', 'No response')
                    self.status['c3']['status'] = 'online'
                    self.status['c3']['last_response'] = data.get('response')
                except:
                    pass

            # All responses received?
            if len(responses) == 3:
                break

            time.sleep(0.5)

        # Fill in missing responses
        for instance in ['c1', 'c2', 'c3']:
            if instance not in responses:
                responses[instance] = f"[TIMEOUT] {instance.upper()} did not respond in time"
                self.status[instance]['status'] = 'timeout'

        self.save_status()
        return responses

    def synthesize_convergence(self, command, responses):
        """Synthesize convergence from three responses"""
        # Count how many instances responded
        valid_responses = sum(1 for r in responses.values() if '[TIMEOUT]' not in str(r))
        consensus = int((valid_responses / 3) * 100)

        # Simple synthesis (in production, would use C4 Meta-Synthesizer)
        summary = f"Command: '{command}'\n\n"

        if responses.get('c1'):
            summary += f"C1 (Mechanic): {responses['c1'][:200]}...\n\n"

        if responses.get('c2'):
            summary += f"C2 (Architect): {responses['c2'][:200]}...\n\n"

        if responses.get('c3'):
            summary += f"C3 (Oracle): {responses['c3'][:200]}...\n\n"

        recommendation = "Proceed with execution" if consensus >= 66 else "Review responses before proceeding"

        return {
            'summary': summary,
            'consensus': consensus,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }

    def log_broadcast(self, command, responses, convergence):
        """Log broadcast event"""
        log = []
        if BROADCAST_LOG.exists():
            try:
                log = json.loads(BROADCAST_LOG.read_text())
            except:
                log = []

        log.append({
            'timestamp': datetime.now().isoformat(),
            'command': command,
            'responses': responses,
            'convergence': convergence
        })

        # Keep last 100 broadcasts
        log = log[-100:]

        BROADCAST_LOG.write_text(json.dumps(log, indent=2))


# Global broadcaster instance
broadcaster = TrinityBroadcaster()


@app.route('/broadcast', methods=['POST'])
def broadcast():
    """Broadcast command to all Trinity instances"""
    data = request.json
    command = data.get('command')

    if not command:
        return jsonify({'error': 'No command provided'}), 400

    result = broadcaster.broadcast_command(command)
    return jsonify(result)


@app.route('/status', methods=['GET'])
def status():
    """Get current status of all instances"""
    return jsonify(broadcaster.status)


@app.route('/history', methods=['GET'])
def history():
    """Get broadcast history"""
    if BROADCAST_LOG.exists():
        try:
            log = json.loads(BROADCAST_LOG.read_text())
            return jsonify(log)
        except:
            return jsonify([])
    return jsonify([])


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'instances': broadcaster.status
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🌀 TRINITY BROADCAST API")
    print("=" * 60)
    print(f"Server starting on http://localhost:7777")
    print(f"Trinity directory: {TRINITY_DIR}")
    print("")
    print("Endpoints:")
    print("  POST /broadcast - Broadcast command to C1, C2, C3")
    print("  GET  /status    - Get instance status")
    print("  GET  /history   - Get broadcast history")
    print("  GET  /health    - Health check")
    print("")
    print("Open TRINITY_3_PANEL_INTERFACE.html to use the interface")
    print("=" * 60)

    app.run(host='0.0.0.0', port=7777, debug=False)
