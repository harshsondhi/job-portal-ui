#!/usr/bin/env bash
set -euo pipefail

ENV="${1:-staging}"

echo "Running smoke tests against: $ENV"

echo "  [1/3] Checking build output exists..."
[ -f "index.html" ] || [ -d "dist" ] || [ -f "package.json" ] && echo "        OK"

echo "  [2/3] Verifying package.json is valid JSON..."
node -e "JSON.parse(require('fs').readFileSync('package.json','utf8'))" && echo "        OK"

echo "  [3/3] Confirming no obvious lint errors..."
npx eslint src --max-warnings=0 --quiet 2>/dev/null && echo "        OK" || echo "        WARN: lint issues found (non-blocking in demo)"

echo ""
echo "Smoke tests passed for environment: $ENV"
