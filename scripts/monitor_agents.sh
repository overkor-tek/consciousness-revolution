#!/bin/bash
# CONTINUOUS AGENT MONITORING DAEMON
# Watches agent activity and alerts on status changes
# Usage: ./monitor_agents.sh [interval_seconds]
#
# This script runs continuously and monitors all 6 agents.
# Press Ctrl+C to stop.

set -e

INTERVAL=${1:-30}  # Default: check every 30 seconds
REPO_DIR="${REPO_DIR:-.}"
LOG_FILE="${LOG_FILE:-.consciousness/monitoring.log}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# State tracking
declare -A PREVIOUS_STATUS
declare -A ALERT_SENT

# Agent definitions
AGENTS=(
    "Cloud-C1:Cloud-C1"
    "Cloud-C2:Cloud-C2|CLOUD-C2"
    "Cloud-C3:Cloud-C3"
    "Terminal-C1:Terminal-C1|TERMINAL-C1"
    "Terminal-C2:Terminal-C2|TERMINAL-C2"
    "Terminal-C3:Terminal-C3|TERMINAL-C3"
)

cd "$REPO_DIR"

# Cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Monitoring stopped.${NC}"
    echo "Session log: $LOG_FILE"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Function to get agent status
get_agent_status() {
    local pattern=$1

    if git log --all --author="$pattern" --since="5 minutes ago" --format="%h" -1 2>/dev/null | grep -q .; then
        echo "ACTIVE"
    else
        last_commit=$(git log --all --author="$pattern" --format="%ar" -1 2>/dev/null || echo "never")
        if [ "$last_commit" = "never" ]; then
            echo "NEVER_ACTIVATED"
        else
            # Get minutes since last commit
            commit_time=$(git log --all --author="$pattern" --format="%ct" -1 2>/dev/null || echo "0")
            current_time=$(date +%s)
            minutes_ago=$(( ($current_time - $commit_time) / 60 ))

            if [ $minutes_ago -lt 60 ]; then
                echo "RECENT"
            elif [ $minutes_ago -lt 240 ]; then
                echo "IDLE"
            else
                echo "OFFLINE"
            fi
        fi
    fi
}

# Function to log event
log_event() {
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    echo "[$timestamp] $1" >> "$LOG_FILE"
}

# Function to send alert
send_alert() {
    local agent=$1
    local old_status=$2
    local new_status=$3
    local timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

    echo ""
    echo -e "${BOLD}🔔 ALERT: $agent status changed${NC}"
    echo "  From: $old_status"
    echo "  To:   $new_status"
    echo "  Time: $timestamp"
    echo ""

    log_event "ALERT: $agent changed from $old_status to $new_status"
}

# Initialize
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║         DUAL TRINITY - CONTINUOUS MONITORING               ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Monitoring interval: ${INTERVAL} seconds"
echo "Log file: $LOG_FILE"
echo "Press Ctrl+C to stop"
echo ""

log_event "Monitoring started (interval: ${INTERVAL}s)"

# Initial status check
echo -e "${BOLD}Initial status check...${NC}"
echo ""

for agent_def in "${AGENTS[@]}"; do
    IFS=':' read -r agent_name agent_pattern <<< "$agent_def"
    status=$(get_agent_status "$agent_pattern")
    PREVIOUS_STATUS[$agent_name]=$status
    ALERT_SENT[$agent_name]=0

    # Display status with icon
    case $status in
        ACTIVE)
            icon="${GREEN}🟢${NC}"
            ;;
        RECENT)
            icon="${GREEN}🟢${NC}"
            ;;
        IDLE)
            icon="${YELLOW}🟡${NC}"
            ;;
        OFFLINE)
            icon="${RED}🔴${NC}"
            ;;
        NEVER_ACTIVATED)
            icon="${RED}⏳${NC}"
            ;;
        *)
            icon="⚪"
            ;;
    esac

    echo -e "  $icon $agent_name: $status"
    log_event "Initial: $agent_name = $status"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Main monitoring loop
ITERATION=0
while true; do
    ITERATION=$((ITERATION + 1))
    TIMESTAMP=$(date +"%H:%M:%S")

    # Pull latest changes (quietly)
    git pull --quiet 2>/dev/null || true

    # Check each agent
    CHANGES_DETECTED=0

    for agent_def in "${AGENTS[@]}"; do
        IFS=':' read -r agent_name agent_pattern <<< "$agent_def"

        # Get current status
        current_status=$(get_agent_status "$agent_pattern")
        previous_status=${PREVIOUS_STATUS[$agent_name]}

        # Check for status change
        if [ "$current_status" != "$previous_status" ]; then
            CHANGES_DETECTED=1
            send_alert "$agent_name" "$previous_status" "$current_status"

            # Update state
            PREVIOUS_STATUS[$agent_name]=$current_status
            ALERT_SENT[$agent_name]=1
        fi
    done

    # Periodic status update (every 10 iterations)
    if [ $((ITERATION % 10)) -eq 0 ]; then
        echo -e "${BLUE}[$TIMESTAMP] Status update (iteration $ITERATION)${NC}"

        online_count=0
        for agent_def in "${AGENTS[@]}"; do
            IFS=':' read -r agent_name agent_pattern <<< "$agent_def"
            status=${PREVIOUS_STATUS[$agent_name]}

            if [ "$status" = "ACTIVE" ] || [ "$status" = "RECENT" ]; then
                online_count=$((online_count + 1))
            fi
        done

        echo "  Agents active: $online_count/6"

        # Recent commit count
        commits=$(git log --all --since="1 hour ago" --format="%h" 2>/dev/null | wc -l)
        echo "  Commits (last hour): $commits"

        echo ""

        log_event "Periodic update: $online_count/6 agents active, $commits commits in last hour"
    fi

    # Sleep until next check
    sleep "$INTERVAL"
done
