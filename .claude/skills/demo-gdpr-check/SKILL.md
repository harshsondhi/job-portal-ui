---
name: demo-gdpr-check
description: Audit database queries for GDPR compliance before execution. Trigger automatically when any query targets tables related to users, events, accounts, or any schema prefixed with `pii_*`, regardless of explicit user intent or mention of compliance. Demonstrates the domain-expertise pattern.
---

## Checklist
For every query interacting with data categories listed in the description, you must evaluate three core pillars prior to approval:

1. **PII Scope**: Identify if the query selects direct or indirect identifiers (e.g., email, name, address, phone, IP address, device IDs, or any column in `pii_*` tables).
2. **Lawful Basis**: Verify the presence of a valid GDPR Article 6 legal ground (e.g., explicit consent, contractual necessity, legal obligation, or documented legitimate interest) explicitly stated in the context.
3. **Data Residency & Transfer**: Identify the target destination and region of the query results. Any transfer outside the EEA or EU-approved adequate countries requires standard contractual clauses (SCCs).

## Output Format
Analyze the query and provide the assessment using this exact Markdown structure:

```markdown
**Query:** [The evaluated SQL statement]
**PII Pulled:** [List specific columns | "None identified"]
**Lawful Basis:** [Identified basis from context | "MISSING — Compliance Failure"]
**Destination:** [Target system / AWS or cloud region / "Unknown"]
**Verdict:** [APPROVE | REFUSE | NEEDS-MORE-INFO]
**Reason:** [Provide explicit justification. For REFUSE or NEEDS-MORE-INFO, cite the relevant GDPR rule, such as Art. 6 (Lawfulness) or Art. 44 (International Transfers)]
```

## Execution Rules
* **Hard Block**: If the verdict is `REFUSE`, do not execute, optimize, or output the requested SQL query.
* **Information Gathering**: If the verdict is `NEEDS-MORE-INFO`, pause execution and prompt the user for the missing compliance details.
