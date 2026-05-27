# bad-example.md — illustrates what NOT to do (principle 7.2 "Before")

## BAD description
description: Process CSV files.

## Why it fails
- No imperative phrasing ("Use when…" is missing)
- "Process" is vague — compute? upload? delete?
- Won't trigger on "spreadsheet", "xlsx", "tabular", "export file"
- No near-miss exclusions, so may false-positive on CSV-adjacent requests

## Contrast with SKILL.md in this folder
SKILL.md uses:
  ✓ Imperative trigger: "Use when the user has…"
  ✓ Intent-focused: lists what user wants (explore, transform, visualize)
  ✓ Pushiness: "even if they don't explicitly mention 'CSV'"
  ✓ Multi-format: CSV, TSV, Excel — catches indirect phrasing
