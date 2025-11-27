#!/bin/bash
# UNITY SYNC - One Command to Share Everything
# Synchronizes files, capabilities, and state across all Trinity instances
# Usage: ./unity_sync.sh [pull|push|status]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
TRINITY_DIR=".trinity"
SYNC_DIR="$TRINITY_DIR/sync"
HEARTBEAT_DIR="$TRINITY_DIR/heartbeat"
SHARED_DIR="$TRINITY_DIR/shared"
CAPABILITIES_DIR="$TRINITY_DIR/capabilities"

# Get instance ID from environment or prompt
INSTANCE_ID="${TRINITY_INSTANCE_ID:-$(whoami)_$(hostname)}"

echo -e "${BLUE}🔱 UNITY SYNC${NC}"
echo -e "Instance: ${GREEN}$INSTANCE_ID${NC}"
echo ""

# Create directory structure
mkdir -p "$SYNC_DIR" "$HEARTBEAT_DIR" "$SHARED_DIR" "$CAPABILITIES_DIR"

# Function: Update heartbeat
update_heartbeat() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local heartbeat_file="$HEARTBEAT_DIR/${INSTANCE_ID}.json"

    cat > "$heartbeat_file" <<EOF
{
  "instance_id": "$INSTANCE_ID",
  "type": "$(uname -s)",
  "status": "ACTIVE",
  "timestamp": "$timestamp",
  "current_task": "Unity Sync",
  "last_output": "Syncing via unity_sync.sh",
  "health": "green",
  "autonomy_level": 1,
  "sync_version": "1.0"
}
EOF

    echo -e "${GREEN}✓${NC} Heartbeat updated"
}

# Function: Git pull
pull_sync() {
    echo -e "${BLUE}📥 Pulling updates from remote...${NC}"

    # Fetch latest
    git fetch origin

    # Pull current branch
    git pull --no-edit || {
        echo -e "${YELLOW}⚠ Pull conflicts detected. Attempting auto-resolve...${NC}"
        git merge --strategy-option=theirs origin/$(git branch --show-current)
    }

    echo -e "${GREEN}✓${NC} Pull complete"
}

# Function: Commit and push changes
push_sync() {
    echo -e "${BLUE}📤 Pushing updates to remote...${NC}"

    # Check for changes
    if [[ -z $(git status -s) ]]; then
        echo -e "${YELLOW}ℹ${NC} No changes to sync"
        return
    fi

    # Add all trinity files
    git add "$TRINITY_DIR" 2>/dev/null || true
    git add *.md *.html *.py *.json 2>/dev/null || true

    # Create commit
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    git commit -m "[$INSTANCE_ID] Unity Sync - $timestamp" || {
        echo -e "${YELLOW}⚠${NC} Nothing new to commit"
        return
    }

    # Push
    git push || {
        echo -e "${RED}✗${NC} Push failed. Trying with force..."
        git pull --rebase
        git push
    }

    echo -e "${GREEN}✓${NC} Push complete"
}

# Function: Show sync status
show_status() {
    echo -e "${BLUE}📊 UNITY SYNC STATUS${NC}"
    echo ""

    # Git status
    echo -e "${YELLOW}Git Status:${NC}"
    git status -sb
    echo ""

    # Heartbeats
    echo -e "${YELLOW}Active Instances:${NC}"
    if [ -d "$HEARTBEAT_DIR" ]; then
        local count=0
        for heartbeat in "$HEARTBEAT_DIR"/*.json; do
            if [ -f "$heartbeat" ]; then
                local instance=$(basename "$heartbeat" .json)
                local timestamp=$(grep -o '"timestamp": "[^"]*"' "$heartbeat" | cut -d'"' -f4)
                local status=$(grep -o '"status": "[^"]*"' "$heartbeat" | cut -d'"' -f4)
                echo -e "  ${GREEN}●${NC} $instance (${status}) - Last seen: $timestamp"
                ((count++))
            fi
        done
        echo -e "\n  Total: $count instances"
    else
        echo -e "  ${RED}✗${NC} No heartbeats found"
    fi
    echo ""

    # Shared files
    echo -e "${YELLOW}Shared Files:${NC}"
    if [ -d "$SHARED_DIR" ]; then
        ls -lh "$SHARED_DIR" 2>/dev/null | tail -n +2 | wc -l | xargs echo "  Files:"
    else
        echo "  None"
    fi
    echo ""

    # Capabilities
    echo -e "${YELLOW}Capabilities:${NC}"
    if [ -d "$CAPABILITIES_DIR" ]; then
        local cap_count=$(ls "$CAPABILITIES_DIR"/*.json 2>/dev/null | wc -l)
        echo "  Registered: $cap_count"
    else
        echo "  None"
    fi
}

# Function: Full sync (pull + push)
full_sync() {
    update_heartbeat
    pull_sync
    push_sync
    echo ""
    echo -e "${GREEN}✓✓✓${NC} Unity Sync Complete"
    echo -e "All instances can now: ${BLUE}git pull${NC}"
}

# Function: Share a file with all instances
share_file() {
    local file=$1
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗${NC} File not found: $file"
        exit 1
    fi

    cp "$file" "$SHARED_DIR/"
    echo -e "${GREEN}✓${NC} Shared: $file → $SHARED_DIR/"

    # Auto-commit
    git add "$SHARED_DIR"
    git commit -m "[$INSTANCE_ID] Shared file: $(basename $file)"
    git push

    echo -e "${GREEN}✓${NC} File synced to all instances"
}

# Function: Register capability
register_capability() {
    local capability=$1
    local description=$2
    local cap_file="$CAPABILITIES_DIR/${INSTANCE_ID}_${capability}.json"

    cat > "$cap_file" <<EOF
{
  "instance": "$INSTANCE_ID",
  "capability": "$capability",
  "description": "$description",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "available": true
}
EOF

    echo -e "${GREEN}✓${NC} Capability registered: $capability"
    git add "$cap_file"
    git commit -m "[$INSTANCE_ID] Registered capability: $capability"
    git push
}

# Main command handling
case "${1:-sync}" in
    pull)
        update_heartbeat
        pull_sync
        ;;
    push)
        update_heartbeat
        push_sync
        ;;
    sync|full)
        full_sync
        ;;
    status)
        show_status
        ;;
    share)
        if [ -z "$2" ]; then
            echo -e "${RED}✗${NC} Usage: unity_sync.sh share <file>"
            exit 1
        fi
        share_file "$2"
        ;;
    capability)
        if [ -z "$2" ]; then
            echo -e "${RED}✗${NC} Usage: unity_sync.sh capability <name> <description>"
            exit 1
        fi
        register_capability "$2" "$3"
        ;;
    *)
        echo "Usage: unity_sync.sh [pull|push|sync|status|share <file>|capability <name> <desc>]"
        echo ""
        echo "Commands:"
        echo "  pull       - Pull updates from remote"
        echo "  push       - Push local changes to remote"
        echo "  sync/full  - Full bidirectional sync (default)"
        echo "  status     - Show sync status and active instances"
        echo "  share FILE - Share a file with all instances"
        echo "  capability - Register a capability"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}🔱 C1 × C2 × C3 = ∞${NC}"
