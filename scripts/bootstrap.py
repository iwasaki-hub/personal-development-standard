#!/usr/bin/env python3
"""Safely bootstrap a NEW template-based repository. Python stdlib only."""
import argparse
import json
import re
from pathlib import Path

STACKS = ("web", "mobile-expo", "api", "database-supabase")
CONFIG_PATH = Path("project.config.json")
WORKFLOW_PATH = Path(".github/workflows/stack-ci.yml")


def validate(project, stacks_raw):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{1,62}", project):
        raise ValueError("project must be 2-63 characters, start with a letter, and contain only letters, digits, - or _")
    stacks = [s.strip() for s in stacks_raw.split(",")]
    if not stacks or any(s not in STACKS for s in stacks):
        raise ValueError("unknown stack; choose from " + ", ".join(STACKS))
    if len(stacks) != len(set(stacks)):
        raise ValueError("duplicate stack")
    return stacks


def workflow(stacks):
    node = any(s in stacks for s in ("web", "mobile-expo", "api"))
    lines = [
        "name: Stack CI",
        "on:",
        "  pull_request:",
        "  push:",
        "    branches: [main]",
        "permissions:",
        "  contents: read",
        "jobs:",
        "  validate:",
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - uses: actions/checkout@v4",
    ]
    if node:
        lines += [
            "      - uses: actions/setup-node@v4",
            "        with:",
            "          node-version: '22'",
            "          cache: npm",
            "      - run: npm ci",
        ]
        scripts = ["lint", "typecheck", "test"]
        if "web" in stacks:
            scripts.append("build")
        lines += ["      - run: npm run " + script for script in scripts]
    if "database-supabase" in stacks:
        lines += [
            "      - name: Review Supabase migrations",
            "        run: |",
            "          echo 'Supabase migrations require separate review, isolated testing and explicit approval.'",
            "          echo 'This workflow does NOT apply migrations or verify RLS.'",
        ]
    return "\n".join(lines) + "\n"


def plan(project, stacks):
    return {
        CONFIG_PATH: json.dumps({"version": "0.3", "name": project, "stacks": stacks}, indent=2, ensure_ascii=False) + "\n",
        WORKFLOW_PATH: workflow(stacks),
    }


def execute(project, stacks, apply=False, root=Path(".")):
    outputs = plan(project, stacks)
    conflicts = [str(root / p) for p in outputs if (root / p).exists()]
    if conflicts:
        raise FileExistsError("refusing to overwrite: " + ", ".join(conflicts))
    if apply:
        for path, content in outputs.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--stacks", required=True, help="comma-separated: " + ",".join(STACKS))
    parser.add_argument("--apply", action="store_true", help="write files (default: dry run)")
    args = parser.parse_args()
    try:
        stacks = validate(args.project, args.stacks)
        outputs = execute(args.project, stacks, args.apply)
    except (ValueError, OSError) as err:
        parser.error(str(err))
    print("Mode:", "APPLY" if args.apply else "DRY RUN")
    for path in outputs:
        print("  ", path)
    if not args.apply:
        print("No files changed. Add --apply to write these files.")
    else:
        print("Files generated; review them before a PR. No GitHub or deployment changes performed.")


if __name__ == "__main__":
    main()
