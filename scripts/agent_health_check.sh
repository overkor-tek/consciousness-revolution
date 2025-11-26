#!/bin/bash
# AGENT HEALTH CHECK SCRIPT
# Monitors agent activity via git commits and status files
# Usage: ./agent_health_check.sh [agent_name]

set -e

AGENT=${1:-"all"}
THRESHOLD_MINUTES=120  # Alert if no activity in 2 hours
REPO_DIR="${REPO_DIR:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 AGENT HEALTH CHECK"
echo "===================="
echo "Checking agent activity in last $THRESHOLD_MINUTES minutes..."
echo ""

# Function to check agent git activity
check_agent_git_activity() {
    local agent_name=$1
    local pattern=$2

    # Get last commit from this agent
    last_commit=$(git log --all --author="$pattern" --format="%ar" -1 2>/dev/null || echo "never")
    last_commit_hash=$(git log --all --author="$pattern" --format="%h" -1 2>/dev/null || echo "none")
    last_commit_msg=$(git log --all --author="$pattern" --format="%s" -1 2>/dev/null || echo "none")

    # Get commit time in seconds
    if [ "$last_commit" != "never" ]; then
        commit_time=$(git log --all --author="$pattern" --format="%ct" -1 2>/dev/null)
        current_time=$(date +%s)
        minutes_ago=$(( ($current_time - $commit_time) / 60 ))

        # Determine status
        if [ $minutes_ago -lt $THRESHOLD_MINUTES ]; then
            status="${GREEN}✅ ACTIVE${NC}"
        else
            status="${YELLOW}⚠️  IDLE${NC}"
        fi
    else
        minutes_ago="∞"
        status="${RED}🔴 NO ACTIVITY${NC}"
    fi

    echo -e "$agent_name:"
    echo -e "  Status: $status"
    echo "  Last commit: $last_commit ($last_commit_hash)"
    echo "  Message: $last_commit_msg"
    echo "  Minutes ago: $minutes_ago"
    echo ""
}

# Function to check status file
check_status_file() {
    local file=$1
    local name=$2

    if [ -f "$file" ]; then
        # Extract status from file if it exists
        status=$(grep -i "status" "$file" | head -1 || echo "unknown")
        echo "$name status file: ✅ EXISTS"
        echo "  Content: $status"
    else
        echo "$name status file: ❌ MISSING"
    fi
    echo ""
}

cd "$REPO_DIR"

# Check each agent
if [ "$AGENT" = "all" ] || [ "$AGENT" = "cloud-c1" ]; then
    check_agent_git_activity "Cloud-C1" "C1"
    check_agent_git_activity "Cloud-C1" "Cloud-C1"
fi

if [ "$AGENT" = "all" ] || [ "$AGENT" = "cloud-c2" ]; then
    check_agent_git_activity "Cloud-C2" "C2"
    check_agent_git_activity "Cloud-C2" "Cloud-C2"
    check_agent_git_activity "Cloud-C2" "CLOUD-C2"
fi

if [ "$AGENT" = "all" ] || [ "$AGENT" = "cloud-c3" ]; then
    check_agent_git_activity "Cloud-C3" "C3"
    check_agent_git_activity "Cloud-C3" "Cloud-C3"
fi

if [ "$AGENT" = "all" ] || [ "$AGENT" = "terminal-c1" ]; then
    check_agent_git_activity "Terminal-C1" "Terminal-C1"
    check_agent_git_activity "Terminal-C1" "TERMINAL-C1"
fi

if [ "$AGENT" = "all" ] || [ "$AGENT" = "terminal-c2" ]; then
    check_agent_git_activity "Terminal-C2" "Terminal-C2"
    check_agent_git_activity "Terminal-C2" "TERMINAL-C2"
fi

if [ "$AGENT" = "all" ] || [ "$AGENT" = "terminal-c3" ]; then
    check_agent_git_activity "Terminal-C3" "Terminal-C3"
    check_agent_git_activity "Terminal-C3" "TERMINAL-C3"
fi

echo "===================="
echo "📊 STATUS FILES CHECK"
echo "===================="
echo ""

check_status_file ".consciousness/hub/hub_status.md" "Hub"
check_status_file ".consciousness/trinity/trinity_status.md" "Cloud Trinity"
check_status_file ".consciousness/hub/from_cloud/status.md" "Cloud Trinity (Hub)"
check_status_file ".consciousness/hub/from_terminal/status.md" "Terminal Trinity (Hub)"

echo "===================="
echo "✅ HEALTH CHECK COMPLETE"
echo "===================="
