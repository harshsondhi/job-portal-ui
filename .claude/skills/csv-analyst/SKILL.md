# csv-analyst skill

## Description
Analyze CSV and tabular data files — compute summary statistics, add derived columns, generate charts, and clean messy data. Use when the user has a CSV, TSV, or Excel file and wants to explore, transform, or visualize the data, even if they don't explicitly mention "CSV" or "analysis."

## Steps
1. Read the file and detect delimiter (comma, tab, pipe, etc.)
2. Print shape, column names, dtypes, and null counts
3. For numeric columns: compute mean, median, std, min/max
4. Apply any transformation the user requested (new column, filter, chart)
5. Save the result unless the user only wanted a summary

## Example Usage
* **User:** "I have q4_results.xlsx — add a profit margin column and flag rows under 10%"
* **User:** "can you summarize this sales.csv for me?"
* **User:** "clean up the date formats in my export file"
