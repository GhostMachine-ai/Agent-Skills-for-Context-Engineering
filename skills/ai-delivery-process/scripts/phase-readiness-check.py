#!/usr/bin/env python3
"""
phase-readiness-check.py

Checks a project directory for the artefacts required to advance past
a given phase gate in the AI delivery process.

This is pseudocode demonstrating the pattern. Adapt file names, directory
structures, and detection logic for your specific project.

Usage:
    python phase-readiness-check.py --phase discovery --project-dir .
    python phase-readiness-check.py --phase alpha --project-dir ~/my-ai-project
    python phase-readiness-check.py --phase all --project-dir .
"""

import argparse
import sys
from pathlib import Path
from typing import NamedTuple


class ArtifactCheck(NamedTuple):
    name: str
    paths: list
    required: bool
    ai_only: bool
    check_content: object  # str or None


PHASE_CHECKS = {
    "alignment": [
        ArtifactCheck("Project Brief / Scope Document", ["project-brief.md", "BRIEF.md", "scope.md"], True, False, None),
        ArtifactCheck("Privacy Impact Assessment (submitted)", ["pia.md", "privacy-impact-assessment.md", "docs/pia.md"], True, False, None),
        ArtifactCheck("Stakeholder Map", ["stakeholder-map.md", "docs/stakeholders.md"], True, False, None),
        ArtifactCheck("AI/Agent Constraints Document", ["ai-constraints.md", "docs/ai-constraints.md"], True, True, "vendor"),
    ],
    "discovery": [
        ArtifactCheck("User Research Summary", ["research-summary.md", "docs/research-summary.md"], True, False, None),
        ArtifactCheck("Journey Map", ["journey-map.md", "docs/journey-map.md", "discovery/journey-map.md"], True, False, None),
        ArtifactCheck("Problem Statement", ["problem-statement.md", "docs/problem-statement.md"], True, False, None),
        ArtifactCheck("User Stories", ["user-stories.md", "backlog.md", "docs/user-stories.md"], True, False, None),
        ArtifactCheck("Data Availability Matrix", ["data-availability-matrix.md", "docs/data-availability-matrix.md"], True, True, "gap"),
        ArtifactCheck("Task-Model Fit Assessment", ["task-model-fit.md", "docs/task-model-fit.md"], True, True, None),
        ArtifactCheck("Human-in-the-Loop Map (draft)", ["hitl-map.md", "docs/hitl-map.md"], True, True, None),
    ],
    "alpha": [
        ArtifactCheck("Tested Prototypes (documented)", ["alpha/prototypes.md", "prototypes/README.md"], True, False, None),
        ArtifactCheck("Technical Feasibility Assessment", ["tech-feasibility.md", "alpha/tech-feasibility.md"], True, False, None),
        ArtifactCheck("Beta Feature Backlog", ["backlog.md", "beta-backlog.md", "alpha/backlog.md"], True, False, None),
        ArtifactCheck("Evaluation Rubric", ["evaluation-rubric.md", "alpha/evaluation-rubric.md"], True, True, "baseline"),
        ArtifactCheck("Manual Prototype Log", ["manual-prototype-log.md", "alpha/manual-prototype-log.md"], True, True, None),
        ArtifactCheck("Failure Mode Catalogue", ["failure-modes.md", "alpha/failure-modes.md"], True, True, None),
        ArtifactCheck("HITL Map (validated)", ["hitl-map.md", "docs/hitl-map.md"], True, True, "validated"),
        ArtifactCheck("Evaluation Harness (scripts)", ["scripts/evaluate.py", "eval/run_eval.py"], True, True, None),
    ],
    "beta": [
        ArtifactCheck("MVP Live (deployment docs)", ["docs/deployment.md", "DEPLOY.md"], True, False, None),
        ArtifactCheck("Privacy Impact Assessment (production)", ["pia-production.md", "docs/pia-production.md"], True, False, None),
        ArtifactCheck("Security Threat and Risk Assessment", ["stra.md", "docs/stra.md"], True, False, None),
        ArtifactCheck("Accessibility Audit Report", ["accessibility-audit.md", "docs/accessibility-audit.md"], True, False, None),
        ArtifactCheck("Prompt Version History", ["prompt-versions.md", "prompts/CHANGELOG.md"], True, True, None),
        ArtifactCheck("Model Deprecation Plan", ["model-deprecation-plan.md", "docs/model-deprecation-plan.md"], True, True, None),
        ArtifactCheck("Production Monitoring Docs", ["docs/monitoring.md", "ops/monitoring.md"], True, True, None),
    ],
}


def is_ai_project(project_dir):
    indicators = [
        project_dir / "ai-constraints.md",
        project_dir / "docs" / "ai-constraints.md",
        project_dir / "evaluation-rubric.md",
        project_dir / "alpha" / "evaluation-rubric.md",
    ]
    return any(p.exists() for p in indicators)


def find_artifact(project_dir, check):
    for rel_path in check.paths:
        candidate = project_dir / rel_path
        if candidate.exists():
            return True, candidate
    return False, None


def check_content_present(path, search_term):
    try:
        return search_term.lower() in path.read_text(encoding="utf-8").lower()
    except Exception:
        return False


def run_phase_check(phase, project_dir, ai_project):
    checks = PHASE_CHECKS.get(phase, [])
    passed = 0
    failed = 0
    messages = []

    for check in checks:
        if check.ai_only and not ai_project:
            continue

        found, path = find_artifact(project_dir, check)
        label = f"[AI] {check.name}" if check.ai_only else check.name

        if not found:
            if check.required:
                messages.append(f"  MISSING  {label}")
                failed += 1
            else:
                messages.append(f"  OPTIONAL {label} — not found (not blocking)")
        else:
            if check.check_content and path:
                content_ok = check_content_present(path, check.check_content)
                if not content_ok:
                    messages.append(f"  INCOMPLETE {label} — found at {path.name} but appears to lack '{check.check_content}' content")
                    failed += 1
                else:
                    messages.append(f"  OK       {label}")
                    passed += 1
            else:
                messages.append(f"  OK       {label}")
                passed += 1

    return passed, failed, messages


def main():
    parser = argparse.ArgumentParser(description="Check project directory for AI delivery phase artefacts")
    parser.add_argument("--project-dir", default=".", help="Project directory to check")
    parser.add_argument("--phase", default="all", choices=list(PHASE_CHECKS.keys()) + ["all"])
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    ai_project = is_ai_project(project_dir)

    print(f"\nPhase Readiness Check")
    print(f"Project: {project_dir}")
    print(f"Project type: {'AI/agent' if ai_project else 'Standard'}")
    print()

    phases = list(PHASE_CHECKS.keys()) if args.phase == "all" else [args.phase]
    total_passed = 0
    total_failed = 0

    for phase in phases:
        print(f"── {phase.capitalize()} ──")
        passed, failed, messages = run_phase_check(phase, project_dir, ai_project)
        for msg in messages:
            print(msg)
        total_passed += passed
        total_failed += failed
        print()

    print(f"Result: {total_passed} passed, {total_failed} missing/incomplete")

    if total_failed > 0:
        print("Action: resolve missing artefacts before phase gate review.")
        sys.exit(1)
    else:
        print("All required artefacts present.")
        sys.exit(0)


if __name__ == "__main__":
    main()
