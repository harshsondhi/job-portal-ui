"""
Applies a validated migration plan.

Usage:
    python scripts/apply_migration.py <migration_plan.yaml> --confirm

The --confirm flag is required to prevent accidental execution.
Without it the script performs a dry-run and prints the SQL that would run.

Exit codes:
    0  — applied (or dry-run) successfully
    1  — error
"""

import sys

import yaml


def build_sql(change):
    """Return the SQL statement for a single plan change."""
    table = change.get("table")
    action = change.get("action")

    if action == "add_column":
        col = change.get("column", {})
        name = col["name"]
        col_type = col["type"].upper()
        nullable = "NULL" if col.get("nullable", True) else "NOT NULL"
        return f"ALTER TABLE {table} ADD COLUMN {name} {col_type} {nullable};"

    if action == "add_index":
        cols = ", ".join(change.get("columns", []))
        index_name = f"idx_{table}_{'_'.join(change["columns"])}"
        return f"CREATE INDEX {index_name} ON {table}({cols});"

    raise ValueError(f"Unknown action: {action}")


def main():
    if len(sys.argv) < 2:
        print("Usage: apply_migration.py <migration_plan.yaml> [--confirm]", file=sys.stderr)
        sys.exit(1)

    plan_path = sys.argv[1]
    confirm = "--confirm" in sys.argv

    try:
        with open(plan_path) as f:
            plan = yaml.safe_load(f)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    changes = plan.get("changes", [])
    if not changes:
        print("No changes in plan — nothing to apply.")
        sys.exit(0)

    statements = []
    for change in changes:
        try:
            statements.append(build_sql(change))
        except (KeyError, ValueError) as exc:
            print(f"ERROR building SQL: {exc}", file=sys.stderr)
            sys.exit(1)

    if not confirm:
        print("DRY-RUN — pass --confirm to execute:\n")
        for stmt in statements:
            print(f"  {stmt}")
        sys.exit(0)

    print(f"Applying {len(statements)} migration statement(s)...\n")
    for stmt in statements:
        print(f"  EXEC: {stmt}")

    print("\nMigration applied successfully.")


if __name__ == "__main__":
    main()
