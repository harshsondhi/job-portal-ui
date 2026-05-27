#!/usr/bin/env python3
"""Manual eval runner for csv-analyst skill trigger detection."""

#python3 .claude/skills/csv-analyst/evals/eval.py

import json
from pathlib import Path


def load_queries():
    path = Path(__file__).parent / "eval_queries.json"
    with open(path) as f:
        return json.load(f)


def prompt_result(query_id, set_name, query, note):
    print(f"\n{'─' * 60}")
    print(f"  ID {query_id:>2}  [{set_name}]")
    print(f"  Query : {query}")
    print(f"  Note  : {note}")
    print()
    while True:
        raw = input("  Did the skill trigger? [t]rigger / [s]kip : ").strip().lower()
        if raw in ("t", "trigger"):
            return True
        if raw in ("s", "skip"):
            return False
        print("  Please enter 't' or 's'.")


def score(results):
    tp = sum(1 for r in results if r["expected"] and r["got"])
    fp = sum(1 for r in results if not r["expected"] and r["got"])
    fn = sum(1 for r in results if r["expected"] and not r["got"])
    tn = sum(1 for r in results if not r["expected"] and not r["got"])
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return tp, fp, fn, tn, precision, recall


def print_summary(label, results):
    if not results:
        return
    tp, fp, fn, tn, precision, recall = score(results)
    total = len(results)
    passed = tp + tn
    print(f"\n  {label}")
    print(f"    Pass      : {passed}/{total}")
    print(f"    Precision : {precision:.0%}  (false positives: {fp})")
    print(f"    Recall    : {recall:.0%}  (false negatives: {fn})")

    failures = [r for r in results if r["expected"] != r["got"]]
    if failures:
        print("    Failures  :")
        for r in failures:
            exp = "trigger" if r["expected"] else "skip"
            got = "trigger" if r["got"] else "skip"
            print(f"      ID {r['id']:>2} — expected {exp}, got {got}  | {r['note']}")


def main():
    data = load_queries()
    queries = data["queries"]

    train = [q for q in queries if q["set"] == "train"]
    validation = [q for q in queries if q["set"] == "validation"]

    print("\ncsv-analyst skill — manual eval")
    print("Run each query in a fresh Claude Code session, then record the result here.")

    train_results = []
    print("\n\n=== TRAIN SET ===")
    for q in train:
        got = prompt_result(q["id"], q["set"], q["query"], q["note"])
        expected = q["should_trigger"]
        passed = got == expected
        label = "PASS" if passed else "FAIL"
        print(f"  → {label}  (expected {'trigger' if expected else 'skip'}, got {'trigger' if got else 'skip'})")
        train_results.append({"id": q["id"], "expected": expected, "got": got, "note": q["note"]})

    print("\n\n=== VALIDATION SET ===")
    print("  Run these only once — do not adjust the skill between queries.")
    val_results = []
    for q in validation:
        got = prompt_result(q["id"], q["set"], q["query"], q["note"])
        expected = q["should_trigger"]
        passed = got == expected
        label = "PASS" if passed else "FAIL"
        print(f"  → {label}  (expected {'trigger' if expected else 'skip'}, got {'trigger' if got else 'skip'})")
        val_results.append({"id": q["id"], "expected": expected, "got": got, "note": q["note"]})

    print("\n\n══════════════════════════════════════════════════")
    print("  RESULTS SUMMARY")
    print("══════════════════════════════════════════════════")
    print_summary("Train (IDs 0–11)", train_results)
    print_summary("Validation (IDs 12–19)", val_results)
    all_results = train_results + val_results
    print_summary("Overall", all_results)
    print()


if __name__ == "__main__":
    main()
