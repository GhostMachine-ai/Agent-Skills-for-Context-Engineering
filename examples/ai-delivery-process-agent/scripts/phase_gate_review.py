#!/usr/bin/env python3
"""
phase_gate_review.py

Runs a structured phase gate review for an AI delivery project.
Checks for required artefacts, prints a summary, and exits with
code 1 if blocking criteria are unmet.

This is pseudocode demonstrating the pattern. Adapt paths, artefact
names, and criteria for your specific project.

Usage:
    python scripts/phase_gate_review.py --phase alpha --project-dir .
    python scripts/phase_gate_review.py --phase all --project-dir .
"""

import argparse
import sys
from pathlib import Path
from typing import NamedTuple


class Criterion(NamedTuple):
    name: str
    description: str
    check_paths: list       # list of relative paths; any must exist
    required: bool
    ai_only: bool
    check_keyword: str      # keyword that must appear in the found file; "" = not checked


PHASE_CRITERIA = {
    "alignment": [
        Criterion("Problem Statement", "Agreed problem statement document", ["problem-statement.md", "docs/problem-statement.md"], True, False, ""),
        Criterion("AI Constraints Document", "Vendor and data sovereignty constraints", ["ai-constraints.md", "docs/ai-constraints.md"], True, True, "vendor"),
        Criterion("Ethics Review Initiated", "Acknowledgement of ethics review submission", ["docs/ethics-review.md", "docs/algorithmic-accountability.md"], True, True, ""),
        Criterion("AI Feasibility Assessment", "Signed-off feasibility by AI/ML Systems Thinker", ["docs/feasibility.md", "alignment/feasibility.md"], True, True, ""),
    ],
    "discovery": [
        Criterion("User Research Report", "Research completed with target users", ["docs/research-report.md", "discovery/research-report.md"], True, False, ""),
        Criterion("Data Availability Matrix", "No TBD severity ratings", ["docs/data-availability-matrix.md", "artefacts/data-availability-matrix.md"], True, True, "severity"),
        Criterion("Task-Model Fit Assessment", "In-scope and out-of-scope tasks defined", ["docs/task-model-fit.md", "artefacts/task-model-fit.md"], True, True, ""),
        Criterion("Draft HITL Map", "Based on user research findings", ["docs/hitl-map.md", "artefacts/hitl-map.md"], True, True, ""),
    ],
    "alpha": [
        Criterion("Manual Prototype Log", "Sessions conducted and documented", ["artefacts/manual-prototype-log.md", "alpha/manual-prototype-log.md"], True, True, ""),
        Criterion("Evaluation Rubric", "Domain expert approved; baseline scores present", ["artefacts/evaluation-rubric.md", "alpha/evaluation-rubric.md"], True, True, "baseline"),
        Criterion("LLM Prototype User Testing Report", "Minimum 5 participants from target population", ["docs/user-testing-report.md", "alpha/user-testing-report.md"], True, False, ""),
        Criterion("Failure Mode Catalogue", "Trigger, impact, and mitigation for each mode", ["artefacts/failure-modes.md", "alpha/failure-modes.md"], True, True, ""),
        Criterion("Validated HITL Map", "Automation levels confirmed with real users", ["artefacts/hitl-map.md", "docs/hitl-map.md"], True, True, "validated"),
        Criterion("Evaluation Harness", "Script that runs rubric on test dataset", ["scripts/evaluate_batch.py", "eval/run_eval.py", "scripts/evaluate.py"], True, True, ""),
        Criterion("Provider/Model Decision", "Security and legal clearance documented", ["docs/model-decision.md", "alpha/model-decision.md"], True, True, ""),
    ],
    "beta": [
        Criterion("Prompt Version History", "CHANGELOG with before/after rubric scores", ["prompts/CHANGELOG.md", "docs/prompt-versions.md"], True, True, ""),
        Criterion("Model Deprecation Plan", "Reviewed by PM and ML Engineer", ["artefacts/model-deprecation-plan.md", "docs/model-deprecation-plan.md"], True, True, ""),
        Criterion("Production Monitoring Docs", "Latency, cost, rubric score instrumented", ["docs/monitoring.md", "ops/monitoring.md"], True, True, "rubric"),
        Criterion("Accessibility Audit Report", "WCAG 2.1 AA minimum", ["docs/accessibility-audit.md"], True, False, ""),
        Criterion("Security STRA", "Signed off by security team", ["docs/stra.md", "security/stra.md"], True, False, ""),
        Criterion("Privacy Impact Assessment (Production)", "Covers model API data flows", ["docs/pia-production.md", "legal/pia-production.md"], True, False, ""),
    ],
}


def is_ai_project(project_dir):
    indicators = [
        project_dir / "ai-constraints.md",
        project_dir / "docs" / "ai-constraints.md",
        project_dir / "artefacts" / "evaluation-rubric.md",
    ]
    return any(p.exists() for p in indicators)


def find_file(project_dir, criterion):
    for rel_path in criterion.check_paths:
        candidate = project_dir / rel_path
        if candidate.exists():
            return candidate
    return None


def check_keyword(path, keyword):
    if not keyword:
        return True
    try:
        return keyword.lower() in path.read_text(encoding="utf-8").lower()
    except Exception:
        return False


def run_phase(phase, project_dir, ai_project):
    criteria = PHASE_CRITERIA.get(phase, [])
    results = []
    for c in criteria:
        if c.ai_only and not ai_project:
            continue
        found = find_file(project_dir, c)
        if not found:
            results.append(("MISSING", c.name, c.description, c.required))
        elif c.check_keyword and not check_keyword(found, c.check_keyword):
            results.append(("INCOMPLETE", c.name, f"{c.description} — keyword '{c.check_keyword}' not found in {found.name}", c.required))
        else:
            results.append(("OK", c.name, c.description, c.required))
    return results


def main():
    parser = argparse.ArgumentParser(description="Run phase gate review for an AI delivery project")
    parser.add_argument("--phase", default="all", choices=list(PHASE_CRITERIA.keys()) + ["all"])
    parser.add_argument("--project-dir", default=".", help="Root of the project directory")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    ai_project = is_ai_project(project_dir)

    print(f"\nPhase Gate Review")
    print(f"Project: {project_dir}")
    print(f"Project type: {'AI/agent' if ai_project else 'Standard'}")
    print()

    phases = list(PHASE_CRITERIA.keys()) if args.phase == "all" else [args.phase]
    blockers = 0
    warnings = 0

    for phase in phases:
        results = run_phase(phase, project_dir, ai_project)
        if not results:
            continue
        print(f"── {phase.upper()} GATE ──")
        for status, name, desc, required in results:
            if status == "OK":
                print(f"  OK         {name}")
            elif status == "MISSING":
                if required:
                    print(f"  MISSING    {name}  ← BLOCKER")
                    blockers += 1
                else:
                    print(f"  MISSING    {name}  (optional)")
                    warnings += 1
            elif status == "INCOMPLETE":
                print(f"  INCOMPLETE {name}  ← BLOCKER")
                print(f"             {desc}")
                blockers += 1
        print()

    print(f"Result: {blockers} blockers, {warnings} warnings")
    if blockers > 0:
        print("Gate: NOT PASSED — resolve blockers before proceeding.")
        sys.exit(1)
    else:
        print("Gate: PASSED — all required artefacts present.")
        sys.exit(0)


if __name__ == "__main__":
    main()
