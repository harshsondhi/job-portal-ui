---
name: demo-pdf-verbose
description: Extract text from a PDF file. A comprehensive walkthrough of the available Python libraries. Use when the user wants a detailed comparison of PDF extraction options before picking one.
---

# PDF text extraction

PDF (Portable Document Format) is a file format developed by Adobe Systems in the 1990s as a way to present documents independent of application software, hardware, and operating systems. PDFs are widely used because they preserve formatting across viewers, can embed fonts, and support both text and images.

To extract text from a PDF in Python, you have several options. The most popular library is `pdfplumber`, which provides a high-level interface for extracting text, tables, and metadata. It is built on top of `pdfminer.six` and is generally considered easier to use than the underlying library.

Another option is `PyPDF2` (now maintained as `pypdf`), which is older and well-established but generally less reliable for complex layouts. There is also `PyMuPDF` (sometimes imported as `fitz`), which is faster but has a more complex API.

For scanned documents that contain only images of text rather than actual text characters, none of these libraries will work directly. You will need to use Optical Character Recognition (OCR). The standard approach is to first convert the PDF pages to images using `pdf2image`, then run OCR on each image using `pytesseract` (a Python wrapper around the Tesseract OCR engine).

Before doing any of this, you should think about what you actually need. If you only need the text from a single page, you can use any of the above libraries with minimal setup. If you need to handle a mix of text and scanned PDFs, you will need a more elaborate pipeline that first attempts text extraction and falls back to OCR.

So, to extract text from a PDF, use pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```