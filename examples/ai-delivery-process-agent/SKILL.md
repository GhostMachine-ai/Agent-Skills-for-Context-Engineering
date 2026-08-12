---
name: ai-delivery-process-example
description: "This skill should be used when the user asks for a worked example of AI project delivery, wants to see completed artefacts for a real project, or wants to understand how ai-delivery-process, agent-observability, and human-ai-collaboration skills apply in practice. Do not activate for general delivery process questions — use the ai-delivery-process skill instead."
---

# AI Delivery Process — Worked Example

## What This Example Shows

A complete AI delivery artefact set for the **AI Document Summariser** project: a government service that summarises policy documents using an LLM. All five phases (Alignment through Live) are documented with completed artefacts and decision rationale.

## Skills Demonstrated

- `ai-delivery-process` — Phase planning, artefact production, phase gate reviews, team staffing
- `agent-observability` — Production monitoring, drift detection, prompt versioning (week 5 regression case)
- `human-ai-collaboration` — HITL Map design, automation level decisions, queue simulator validation
- `evaluation` — Rubric design, baseline from manual prototype, LLM-as-judge setup

## Key Files

- [HOW-SKILLS-BUILT-THIS.md](HOW-SKILLS-BUILT-THIS.md) — Narrative account of how each skill changed the project outcome
- [SKILLS-MAPPING.md](SKILLS-MAPPING.md) — Decision → skill traceability, including "without the skill" column
- [phases/alpha.md](phases/alpha.md) — Evaluation rubric with manual prototype baseline and LLM prototype results
- [phases/beta.md](phases/beta.md) — Prompt version history including week 5 regression and same-day rollback
- [artefacts/hitl-map-template.md](artefacts/hitl-map-template.md) — HITL Map template with real project entries
- [artefacts/evaluation-rubric-template.md](artefacts/evaluation-rubric-template.md) — Rubric template with worked dimensions
- [references/ai-delivery-differences.md](references/ai-delivery-differences.md) — Why AI delivery is different from standard delivery
- [references/phase-exit-criteria.md](references/phase-exit-criteria.md) — Detailed exit criteria with anti-patterns

## How to Use This Example

1. Read `HOW-SKILLS-BUILT-THIS.md` to understand what changed at each phase
2. Read `SKILLS-MAPPING.md` to trace which skill informed which decision
3. Browse `phases/` to see what completed artefacts look like
4. Copy templates from `artefacts/` for use on your own project
5. Run `scripts/phase_gate_review.py` or `scripts/artefact_inventory.py` on your own project directory
