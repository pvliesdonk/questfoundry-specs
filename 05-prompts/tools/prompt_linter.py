#!/usr/bin/env python3
"""
Prompt Linter: enforce the shared scaffold on prompt-pack markdown files.

- Default root: 05-prompts/packs
- Only scans within the chosen root (no repo-wide crawl)
- Ignores files named HEURISTICS.md (the policy doc itself)
"""

import sys
import pathlib
import re

REQUIRED = ["Context", "Goal", "Constraints", "Inputs", "Outputs", "Failure Policy"]

def find_md_files(root: pathlib.Path):
    for p in root.rglob("*.md"):
        # Skip the heuristics policy and anything outside root (rglob guarantees inside)
        if p.name.lower() == "heuristics.md":
            continue
        yield p

def lint(root: pathlib.Path, fail_on_missing: bool = True) -> int:
    missing = []
    for p in find_md_files(root):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for h in REQUIRED:
            # accept headings at any level; must appear as a heading (start of line, optional #'s, then term)
            if re.search(rf"(?m)^\s*#*\s*{re.escape(h)}\b", text, re.IGNORECASE) is None:
                missing.append((p, h))
    if missing:
        for f, h in missing:
            print(f"[LINT] {f} missing section: {h}")
        if fail_on_missing:
            return 1
    else:
        print("Prompt lint OK")
    return 0

def main():
    argv = sys.argv[1:]
    if argv:
        root = pathlib.Path(argv[0]).resolve()
    else:
        root = pathlib.Path("05-prompts/packs").resolve()
    if not root.exists():
        print(f"[WARN] Path not found: {root}")
        return 0
    rc = lint(root)
    sys.exit(rc)

if __name__ == "__main__":
    main()

