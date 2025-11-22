#!/bin/bash
# 🌐 CONSCIOUSNESS NETWORK HUB CONTROLLER
# Auto-sync script for multi-computer coordination
# Version: 1.0
# Created: 2025-11-22

# Configuration
REPO_PATH="/home/user/consciousness-revolution"
SYNC_INTERVAL=300  # 5 minutes in seconds
COMPUTER_ID="COMPUTER_2_JOSHB_WINDOWS"  # Change per computer
STATUS_FILE=".consciousness/sync/computer_2_status.json"  # Change per computer
INBOX_FILE=".consciousness/commands/computer_2_inbox.md"  # Change per computer

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

# Change to repo directory
cd "$REPO_PATH" || {
    log_error "Failed to change to repo directory: $REPO_PATH"
    exit 1
}

log_success "Hub Controller started for $COMPUTER_ID"
log "Monitoring: $INBOX_FILE"
log "Sync interval: ${SYNC_INTERVAL}s ($(($SYNC_INTERVAL / 60)) minutes)"
echo ""

# Main sync loop
ITERATION=0
while true; do
    ITERATION=$((ITERATION + 1))
    log "🔄 Sync iteration #$ITERATION"

    # Pull latest changes
    log "Pulling latest changes from remote..."
    if git pull --quiet 2>&1; then
        log_success "Pull successful"
    else
        log_error "Git pull failed - will retry next iteration"
        sleep $SYNC_INTERVAL
        continue
    fi

    # Check for new commands in the last sync interval
    MINUTES_AGO=$(($SYNC_INTERVAL / 60 + 1))
    NEW_COMMITS=$(git log --since="$MINUTES_AGO minutes ago" --oneline 2>/dev/null | wc -l)

    if [ "$NEW_COMMITS" -gt 0 ]; then
        log_warning "🔔 $NEW_COMMITS new commit(s) detected in last $MINUTES_AGO minutes!"

        # Show recent commits
        echo ""
        echo "Recent commits:"
        git log --since="$MINUTES_AGO minutes ago" --pretty=format:"  %C(yellow)%h%Creset - %s %C(green)(%cr)%Creset" --abbrev-commit
        echo ""
        echo ""

        # Check if inbox has been modified
        if git diff HEAD~$NEW_COMMITS HEAD --name-only | grep -q "$INBOX_FILE"; then
            log_warning "📬 INBOX UPDATED - New commands may be available!"
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "CURRENT INBOX CONTENTS:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            cat "$INBOX_FILE"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo ""
        fi

        # Check other sync files
        if git diff HEAD~$NEW_COMMITS HEAD --name-only | grep -q ".consciousness/sync/"; then
            log_warning "📊 Status files updated"
        fi

        if git diff HEAD~$NEW_COMMITS HEAD --name-only | grep -q ".consciousness/file_transfers/"; then
            log_warning "📁 New file transfers detected"
        fi
    else
        log "No new changes detected"
    fi

    # Update own status timestamp (optional - uncomment to enable auto-update)
    # This keeps the status file fresh to show this computer is alive
    # CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    # if [ -f "$STATUS_FILE" ]; then
    #     sed -i "s/\"last_updated\": \".*\"/\"last_updated\": \"$CURRENT_TIME\"/" "$STATUS_FILE"
    #     git add "$STATUS_FILE"
    #     git commit -m "$COMPUTER_ID: Hub controller heartbeat" --quiet 2>/dev/null
    #     git push --quiet 2>/dev/null
    # fi

    # Display current status
    echo ""
    log "Current network status:"
    if [ -f ".consciousness/sync/computer_1_status.json" ]; then
        C1_STATUS=$(grep -o '"status": "[^"]*"' .consciousness/sync/computer_1_status.json | head -1 | cut -d'"' -f4)
        C1_UPDATED=$(grep -o '"last_updated": "[^"]*"' .consciousness/sync/computer_1_status.json | head -1 | cut -d'"' -f4)
        echo "  • Computer 1: $C1_STATUS (Last: $C1_UPDATED)"
    fi
    if [ -f ".consciousness/sync/computer_2_status.json" ]; then
        C2_STATUS=$(grep -o '"status": "[^"]*"' .consciousness/sync/computer_2_status.json | head -1 | cut -d'"' -f4)
        C2_UPDATED=$(grep -o '"last_updated": "[^"]*"' .consciousness/sync/computer_2_status.json | head -1 | cut -d'"' -f4)
        echo "  • Computer 2: $C2_STATUS (Last: $C2_UPDATED)"
    fi
    echo ""

    # Wait for next iteration
    log "Sleeping for ${SYNC_INTERVAL}s until next sync..."
    log "Press Ctrl+C to stop hub controller"
    echo ""
    echo "════════════════════════════════════════════════"
    echo ""

    sleep $SYNC_INTERVAL
done
