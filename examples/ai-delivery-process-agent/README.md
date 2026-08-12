# Example: AI Delivery Process — AI Document Summariser

A complete worked example of an AI agent project delivered using the skills in this collection.

## About This Example

This directory contains the full artefact set for the **AI Document Summariser**: a government service that produces structured summaries of uploaded policy documents using an LLM.

It demonstrates what completed artefacts look like at each phase, and maps every key design decision to the skill that informed it.

## Skills Used

| Skill | Role in This Project |
|-------|---------------------|
| `ai-delivery-process` | Phase planning, artefact production, phase gate reviews, team staffing |
| `agent-observability` | Production monitoring, drift detection, prompt versioning |
| `human-ai-collaboration` | HITL Map, automation level decisions, trust calibration |
| `evaluation` | Evaluation rubric design, LLM-as-judge setup, sampling programme |

## Project Summary

**Problem**: Civil servants spend hours reading lengthy policy documents to extract decisions and action items.

**Solution**: LLM-powered service that accepts PDF/Word uploads and returns a structured summary with four sections: Executive Summary, Key Decisions, Action Items, Risk Flags.

**Phase**: This example documents Alignment through Beta. Live artefacts are stubs.

## Structure

```
phases/          Phase-by-phase artefacts and activities
artefacts/       Reusable templates used in this project
scripts/         Automation for phase gate reviews and artefact tracking
references/      Background material on AI delivery differences
```

## Quick Start

```bash
# Check artefact completeness for a phase
python scripts/artefact_inventory.py --phase discovery --project-dir .

# Run a phase gate review
python scripts/phase_gate_review.py --phase alpha --project-dir .

# Generate an evaluation rubric scaffold
python scripts/generate_eval_rubric.py --task-name "document-summarisation"
```

## Key Files

- [HOW-SKILLS-BUILT-THIS.md](HOW-SKILLS-BUILT-THIS.md) — Narrative account of how skills were applied
- [SKILLS-MAPPING.md](SKILLS-MAPPING.md) — Decision → skill traceability table
- [phases/alpha.md](phases/alpha.md) — Evaluation rubric and manual prototype log
- [artefacts/hitl-map-template.md](artefacts/hitl-map-template.md) — HITL Map with real entries
- [references/ai-delivery-differences.md](references/ai-delivery-differences.md) — Why AI delivery is different

## Lessons Learned

1. The manual prototype (human-as-model) in Alpha revealed that users wanted action items and risk flags as separate sections — a distinction the initial prompt design missed.
2. Defining the evaluation rubric before building the automated prototype saved approximately two weeks of rework.
3. A prompt change in Beta that improved factual density also increased P95 latency by 40% — caught by the monitoring stack before full rollout.
4. The HITL queue simulator predicted SLA breaches at peak volume before Beta launch; an extra reviewer pool was added proactively.
