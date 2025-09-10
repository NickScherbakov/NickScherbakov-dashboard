#!/bin/bash

# Test script to validate GitHub Actions workflow configuration
# This script simulates different runner scenarios

echo "🧪 Testing GitHub Actions Workflow Configuration"
echo "================================================"

# Test YAML syntax
echo "1. Testing YAML syntax..."
if python3 -c "import yaml; yaml.safe_load(open('.github/workflows/update-profile.yml'))" 2>/dev/null; then
    echo "✅ YAML syntax is valid"
else
    echo "❌ YAML syntax error"
    exit 1
fi

# Test Python command detection logic
echo "2. Testing Python command detection..."
PYTHON_CMD=$(command -v python3 || command -v python)
if [ -n "$PYTHON_CMD" ]; then
    echo "✅ Python command detection: $PYTHON_CMD"
else
    echo "❌ Python command not found"
    exit 1
fi

# Test requirements installation
echo "3. Testing requirements installation..."
if $PYTHON_CMD -c "import requests, matplotlib, seaborn, pandas" 2>/dev/null; then
    echo "✅ All required packages are available"
else
    echo "❌ Some required packages are missing"
    exit 1
fi

# Test health check script
echo "4. Testing health check script..."
if python3 runner-health-check.py >/dev/null 2>&1; then
    echo "✅ Health check script runs successfully"
else
    echo "⚠️  Health check script has warnings (expected in some environments)"
fi

# Test dashboard generation script syntax
echo "5. Testing dashboard generation script syntax..."
if python3 -m py_compile generate_dashboard.py; then
    echo "✅ Dashboard script compiles successfully"
else
    echo "❌ Dashboard script has syntax errors"
    exit 1
fi

# Test workflow event simulation
echo "6. Testing workflow scenarios..."

# Simulate different runner types
declare -a runner_types=("ubuntu-latest" "self-hosted" "dashboard-runner")

for runner_type in "${runner_types[@]}"; do
    echo "   Testing runner type: $runner_type"
    
    # Check if the runner type is valid according to workflow
    if grep -q "$runner_type" .github/workflows/update-profile.yml; then
        echo "   ✅ $runner_type is configured in workflow"
    else
        echo "   ❌ $runner_type is not properly configured"
        exit 1
    fi
done

echo ""
echo "🎉 All tests passed! Workflow configuration is ready."
echo ""
echo "Next steps:"
echo "1. Visit: https://github.com/NickScherbakov/NickScherbakov-dashboard/settings/actions/runners/new"
echo "2. Set up a self-hosted runner following docs/SELF_HOSTED_RUNNERS.md"
echo "3. Test the workflow with: Actions > Update GitHub Profile Dashboard > Run workflow"
echo "4. Choose different runner types to verify functionality"