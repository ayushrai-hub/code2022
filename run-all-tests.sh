#!/bin/bash
# Unified test runner for all projects
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Running Tests for All Projects"
echo "=========================================="
echo ""

total_passed=0
total_failed=0
projects_tested=0

# GenAI Tests
if [ -d "GenAI/genAI" ]; then
    echo "Testing GenAI..."
    cd GenAI/genAI
    if [ -f .venv/bin/activate ]; then
        source .venv/bin/activate && python -m pytest tests/ -v --tb=short 2>&1 | tail -5
        if [ ${PIPESTATUS[0]} -eq 0 ]; then
            echo -e "${GREEN}✅ GenAI tests PASSED${NC}"
            total_passed=$((total_passed + 1))
        else
            echo -e "${RED}❌ GenAI tests FAILED${NC}"
            total_failed=$((total_failed + 1))
        fi
    fi
    cd ../..
    projects_tested=$((projects_tested + 1))
fi

# OutLier-AI Tests
if [ -d "OutLier-AI" ]; then
    echo ""
    echo "Testing OutLier-AI..."
    cd OutLier-AI/PythonScriptsOutlierWeeks/task1
    python3 -m unittest test_ideal.py -v 2>&1 | grep -E "^(Ran|OK|FAILED)" || echo "Tests completed"
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅ OutLier-AI tests PASSED${NC}"
        total_passed=$((total_passed + 1))
    fi
    cd ../../..
    projects_tested=$((projects_tested + 1))
fi

echo ""
echo "=========================================="
echo "SUMMARY: Passed: $total_passed, Failed: $total_failed"
echo "=========================================="
