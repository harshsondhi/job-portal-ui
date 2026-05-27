---
name: demo-release
description: Cut a release of the current project. Trigger when the user says "ship it", "cut a release", "deploy", "release the new version", or invokes /demo-release directly. Demonstrates the checklist pattern with strict sequential orchestration.
disable-model-invocation: true
---

# Release Orchestration: `$ARGUMENTS`

Interpret the first argument as the target version (e.g., `v1.2.3`). If no version is provided, run `git describe --tags` or check `package.json`/`Cargo.toml` to suggest the next logical semantic version before proceeding.

## Execution Rules
1. **Linear Progression**: You must execute steps in exact numerical order.
2. **State Persistence**: Rewrite this checklist in every turn, changing `[ ]` to `[x]` ONLY after verifying the successful exit code of the tool command.
3. **Hard Stop on Failure**: If any command returns a non-zero exit code or explicit error text, STOP immediately. Do not proceed to the next step.

## Progress Checklist

- [ ] **Step 1: Sanity Check Working Tree**
  * Run: `git status --porcelain`
  * Verification: Output must be completely empty. If uncommitted changes exist, halt and ask to stash or commit.

- [ ] **Step 2: Pre-Flight Staging Smoke Tests**
  * Run: `scripts/smoke.sh staging`
  * Verification: Confirm the script exits with code 0 and outputs a success confirmation.

- [ ] **Step 3: Local Semantic Version Tagging**
  * Run: `git tag -a $ARGUMENTS -m "Release $ARGUMENTS via demo-release skill"`
  * Verification: Confirm tag creation by running `git tag -l $ARGUMENTS`.

- [ ] **Step 4: Upstream Synchronization**
  * Run: `git push origin $ARGUMENTS`
  * Verification: Ensure the remote repository accepts the new tag reference.

- [ ] **Step 5: Post-Deployment Production Health Audit**
  * Run: `scripts/verify_health.sh prod`
  * Verification: Confirm all live production endpoints return successful HTTP status codes.

## Error Recovery Protocol
If a failure occurs during or after **Step 3**, you must offer the user an automated rollback option:
* Run `git tag -d $ARGUMENTS` to delete the local tag.
* Run `git push --delete origin $ARGUMENTS` if the tag reached the remote server.
