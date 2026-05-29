---
name: demo-migrate-component
description: Migrate a UI component from one framework to another. Use when invoked as /demo-migrate-component <component> <from> <to>. Demonstrates named positional arguments via the `arguments` frontmatter field.
arguments: [component, from_framework, to_framework]
argument-hint: "[ComponentName] [from-framework] [to-framework]"
disable-model-invocation: true
---

Migrate the **$component** component from **$from_framework** to **$to_framework**.

## Approach

1. **Locate the source component**: Search for files named `$component.*` or matching the pattern.
2. **Analyze the source**: Read the file and list the framework-specific APIs it uses (e.g., `useState`, `v-model`, signals).
3. **Map the APIs**: Translate each identified API to its direct equivalent in `$to_framework`.
4. **Generate the migrated component**: Create the new component while strictly preserving:
   - All existing behaviors and functionality.
   - Props and external API shapes so dependent callers do not break.
   - Existing unit tests (translate the test suite to the new framework as well).
5. **Save the output**: Write the new file alongside the original codebase. Do not delete the source file until the user explicitly confirms the migration.
