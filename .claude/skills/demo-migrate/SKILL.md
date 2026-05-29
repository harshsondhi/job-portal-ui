---
name: demo-migrate
description: Run a database schema migration safely using pre-dumped schemas. Use when the user mentions migration, alter table, add column, schema change, or anything touching production database schema. Demonstrates the plan-validate-execute pattern.
disable-model-invocation: true
---

## Workflow

### 1. Plan
Document every intended structural change directly in the skill's migration plan file:
`./migration_plan.yaml`

**Example Plan:**
```yaml
changes:
  - table: users
    action: add_column
    column: 
      name: deleted_at
      type: timestamptz
      nullable: true
  - table: orders
    action: add_index
    on: [customer_id, created_at]
```

### 2. Validate
Run the automated validation script against the existing local schema file `./current_schema.sql`:

```bash
python ./scripts/validate_migration.py \
  ./current_schema.sql \
  ./migration_plan.yaml
```

**Required Validation Checks:**
* **Duplicate Prevention:** Column or index must not already exist.
* **Type Compatibility:** Type changes must be compatible with existing table data.
* **Integrity Constraints:** No unresolved foreign-key or unique constraint conflicts.
* **Concurrency:** Verify no other concurrent migration is currently in flight.

### 3. Iterate
If validation fails, read the error output carefully. Revise the `./migration_plan.yaml` file and re-run step 2. Do not proceed to step 4 until validation passes with zero errors.

### 4. Apply
Execute the migration on the production database only after achieving a successful validation status:
```bash
python ./scripts/apply_migration.py \
  ./migration_plan.yaml --confirm
```
