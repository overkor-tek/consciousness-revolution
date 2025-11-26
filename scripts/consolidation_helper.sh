#!/bin/bash
# CONSOLIDATION HELPER
# Assists with Trinity consolidation workflow
# Usage: ./consolidation_helper.sh [cloud|terminal|master]

set -e

MODE=${1:-"help"}
REPO_DIR="${REPO_DIR:-.}"

cd "$REPO_DIR"

case "$MODE" in
    cloud)
        echo "🌥️  CLOUD TRINITY CONSOLIDATION HELPER"
        echo "======================================"
        echo ""
        echo "Reading Cloud Trinity outputs..."
        echo ""

        if [ -f ".consciousness/trinity/c2_to_c1.md" ]; then
            echo "📝 Cloud-C2 Output:"
            echo "---"
            tail -20 .consciousness/trinity/c2_to_c1.md
            echo ""
        fi

        if [ -f ".consciousness/trinity/c3_to_c1.md" ]; then
            echo "📝 Cloud-C3 Output:"
            echo "---"
            tail -20 .consciousness/trinity/c3_to_c1.md
            echo ""
        fi

        echo "Next steps for Cloud-C1:"
        echo "1. Review C2 and C3 outputs above"
        echo "2. Synthesize into unified response"
        echo "3. Write to: .consciousness/hub/from_cloud/consolidated_output.md"
        echo "4. Commit and push"
        ;;

    terminal)
        echo "💻 TERMINAL TRINITY CONSOLIDATION HELPER"
        echo "========================================"
        echo ""
        echo "Reading Terminal Trinity outputs..."
        echo ""

        if [ -f ".consciousness/trinity_terminal/c2_to_c1.md" ]; then
            echo "📝 Terminal-C2 Output:"
            echo "---"
            tail -20 .consciousness/trinity_terminal/c2_to_c1.md
            echo ""
        fi

        if [ -f ".consciousness/trinity_terminal/c3_to_c1.md" ]; then
            echo "📝 Terminal-C3 Output:"
            echo "---"
            tail -20 .consciousness/trinity_terminal/c3_to_c1.md
            echo ""
        fi

        echo "Next steps for Terminal-C1:"
        echo "1. Review C2 and C3 outputs above"
        echo "2. Synthesize into unified response"
        echo "3. Write to: .consciousness/hub/from_terminal/consolidated_output.md"
        echo "4. Commit and push"
        ;;

    master)
        echo "🌟 MASTER CONSOLIDATION HELPER"
        echo "================================"
        echo ""
        echo "Reading both Trinity outputs..."
        echo ""

        if [ -f ".consciousness/hub/from_cloud/consolidated_output.md" ]; then
            echo "📝 Cloud Trinity Output:"
            echo "---"
            tail -30 .consciousness/hub/from_cloud/consolidated_output.md
            echo ""
        else
            echo "⚠️  Cloud Trinity output not found"
            echo ""
        fi

        if [ -f ".consciousness/hub/from_terminal/consolidated_output.md" ]; then
            echo "📝 Terminal Trinity Output:"
            echo "---"
            tail -30 .consciousness/hub/from_terminal/consolidated_output.md
            echo ""
        else
            echo "⚠️  Terminal Trinity output not found"
            echo ""
        fi

        echo "Next steps for Terminal-C1★ (MASTER):"
        echo "1. Review both Trinity outputs above"
        echo "2. Synthesize into UNIFIED master response"
        echo "3. Write to: .consciousness/hub/master_consolidated.md"
        echo "4. Commit and push"
        echo "5. Report to user"
        ;;

    *)
        echo "📖 CONSOLIDATION HELPER - USAGE"
        echo "================================="
        echo ""
        echo "This script helps with the consolidation workflow."
        echo ""
        echo "Usage:"
        echo "  ./consolidation_helper.sh cloud     - Cloud Trinity consolidation"
        echo "  ./consolidation_helper.sh terminal  - Terminal Trinity consolidation"
        echo "  ./consolidation_helper.sh master    - Master hub consolidation"
        echo ""
        echo "Consolidation Flow:"
        echo "  1. Cloud-C1 consolidates Cloud-C2 + Cloud-C3"
        echo "  2. Terminal-C1 consolidates Terminal-C2 + Terminal-C3"
        echo "  3. Terminal-C1★ consolidates both Trinities (master)"
        echo ""
        ;;
esac
