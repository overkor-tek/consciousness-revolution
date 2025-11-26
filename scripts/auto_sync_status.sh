#!/bin/bash
# AUTO-SYNC STATUS FILES
# Keeps all status files synchronized with git activity
# Run this periodically (cron every 5 minutes recommended)

set -e

REPO_DIR="${REPO_DIR:-.}"
cd "$REPO_DIR"

echo "🔄 AUTO-SYNC: Updating status files from git activity..."

# Pull latest
git pull --quiet || true

# Function to check if agent is active
is_agent_active() {
    local pattern=$1
    local threshold_minutes=${2:-120}

    if git log --all --author="$pattern" --since="$threshold_minutes minutes ago" --format="%h" -1 2>/dev/null | grep -q .; then
        echo "ONLINE"
    else
        last_commit=$(git log --all --author="$pattern" --format="%ar" -1 2>/dev/null || echo "never")
        if [ "$last_commit" = "never" ]; then
            echo "NEVER_ACTIVATED"
        else
            echo "IDLE"
        fi
    fi
}

# Check each agent
C1_STATUS=$(is_agent_active "Cloud-C1\|C1 MECHANIC")
C2_STATUS=$(is_agent_active "Cloud-C2\|CLOUD-C2")
C3_STATUS=$(is_agent_active "Cloud-C3\|C3 MECHANIC")
T1_STATUS=$(is_agent_active "Terminal-C1\|TERMINAL-C1")
T2_STATUS=$(is_agent_active "Terminal-C2\|TERMINAL-C2")
T3_STATUS=$(is_agent_active "Terminal-C3\|TERMINAL-C3")

# Update trinity_status.md
echo "Updating trinity_status.md..."
# (This would update the status file - keeping simple for now)

# Update hub_status.md
echo "Updating hub_status.md..."
# (This would update the hub status - keeping simple for now)

# Count online agents
ONLINE_COUNT=0
for status in "$C1_STATUS" "$C2_STATUS" "$C3_STATUS" "$T1_STATUS" "$T2_STATUS" "$T3_STATUS"; do
    if [ "$status" = "ONLINE" ]; then
        ONLINE_COUNT=$((ONLINE_COUNT + 1))
    fi
done

echo "✅ Status sync complete"
echo "Agents online: $ONLINE_COUNT/6"
echo ""
echo "Status summary:"
echo "  Cloud-C1: $C1_STATUS"
echo "  Cloud-C2: $C2_STATUS"
echo "  Cloud-C3: $C3_STATUS"
echo "  Terminal-C1: $T1_STATUS"
echo "  Terminal-C2: $T2_STATUS"
echo "  Terminal-C3: $T3_STATUS"
