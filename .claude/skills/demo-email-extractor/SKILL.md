---
name: demo-email-extractor
description: Extract email addresses from an HTML file using a bundled Python script. Use when the user asks to find, pull, list, or extract emails from a webpage, HTML file, or document.
---

### Execution
Run the bundled extractor script using `uv`:
```bash
uv run scripts/extract_emails.py <path-to-html>
```

### Behavior & Dependencies
* **Zero Setup**: The script declares its own inline dependencies (PEP 723). No manual environment setup is required.
* **Mechanism**: The script parses content via BeautifulSoup to strip HTML tags and uses regular expressions to isolate email addresses.

### Output Formatting
* Present the discovered unique emails as a plain list, with one email per line.
* If no emails are found, explicitly state that zero emails were detected.
