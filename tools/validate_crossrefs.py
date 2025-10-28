#!/usr/bin/env python3
"""Validate cross-references using rules from /04-contracts/tests/crossref_assertions/rules.json."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "04-contracts" / "tests" / "crossref_assertions" / "rules.json"

def main(project_root="."):
    project_root = Path(project_root)
    if not RULES.exists():
        print("No rules.json found; skipping cross-ref validation.")
        return 0
    rules = json.loads(RULES.read_text(encoding="utf-8"))
    print(f"Loaded {len(rules.get('rules', []))} rules from {RULES}")
    # TODO: implement collectors & checks
    return 0

if __name__ == "__main__":
    sys.exit(main())
