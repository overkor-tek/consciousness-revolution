#!/usr/bin/env python3
"""
CREDIT MONITOR - API Credit Exhaustion Detection & Handoff System
Monitors for credit exhaustion signals and triggers automatic handoff to next PC
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import deque
import logging

# Configuration
REPO_PATH = Path.home() / "100X_DEPLOYMENT"
CREDIT_STATE_FILE = REPO_PATH / ".trinity" / "credit_state.json"
LOG_FILE = REPO_PATH / ".trinity" / "logs" / "credit_monitor.log"
HANDOFF_DIR = REPO_PATH / ".trinity" / "handoff"

# Monitoring thresholds
RATE_LIMIT_THRESHOLD = 3  # Number of rate limit errors before handoff
SLOW_RESPONSE_THRESHOLD = 10.0  # Seconds - response slower than this triggers warning
CONSECUTIVE_SLOW_THRESHOLD = 5  # Number of consecutive slow responses before handoff
ERROR_RATE_THRESHOLD = 0.3  # 30% error rate triggers handoff

# PC rotation order
PC_ROTATION = ["PC1", "PC2", "PC3"]

# Computer identity
COMPUTER_NAME = os.environ.get("COMPUTERNAME", "UNKNOWN")
if "MSMCFH2" in COMPUTER_NAME.upper():
    MY_ID = "PC2"
elif "S72LRRO" in COMPUTER_NAME.upper():
    MY_ID = "PC3"
elif "dwrek" in COMPUTER_NAME.lower():
    MY_ID = "PC1"
else:
    MY_ID = "UNKNOWN"

# Setup logging
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class CreditMonitor:
    def __init__(self):
        self.rate_limit_count = 0
        self.slow_response_count = 0
        self.error_count = 0
        self.success_count = 0
        self.response_times = deque(maxlen=100)  # Last 100 response times
        self.recent_errors = deque(maxlen=50)    # Last 50 errors

        # Load state if exists
        self.load_state()

    def load_state(self):
        """Load previous monitoring state"""
        if CREDIT_STATE_FILE.exists():
            try:
                with open(CREDIT_STATE_FILE, 'r') as f:
                    state = json.load(f)
                    self.rate_limit_count = state.get('rate_limit_count', 0)
                    self.slow_response_count = state.get('slow_response_count', 0)
                    self.error_count = state.get('error_count', 0)
                    self.success_count = state.get('success_count', 0)
                    logging.info("Loaded previous credit monitor state")
            except Exception as e:
                logging.error(f"Failed to load state: {e}")

    def save_state(self):
        """Save current monitoring state"""
        CREDIT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

        state = {
            'pc': MY_ID,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'rate_limit_count': self.rate_limit_count,
            'slow_response_count': self.slow_response_count,
            'error_count': self.error_count,
            'success_count': self.success_count,
            'error_rate': self.get_error_rate(),
            'avg_response_time': self.get_avg_response_time(),
            'status': self.get_status()
        }

        try:
            with open(CREDIT_STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logging.error(f"Failed to save state: {e}")

    def record_rate_limit(self):
        """Record a rate limit error"""
        self.rate_limit_count += 1
        self.error_count += 1
        self.recent_errors.append({
            'type': 'rate_limit',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })

        logging.warning(f"Rate limit detected! Count: {self.rate_limit_count}")

        if self.rate_limit_count >= RATE_LIMIT_THRESHOLD:
            logging.critical(f"Rate limit threshold reached ({RATE_LIMIT_THRESHOLD})!")
            return True  # Trigger handoff

        return False

    def record_response_time(self, response_time):
        """Record API response time"""
        self.response_times.append(response_time)

        if response_time > SLOW_RESPONSE_THRESHOLD:
            self.slow_response_count += 1
            logging.warning(f"Slow response detected: {response_time:.2f}s")

            if self.slow_response_count >= CONSECUTIVE_SLOW_THRESHOLD:
                logging.critical(f"Consecutive slow responses threshold reached!")
                return True  # Trigger handoff
        else:
            # Reset slow count on fast response
            self.slow_response_count = max(0, self.slow_response_count - 1)

        return False

    def record_success(self):
        """Record successful API call"""
        self.success_count += 1
        # Gradually decrease error indicators on success
        if self.rate_limit_count > 0:
            self.rate_limit_count -= 0.1
        if self.slow_response_count > 0:
            self.slow_response_count -= 0.1

    def record_error(self, error_type="unknown"):
        """Record general API error"""
        self.error_count += 1
        self.recent_errors.append({
            'type': error_type,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })

        if self.get_error_rate() > ERROR_RATE_THRESHOLD:
            logging.critical(f"Error rate threshold exceeded: {self.get_error_rate():.2%}")
            return True  # Trigger handoff

        return False

    def get_error_rate(self):
        """Calculate recent error rate"""
        total = self.error_count + self.success_count
        if total == 0:
            return 0.0
        return self.error_count / total

    def get_avg_response_time(self):
        """Calculate average response time"""
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

    def get_status(self):
        """Get current credit status"""
        if self.rate_limit_count >= RATE_LIMIT_THRESHOLD:
            return "EXHAUSTED"
        elif self.rate_limit_count >= RATE_LIMIT_THRESHOLD * 0.7:
            return "CRITICAL"
        elif self.slow_response_count >= CONSECUTIVE_SLOW_THRESHOLD * 0.7:
            return "WARNING"
        elif self.get_error_rate() > ERROR_RATE_THRESHOLD * 0.7:
            return "WARNING"
        else:
            return "HEALTHY"

    def check_exhaustion(self):
        """Check if credits are exhausted"""
        status = self.get_status()
        return status in ["EXHAUSTED", "CRITICAL"]

def get_next_pc():
    """Determine next PC in rotation"""
    try:
        current_index = PC_ROTATION.index(MY_ID)
        next_index = (current_index + 1) % len(PC_ROTATION)
        return PC_ROTATION[next_index]
    except ValueError:
        # If MY_ID not in rotation, default to PC1
        return "PC1"

def save_handoff_state(task_queue=None, current_work=None):
    """Save current state for handoff"""
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)

    handoff_state = {
        'from_pc': MY_ID,
        'to_pc': get_next_pc(),
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'reason': 'credit_exhaustion',
        'task_queue': task_queue or [],
        'current_work': current_work or {},
        'credit_state': {
            'rate_limit_count': monitor.rate_limit_count,
            'error_rate': monitor.get_error_rate(),
            'avg_response_time': monitor.get_avg_response_time()
        }
    }

    handoff_file = HANDOFF_DIR / f"handoff_{MY_ID}_to_{get_next_pc()}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

    try:
        with open(handoff_file, 'w') as f:
            json.dump(handoff_state, f, indent=2)
        logging.info(f"Handoff state saved to {handoff_file}")
        return handoff_file
    except Exception as e:
        logging.error(f"Failed to save handoff state: {e}")
        return None

def trigger_handoff(next_pc=None):
    """Trigger handoff to next PC"""
    if next_pc is None:
        next_pc = get_next_pc()

    logging.critical(f"TRIGGERING HANDOFF: {MY_ID} → {next_pc}")

    # Save current state
    handoff_file = save_handoff_state()

    if not handoff_file:
        logging.error("Failed to save handoff state - aborting handoff")
        return False

    # Commit handoff state to git
    try:
        os.chdir(REPO_PATH)
        subprocess.run(['git', 'add', str(handoff_file.relative_to(REPO_PATH))], timeout=10)
        subprocess.run(['git', 'commit', '-m', f'handoff: {MY_ID} → {next_pc} (credit exhaustion)'], timeout=10)
        subprocess.run(['git', 'push'], timeout=30)
        logging.info("Handoff state committed to git")
    except Exception as e:
        logging.error(f"Failed to commit handoff state: {e}")

    # Wake next PC using auto-wake system
    try:
        wake_script = REPO_PATH / ".trinity" / "automation" / "AUTO_WAKE_DAEMON.py"
        if wake_script.exists():
            result = subprocess.run(
                ['python', str(wake_script), '--send', next_pc,
                 '--task', 'credit_handoff',
                 '--message', f'Taking over from {MY_ID} due to credit exhaustion'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logging.info(f"Wake signal sent to {next_pc}")
            else:
                logging.error(f"Failed to send wake signal: {result.stderr}")
        else:
            logging.warning("AUTO_WAKE_DAEMON.py not found - skipping wake")
    except Exception as e:
        logging.error(f"Failed to wake next PC: {e}")

    # Create handoff marker in heartbeat
    heartbeat_file = REPO_PATH / ".trinity" / "heartbeat" / f"{MY_ID}.json"
    try:
        with open(heartbeat_file, 'w') as f:
            json.dump({
                'pc': MY_ID,
                'status': 'handoff_initiated',
                'to_pc': next_pc,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'reason': 'credit_exhaustion'
            }, f, indent=2)
        logging.info(f"Handoff marker created in heartbeat")
    except Exception as e:
        logging.error(f"Failed to create handoff marker: {e}")

    return True

def check_for_handoff_signal():
    """Check if there's an incoming handoff for this PC"""
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)

    # Look for handoff files directed to this PC
    for handoff_file in HANDOFF_DIR.glob(f"handoff_*_to_{MY_ID}_*.json"):
        try:
            with open(handoff_file, 'r') as f:
                handoff = json.load(f)

            logging.info(f"Incoming handoff detected from {handoff.get('from_pc')}")

            # Process handoff (load task queue, resume work)
            process_incoming_handoff(handoff, handoff_file)

            return True
        except Exception as e:
            logging.error(f"Failed to process handoff: {e}")

    return False

def process_incoming_handoff(handoff, handoff_file):
    """Process incoming handoff from another PC"""
    from_pc = handoff.get('from_pc', 'unknown')
    task_queue = handoff.get('task_queue', [])
    current_work = handoff.get('current_work', {})

    logging.info(f"Processing handoff from {from_pc}")
    logging.info(f"Task queue: {len(task_queue)} tasks")
    logging.info(f"Current work: {current_work}")

    # Archive handoff file
    archive_dir = HANDOFF_DIR / "processed"
    archive_dir.mkdir(parents=True, exist_ok=True)

    try:
        archive_file = archive_dir / handoff_file.name
        handoff_file.rename(archive_file)
        logging.info(f"Handoff archived to {archive_file}")
    except Exception as e:
        logging.error(f"Failed to archive handoff: {e}")

    # Reset credit monitor state (fresh start)
    global monitor
    monitor = CreditMonitor()
    monitor.save_state()

    logging.info("Handoff processing complete - ready for work")

def generate_dashboard_data():
    """Generate data for credit dashboard"""
    return {
        'pc': MY_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'status': monitor.get_status(),
        'rate_limit_count': monitor.rate_limit_count,
        'slow_response_count': monitor.slow_response_count,
        'error_rate': monitor.get_error_rate(),
        'success_count': monitor.success_count,
        'error_count': monitor.error_count,
        'avg_response_time': monitor.get_avg_response_time(),
        'recent_errors': list(monitor.recent_errors)[-10:],  # Last 10 errors
        'next_pc': get_next_pc()
    }

def update_dashboard():
    """Update credit dashboard with current data"""
    dashboard_file = REPO_PATH / ".trinity" / "dashboards" / "credit_status.json"
    dashboard_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Load existing dashboard data
        if dashboard_file.exists():
            with open(dashboard_file, 'r') as f:
                dashboard = json.load(f)
        else:
            dashboard = {'pcs': {}}

        # Update this PC's data
        dashboard['pcs'][MY_ID] = generate_dashboard_data()
        dashboard['last_update'] = datetime.utcnow().isoformat() + 'Z'

        # Write updated dashboard
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard, f, indent=2)

        logging.debug("Dashboard updated")
    except Exception as e:
        logging.error(f"Failed to update dashboard: {e}")

# Global monitor instance
monitor = CreditMonitor()

def monitor_loop(interval=60):
    """Main monitoring loop"""
    logging.info(f"CREDIT MONITOR started for {MY_ID}")
    logging.info(f"Monitoring interval: {interval}s")

    # Check for incoming handoff on startup
    if check_for_handoff_signal():
        logging.info("Incoming handoff processed - starting with fresh state")

    last_dashboard_update = 0

    while True:
        try:
            current_time = time.time()

            # Update dashboard every 30 seconds
            if current_time - last_dashboard_update >= 30:
                update_dashboard()
                monitor.save_state()
                last_dashboard_update = current_time

            # Check for exhaustion
            if monitor.check_exhaustion():
                logging.critical("CREDIT EXHAUSTION DETECTED!")
                trigger_handoff()

                # After handoff, pause monitoring to allow next PC to take over
                logging.info("Handoff complete - pausing monitoring for 5 minutes")
                time.sleep(300)  # 5 minute pause

                # Reset monitor after pause
                monitor.rate_limit_count = 0
                monitor.slow_response_count = 0
                monitor.save_state()

            # Sleep before next check
            time.sleep(interval)

        except KeyboardInterrupt:
            logging.info("Monitor stopped by user")
            break
        except Exception as e:
            logging.error(f"Error in monitor loop: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Credit Exhaustion Monitor and Handoff System")
    parser.add_argument("--interval", type=int, default=60, help="Monitoring interval in seconds")
    parser.add_argument("--record-rate-limit", action="store_true", help="Record a rate limit error")
    parser.add_argument("--record-slow", type=float, help="Record slow response time (seconds)")
    parser.add_argument("--record-success", action="store_true", help="Record successful call")
    parser.add_argument("--status", action="store_true", help="Show current credit status")
    parser.add_argument("--force-handoff", action="store_true", help="Force immediate handoff")

    args = parser.parse_args()

    if args.record_rate_limit:
        trigger = monitor.record_rate_limit()
        print(f"Rate limit recorded. Trigger handoff: {trigger}")
        monitor.save_state()
        if trigger:
            trigger_handoff()
        sys.exit(0)

    if args.record_slow:
        trigger = monitor.record_response_time(args.record_slow)
        print(f"Slow response recorded ({args.record_slow}s). Trigger handoff: {trigger}")
        monitor.save_state()
        if trigger:
            trigger_handoff()
        sys.exit(0)

    if args.record_success:
        monitor.record_success()
        print("Success recorded")
        monitor.save_state()
        sys.exit(0)

    if args.status:
        print(f"\nCredit Status for {MY_ID}:")
        print(f"  Status: {monitor.get_status()}")
        print(f"  Rate Limits: {monitor.rate_limit_count}")
        print(f"  Slow Responses: {monitor.slow_response_count}")
        print(f"  Error Rate: {monitor.get_error_rate():.2%}")
        print(f"  Avg Response Time: {monitor.get_avg_response_time():.2f}s")
        print(f"  Next PC: {get_next_pc()}")
        print()
        sys.exit(0)

    if args.force_handoff:
        print(f"Forcing handoff from {MY_ID} to {get_next_pc()}")
        trigger_handoff()
        sys.exit(0)

    # Default: run monitoring loop
    monitor_loop(args.interval)
