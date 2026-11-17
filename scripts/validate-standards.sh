#!/usr/bin/env bash
set -euo pipefail
required=(
  README.md AGENTS.md .env.example .gitignore
  .github/workflows/standards.yml .github/pull_request_template.md
  .github/ISSUE_TEMPLATE/task.yml
  docs/requirements.md docs/architecture.md docs/security.md docs/deployment.md
  docs/development/working-agreement.md docs/development/roadmap.md
  docs/development/task-template.md docs/development/adoption-checklist.md
)
for path in "${required[@]}"; do
  if [[ ! -s "$path" ]]; then
    echo "Missing or empty required file: $path" >&2
    exit 1
  fi
done
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # Check tracked changes when a git repository is present.
  git diff --check
fi
echo "Standards structure: OK (${#required[@]} required files)"
