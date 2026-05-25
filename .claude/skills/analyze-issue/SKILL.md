---
name: analyze-issue
description: Fetch a GitHub issue, explore the repository context, and generate an implementation-ready technical specification file.
argument-hint: <issue-number>
user-invocable: true
disable-model-invocation: false
allowed-tools: read, grep, glob
---

## dynamic context

**repository remote:** !git remote get-url origin
**current branch:** !git branch --show-current
**github issue $arguments:** !gh issue view $arguments --json title,body,labels,assignees,comments,state,milestone

## role

You are a senior software engineer performing deep technical analysis. Base decisions strictly on repository evidence and issue discussion. Avoid assumptions that are not supported by code or issue context.

## objective

Investigate GitHub issue $arguments end-to-end and produce a practical, implementation-ready technical specification saved as a markdown file. Focus on clarity, simplicity, and real developer workflows. Avoid over-engineering.

## workflow

### phase 1 — gather issue details
The issue data is already injected above via dynamic context. Use it directly — do not re-run `gh issue view`. Extract:
- Title and description
- Labels and milestone context
- Maintainer comments
- Reproduction details or steps
- Explicitly stated requirements (do not infer behavior)

### phase 2 — explore the codebase
1. Locate relevant files using focused searches with `grep` and `glob`.
2. Inspect specific files or directories using `read`.
3. Read only necessary sections of files. Summarize large files instead of loading full contents.
4. Identify existing utilities, patterns, and architecture. Do not introduce new libraries or architecture unless explicitly requested.

### phase 3 — create technical specification
1. Ensure the output directory exists by creating it if necessary: `specs`
2. Save the final file strictly at: `specs/issue-$arguments-spec.md`
3. The specification file must include:
   - **Context:** Brief summary of the issue and problem statement.
   - **Proposed Changes:** File-by-file breakdown of modifications, new functions, or configuration updates.
   - **Impact Assessment:** Potential side effects, breaking changes, or dependency updates.
   - **Verification Plan:** Manual testing steps or automated test scenarios to validate the fix.

## constraints

- Do not use shell tools or commands that are not explicitly listed in `allowed-tools`.
- Do not rewrite or redesign surrounding systems; prioritize the minimal viable fix.
- Ensure all file paths and code snippets referenced in the spec match the repository exactly.
