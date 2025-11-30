#!/usr/bin/env python3
"""
TRINITY WAKE TRIGGER
====================
Utility to send wake signals to Trinity instances.

Usage:
    # Simple wake with prompt
    python trinity_trigger.py C1T1 "Build a hello world script"
    
    # Wake with chain (C1T1 -> C2T1 -> C3T1)
    python trinity_trigger.py C1T1 "Start the build" --chain C2T1,C3T1
    
    # Echo test
    python trinity_trigger.py C1T1 --echo "Hello Trinity!"
    
    # Bash command
    python trinity_trigger.py C1T1 --bash "ls -la"
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

# Default Trinity base directory
TRINITY_BASE = Path(os.environ.get("TRINITY_BASE", os.path.expanduser("~/trinity_shared")))
WAKE_DIR = TRINITY_BASE / "wake"

def create_wake_file(
    instance_id: str,
    prompt: str = None,
    task_type: str = "claude",
    command: str = None,
    message: str = None,
    chain: list = None,
    chain_task: str = None,
    allowed_tools: str = "Bash,Read,Write",
    report_to_oracle: bool = False
):
    """Create a wake file for the specified instance."""
    
    # Ensure wake directory exists
    WAKE_DIR.mkdir(parents=True, exist_ok=True)
    
    wake_file = WAKE_DIR / f"{instance_id}.task"
    
    # Build task data
    task_data = {
        "task_type": task_type,
        "triggered_by": "manual_trigger",
        "timestamp": datetime.now().isoformat(),
        "report_to_oracle": report_to_oracle
    }
    
    if task_type == "claude":
        task_data["prompt"] = prompt
        task_data["allowed_tools"] = allowed_tools
    elif task_type == "bash":
        task_data["command"] = command
    elif task_type == "echo":
        task_data["message"] = message
    
    # Handle chain
    if chain and len(chain) > 0:
        task_data["wake_next"] = chain[0]
        task_data["chain_task"] = chain_task or prompt
        if len(chain) > 1:
            task_data["chain_next"] = chain[1]  # Pass remaining chain
    
    # Write the wake file
    with open(wake_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    print(f"✅ Wake signal sent to {instance_id}")
    print(f"   File: {wake_file}")
    print(f"   Type: {task_type}")
    if chain:
        print(f"   Chain: {' -> '.join([instance_id] + chain)}")
    
    return wake_file

def main():
    parser = argparse.ArgumentParser(
        description="Trinity Wake Trigger - Send wake signals to instances"
    )
    
    parser.add_argument(
        "instance",
        help="Instance ID to wake (e.g., C1T1, C2T1)"
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        default=None,
        help="Prompt for Claude Code execution"
    )
    
    parser.add_argument(
        "--bash", "-b",
        dest="bash_cmd",
        help="Execute a bash command instead of Claude prompt"
    )
    
    parser.add_argument(
        "--echo", "-e",
        dest="echo_msg",
        help="Simple echo test (no Claude execution)"
    )
    
    parser.add_argument(
        "--chain", "-c",
        help="Comma-separated list of instances to wake in chain (e.g., C2T1,C3T1)"
    )
    
    parser.add_argument(
        "--chain-task",
        help="Task to pass to chained instances (defaults to original prompt)"
    )
    
    parser.add_argument(
        "--tools", "-t",
        default="Bash,Read,Write",
        help="Allowed tools for Claude (default: Bash,Read,Write)"
    )
    
    parser.add_argument(
        "--oracle", "-o",
        action="store_true",
        help="Report result back to Oracle inbox"
    )
    
    args = parser.parse_args()
    
    # Parse chain
    chain = args.chain.split(",") if args.chain else None
    
    # Determine task type and execute
    if args.echo_msg:
        create_wake_file(
            args.instance,
            task_type="echo",
            message=args.echo_msg,
            chain=chain,
            report_to_oracle=args.oracle
        )
    elif args.bash_cmd:
        create_wake_file(
            args.instance,
            task_type="bash",
            command=args.bash_cmd,
            chain=chain,
            chain_task=args.chain_task,
            report_to_oracle=args.oracle
        )
    elif args.prompt:
        create_wake_file(
            args.instance,
            task_type="claude",
            prompt=args.prompt,
            chain=chain,
            chain_task=args.chain_task,
            allowed_tools=args.tools,
            report_to_oracle=args.oracle
        )
    else:
        print("❌ Error: Must provide a prompt, --bash command, or --echo message")
        parser.print_help()
        exit(1)

if __name__ == "__main__":
    main()
