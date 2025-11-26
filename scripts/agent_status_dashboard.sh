#!/bin/bash
# AGENT STATUS DASHBOARD
# Real-time view of all agent status
# Usage: ./agent_status_dashboard.sh

set -e

REPO_DIR="${REPO_DIR:-.}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

clear
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║         DUAL TRINITY SYSTEM - AGENT DASHBOARD              ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

cd "$REPO_DIR"

# Function to get agent status from git
get_agent_status() {
    local pattern=$1
    last_commit=$(git log --all --author="$pattern" --format="%ar" -1 2>/dev/null || echo "never")

    if [ "$last_commit" != "never" ]; then
        commit_time=$(git log --all --author="$pattern" --format="%ct" -1 2>/dev/null)
        current_time=$(date +%s)
        minutes_ago=$(( ($current_time - $commit_time) / 60 ))

        if [ $minutes_ago -lt 60 ]; then
            echo -e "${GREEN}🟢 ONLINE${NC} (active $last_commit)"
        elif [ $minutes_ago -lt 240 ]; then
            echo -e "${YELLOW}🟡 IDLE${NC} (last seen $last_commit)"
        else
            echo -e "${RED}🔴 OFFLINE${NC} (last seen $last_commit)"
        fi
    else
        echo -e "${RED}⏳ NEVER ACTIVATED${NC}"
    fi
}

echo -e "${BOLD}CLOUD TRINITY (Browser-Based)${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -n "Cloud-C1 (Coordinator): "
get_agent_status "Cloud-C1\|C1 MECHANIC"

echo -n "Cloud-C2 (Builder):     "
get_agent_status "Cloud-C2\|CLOUD-C2\|C2 MECHANIC"

echo -n "Cloud-C3 (Validator):   "
get_agent_status "Cloud-C3\|C3 MECHANIC"

echo ""
echo -e "${BOLD}TERMINAL TRINITY (CLI-Based)${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -n "Terminal-C1★ (MASTER):  "
get_agent_status "Terminal-C1\|TERMINAL-C1"

echo -n "Terminal-C2 (Builder):  "
get_agent_status "Terminal-C2\|TERMINAL-C2"

echo -n "Terminal-C3 (Validator): "
get_agent_status "Terminal-C3\|TERMINAL-C3"

echo ""
echo -e "${BOLD}SYSTEM METRICS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count agents online (commits in last hour)
online_count=0
for pattern in "Cloud-C1" "CLOUD-C2" "Cloud-C3" "Terminal-C1" "Terminal-C2" "Terminal-C3"; do
    if git log --all --author="$pattern" --since="1 hour ago" --format="%h" -1 2>/dev/null | grep -q .; then
        online_count=$((online_count + 1))
    fi
done

echo "Agents Online: $online_count/6 ($(( online_count * 100 / 6 ))%)"

# Recent commits (last 10)
recent_commits=$(git log --all --oneline -10 2>/dev/null | wc -l)
echo "Recent Commits (24h): $recent_commits"

# Git status
if git diff --quiet && git diff --staged --quiet; then
    echo -e "Working Tree: ${GREEN}✅ Clean${NC}"
else
    echo -e "Working Tree: ${YELLOW}⚠️  Uncommitted changes${NC}"
fi

# Check if behind remote
git fetch --quiet 2>/dev/null || true
LOCAL=$(git rev-parse @ 2>/dev/null)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")
if [ "$LOCAL" = "$REMOTE" ]; then
    echo -e "Git Sync: ${GREEN}✅ Up to date${NC}"
elif [ -z "$REMOTE" ]; then
    echo -e "Git Sync: ${YELLOW}⚠️  No remote${NC}"
else
    echo -e "Git Sync: ${RED}❌ Behind remote${NC}"
fi

echo ""
echo -e "${BOLD}DOCUMENTATION STATUS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
doc_lines=$(find . -name "*.md" -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}')
echo "Total Documentation: $doc_lines lines"

md_files=$(find . -name "*.md" 2>/dev/null | wc -l)
echo "Markdown Files: $md_files"

py_files=$(find . -name "*.py" 2>/dev/null | wc -l)
js_files=$(find . -name "*.js" 2>/dev/null | wc -l)
sh_files=$(find . -name "*.sh" 2>/dev/null | wc -l)
echo "Implementation Files: $py_files Python, $js_files JavaScript, $sh_files Shell"

echo ""
echo -e "${BOLD}QUICK ACTIONS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• Health Check: ./scripts/agent_health_check.sh"
echo "• Activate Agent: cat .consciousness/trinity/[AGENT]_ACTIVATION_INSTRUCTIONS.md"
echo "• Hub Status: cat .consciousness/hub/hub_status.md"
echo "• Git Pull: git pull"
echo ""
