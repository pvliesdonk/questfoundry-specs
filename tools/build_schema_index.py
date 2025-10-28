#!/usr/bin/env python3
"""Generate /04-contracts/SCHEMA_INDEX.md by scanning JSON schema files."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "04-contracts" / "SCHEMA_INDEX.md"

def iter_schemas(base):
    for p in base.rglob("*.json"):
        if "tests" in p.parts:
            continue
        name = p.name.lower()
        if ".schema." in name or "schemas" in "/".join(p.parts).lower() or name.endswith("_schema.json"):
            yield p

def main():
    schemas = list(iter_schemas(ROOT/"04-contracts")) + list(iter_schemas(ROOT/"03-protocol"))
    lines = ["# SCHEMA INDEX", ""]
    count = 0
    for p in sorted(schemas):
        try:
            data = json.loads(p.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            data = {}
        title = data.get("title") or data.get("$id") or p.name
        desc = data.get("description") or data.get("$comment") or ""
        rel = p.relative_to(ROOT).as_posix()
        lines.append(f"- **{title}** — `{rel}`")
        if isinstance(desc, str) and desc.strip():
            lines.append(f"  - {desc.strip()}")
        count += 1
    lines.append(f"\n_Total schemas discovered: {count}_\n")
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {TARGET} with {count} entries.")

if __name__ == "__main__":
    main()

