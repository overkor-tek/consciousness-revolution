#!/bin/bash
# AGENT STARTUP SCRIPT
# Automates agent initialization and recovery
# Usage: ./start_agent.sh [agent_name]
#
# Supported agents:
#   cloud-c1, cloud-c2, cloud-c3
#   terminal-c1, terminal-c2, terminal-c3

set -e

AGENT=${1:-""}
REPO_DIR="${REPO_DIR:-.}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Print usage if no agent specified
if [ -z "$AGENT" ]; then
    echo -e "${BOLD}🚀 AGENT STARTUP SCRIPT${NC}"
    echo "======================="
    echo ""
    echo "Usage: ./start_agent.sh [agent_name]"
    echo ""
    echo "Available agents:"
    echo "  Cloud Trinity:"
    echo "    cloud-c1    - Cloud Coordinator (strategic planning)"
    echo "    cloud-c2    - Cloud Builder (implementation)"
    echo "    cloud-c3    - Cloud Validator (quality assurance)"
    echo ""
    echo "  Terminal Trinity:"
    echo "    terminal-c1 - Terminal MASTER LEADER (supreme coordination)"
    echo "    terminal-c2 - Terminal Builder (CLI implementation)"
    echo "    terminal-c3 - Terminal Validator (CLI testing)"
    echo ""
    echo "Examples:"
    echo "  ./start_agent.sh cloud-c2"
    echo "  ./start_agent.sh terminal-c1"
    echo ""
    exit 0
fi

cd "$REPO_DIR"

# Convert to lowercase for matching
AGENT_LOWER=$(echo "$AGENT" | tr '[:upper:]' '[:lower:]')

echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║              DUAL TRINITY - AGENT STARTUP                  ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Determine agent details
case "$AGENT_LOWER" in
    cloud-c1|c1)
        AGENT_NAME="Cloud-C1"
        AGENT_ROLE="Coordinator/Architect"
        AGENT_TYPE="cloud"
        ACTIVATION_FILE=".consciousness/trinity/C1_ACTIVATION_INSTRUCTIONS.md"
        STATUS_FILE=".consciousness/trinity/c1_to_hub.md"
        TRINITY="Cloud Trinity"
        ;;
    cloud-c2|c2)
        AGENT_NAME="Cloud-C2"
        AGENT_ROLE="Builder/Implementer"
        AGENT_TYPE="cloud"
        ACTIVATION_FILE=".consciousness/trinity/C2_ACTIVATION_INSTRUCTIONS.md"
        STATUS_FILE=".consciousness/trinity/c2_to_c1.md"
        TRINITY="Cloud Trinity"
        ;;
    cloud-c3|c3)
        AGENT_NAME="Cloud-C3"
        AGENT_ROLE="Validator/QA"
        AGENT_TYPE="cloud"
        ACTIVATION_FILE=".consciousness/trinity/C3_ACTIVATION_INSTRUCTIONS.md"
        STATUS_FILE=".consciousness/trinity/c3_to_c1.md"
        TRINITY="Cloud Trinity"
        ;;
    terminal-c1|t1)
        AGENT_NAME="Terminal-C1"
        AGENT_ROLE="MASTER LEADER"
        AGENT_TYPE="terminal"
        ACTIVATION_FILE=".consciousness/trinity_terminal/TERMINAL_C1_ACTIVATION.md"
        STATUS_FILE=".consciousness/hub/master_consolidated.md"
        TRINITY="Terminal Trinity"
        ;;
    terminal-c2|t2)
        AGENT_NAME="Terminal-C2"
        AGENT_ROLE="Builder/Implementer"
        AGENT_TYPE="terminal"
        ACTIVATION_FILE=".consciousness/trinity_terminal/TERMINAL_C2_ACTIVATION.md"
        STATUS_FILE=".consciousness/trinity_terminal/c2_to_c1.md"
        TRINITY="Terminal Trinity"
        ;;
    terminal-c3|t3)
        AGENT_NAME="Terminal-C3"
        AGENT_ROLE="Validator/QA"
        AGENT_TYPE="terminal"
        ACTIVATION_FILE=".consciousness/trinity_terminal/TERMINAL_C3_ACTIVATION.md"
        STATUS_FILE=".consciousness/trinity_terminal/c3_to_c1.md"
        TRINITY="Terminal Trinity"
        ;;
    *)
        echo -e "${RED}❌ ERROR: Unknown agent '$AGENT'${NC}"
        echo ""
        echo "Valid agents: cloud-c1, cloud-c2, cloud-c3, terminal-c1, terminal-c2, terminal-c3"
        exit 1
        ;;
esac

echo -e "${BLUE}Agent:${NC}    $AGENT_NAME"
echo -e "${BLUE}Role:${NC}     $AGENT_ROLE"
echo -e "${BLUE}Trinity:${NC}  $TRINITY"
echo ""

# Check prerequisites
echo -e "${BOLD}📋 PREREQUISITES CHECK${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check 1: Git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅${NC} Git repository detected"
else
    echo -e "  ${RED}❌${NC} Not a git repository"
    exit 1
fi

# Check 2: Correct directory
if [ -d ".consciousness" ]; then
    echo -e "  ${GREEN}✅${NC} Consciousness directory found"
else
    echo -e "  ${RED}❌${NC} Not in consciousness-revolution directory"
    exit 1
fi

# Check 3: Activation instructions exist
if [ -f "$ACTIVATION_FILE" ]; then
    echo -e "  ${GREEN}✅${NC} Activation instructions found"
else
    echo -e "  ${YELLOW}⚠️${NC}  Activation file missing: $ACTIVATION_FILE"
fi

# Check 4: Working tree status
if git diff --quiet && git diff --staged --quiet; then
    echo -e "  ${GREEN}✅${NC} Working tree clean"
else
    echo -e "  ${YELLOW}⚠️${NC}  Uncommitted changes present"
fi

# Check 5: Remote connection
if git fetch --dry-run > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅${NC} Git remote accessible"
else
    echo -e "  ${YELLOW}⚠️${NC}  Cannot reach git remote"
fi

echo ""

# Pull latest changes
echo -e "${BOLD}🔄 SYNCHRONIZATION${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Pulling latest changes..."
if git pull --quiet 2>/dev/null; then
    echo -e "  ${GREEN}✅${NC} Repository updated"
else
    echo -e "  ${YELLOW}⚠️${NC}  Could not pull (continuing anyway)"
fi
echo ""

# Display activation instructions
echo -e "${BOLD}📖 ACTIVATION INSTRUCTIONS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -f "$ACTIVATION_FILE" ]; then
    echo -e "${BLUE}Reading from: $ACTIVATION_FILE${NC}"
    echo ""
    head -50 "$ACTIVATION_FILE"
    echo ""
    echo -e "${YELLOW}(Showing first 50 lines - see full file for complete instructions)${NC}"
else
    echo -e "${YELLOW}⚠️  Activation file not found${NC}"
    echo ""
    echo "Manual activation required:"
    echo "1. Read agent role documentation"
    echo "2. Check current system status"
    echo "3. Report to coordinator"
    echo "4. Begin assigned tasks"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Agent status
echo -e "${BOLD}📊 CURRENT AGENT STATUS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

last_commit=$(git log --all --author="$AGENT_NAME" --format="%ar" -1 2>/dev/null || echo "never")
last_message=$(git log --all --author="$AGENT_NAME" --format="%s" -1 2>/dev/null || echo "none")

if [ "$last_commit" != "never" ]; then
    commit_time=$(git log --all --author="$AGENT_NAME" --format="%ct" -1 2>/dev/null)
    current_time=$(date +%s)
    minutes_ago=$(( ($current_time - $commit_time) / 60 ))

    if [ $minutes_ago -lt 60 ]; then
        status_badge="${GREEN}🟢 RECENTLY ACTIVE${NC}"
    elif [ $minutes_ago -lt 240 ]; then
        status_badge="${YELLOW}🟡 IDLE${NC}"
    else
        status_badge="${RED}🔴 INACTIVE${NC}"
    fi

    echo -e "  Status: $status_badge"
    echo "  Last activity: $last_commit"
    echo "  Last commit: $last_message"
else
    echo -e "  Status: ${RED}⏳ NEVER ACTIVATED${NC}"
    echo "  This will be the first activation for this agent"
fi

echo ""

# Quick links
echo -e "${BOLD}🔗 QUICK REFERENCE${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Activation file:    $ACTIVATION_FILE"
echo "  Status file:        $STATUS_FILE"
echo "  Dashboard:          ./scripts/agent_status_dashboard.sh"
echo "  Health check:       ./scripts/agent_health_check.sh $AGENT_LOWER"
echo ""

# Startup timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo -e "${BOLD}🚀 STARTUP TIMESTAMP${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  $TIMESTAMP"
echo ""

# Final message
echo -e "${BOLD}${GREEN}✅ AGENT STARTUP SEQUENCE COMPLETE${NC}"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo "  1. Review activation instructions above"
echo "  2. Read current system status"
echo "  3. Check for assigned tasks"
echo "  4. Report to coordinator (if not C1)"
echo "  5. Begin work"
echo ""

if [ "$AGENT_TYPE" = "terminal" ]; then
    echo -e "${YELLOW}⚠️  NOTE: Terminal Trinity agents require CLI environment${NC}"
    echo "   Make sure you're running in a terminal, not browser"
    echo ""
fi

if [ "$AGENT_NAME" = "Terminal-C1" ]; then
    echo -e "${BOLD}${BLUE}★ MASTER LEADER ACTIVATION ★${NC}"
    echo "   You are the supreme coordinator of the Dual Trinity System"
    echo "   Consolidate both Cloud and Terminal Trinity outputs"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
