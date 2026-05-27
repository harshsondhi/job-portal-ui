#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4>=4.12"]
# ///
"""
Extract unique email addresses from an HTML file.

Examples:
    uv run scripts/extract_emails.py page.html
    uv run scripts/extract_emails.py page.html --json
    uv run scripts/extract_emails.py page.html --include-mailto

Features:
- Extracts emails from visible text
- Optionally extracts emails from mailto: links
- Deduplicates results case-insensitively
- Outputs plain text or JSON
- Returns non-zero exit codes on failure
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup

EMAIL_PATTERN = re.compile(
    r"""
    (?<![\w.+-])                # left boundary
    [A-Z0-9._%+-]+              # local part
    @
    [A-Z0-9.-]+                 # domain
    \.[A-Z]{2,}                 # TLD
    (?![\w.-])                  # right boundary
    """,
    re.IGNORECASE | re.VERBOSE,
)


def extract_emails_from_text(text: str) -> set[str]:
    """Extract emails from plain text."""
    return {
        match.group(0).strip().lower()
        for match in EMAIL_PATTERN.finditer(text)
    }


def extract_mailto_links(soup: BeautifulSoup) -> set[str]:
    """Extract emails from mailto: links."""
    emails: set[str] = set()

    for tag in soup.select('a[href^="mailto:"]'):
        href = tag.get("href", "")
        email = href.removeprefix("mailto:").split("?")[0].strip()

        if email and EMAIL_PATTERN.fullmatch(email):
            emails.add(email.lower())

    return emails


def load_html(path: Path) -> str:
    """Read HTML file safely."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        raise RuntimeError(f"Unable to read file: {path}") from exc


def collect_emails(
    html: str,
    include_mailto: bool = True,
) -> list[str]:
    """Extract and return sorted unique emails."""
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text(separator=" ", strip=True)

    emails = extract_emails_from_text(text)

    if include_mailto:
        emails.update(extract_mailto_links(soup))

    return sorted(emails)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract unique email addresses from an HTML file."
    )

    parser.add_argument(
        "html_file",
        type=Path,
        help="Path to the HTML file",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output emails as JSON",
    )

    parser.add_argument(
        "--no-mailto",
        action="store_true",
        help="Do not extract emails from mailto: links",
    )

    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    path: Path = args.html_file

    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 1

    if not path.is_file():
        print(f"Error: not a file: {path}", file=sys.stderr)
        return 1

    try:
        html = load_html(path)

        emails = collect_emails(
            html,
            include_mailto=not args.no_mailto,
        )

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        json.dump(emails, sys.stdout, indent=2)
        print()
    else:
        for email in emails:
            print(email)

    print(
        f"Found {len(emails)} unique email(s)",
        file=sys.stderr,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())