
#!/usr/bin/env python3
import json, argparse
from pathlib import Path
try:
    import jsonschema
except Exception:
    jsonschema = None

SCHEMAS_DIR = Path("protocol/schemas")
EXAMPLES_DIR = Path("examples/golden")

def build_store():
    store = {}
    for p in SCHEMAS_DIR.rglob("*.json"):
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        store[p.name] = obj
        try:
            store['file://' + str(p.resolve())] = obj
            store[str(p.relative_to(SCHEMAS_DIR))] = obj
        except Exception:
            pass
        if isinstance(obj, dict) and obj.get("$id"):
            store[obj["$id"]] = obj
    return store

def load_registry():
    reg = {}
    for p in SCHEMAS_DIR.rglob("*.json"):
        try:
            reg[p.name] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return reg

def find_schema(msg, reg):
    mt = msg.get("message_type","")
    for c in (f"{mt}.schema.json", f"{mt.rsplit('.',1)[0]}.schema.json" if '.' in mt else None):
        if c and c in reg: return reg[c]
    return None

def validate(msg, schema, store):
    if jsonschema is None or schema is None: return True, "parsed"
    base_uri = (SCHEMAS_DIR / "events").resolve().as_uri() + "/"
    resolver = jsonschema.RefResolver(base_uri=base_uri, referrer=schema, store=store)
    try:
        jsonschema.validate(instance=msg, schema=schema, resolver=resolver)
        return True, "ok"
    except Exception as e:
        return False, str(e)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    store = build_store()
    reg = load_registry()
    ok = True
    for p in sorted(EXAMPLES_DIR.glob("*.json")):
        try:
            msg = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            ok=False; print(f"[FAIL] {p.name}: invalid json {e}"); continue
        schema = find_schema(msg, reg)
        good, info = validate(msg, schema, store)
        if good:
            if a.verbose: print(f"[OK] {p.name} [{msg.get('message_type','?')}]")
        else:
            ok=False; print(f"[FAIL] {p.name}: {info}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
