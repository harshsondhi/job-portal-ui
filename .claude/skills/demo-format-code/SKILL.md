---
name: demo-format-code
description: Format Python files using Black. Use when the user asks to format, beautify, prettify, or auto-style Python code. Demonstrates the "one-off command" pattern without bundled scripts.
---

### Execution Rule
* Run Black via `uvx` without local installation.

### Command
```bash
uvx black@24.10.0 <file-or-directory>
```

### Critical Notes
* **Version Pinning**: The pinned version (`@24.10.0`) guarantees identical formatting outcomes over time.
* **Drift Prevention**: Running without a pinned version causes formatting drift as upstream packages update.
