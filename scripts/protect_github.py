#!/usr/bin/env python3
"""Preview or create a repository-level main ruleset with explicit approval."""
import argparse
import json
import re
import subprocess
import sys


class ProtectionError(Exception):
    pass


def api(method, path, payload=None):
    cmd = ["gh", "api", "--method", method, path, "-H", "Accept: application/vnd.github+json"]
    if payload is not None:
        cmd += ["--input", "-"]
    try:
        result = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                                capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise ProtectionError("GitHub CLI (gh) is not installed") from exc
    if result.returncode:
        raise ProtectionError("GitHub API request failed (" + method + " " + path +
                              ", exit " + str(result.returncode) + "). Check permissions and plan.")
    try:
        return json.loads(result.stdout)
    except ValueError as exc:
        raise ProtectionError("GitHub returned invalid JSON") from exc


def make_ruleset(check):
    rules = [
        {"type": "deletion"},
        {"type": "non_fast_forward"},
        {"type": "pull_request", "parameters": {
            "required_approving_review_count": 0,
            "dismiss_stale_reviews_on_push": False,
            "require_code_owner_review": False,
            "require_last_push_approval": False,
            "required_review_thread_resolution": False,
        }},
    ]
    if check:
        rules.append({"type": "required_status_checks", "parameters": {
            "strict_required_status_checks_policy": True,
            "do_not_enforce_on_create": False,
            "required_status_checks": [{"context": check}],
        }})
    return {
        "name": "main-protection",
        "target": "branch",
        "enforcement": "active",
        "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
        "rules": rules,
    }


def validate_repo(repo):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repo) or ".." in repo:
        raise ProtectionError("Expected --repo OWNER/REPOSITORY")


def check_existing(repo):
    return api("GET", "repos/" + repo + "/rulesets")


def run(repo, check=None, apply=False, approve=None):
    validate_repo(repo)
    if check and not re.fullmatch(r"[A-Za-z0-9_. /-]{1,100}", check):
        raise ProtectionError("Invalid required status check name")
    target = make_ruleset(check)
    if not apply:
        return {"mode": "DRY RUN", "repo": repo, "planned_ruleset": target,
                "note": "No GitHub API write or read performed."}
    if approve != repo:
        raise ProtectionError("--approve must exactly match the target repository")
    metadata = api("GET", "repos/" + repo)
    if metadata.get("full_name", "").lower() != repo.lower():
        raise ProtectionError("Repository identity mismatch")
    if metadata.get("default_branch") != "main":
        raise ProtectionError("Default branch is not main; refusing to configure")
    existing = check_existing(repo)
    if not isinstance(existing, list):
        raise ProtectionError("Could not verify existing rulesets")
    if any(r.get("name") == "main-protection" for r in existing):
        raise ProtectionError("main-protection already exists; refusing to overwrite")
    if any(r.get("target") == "branch" for r in existing):
        raise ProtectionError("Other branch rulesets exist; review them manually before proceeding")
    if check:
        # A status check must be visible in a completed GitHub Actions workflow run
        # before it is required. This is an operator assertion, not an automatic check.
        raise ProtectionError("Set the required status check later, after verifying its run; omit --check for first application")
    created = api("POST", "repos/" + repo + "/rulesets", target)
    ruleset_id = created.get("id")
    if not isinstance(ruleset_id, int):
        raise ProtectionError("Creation response lacks an ID; inspect GitHub before retrying")
    verified = api("GET", "repos/" + repo + "/rulesets/" + str(ruleset_id))
    if verified.get("enforcement") != "active" or verified.get("conditions", {}).get("ref_name", {}).get("include") != ["refs/heads/main"]:
        raise ProtectionError("Ruleset created but verification failed; inspect GitHub settings")
    types = {r.get("type") for r in verified.get("rules", [])}
    if not {"pull_request", "deletion", "non_fast_forward"}.issubset(types):
        raise ProtectionError("Ruleset created but some protections missing")
    return {"mode": "APPLIED", "repo": repo, "ruleset_id": ruleset_id, "verified": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="OWNER/REPOSITORY")
    parser.add_argument("--check", help="preview only: planned required CI check")
    parser.add_argument("--apply", action="store_true", help="create a ruleset on GitHub")
    parser.add_argument("--approve", help="exact OWNER/REPOSITORY confirmation required with --apply")
    args = parser.parse_args()
    try:
        outcome = run(args.repo, args.check, args.apply, args.approve)
    except ProtectionError as exc:
        parser.error(str(exc))
    print(json.dumps(outcome, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
