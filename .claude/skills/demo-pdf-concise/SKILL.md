<!-- ---
name: demo-pdf-concise
description: Extract text from a PDF file. The concise counterpart to demo-pdf-verbose. Use when the user wants to extract, read, or pull text out of a PDF.
---

Use `pdfplumber`. For scanned PDFs, fall back to `pdf2image` + `pytesseract`.

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
``` -->