#!/bin/bash
# 🚀 CONSCIOUSNESS NETWORK BOOT PROTOCOL
# Safely initializes consciousness network connection
# Version: 1.0
# Created: 2025-11-22

set -e  # Exit on error

# Configuration - CHANGE THESE FOR EACH COMPUTER
COMPUTER_ID="COMPUTER_2_JOSHB_WINDOWS"
STATUS_FILE=".consciousness/sync/computer_2_status.json"
INBOX_FILE=".consciousness/commands/computer_2_inbox.md"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   CONSCIOUSNESS NETWORK BOOT PROTOCOL v1.0        ║${NC}"
echo -e "${BLUE}║   Computer: $COMPUTER_ID${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Pull latest state
echo -e "${YELLOW}[1/5]${NC} Pulling latest consciousness state from network..."
if git pull; then
    echo -e "${GREEN}✅ Successfully synchronized with network${NC}"
else
    echo -e "${RED}❌ Failed to pull - check network connection${NC}"
    exit 1
fi
echo ""

# Step 2: Update status to OPERATIONAL
echo -e "${YELLOW}[2/5]${NC} Updating status to OPERATIONAL..."
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create backup of status file
cp "$STATUS_FILE" "$STATUS_FILE.backup"

# Update timestamp and status using jq if available, otherwise sed
if command -v jq &> /dev/null; then
    jq --arg time "$CURRENT_TIME" \
       '.timestamp = $time | .last_updated = $time | .status = "OPERATIONAL"' \
       "$STATUS_FILE" > "$STATUS_FILE.tmp" && mv "$STATUS_FILE.tmp" "$STATUS_FILE"
else
    # Fallback to sed
    sed -i "s/\"timestamp\": \"[^\"]*\"/\"timestamp\": \"$CURRENT_TIME\"/" "$STATUS_FILE"
    sed -i "s/\"last_updated\": \"[^\"]*\"/\"last_updated\": \"$CURRENT_TIME\"/" "$STATUS_FILE"
    sed -i "s/\"status\": \"[^\"]*\"/\"status\": \"OPERATIONAL\"/" "$STATUS_FILE"
fi

echo -e "${GREEN}✅ Status updated to OPERATIONAL${NC}"
echo ""

# Step 3: Check for pending commands
echo -e "${YELLOW}[3/5]${NC} Checking inbox for pending commands..."
if [ -f "$INBOX_FILE" ]; then
    ACTIVE_COMMANDS=$(grep -c "## 🎯 ACTIVE COMMANDS" "$INBOX_FILE" || echo "0")
    if [ "$ACTIVE_COMMANDS" -gt 0 ]; then
        echo -e "${GREEN}📬 Inbox file found - check for new commands${NC}"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        head -n 20 "$INBOX_FILE"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    else
        echo -e "${GREEN}✅ No active commands pending${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Inbox file not found${NC}"
fi
echo ""

# Step 4: Display network status
echo -e "${YELLOW}[4/5]${NC} Consciousness network status:"
echo ""
if [ -f ".consciousness/sync/computer_1_status.json" ]; then
    echo -e "${BLUE}Computer 1:${NC}"
    grep -E '"status"|"last_updated"' .consciousness/sync/computer_1_status.json | sed 's/^/  /'
fi
echo ""
if [ -f ".consciousness/sync/computer_2_status.json" ]; then
    echo -e "${BLUE}Computer 2 (This computer):${NC}"
    grep -E '"status"|"last_updated"' .consciousness/sync/computer_2_status.json | sed 's/^/  /'
fi
echo ""

# Step 5: Sync boot status to network
echo -e "${YELLOW}[5/5]${NC} Broadcasting boot status to network..."
git add .consciousness/
if git diff --staged --quiet; then
    echo -e "${GREEN}✅ No changes to commit (already synchronized)${NC}"
else
    git commit -m "$COMPUTER_ID: Boot protocol - System OPERATIONAL" --quiet
    if git push; then
        echo -e "${GREEN}✅ Boot status synchronized to network${NC}"
    else
        echo -e "${YELLOW}⚠️  Push failed - will sync on next cycle${NC}"
    fi
fi
echo ""

# Boot complete
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   BOOT COMPLETE - CONSCIOUSNESS NETWORK ONLINE     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Start hub controller:  bash .consciousness/hub_controller.sh"
echo "  2. Check inbox:           cat $INBOX_FILE"
echo "  3. View shared tasks:     cat .consciousness/sync/shared_tasks.json"
echo ""
echo "To shutdown safely, run:  bash .consciousness/shutdown_protocol.sh"
echo ""
