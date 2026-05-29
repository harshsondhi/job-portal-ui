"""
Skill trigger eval: reads eval_queries.json, asks Claude whether the skill
description would trigger for each query, then reports accuracy by split.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-...
    python eval.py
"""

import json
import os
from pathlib import Path
import anthropic

SKILL_DESCRIPTION = """
Analyze CSV and tabular data files — compute summary statistics, add derived
columns, generate charts, and clean messy data. Use when the user has a CSV,
TSV, or Excel file and wants to explore, transform, or visualize the data,
even if they don't explicitly mention "CSV" or "analysis."
""".strip()

JUDGE_PROMPT = """You are evaluating whether an AI agent should activate a skill.

Skill description:
{description}

User query:
"{query}"

Should the skill activate for this query? Reply with exactly one word: YES or NO.
"""


def judge(client: anthropic.Anthropic, query: str) -> bool:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=5,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(description=SKILL_DESCRIPTION, query=query)
        }]
    )
    answer = response.content[0].text.strip().upper()
    return answer.startswith("YES")


def run_eval():
    data = json.loads(Path("eval_queries.json").read_text())
    queries = data["queries"]

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    results = {"train": {"correct": 0, "total": 0}, "validation": {"correct": 0, "total": 0}}
    failures = []

    for q in queries:
        triggered = judge(client, q["query"])
        expected = q["should_trigger"]
        correct = triggered == expected
        split = q["set"]

        results[split]["total"] += 1
        if correct:
            results[split]["correct"] += 1
        else:
            failures.append({
                "id": q["id"],
                "split": split,
                "query": q["query"][:60] + "…",
                "expected": "TRIGGER" if expected else "NO-TRIGGER",
                "got": "TRIGGER" if triggered else "NO-TRIGGER",
                "note": q.get("note", ""),
            })

    print("\n=== Results ===")
    for split, r in results.items():
        pct = 100 * r["correct"] / r["total"] if r["total"] else 0
        print(f"  {split:12s}: {r['correct']}/{r['total']}  ({pct:.0f}%)")

    if failures:
        print("\n=== Failures ===")
        for f in failures:
            direction = "FALSE POSITIVE" if f["got"] == "TRIGGER" else "FALSE NEGATIVE"
            print(f"  [{f['split']}] id={f['id']} {direction}")
            print(f"    query : {f['query']}")
            print(f"    note  : {f['note']}")
            print()

    print("Fix guide:")
    fp = [f for f in failures if f["got"] == "TRIGGER"]
    fn = [f for f in failures if f["got"] == "NO-TRIGGER"]
    if fn:
        print(f"  {len(fn)} false negative(s) → description too narrow, broaden trigger phrases")
    if fp:
        print(f"  {len(fp)} false positive(s) → description too broad, add anti-trigger context")


if __name__ == "__main__":
    run_eval()
