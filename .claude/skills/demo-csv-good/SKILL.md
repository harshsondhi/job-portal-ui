---
name: demo-csv-good
description: Analyzes CSV, TSV, and Excel-style tabular data. Reads columns, summarizes rows, computes stats, generates charts, and identifies missing data. Trigger this skill whenever a user references tabular files (even implicitly without using keywords like "CSV" or "spreadsheet") to explore, transform, or visualize data.
---

# Tabular Data Analyzer

## Intent
The user wants to explore, summarize, transform, or visualize a structured data file (CSV, TSV, or XLSX), regardless of where the file is stored.

## Actions
1. **Read File**: Locate and open the tabular file mentioned or implied by the user.
2. **Metadata Extraction**: Compute the total row count and identify all column names along with their inferred data types.
3. **Data Preview**: Extract the first 3 rows of the dataset to show a quick preview.
4. **Data Quality Audit**: Scan the dataset to find obvious data-quality issues, such as columns with high null counts or mixed data types.
5. **Generate Summary**: Output all the gathered information into a clean, structured Markdown summary.
6. **Conditional Visualization**: If the user explicitly requests a chart, execute a Python script using `matplotlib` via a one-off command: `uvx --with matplotlib python -c "..."`.
