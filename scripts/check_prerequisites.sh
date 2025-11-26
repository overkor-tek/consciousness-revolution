#!/bin/bash
# PREREQUISITES CHECK SCRIPT
# Validates environment readiness for Dual Trinity System
# Usage: ./check_prerequisites.sh [--verbose]

set -e

VERBOSE=${1:-""}
REPO_DIR="${REPO_DIR:-.}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

ISSUES_COUNT=0
WARNINGS_COUNT=0
PASSED_COUNT=0

echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║        DUAL TRINITY - PREREQUISITES VALIDATION             ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

cd "$REPO_DIR" 2>/dev/null || {
    echo -e "${RED}❌ CRITICAL: Cannot access repository directory${NC}"
    exit 1
}

# Function to check and report
check_requirement() {
    local name=$1
    local check_command=$2
    local critical=${3:-"yes"}

    if eval "$check_command" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅${NC} $name"
        PASSED_COUNT=$((PASSED_COUNT + 1))
        return 0
    else
        if [ "$critical" = "yes" ]; then
            echo -e "  ${RED}❌${NC} $name"
            ISSUES_COUNT=$((ISSUES_COUNT + 1))
        else
            echo -e "  ${YELLOW}⚠️${NC}  $name"
            WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
        fi
        return 1
    fi
}

# ============================================================================
# SECTION 1: CORE SYSTEM REQUIREMENTS
# ============================================================================
echo -e "${BOLD}1️⃣  CORE SYSTEM REQUIREMENTS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_requirement "Git installed" "command -v git"
check_requirement "Bash shell available" "command -v bash"
check_requirement "Standard Unix tools (grep, awk, sed)" "command -v grep && command -v awk && command -v sed"

echo ""

# ============================================================================
# SECTION 2: REPOSITORY STRUCTURE
# ============================================================================
echo -e "${BOLD}2️⃣  REPOSITORY STRUCTURE${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_requirement "Git repository initialized" "git rev-parse --git-dir"
check_requirement ".consciousness directory exists" "[ -d .consciousness ]"
check_requirement "Hub directory exists" "[ -d .consciousness/hub ]"
check_requirement "Cloud Trinity directory exists" "[ -d .consciousness/trinity ]"
check_requirement "Terminal Trinity directory exists" "[ -d .consciousness/trinity_terminal ]"
check_requirement "Scripts directory exists" "[ -d scripts ]"
check_requirement "Sync directory exists" "[ -d .consciousness/sync ]" "no"

echo ""

# ============================================================================
# SECTION 3: CRITICAL FILES
# ============================================================================
echo -e "${BOLD}3️⃣  CRITICAL DOCUMENTATION FILES${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_requirement "Hub protocol exists" "[ -f .consciousness/hub/HUB_PROTOCOL.md ]"
check_requirement "Multi-level architecture exists" "[ -f .consciousness/hub/MULTI_LEVEL_TRINITY_ARCHITECTURE.md ]"
check_requirement "Hub status file exists" "[ -f .consciousness/hub/hub_status.md ]"
check_requirement "Trinity status file exists" "[ -f .consciousness/trinity/trinity_status.md ]"

# Activation files
check_requirement "Cloud-C1 activation instructions" "[ -f .consciousness/trinity/C1_ACTIVATION_INSTRUCTIONS.md ]"
check_requirement "Cloud-C2 activation instructions" "[ -f .consciousness/trinity/C2_ACTIVATION_INSTRUCTIONS.md ]"
check_requirement "Cloud-C3 activation instructions" "[ -f .consciousness/trinity/C3_ACTIVATION_INSTRUCTIONS.md ]"
check_requirement "Terminal Trinity activation guide" "[ -f .consciousness/trinity_terminal/TERMINAL_TRINITY_ACTIVATION_GUIDE.md ]" "no"

echo ""

# ============================================================================
# SECTION 4: AUTOMATION SCRIPTS
# ============================================================================
echo -e "${BOLD}4️⃣  AUTOMATION INFRASTRUCTURE${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_requirement "Agent health check script" "[ -f scripts/agent_health_check.sh ]"
check_requirement "Agent status dashboard script" "[ -f scripts/agent_status_dashboard.sh ]"
check_requirement "Auto-sync status script" "[ -f scripts/auto_sync_status.sh ]"
check_requirement "Consolidation helper script" "[ -f scripts/consolidation_helper.sh ]"
check_requirement "Agent startup script" "[ -f scripts/start_agent.sh ]" "no"

# Check if scripts are executable
if [ -f scripts/agent_health_check.sh ]; then
    check_requirement "Health check script is executable" "[ -x scripts/agent_health_check.sh ]"
fi

if [ -f scripts/agent_status_dashboard.sh ]; then
    check_requirement "Dashboard script is executable" "[ -x scripts/agent_status_dashboard.sh ]"
fi

echo ""

# ============================================================================
# SECTION 5: GIT CONFIGURATION
# ============================================================================
echo -e "${BOLD}5️⃣  GIT CONFIGURATION${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_requirement "Git user.name configured" "git config user.name"
check_requirement "Git user.email configured" "git config user.email"
check_requirement "Git remote configured" "git remote get-url origin"

# Check git connectivity
if git ls-remote --exit-code --heads origin > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅${NC} Git remote accessible"
    PASSED_COUNT=$((PASSED_COUNT + 1))
else
    echo -e "  ${YELLOW}⚠️${NC}  Cannot connect to git remote"
    WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
fi

# Check for uncommitted changes
if git diff --quiet && git diff --staged --quiet; then
    echo -e "  ${GREEN}✅${NC} Working tree clean"
    PASSED_COUNT=$((PASSED_COUNT + 1))
else
    echo -e "  ${YELLOW}⚠️${NC}  Uncommitted changes present"
    WARNINGS_COUNT=$((WARNINGS_COUNT + 1))

    if [ "$VERBOSE" = "--verbose" ] || [ "$VERBOSE" = "-v" ]; then
        echo "     Modified files:"
        git status --short | head -5
    fi
fi

# Check if behind remote
git fetch --quiet 2>/dev/null || true
LOCAL=$(git rev-parse @ 2>/dev/null)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")

if [ -n "$REMOTE" ]; then
    if [ "$LOCAL" = "$REMOTE" ]; then
        echo -e "  ${GREEN}✅${NC} Up to date with remote"
        PASSED_COUNT=$((PASSED_COUNT + 1))
    else
        BEHIND=$(git rev-list --count HEAD..@{u} 2>/dev/null || echo "0")
        AHEAD=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo "0")

        if [ "$BEHIND" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️${NC}  Behind remote by $BEHIND commit(s)"
            WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
        fi

        if [ "$AHEAD" -gt 0 ]; then
            echo -e "  ${BLUE}ℹ️${NC}  Ahead of remote by $AHEAD commit(s)"
        fi
    fi
fi

echo ""

# ============================================================================
# SECTION 6: AGENT STATUS
# ============================================================================
echo -e "${BOLD}6️⃣  AGENT STATUS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Function to check agent activity
check_agent_active() {
    local agent_name=$1
    local pattern=$2

    if git log --all --author="$pattern" --since="1 hour ago" --format="%h" -1 2>/dev/null | grep -q .; then
        echo -e "  ${GREEN}✅${NC} $agent_name is active"
        PASSED_COUNT=$((PASSED_COUNT + 1))
        return 0
    else
        last_commit=$(git log --all --author="$pattern" --format="%ar" -1 2>/dev/null || echo "never")
        if [ "$last_commit" = "never" ]; then
            echo -e "  ${YELLOW}⏳${NC} $agent_name never activated"
        else
            echo -e "  ${YELLOW}🟡${NC} $agent_name idle (last: $last_commit)"
        fi
        WARNINGS_COUNT=$((WARNINGS_COUNT + 1))
        return 1
    fi
}

# Check Cloud Trinity
check_agent_active "Cloud-C1" "Cloud-C1"
check_agent_active "Cloud-C2" "Cloud-C2\|CLOUD-C2"
check_agent_active "Cloud-C3" "Cloud-C3"

# Check Terminal Trinity
check_agent_active "Terminal-C1" "Terminal-C1\|TERMINAL-C1"
check_agent_active "Terminal-C2" "Terminal-C2\|TERMINAL-C2"
check_agent_active "Terminal-C3" "Terminal-C3\|TERMINAL-C3"

echo ""

# ============================================================================
# SECTION 7: SYSTEM METRICS
# ============================================================================
echo -e "${BOLD}7️⃣  SYSTEM METRICS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count documentation
md_files=$(find . -name "*.md" 2>/dev/null | wc -l)
echo "  Documentation files: $md_files markdown files"

# Count implementation
sh_files=$(find scripts -name "*.sh" 2>/dev/null | wc -l || echo "0")
py_files=$(find . -name "*.py" 2>/dev/null | wc -l)
js_files=$(find . -name "*.js" 2>/dev/null | wc -l)
echo "  Implementation files: $sh_files shell, $py_files python, $js_files javascript"

# Recent commits
commits_24h=$(git log --all --since="24 hours ago" --format="%h" 2>/dev/null | wc -l)
echo "  Recent commits (24h): $commits_24h"

# Total commits
total_commits=$(git rev-list --all --count 2>/dev/null || echo "0")
echo "  Total commits: $total_commits"

echo ""

# ============================================================================
# FINAL REPORT
# ============================================================================
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║                    VALIDATION SUMMARY                      ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

TOTAL_CHECKS=$((PASSED_COUNT + WARNINGS_COUNT + ISSUES_COUNT))

echo -e "  ${GREEN}✅ Passed:${NC}   $PASSED_COUNT / $TOTAL_CHECKS"
echo -e "  ${YELLOW}⚠️  Warnings:${NC} $WARNINGS_COUNT / $TOTAL_CHECKS"
echo -e "  ${RED}❌ Failed:${NC}   $ISSUES_COUNT / $TOTAL_CHECKS"
echo ""

# Overall status
if [ $ISSUES_COUNT -eq 0 ]; then
    if [ $WARNINGS_COUNT -eq 0 ]; then
        echo -e "${BOLD}${GREEN}🎉 PERFECT - System is fully ready!${NC}"
        echo ""
        echo "All prerequisites met. You can safely activate agents."
        EXIT_CODE=0
    else
        echo -e "${BOLD}${GREEN}✅ READY - System is operational${NC}"
        echo ""
        echo "System is ready with minor warnings. Safe to proceed."
        echo "Warnings are informational and don't block operation."
        EXIT_CODE=0
    fi
else
    echo -e "${BOLD}${RED}❌ NOT READY - Critical issues detected${NC}"
    echo ""
    echo "Please fix critical issues before activating agents."
    echo "Run with --verbose flag for more details:"
    echo "  ./scripts/check_prerequisites.sh --verbose"
    EXIT_CODE=1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit $EXIT_CODE
