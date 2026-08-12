#!/usr/bin/env python3
"""
generate_eval_rubric.py

Generates a starter evaluation rubric scaffold for a named AI task.
Outputs a Markdown file using the standard rubric template with
placeholder dimensions derived from the task name.

This is pseudocode demonstrating the pattern. The output is a scaffold
to fill in with domain knowledge — it does not produce a complete rubric.

Usage:
    python scripts/generate_eval_rubric.py --task-name "document-summarisation"
    python scripts/generate_eval_rubric.py --task-name "intent-classification" --output artefacts/
    python scripts/generate_eval_rubric.py --task-name "code-review" --dimensions accuracy coherence relevance
"""

import argparse
import sys
from pathlib import Path
from datetime import date

DEFAULT_DIMENSIONS = {
    "summarisation": [
        ("Accuracy", 35, "All key information from source present; no hallucinations or invented facts"),
        ("Coherence", 25, "Summary reads fluently; logical structure; no contradictions"),
        ("Completeness", 20, "All required elements captured; no material omissions"),
        ("Format Compliance", 20, "Required structure followed; correct sections and formatting"),
    ],
    "classification": [
        ("Precision", 40, "Classified items are correctly categorised"),
        ("Recall", 35, "All items that should be classified are classified"),
        ("Confidence Calibration", 25, "Confidence scores reflect actual accuracy"),
    ],
    "generation": [
        ("Accuracy", 35, "Generated content is factually correct"),
        ("Relevance", 30, "Output addresses the specified task or prompt"),
        ("Coherence", 20, "Output reads naturally; no contradictions or non-sequiturs"),
        ("Safety", 15, "Output contains no harmful, biased, or policy-violating content"),
    ],
    "extraction": [
        ("Precision", 35, "Extracted items are correct"),
        ("Recall", 35, "All target items are extracted; no omissions"),
        ("Format", 30, "Extracted items presented in required format"),
    ],
    "default": [
        ("Quality", 40, "Overall output quality meets task requirements"),
        ("Accuracy", 35, "Output is factually correct and grounded"),
        ("Completeness", 25, "All required elements present; no material omissions"),
    ],
}

SCORING_GUIDE_TEMPLATE = """
| Score | Anchor |
|-------|--------|
| 5 | Excellent — fully meets criterion; no issues |
| 4 | Good — meets criterion with minor issues that do not affect usefulness |
| 3 | Acceptable — mostly meets criterion; one notable issue |
| 2 | Poor — partially meets criterion; significant issues |
| 1 | Failing — does not meet criterion; output is misleading or unusable |
"""


def infer_task_type(task_name):
    name_lower = task_name.lower()
    if any(k in name_lower for k in ["summar", "abstract", "distil"]):
        return "summarisation"
    if any(k in name_lower for k in ["classif", "categor", "label", "intent"]):
        return "classification"
    if any(k in name_lower for k in ["generat", "draft", "write", "compose"]):
        return "generation"
    if any(k in name_lower for k in ["extract", "pars", "identify", "find"]):
        return "extraction"
    return "default"


def generate_rubric(task_name, dimensions=None, output_dir=None):
    task_type = infer_task_type(task_name)
    dim_list = dimensions if dimensions else DEFAULT_DIMENSIONS.get(task_type, DEFAULT_DIMENSIONS["default"])

    if isinstance(dim_list[0], str):
        # Custom dimension names passed as CLI args; assign equal weights
        weight = 100 // len(dim_list)
        remainder = 100 - weight * len(dim_list)
        dim_list = [
            (name, weight + (remainder if i == 0 else 0), "TODO: describe what this means for this task")
            for i, name in enumerate(dim_list)
        ]

    total_weight = sum(w for _, w, _ in dim_list)
    if total_weight != 100:
        print(f"Warning: dimension weights sum to {total_weight}, not 100. Adjust before use.", file=sys.stderr)

    lines = [
        f"# Evaluation Rubric: {task_name.replace('-', ' ').title()}",
        "",
        f"Generated: {date.today().isoformat()}  ",
        "Status: SCAFFOLD — fill in with domain expert input before use",
        "",
        "## Task Description",
        "",
        f"**Task**: {task_name}  ",
        "**Inferred type**: " + task_type + "  ",
        "**Composite threshold for gate**: TODO (e.g., ≥ 3.5/5)  ",
        "**Rubric owner**: TODO  ",
        "**Domain expert approval**: TODO",
        "",
        "---",
        "",
        "## Evaluation Dimensions",
        "",
        "| Dimension | Weight | Description | Threshold |",
        "|-----------|--------|-------------|-----------|",
    ]

    for name, weight, desc in dim_list:
        lines.append(f"| {name} | {weight}% | {desc} | TODO |")

    lines += [
        "",
        "---",
        "",
        "## Scoring Guide",
        "",
    ]

    for name, _, _ in dim_list:
        lines += [
            f"### {name}",
            "",
            SCORING_GUIDE_TEMPLATE.strip(),
            "",
        ]

    lines += [
        "---",
        "",
        "## Test Cases",
        "",
        "| Case ID | Input Description | Expected Output | Difficulty |",
        "|---------|------------------|-----------------|------------|",
        "| TC-001 | TODO | TODO | Easy |",
        "| TC-002 | TODO | TODO | Medium |",
        "| TC-003 | TODO | TODO | Hard |",
        "",
        "---",
        "",
        "## Baseline and Targets",
        "",
        "| Source | Composite Score | Notes |",
        "|--------|----------------|-------|",
        "| Manual prototype | TODO | Establish before building LLM prototype |",
        "| Alpha LLM prototype | TODO | Must meet threshold |",
        "| Beta target | TODO | Post-prompt-tuning |",
        "| Live steady-state | TODO | Monitored via sampling |",
        "",
        "---",
        "",
        "## Evaluation Method",
        "",
        "| Dimension | Method | Sampling Rate | Human Calibration |",
        "|-----------|--------|--------------|------------------|",
    ]

    for name, _, _ in dim_list:
        lines.append(f"| {name} | TODO (Human / LLM-as-judge / Automated) | TODO | TODO |")

    lines += [
        "",
        "---",
        "",
        "## Human Review Criteria",
        "",
        "Route output to human review if:",
        "- [ ] Composite score < TODO",
        "- [ ] Any hard-constraint dimension scores 1 or 2",
        "- [ ] Confidence score < TODO",
        "- [ ] TODO (add project-specific triggers)",
    ]

    content = "\n".join(lines)

    output_name = f"evaluation-rubric-{task_name}.md"
    if output_dir:
        out_path = Path(output_dir) / output_name
    else:
        out_path = Path(output_name)

    out_path.write_text(content, encoding="utf-8")
    print(f"Rubric scaffold written to: {out_path}")
    print(f"Task type inferred: {task_type}")
    print(f"Dimensions: {', '.join(name for name, _, _ in dim_list)}")
    print(f"Weight total: {total_weight}%")
    print()
    print("Next steps:")
    print("  1. Review dimension descriptions with a domain expert")
    print("  2. Set composite threshold (consult with PM and Eval Specialist)")
    print("  3. Fill in test cases with real examples")
    print("  4. Establish baseline scores from manual prototype BEFORE building LLM prototype")
    print("  5. Get domain expert sign-off before Alpha gate review")


def main():
    parser = argparse.ArgumentParser(description="Generate evaluation rubric scaffold for an AI task")
    parser.add_argument("--task-name", required=True, help="Hyphenated task name (e.g. document-summarisation)")
    parser.add_argument("--output", default=None, help="Output directory (default: current directory)")
    parser.add_argument("--dimensions", nargs="+", default=None, help="Custom dimension names (optional; overrides inferred defaults)")
    args = parser.parse_args()

    generate_rubric(args.task_name, args.dimensions, args.output)


if __name__ == "__main__":
    main()
