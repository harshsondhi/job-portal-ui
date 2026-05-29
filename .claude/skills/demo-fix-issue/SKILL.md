---
name: demo-fix-issue
description: Fix a GitHub issue by number, following the project's coding standards. Use when invoked as /demo-fix-issue <number>. Demonstrates the $arguments placeholder.
disable-model-invocation: true
---

Fix GitHub issue **$arguments** following our coding standards.

## Workflow

1. **Fetch the issue:** Run `gh issue view $arguments` to view details.
2. **Analyze requirements:** Restate the core requirements in your own words.
3. **Implement the fix:** Modify the codebase to resolve the issue.
4. **Update tests:** Write or update tests to cover the new behavior.
5. **Verify changes:** Run the test suite to ensure everything passes.
6. **Commit changes:** Use the exact message `fix: <one-line description> (#$arguments)`.
7. **Final step:** Do not push the changes—leave that decision to the user.
