#!/usr/bin/env python3
"""Validation script to keep docs/index.md, router files, and registry in sync."""

from __future__ import annotations

import argparse
import pathlib
import sys
import textwrap
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS_INDEX = ROOT / "docs" / "index.md"
REGISTRY = ROOT / "scripts" / "workflow_registry.yaml"


def load_registry() -> dict:
    if not REGISTRY.exists():
        raise SystemExit(f"Registry file missing: {REGISTRY}")
    with REGISTRY.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def ensure_router(router_path: pathlib.Path, canonical_path: pathlib.Path, errors: list[str]):
    if not router_path.exists():
        errors.append(f"Missing router file: {router_path}")
        return

    content = router_path.read_text(encoding="utf-8")
    if str(canonical_path.relative_to(ROOT)) not in content:
        errors.append(
            f"Router {router_path} does not reference canonical {canonical_path.relative_to(ROOT)}"
        )


def check_section(keyword: str, registry_entries: dict, errors: list[str]):
    if DOCS_INDEX.exists():
        index_text = DOCS_INDEX.read_text(encoding="utf-8")
        for key, meta in registry_entries.items():
            router_rel = meta["router"]
            if router_rel.split("/", 1)[-1].split(".md")[0] not in index_text:
                errors.append(
                    f"docs/index.md missing link mention for {keyword} entry '{key}' (router {router_rel})"
                )
    else:
        errors.append(f"docs/index.md missing at {DOCS_INDEX}")


def validate_registry(registry: dict) -> list[str]:
    errors: list[str] = []
    for section, entries in registry.items():
        for name, meta in entries.items():
            router = ROOT / meta["router"]
            canonical = ROOT / meta["canonical"]
            if not canonical.exists():
                errors.append(f"Canonical file missing for {section}.{name}: {canonical}")
            ensure_router(router, canonical, errors)
        check_section(section, entries, errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    registry = load_registry()
    errors = validate_registry(registry)
    if errors:
        message = "\n".join(f"- {err}" for err in errors)
        print(textwrap.dedent(
            f"""\nValidation failed with {len(errors)} issue(s):\n{message}\n"""
        ))
        return 1

    print("All documentation entries validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
