---
name: demo-api-helper
description: Diagnoses internal Users API issues, 4xx/5xx status codes, and user lookup failures.
---

# Intent Trigger
Use this skill when the user mentions:
* Users API errors
* 4xx or 5xx status codes from the users service
* User lookup failures

# Instructions

## 1. Handle Known Errors
* Read `references/api-errors.md` to look up the error code.
* Apply the specific recovery procedure documented for that code.

## 2. Handle Unknown Errors
* If the error code is missing from `api-errors.md`, explicitly state that it is not documented.
* Recommend that the user capture a `curl` reproduction command.

## 3. Reference Material
* Read `references/request-examples.md` when you need request body examples.

# Design Architecture
* **Context Efficiency:** Reference data is split into the `references/` directory to prevent context bloat. 
* **Dynamic Loading:** The agent must only load these secondary files upon encountering an actual error, rather than during initial invocation.
