#!/usr/bin/env python3
"""
Generate aggregated protocol artifacts from the canonical JSON schemas.

Outputs (written to protocol/dist/):
  - questfoundry.bundle.schema.json: all schemas combined under $defs with local $refs.
  - questfoundry.bundle.deref.schema.json: fully dereferenced version for consumers without $ref support.
  - questfoundry-schema.dot: Graphviz diagram of schema reference relationships.
  - questfoundry-schema.puml: PlantUML component diagram mirroring the Graphviz content.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOTS = [
    ROOT / "protocol" / "schemas",
    ROOT / "schemas",
]
DIST_DIR = ROOT / "protocol" / "dist"


def discover_schema_files() -> List[Tuple[Path, Path]]:
    discovery: List[Tuple[Path, Path]] = []
    for root in SCHEMA_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            discovery.append((path, root))
    discovery.sort(key=lambda item: item[0].as_posix())
    return discovery


def key_for(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix()
    if relative.endswith(".schema.json"):
        relative = relative[: -len(".schema.json")]
    elif relative.endswith(".json"):
        relative = relative[: -len(".json")]
    return relative.replace("/", ".")


def build_reference_map(schema_files: Iterable[Tuple[Path, Path]]) -> Dict[str, str]:
    ref_map: Dict[str, str] = {}
    for path, root in schema_files:
        key = key_for(path, root)
        data = json.loads(path.read_text(encoding="utf-8"))
        rel = path.relative_to(root).as_posix()
        name = path.name
        aliases = {rel, name}
        if rel.endswith(".json"):
            aliases.add(rel[:-5])
        if rel.endswith(".schema.json"):
            aliases.add(rel[:-len(".schema.json")] + ".json")
        schema_id = data.get("$id")
        if schema_id:
            aliases.add(schema_id)
            aliases.add(schema_id.rstrip("/"))
        for alias in aliases:
            ref_map[alias] = f"#/$defs/{key}"
    return ref_map


def rewrite_refs(node, ref_map: Dict[str, str]):
    if isinstance(node, dict):
        new_node = {}
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str) and v in ref_map:
                new_node[k] = ref_map[v]
            else:
                new_node[k] = rewrite_refs(v, ref_map)
        return new_node
    if isinstance(node, list):
        return [rewrite_refs(item, ref_map) for item in node]
    return node


def dereference(node, defs: Dict[str, dict], cache: Dict[str, dict] | None = None):
    cache = cache or {}
    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str) and node["$ref"].startswith("#/$defs/"):
            target_key = node["$ref"].split("/", 2)[-1]
            if target_key in cache:
                return cache[target_key]
            target_schema = deepcopy(defs[target_key])
            cache[target_key] = {}  # placeholder to break potential cycles
            resolved = dereference(target_schema, defs, cache)
            cache[target_key] = resolved
            return resolved
        return {k: dereference(v, defs, cache) for k, v in node.items()}
    if isinstance(node, list):
        return [dereference(item, defs, cache) for item in node]
    return node


def collect_edges(defs: Dict[str, dict]) -> Set[Tuple[str, str]]:
    edges: Set[Tuple[str, str]] = set()

    def walk(source_key: str, node):
        if isinstance(node, dict):
            ref = node.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/$defs/"):
                target_key = ref.split("/", 2)[-1]
                edges.add((source_key, target_key))
            for value in node.values():
                walk(source_key, value)
        elif isinstance(node, list):
            for item in node:
                walk(source_key, item)

    for key, schema in defs.items():
        walk(key, schema)
    return edges


def format_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def ensure_dist_dir() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def format_with_prettier(paths: List[Path]) -> None:
    if not paths:
        return
    prettier = shutil.which("prettier")
    npx = shutil.which("npx")
    command: List[str] | None = None
    path_args = [str(path) for path in paths]
    if prettier:
        command = [prettier, "--write", *path_args]
    elif npx:
        command = [npx, "--yes", "prettier@3.3.2", "--write", *path_args]
    if command is None:
        raise RuntimeError(
            "Prettier is required to format generated JSON. Install Node.js (providing either "
            "'prettier' or 'npx') and re-run the generator."
        )
    subprocess.run(command, check=True)


def build_bundle() -> Tuple[dict, Dict[str, dict]]:
    schema_files = discover_schema_files()
    ref_map = build_reference_map(schema_files)
    defs: Dict[str, dict] = {}
    for path, root in schema_files:
        key = key_for(path, root)
        original = json.loads(path.read_text(encoding="utf-8"))
        defs[key] = rewrite_refs(original, ref_map)

    bundle = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Questfoundry Protocol Schemas",
        "description": (
            "Machine-generated bundle of Questfoundry protocol schemas. "
            "Regenerate via tools/build_schema_artifacts.py."
        ),
        "type": "object",
        "$comment": "Generated file. Do not edit by hand.",
        "$defs": defs,
    }
    return bundle, defs


def generate_graphviz(defs: Dict[str, dict], edges: Set[Tuple[str, str]]) -> str:
    categories: Dict[str, List[str]] = defaultdict(list)
    for key in defs:
        category = key.split(".", 1)[0]
        categories[category].append(key)

    lines = [
        "digraph QuestfoundrySchemas {",
        "  rankdir=LR;",
        "  node [shape=box, style=rounded, fontname=\"Helvetica\", fontsize=10];",
    ]

    for category, items in sorted(categories.items()):
        lines.append(f'  subgraph cluster_{category.replace("-", "_")} {{')
        lines.append(f'    label="{category.capitalize()}";')
        for item in sorted(items):
            lines.append(f'    "{item}";')
        lines.append("  }")

    for source, target in sorted(edges):
        lines.append(f'  "{source}" -> "{target}";')

    lines.append("}")
    return "\n".join(lines) + "\n"


def safe_identifier(name: str) -> str:
    return re.sub(r"[^0-9A-Za-z_]", "_", name)


def generate_plantuml(defs: Dict[str, dict], edges: Set[Tuple[str, str]]) -> str:
    categories: Dict[str, List[str]] = defaultdict(list)
    for key in defs:
        category = key.split(".", 1)[0]
        categories[category].append(key)

    lines = ["@startuml", "left to right direction", "skinparam componentStyle rectangle"]

    for category, items in sorted(categories.items()):
        lines.append(f'package "{category.capitalize()}" {{')
        for item in sorted(items):
            identifier = safe_identifier(item)
            lines.append(f'  component "{item}" as {identifier}')
        lines.append("}")

    for source, target in sorted(edges):
        lines.append(f"{safe_identifier(source)} --> {safe_identifier(target)}")

    lines.append("@enduml")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--graph-only",
        action="store_true",
        help="Skip JSON bundle generation and only refresh diagram outputs.",
    )
    args = parser.parse_args()

    ensure_dist_dir()
    bundle, defs = build_bundle()
    edges = collect_edges(defs)

    if not args.graph_only:
        write_file(DIST_DIR / "questfoundry.bundle.schema.json", format_json(bundle))
        deref_bundle = dereference(bundle, bundle["$defs"])
        write_file(DIST_DIR / "questfoundry.bundle.deref.schema.json", format_json(deref_bundle))
        format_with_prettier(sorted(DIST_DIR.glob("*.json")))

    graphviz_src = generate_graphviz(defs, edges)
    write_file(DIST_DIR / "questfoundry-schema.dot", graphviz_src)

    plantuml_src = generate_plantuml(defs, edges)
    write_file(DIST_DIR / "questfoundry-schema.puml", plantuml_src)


if __name__ == "__main__":
    main()
