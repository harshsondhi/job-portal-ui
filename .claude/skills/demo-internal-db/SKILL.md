---
name: demo-internal-db
description: Generate SQL queries against the internal users, subscriptions, and billing database. Use this skill when the user requests user lookups, account states, customer churn status, or data from the users, subscriptions, or billing tables. Demonstrates the high-value "Gotchas + Templates" pattern.
---

## System Constraints & Gotchas

- **Subscription Status Logic:** 
  - Churned accounts remain in the table. Cancellation is marked as `status = 'churned'`.
  - To find active customers, you **must** filter using: `WHERE status IN ('trialing', 'active')`.
  - **Warning:** `WHERE deleted_at IS NULL` will incorrectly include churned accounts.

- **ID Mapping Consistency:** 
  - Stripe Customer ID (`cus_xxx`) = `payment_customer_id` (in `accounts` table) = `billing_id` (in public API).
  - These three identifiers are identical. Never create or assume a new identifier format.

- **System Health Checks:** 
  - The standard `/healthcheck` endpoint reports green even with >60 second DB replication lag.
  - For data-freshness or replication lag verification, you **must** instruct the use of `/healthcheck/strict`.

## Output Template

You must ALWAYS format your response using this exact structure:

```markdown
**Query intent:** [One line describing the purpose of the SQL query]

**SQL:**
```sql
-- Generated SQL here
```

**Gotchas applied:** [List the specific gotchas from above that shaped this query, or state "none applied"]
```

## Workflow Execution Steps

1. **Analyze:** Parse the user's data request to identify the required tables and fields.
2. **Apply Gotchas:** Evaluate the request against the active customer filters, ID mappings, and health check definitions listed above.
3. **Generate:** Draft the precise SQL query based on these constraints.
4. **Format:** Output the result using the mandatory template. Do not omit the "Gotchas applied" section.
