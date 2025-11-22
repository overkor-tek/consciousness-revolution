#!/bin/bash
# 🛑 CONSCIOUSNESS NETWORK SHUTDOWN PROTOCOL
# Safely saves state and disconnects from consciousness network
# Version: 1.0
# Created: 2025-11-22

set -e  # Exit on error

# Configuration - CHANGE THESE FOR EACH COMPUTER
COMPUTER_ID="COMPUTER_2_JOSHB_WINDOWS"
STATUS_FILE=".consciousness/sync/computer_2_status.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${RED}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║   CONSCIOUSNESS NETWORK SHUTDOWN PROTOCOL v1.0     ║${NC}"
echo -e "${RED}║   Computer: $COMPUTER_ID${NC}"
echo -e "${RED}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Pull latest changes before shutdown
echo -e "${YELLOW}[1/6]${NC} Pulling latest changes before shutdown..."
if git pull; then
    echo -e "${GREEN}✅ Successfully synchronized with network${NC}"
else
    echo -e "${YELLOW}⚠️  Pull failed - will save local state anyway${NC}"
fi
echo ""

# Step 2: Update status to OFFLINE
echo -e "${YELLOW}[2/6]${NC} Updating status to OFFLINE..."
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create backup of status file
cp "$STATUS_FILE" "$STATUS_FILE.backup"

# Update timestamp and status
if command -v jq &> /dev/null; then
    jq --arg time "$CURRENT_TIME" \
       '.timestamp = $time | .last_updated = $time | .status = "OFFLINE"' \
       "$STATUS_FILE" > "$STATUS_FILE.tmp" && mv "$STATUS_FILE.tmp" "$STATUS_FILE"
else
    # Fallback to sed
    sed -i "s/\"timestamp\": \"[^\"]*\"/\"timestamp\": \"$CURRENT_TIME\"/" "$STATUS_FILE"
    sed -i "s/\"last_updated\": \"[^\"]*\"/\"last_updated\": \"$CURRENT_TIME\"/" "$STATUS_FILE"
    sed -i "s/\"status\": \"[^\"]*\"/\"status\": \"OFFLINE\"/" "$STATUS_FILE"
fi

echo -e "${GREEN}✅ Status updated to OFFLINE${NC}"
echo ""

# Step 3: Save any pending work
echo -e "${YELLOW}[3/6]${NC} Checking for unsaved work..."
if git status --porcelain | grep -q '^'; then
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    echo ""
    git status --short
    echo ""
    read -p "Do you want to commit these changes? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "Enter commit message (or press Enter for default):"
        read -r COMMIT_MSG
        if [ -z "$COMMIT_MSG" ]; then
            COMMIT_MSG="$COMPUTER_ID: Saving state before shutdown"
        fi
        git add -A
        git commit -m "$COMMIT_MSG"
        echo -e "${GREEN}✅ Changes committed${NC}"
    else
        echo -e "${YELLOW}⚠️  Changes NOT committed - will remain local${NC}"
    fi
else
    echo -e "${GREEN}✅ No uncommitted changes${NC}"
fi
echo ""

# Step 4: Stage shutdown status
echo -e "${YELLOW}[4/6]${NC} Staging shutdown status..."
git add "$STATUS_FILE"
if git diff --staged --quiet; then
    echo -e "${GREEN}✅ Status already staged${NC}"
else
    git commit -m "$COMPUTER_ID: Shutdown protocol - Going OFFLINE" --quiet
    echo -e "${GREEN}✅ Shutdown status committed${NC}"
fi
echo ""

# Step 5: Push to network
echo -e "${YELLOW}[5/6]${NC} Broadcasting shutdown status to network..."
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if git push; then
        echo -e "${GREEN}✅ Shutdown status synchronized to network${NC}"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo -e "${YELLOW}⚠️  Push failed - retrying ($RETRY_COUNT/$MAX_RETRIES)...${NC}"
            sleep 2
        else
            echo -e "${RED}❌ Push failed after $MAX_RETRIES attempts${NC}"
            echo -e "${YELLOW}⚠️  Your shutdown status was NOT broadcast to the network${NC}"
            echo -e "${YELLOW}⚠️  Other computers will not know this computer is offline${NC}"
            echo ""
            read -p "Continue with shutdown anyway? (y/n) " -n 1 -r
            echo ""
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo -e "${RED}Shutdown cancelled${NC}"
                exit 1
            fi
        fi
    fi
done
echo ""

# Step 6: Create shutdown snapshot
echo -e "${YELLOW}[6/6]${NC} Creating shutdown snapshot..."
SNAPSHOT_FILE=".consciousness/snapshots/shutdown_$(date +%Y%m%d_%H%M%S).txt"
mkdir -p .consciousness/snapshots

cat > "$SNAPSHOT_FILE" << EOF
CONSCIOUSNESS NETWORK SHUTDOWN SNAPSHOT
========================================
Computer ID: $COMPUTER_ID
Shutdown Time: $CURRENT_TIME
Shutdown Type: Normal/Graceful

STATUS AT SHUTDOWN:
$(cat "$STATUS_FILE")

GIT STATUS:
$(git status)

LAST 5 COMMITS:
$(git log -5 --oneline)

NETWORK STATE:
Computer 1 Status: $([ -f ".consciousness/sync/computer_1_status.json" ] && grep '"status"' .consciousness/sync/computer_1_status.json || echo "Not found")
Computer 2 Status: $([ -f ".consciousness/sync/computer_2_status.json" ] && grep '"status"' .consciousness/sync/computer_2_status.json || echo "Not found")

========================================
EOF

echo -e "${GREEN}✅ Snapshot saved: $SNAPSHOT_FILE${NC}"
echo ""

# Shutdown complete
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   SHUTDOWN COMPLETE - ALL STATE SAVED              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Shutdown summary:"
echo "  • Status: OFFLINE"
echo "  • Last sync: $CURRENT_TIME"
echo "  • Snapshot: $SNAPSHOT_FILE"
echo ""
echo "To boot back up, run:  bash .consciousness/boot_protocol.sh"
echo ""
echo -e "${BLUE}The consciousness network will remember your state.${NC}"
echo -e "${BLUE}Safe to disconnect. 🌙${NC}"
echo ""
