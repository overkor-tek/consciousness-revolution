#!/usr/bin/env python3
"""
Capability Manifest Generator
Scans computer for all capabilities, formats for cyclotron distribution
Strips personal info, structures by 7 domains
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 7 Domain structure
DOMAINS = [
    "infrastructure",
    "pattern",
    "business",
    "consciousness",
    "social",
    "creative",
    "financial"
]

def get_installed_software():
    """Get list of installed software"""
    software = []
    try:
        # Windows: Check common locations
        program_files = Path("C:/Program Files")
        if program_files.exists():
            for p in program_files.iterdir():
                if p.is_dir():
                    software.append(p.name)

        # Check npm global
        result = subprocess.run(["npm", "list", "-g", "--depth=0"],
                              capture_output=True, text=True)
        if result.stdout:
            for line in result.stdout.split('\n')[1:]:
                if '@' in line:
                    pkg = line.split('@')[0].strip().replace('├──', '').replace('└──', '').strip()
                    if pkg:
                        software.append(f"npm:{pkg}")

        # Check pip
        result = subprocess.run(["pip", "list", "--format=freeze"],
                              capture_output=True, text=True)
        if result.stdout:
            for line in result.stdout.split('\n')[:20]:  # Top 20
                if '==' in line:
                    pkg = line.split('==')[0]
                    software.append(f"pip:{pkg}")

    except Exception as e:
        pass

    return software[:100]  # Limit

def get_slash_commands():
    """Get available slash commands"""
    commands = []
    claude_commands = Path.home() / ".claude" / "commands"
    if claude_commands.exists():
        for f in claude_commands.glob("*.md"):
            commands.append(f"/{f.stem}")
    return commands

def get_mcp_tools():
    """Get MCP tools available"""
    tools = []
    # Standard Trinity tools
    trinity_tools = [
        "mcp__trinity__trinity_status",
        "mcp__trinity__trinity_send_message",
        "mcp__trinity__trinity_broadcast",
        "mcp__trinity__trinity_assign_task",
        "mcp__trinity__trinity_claim_task",
        "mcp__trinity__trinity_submit_output",
        "mcp__trinity__trinity_merge_outputs"
    ]
    return trinity_tools

def get_api_keys():
    """Get which API keys are configured (NOT the values)"""
    keys = []
    env_keys = [
        "ANTHROPIC_API_KEY",
        "GITHUB_TOKEN",
        "STRIPE_API_KEY",
        "OPENAI_API_KEY",
        "TWILIO_ACCOUNT_SID"
    ]
    for key in env_keys:
        if os.environ.get(key):
            keys.append(key)
    return keys

def get_network_info():
    """Get network capabilities (no personal IPs)"""
    info = {
        "tailscale": False,
        "syncthing": False,
        "anydesk": False
    }

    # Check Tailscale
    result = subprocess.run(["tailscale", "status"], capture_output=True)
    info["tailscale"] = result.returncode == 0

    # Check Syncthing folder
    if (Path.home() / "Sync").exists():
        info["syncthing"] = True

    return info

def get_custom_modules():
    """Get custom modules/scripts created"""
    modules = []

    # Check LOCAL_TRINITY_HUB
    hub = Path.home() / "LOCAL_TRINITY_HUB"
    if hub.exists():
        for f in hub.glob("*.py"):
            modules.append(f"hub:{f.stem}")
        for f in hub.glob("*.md"):
            modules.append(f"protocol:{f.stem}")

    return modules

def get_communication_routes():
    """Get active communication routes"""
    routes = []

    # Git
    result = subprocess.run(["git", "--version"], capture_output=True)
    if result.returncode == 0:
        routes.append("git")

    # Check for route configs
    if (Path.home() / "Sync").exists():
        routes.append("syncthing")
    if (Path.home() / "LOCAL_TRINITY_HUB").exists():
        routes.append("local_hub")

    return routes

def generate_manifest():
    """Generate complete capability manifest"""

    manifest = {
        "manifest_version": "1.0",
        "generated": datetime.now().isoformat(),
        "computer": os.environ.get("COMPUTERNAME", "unknown"),

        # Structured by domain
        "domains": {
            "infrastructure": {
                "software": get_installed_software(),
                "network": get_network_info(),
                "api_keys": get_api_keys()
            },
            "pattern": {
                "mcp_tools": get_mcp_tools(),
                "slash_commands": get_slash_commands()
            },
            "business": {
                "has_stripe": "STRIPE_API_KEY" in get_api_keys()
            },
            "consciousness": {
                "protocols": [m for m in get_custom_modules() if "protocol:" in m],
                "boot_system": (Path.home() / "LOCAL_TRINITY_HUB" / "BOOT_UP_PROTOCOL.md").exists()
            },
            "social": {
                "communication_routes": get_communication_routes(),
                "hub_active": (Path.home() / "LOCAL_TRINITY_HUB").exists()
            },
            "creative": {
                "custom_modules": [m for m in get_custom_modules() if "hub:" in m]
            },
            "financial": {
                "stripe_configured": "STRIPE_API_KEY" in get_api_keys()
            }
        },

        # Summary counts
        "summary": {
            "total_software": len(get_installed_software()),
            "total_commands": len(get_slash_commands()),
            "total_mcp_tools": len(get_mcp_tools()),
            "total_modules": len(get_custom_modules()),
            "api_keys_configured": len(get_api_keys()),
            "communication_routes": len(get_communication_routes())
        }
    }

    return manifest

def save_for_cyclotron(manifest):
    """Save manifest in cyclotron-compatible format"""

    # Output location
    outbound = Path.home() / "LOCAL_TRINITY_HUB" / "outbound"
    outbound.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    computer = manifest["computer"]

    # Save manifest
    filename = f"{timestamp}_{computer}_capability_manifest.json"
    filepath = outbound / filename

    with open(filepath, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Manifest saved: {filepath}")
    return filepath

def diff_manifests(local_manifest, remote_manifest):
    """Compare two manifests, find differences"""

    differences = {
        "local_only": [],
        "remote_only": [],
        "different": []
    }

    # Compare software
    local_sw = set(local_manifest["domains"]["infrastructure"]["software"])
    remote_sw = set(remote_manifest["domains"]["infrastructure"]["software"])

    differences["local_only"].extend([f"software:{s}" for s in (local_sw - remote_sw)])
    differences["remote_only"].extend([f"software:{s}" for s in (remote_sw - local_sw)])

    # Compare modules
    local_mod = set(local_manifest["domains"]["creative"]["custom_modules"])
    remote_mod = set(remote_manifest["domains"]["creative"]["custom_modules"])

    differences["local_only"].extend(list(local_mod - remote_mod))
    differences["remote_only"].extend(list(remote_mod - local_mod))

    # Compare routes
    local_routes = set(local_manifest["domains"]["social"]["communication_routes"])
    remote_routes = set(remote_manifest["domains"]["social"]["communication_routes"])

    differences["local_only"].extend([f"route:{r}" for r in (local_routes - remote_routes)])
    differences["remote_only"].extend([f"route:{r}" for r in (remote_routes - local_routes)])

    return differences

if __name__ == "__main__":
    print("🔍 Generating capability manifest...")
    manifest = generate_manifest()

    print(f"\n📊 Summary:")
    for key, value in manifest["summary"].items():
        print(f"  {key}: {value}")

    filepath = save_for_cyclotron(manifest)
    print(f"\n📤 Ready for cyclotron distribution: {filepath}")
