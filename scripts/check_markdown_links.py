#!/usr/bin/env python3
"""Validate local Markdown file/directory links without network dependencies.

External URLs and same-page anchors are intentionally out of scope.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[[^\]\n]*\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+"[^"]*")?\)')


def check_file(path: Path) -> list[str]:
    errors = []
    fenced = False
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith(("~~~", "```")):
            fenced = not fenced
            continue
        if fenced:
            continue
        for match in LINK.finditer(line):
            target = match.group("target").strip("<>")
            if not target or target.startswith("#") or "://" in target:
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            local = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not local:
                continue
            dest = (path.parent / local).resolve()
            if not dest.is_relative_to(ROOT) or not dest.exists():
                errors.append(f"{path.relative_to(ROOT)}:{line_no}: broken local link: {target}")
    return errors


def main() -> int:
    errors = [error for path in ROOT.rglob("*.md") for error in check_file(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Local Markdown links: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
