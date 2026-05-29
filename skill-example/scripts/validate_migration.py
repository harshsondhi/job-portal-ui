"""
Validates a migration plan against a current schema snapshot.

Usage:
    python scripts/validate_migration.py <schema.sql> <migration_plan.yaml>

Exit codes:
    0  — validation passed
    1  — validation failed (details printed to stderr)
"""

import re
import sys

import yaml


VALID_TYPES = {
    "int", "integer", "serial", "bigint", "bigserial",
    "varchar", "text", "char",
    "numeric", "decimal", "float", "real", "double precision",
    "boolean", "bool",
    "timestamptz", "timestamp", "date", "time",
    "uuid", "json", "jsonb",
}


def parse_schema(sql_path):
    """Return {table: {columns: set, indexes: list}} from a pg_dump SQL file."""
    schema = {}
    with open(sql_path) as f:
        content = f.read()

    for match in re.finditer(
        r"CREATE TABLE (\w+)\s*\((.+?)\);",
        content,
        re.DOTALL | re.IGNORECASE,
    ):
        table = match.group(1).lower()
        body = match.group(2)
        columns = set()
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if not line or line.upper().startswith(("PRIMARY", "UNIQUE", "FOREIGN", "CHECK", "CONSTRAINT")):
                continue
            col_name = line.split()[0].lower()
            columns.add(col_name)
        schema[table] = {"columns": columns, "indexes": []}

    for match in re.finditer(
        r"CREATE(?:\s+UNIQUE)?\s+INDEX\s+\w+\s+ON\s+(\w+)\s*\((.+?)\)",
        content,
        re.IGNORECASE,
    ):
        table = match.group(1).lower()
        cols = tuple(c.strip().lower() for c in match.group(2).split(","))
        if table in schema:
            schema[table]["indexes"].append(cols)

    return schema


def load_plan(yaml_path):
    with open(yaml_path) as f:
        return yaml.safe_load(f)


def validate(schema, plan):
    errors = []

    for change in plan.get("changes", []):
        table = change.get("table", "").lower()
        action = change.get("action", "")

        if table not in schema:
            errors.append(f"[{action}] Table '{table}' does not exist in schema.")
            continue

        if action == "add_column":
            col = change.get("column", {})
            col_name = col.get("name", "").lower()
            col_type = col.get("type", "").lower()

            if col_name in schema[table]["columns"]:
                errors.append(
                    f"[add_column] Column '{col_name}' already exists on '{table}'."
                )

            base_type = re.split(r"[\s(]", col_type)[0]
            if base_type not in VALID_TYPES:
                errors.append(
                    f"[add_column] Unknown type '{col_type}' for '{table}.{col_name}'."
                )

        elif action == "add_index":
            on_cols = tuple(c.lower() for c in change.get("columns", []))
            missing = [c for c in on_cols if c not in schema[table]["columns"]]
            if missing:
                errors.append(
                    f"[add_index] Column(s) {missing} do not exist on '{table}'."
                )
            if on_cols in schema[table]["indexes"]:
                errors.append(
                    f"[add_index] Index on {list(on_cols)} already exists on '{table}'."
                )

        else:
            errors.append(f"Unknown action '{action}' on table '{table}'.")

    return errors


def main():
    if len(sys.argv) != 3:
        print("Usage: validate_migration.py <schema.sql> <migration_plan.yaml>", file=sys.stderr)
        sys.exit(1)

    schema_path, plan_path = sys.argv[1], sys.argv[2]

    try:
        schema = parse_schema(schema_path)
        plan = load_plan(plan_path)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    errors = validate(schema, plan)

    if errors:
        print("Validation FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"Validation PASSED — {len(plan.get('changes', []))} change(s) ready to apply.")


if __name__ == "__main__":
    main()
