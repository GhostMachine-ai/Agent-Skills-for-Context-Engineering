#!/usr/bin/env python3
"""
artefact_inventory.py

Scans a project directory and produces an inventory of all artefacts
present and absent for a given phase of the AI delivery process.

This is pseudocode demonstrating the pattern. Adapt paths and artefact
definitions for your specific project.

Usage:
    python scripts/artefact_inventory.py --phase discovery
    python scripts/artefact_inventory.py --phase all --project-dir .
    python scripts/artefact_inventory.py --phase alpha --format json
"""

import argparse
import json
import sys
from pathlib import Path

ARTEFACT_REGISTRY = {
    "alignment": [
        {"name": "Project Brief", "paths": ["project-brief.md", "docs/project-brief.md"], "required": True, "ai_only": False},
        {"name": "Stakeholder Map", "paths": ["docs/stakeholders.md", "alignment/stakeholders.md"], "required": True, "ai_only": False},
        {"name": "Privacy Impact Assessment (Discovery)", "paths": ["docs/pia.md", "legal/pia.md"], "required": True, "ai_only": False},
        {"name": "AI Constraints Document", "paths": ["ai-constraints.md", "docs/ai-constraints.md"], "required": True, "ai_only": True},
        {"name": "AI Feasibility Assessment", "paths": ["docs/feasibility.md", "alignment/feasibility.md"], "required": True, "ai_only": True},
    ],
    "discovery": [
        {"name": "User Research Report", "paths": ["docs/research-report.md", "discovery/research-report.md"], "required": True, "ai_only": False},
        {"name": "Journey Map", "paths": ["docs/journey-map.md", "discovery/journey-map.md"], "required": True, "ai_only": False},
        {"name": "Problem Statement", "paths": ["problem-statement.md", "docs/problem-statement.md"], "required": True, "ai_only": False},
        {"name": "User Stories", "paths": ["docs/user-stories.md", "backlog.md"], "required": True, "ai_only": False},
        {"name": "Data Availability Matrix", "paths": ["artefacts/data-availability-matrix.md", "docs/data-availability-matrix.md"], "required": True, "ai_only": True},
        {"name": "Task-Model Fit Assessment", "paths": ["artefacts/task-model-fit.md", "docs/task-model-fit.md"], "required": True, "ai_only": True},
        {"name": "Draft HITL Map", "paths": ["artefacts/hitl-map.md", "docs/hitl-map.md"], "required": True, "ai_only": True},
    ],
    "alpha": [
        {"name": "Tested Prototypes (documented)", "paths": ["alpha/prototypes.md", "docs/prototypes.md"], "required": True, "ai_only": False},
        {"name": "Technical Feasibility Assessment", "paths": ["docs/tech-feasibility.md", "alpha/tech-feasibility.md"], "required": True, "ai_only": False},
        {"name": "Beta Feature Backlog", "paths": ["backlog.md", "alpha/backlog.md"], "required": True, "ai_only": False},
        {"name": "Manual Prototype Log", "paths": ["artefacts/manual-prototype-log.md", "alpha/manual-prototype-log.md"], "required": True, "ai_only": True},
        {"name": "Evaluation Rubric", "paths": ["artefacts/evaluation-rubric.md", "alpha/evaluation-rubric.md"], "required": True, "ai_only": True},
        {"name": "Failure Mode Catalogue", "paths": ["artefacts/failure-modes.md", "alpha/failure-modes.md"], "required": True, "ai_only": True},
        {"name": "Validated HITL Map", "paths": ["artefacts/hitl-map.md", "docs/hitl-map.md"], "required": True, "ai_only": True},
        {"name": "Evaluation Harness", "paths": ["scripts/evaluate_batch.py", "eval/run_eval.py"], "required": True, "ai_only": True},
    ],
    "beta": [
        {"name": "MVP Deployment Documentation", "paths": ["docs/deployment.md", "ops/deployment.md"], "required": True, "ai_only": False},
        {"name": "Accessibility Audit Report", "paths": ["docs/accessibility-audit.md"], "required": True, "ai_only": False},
        {"name": "Security STRA", "paths": ["docs/stra.md", "security/stra.md"], "required": True, "ai_only": False},
        {"name": "Privacy Impact Assessment (Production)", "paths": ["docs/pia-production.md", "legal/pia-production.md"], "required": True, "ai_only": False},
        {"name": "Prompt Version History", "paths": ["prompts/CHANGELOG.md", "docs/prompt-versions.md"], "required": True, "ai_only": True},
        {"name": "Model Deprecation Plan", "paths": ["artefacts/model-deprecation-plan.md", "docs/model-deprecation-plan.md"], "required": True, "ai_only": True},
        {"name": "Production Monitoring Documentation", "paths": ["docs/monitoring.md", "ops/monitoring.md"], "required": True, "ai_only": True},
    ],
}


def is_ai_project(project_dir):
    indicators = [
        project_dir / "ai-constraints.md",
        project_dir / "docs" / "ai-constraints.md",
        project_dir / "artefacts" / "evaluation-rubric.md",
    ]
    return any(p.exists() for p in indicators)


def check_artefact(project_dir, artefact):
    for rel_path in artefact["paths"]:
        candidate = project_dir / rel_path
        if candidate.exists():
            return True, str(candidate.relative_to(project_dir))
    return False, None


def inventory_phase(phase, project_dir, ai_project):
    artefacts = ARTEFACT_REGISTRY.get(phase, [])
    results = []
    for a in artefacts:
        if a["ai_only"] and not ai_project:
            continue
        found, location = check_artefact(project_dir, a)
        results.append({
            "name": a["name"],
            "required": a["required"],
            "ai_only": a["ai_only"],
            "present": found,
            "location": location,
        })
    return results


def print_table(phase, results):
    print(f"\n── {phase.upper()} ARTEFACTS ──")
    present = [r for r in results if r["present"]]
    missing_required = [r for r in results if not r["present"] and r["required"]]
    missing_optional = [r for r in results if not r["present"] and not r["required"]]

    for r in present:
        label = "[AI]" if r["ai_only"] else "    "
        print(f"  PRESENT  {label} {r['name']}  ({r['location']})")
    for r in missing_required:
        label = "[AI]" if r["ai_only"] else "    "
        print(f"  MISSING  {label} {r['name']}  ← required")
    for r in missing_optional:
        label = "[AI]" if r["ai_only"] else "    "
        print(f"  MISSING  {label} {r['name']}  (optional)")

    print(f"  Summary: {len(present)} present, {len(missing_required)} required missing, {len(missing_optional)} optional missing")


def main():
    parser = argparse.ArgumentParser(description="Inventory artefacts for an AI delivery project")
    parser.add_argument("--phase", default="all", choices=list(ARTEFACT_REGISTRY.keys()) + ["all"])
    parser.add_argument("--project-dir", default=".", help="Root of the project directory")
    parser.add_argument("--format", default="table", choices=["table", "json"])
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    ai_project = is_ai_project(project_dir)
    phases = list(ARTEFACT_REGISTRY.keys()) if args.phase == "all" else [args.phase]

    all_results = {}
    total_missing = 0

    for phase in phases:
        results = inventory_phase(phase, project_dir, ai_project)
        all_results[phase] = results
        total_missing += sum(1 for r in results if not r["present"] and r["required"])

    if args.format == "json":
        print(json.dumps(all_results, indent=2))
    else:
        print(f"\nArtefact Inventory")
        print(f"Project: {project_dir}")
        print(f"Project type: {'AI/agent' if ai_project else 'Standard'}")
        for phase, results in all_results.items():
            print_table(phase, results)
        print(f"\nTotal required artefacts missing: {total_missing}")

    sys.exit(1 if total_missing > 0 else 0)


if __name__ == "__main__":
    main()
