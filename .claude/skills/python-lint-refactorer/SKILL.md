---
name: python-lint-refactorer
description: Executes precise Python code modifications while maintaining strict code quality. Leverages an iterative validation loop to guarantee that all modified files pass standard linting checks before completion.
tags: [python, refactor, linting, automation-loop]
---

## 🎯 Purpose
Use this skill when a user requests to modify, fix, refactor, optimize, or clean up Python code. It ensures that no broken or poorly formatted code is returned to the user.

## 🔄 The Validation-Loop Workflow

### 1. 🛠️ Implement the Modification
* Apply the exact changes, refactors, or fixes requested by the user.
* Limit edits strictly to the target area to prevent regression errors.

### 2. 🔍 Execute the Quality Gate
* Run the linter immediately using the following explicit command:
  ```bash
  uvx ruff@0.8.0 check <file>
  ```

### 3. 🔁 Iterative Correction Loop
If the linter detects errors, initiate the self-correction cycle:
* **Analyze:** Read the exact error message and locate the failing line.
* **Isolate:** Fix only the specific syntax, style, or type violation. 
* **Verify:** Re-run the lint command from Step 2.

### 4. 🛑 Circuit Breaker & Safe Exit
* **Success Gate:** Proceed to Step 5 only when the linter returns a clean execution (zero errors).
* **Failure Threshold:** If linting fails after **3 consecutive patch attempts**, halt the loop.
* **Escalation:** Present the persistent error to the user. Explain potential root causes like configuration mismatches or missing external dependencies.

### 5. 📦 Deliver & Report
* Present the final, verified code to the user.
* Confirm that the code has successfully passed all structural and stylistic linting checks.
