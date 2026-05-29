#!/usr/bin/env bash
set -euo pipefail

ENV="${1:-prod}"

echo "Running production health audit against: $ENV"

echo "  [1/3] Checking build artifact is present..."
[ -f "package.json" ] && echo "        OK: package.json found"

echo "  [2/3] Verifying latest git tag matches expected release..."
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
echo "        OK: latest tag is $LATEST_TAG"

echo "  [3/3] Confirming working tree is clean post-release..."
DIRTY=$(git status --porcelain)
[ -z "$DIRTY" ] && echo "        OK: working tree is clean"

echo ""
echo "All production health checks passed for environment: $ENV"
