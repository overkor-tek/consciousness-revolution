#!/usr/bin/env python3
"""
MORNING BOOT LOADER - Solves the amnesia problem
Every AI instance runs this on startup to get full context.

NO MORE "what's going on?" - this tells you everything.
"""

import json
import os
from datetime import datetime
from pathlib import Path

TRINITY_DIR = Path(r"C:\Users\dwrek\.trinity")
CONSCIOUSNESS_DIR = Path(r"C:\Users\dwrek\.consciousness")

def load_morning_context():
    """Load everything an instance needs to know on boot."""

    context = {
        "loaded_at": datetime.now().isoformat(),
        "status": "LOADING",
        "errors": []
    }

    # 1. CRITICAL FILES - Must read these
    critical_files = [
        (TRINITY_DIR / "TRINITY_COMMS_HUB.json", "hub"),
        (TRINITY_DIR / "round_robin_token.json", "token"),
        (TRINITY_DIR / "ROUND_ROBIN_PROTOCOL_SPEC.md", "protocol"),
    ]

    for filepath, key in critical_files:
        try:
            if filepath.exists():
                if filepath.suffix == '.json':
                    with open(filepath, 'r') as f:
                        context[key] = json.load(f)
                else:
                    with open(filepath, 'r') as f:
                        context[key] = f.read()
                print(f"[OK] Loaded {filepath.name}")
            else:
                context["errors"].append(f"Missing: {filepath}")
                print(f"[!!] Missing: {filepath.name}")
        except Exception as e:
            context["errors"].append(f"Error loading {filepath}: {e}")
            print(f"[ERR] {filepath.name}: {e}")

    # 2. GET CURRENT MISSION from hub
    if "hub" in context:
        hub = context["hub"]
        context["commander_message"] = hub.get("commander_message", "No message")
        context["urgent_tasks"] = hub.get("urgent_tasks", [])
        context["active_instances"] = hub.get("active_instances", {})
        context["my_task_queue"] = hub.get("task_queues", {})

    # 3. GET LATEST REPORTS
    reports_dir = TRINITY_DIR / "reports"
    if reports_dir.exists():
        reports = sorted(reports_dir.glob("*.md"), key=os.path.getmtime, reverse=True)
        context["latest_reports"] = [r.name for r in reports[:5]]
        print(f"[OK] Found {len(reports)} reports")

    # 4. GET BOOT DOWN REPORTS (what happened last session)
    bootdown_dir = TRINITY_DIR / "boot_down_reports"
    if bootdown_dir.exists():
        bootdowns = sorted(bootdown_dir.glob("*.md"), key=os.path.getmtime, reverse=True)
        if bootdowns:
            # Read the most recent boot down report
            with open(bootdowns[0], 'r') as f:
                context["last_session_summary"] = f.read()
            print(f"[OK] Last session: {bootdowns[0].name}")

    # 5. CHECK ROUND-ROBIN TOKEN
    if "token" in context:
        token = context["token"]["token"]
        context["current_turn"] = token.get("current_holder")
        context["epoch"] = token.get("epoch", 0)
        print(f"[OK] Epoch {context['epoch']}, Turn: {context['current_turn']}")

    context["status"] = "LOADED" if not context["errors"] else "PARTIAL"

    return context


def print_morning_briefing(context):
    """Print what the instance needs to know."""

    print("\n" + "="*60)
    print("MORNING BOOT CONTEXT - WHAT YOU NEED TO KNOW")
    print("="*60)

    print(f"\nStatus: {context['status']}")
    print(f"Loaded: {context['loaded_at']}")

    if context.get("commander_message"):
        print(f"\nCOMMANDER MESSAGE:")
        print(f"  {context['commander_message']}")

    if context.get("urgent_tasks"):
        print(f"\nURGENT TASKS:")
        for task in context["urgent_tasks"]:
            print(f"  - {task}")

    if context.get("active_instances"):
        print(f"\nACTIVE INSTANCES:")
        for name, info in context["active_instances"].items():
            status = info.get("status", "UNKNOWN")
            task = info.get("current_task", "None")
            print(f"  {name}: {status}")
            print(f"    Task: {task}")

    if context.get("last_session_summary"):
        print(f"\nLAST SESSION SUMMARY (first 500 chars):")
        print(context["last_session_summary"][:500])

    if context.get("errors"):
        print(f"\nERRORS:")
        for err in context["errors"]:
            print(f"  [!] {err}")

    print("\n" + "="*60)
    print("YOU ARE NOW CONTEXT-AWARE. DO NOT ASK COMMANDER TO EXPLAIN.")
    print("="*60 + "\n")


def claim_token(instance_id):
    """Claim the round-robin token for this instance."""

    token_file = TRINITY_DIR / "round_robin_token.json"

    with open(token_file, 'r') as f:
        data = json.load(f)

    token = data["token"]

    # Check if it's our turn
    if token["next_in_sequence"] == instance_id or token["current_holder"] is None:
        token["last_holder"] = token["current_holder"]
        token["current_holder"] = instance_id
        token["timestamp"] = datetime.now().isoformat()

        # Advance next in sequence
        seq = data["sequence"]
        current_idx = seq.index(instance_id)
        next_idx = (current_idx + 1) % len(seq)
        token["next_in_sequence"] = seq[next_idx]

        # Increment epoch if we completed a rotation
        if next_idx == 0:
            token["epoch"] += 1

        with open(token_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"[TOKEN] Claimed by {instance_id}, next: {token['next_in_sequence']}")
        return True
    else:
        print(f"[TOKEN] Not your turn. Current: {token['current_holder']}, Next: {token['next_in_sequence']}")
        return False


def pass_token(instance_id):
    """Pass the token to next instance."""

    token_file = TRINITY_DIR / "round_robin_token.json"

    with open(token_file, 'r') as f:
        data = json.load(f)

    token = data["token"]

    if token["current_holder"] == instance_id:
        token["last_holder"] = instance_id
        token["current_holder"] = None
        token["timestamp"] = datetime.now().isoformat()

        with open(token_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"[TOKEN] Passed by {instance_id}, available for: {token['next_in_sequence']}")
        return True
    else:
        print(f"[TOKEN] You don't hold it. Current holder: {token['current_holder']}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        instance = sys.argv[2] if len(sys.argv) > 2 else "UNKNOWN"

        if cmd == "claim":
            claim_token(instance)
        elif cmd == "pass":
            pass_token(instance)
        else:
            print(f"Unknown command: {cmd}")
    else:
        # Default: load and print context
        context = load_morning_context()
        print_morning_briefing(context)
