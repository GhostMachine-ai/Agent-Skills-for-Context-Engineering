# How Skills Built This Project

A narrative account of how the `ai-delivery-process`, `agent-observability`, and `human-ai-collaboration` skills shaped the AI Document Summariser at each phase.

## Alignment

When the project was initiated, the team had no prior experience delivering AI services. The `ai-delivery-process` skill's Alignment checklist flagged two constraints that had not been on the team's radar:

**Data sovereignty**: Government documents cannot be processed by US-hosted LLM APIs without specific legal agreements under UK GDPR. Identifying this during Alignment (not Beta) allowed the team to evaluate sovereign-cloud model providers over six weeks rather than six days.

**Ethics and accountability review**: The algorithmic accountability review was initiated during Alignment, giving the ethics and legal teams the lead time they needed. A Beta-stage discovery would have added six weeks of delay.

The AI/ML Systems Thinker role (introduced by the skill) performed an initial feasibility assessment, confirming that document summarisation is tractable for current LLM capabilities given the team's data constraints.

## Discovery

The `ai-delivery-process` skill's Data Availability Matrix template structured the Discovery data assessment. The team had assumed clean, machine-readable PDFs. User research and the matrix exercise uncovered that approximately 30% of documents were scanned images requiring OCR. The matrix flagged this as a **High-severity gap**, prompting an explicit phase-scoping decision: scanned documents deferred to Phase 2.

The `human-ai-collaboration` automation level framework was applied in two Discovery workshops with policy domain experts. The team's initial instinct was Level 3 (AI produces output, human spot-checks). After applying the framework's consequence, reversibility, and regulatory criteria, the team differentiated by classification level:

- **UNCLASSIFIED documents**: Level 2 (AI draft, human edits before use)
- **OFFICIAL-SENSITIVE documents**: Level 1 (human decides, AI informs)

Making this distinction in Discovery — not Beta — meant the HITL requirements were baked into the Beta build specification, not retrofitted.

## Alpha

Two decisions in Alpha, both from the `ai-delivery-process` skill, defined the project's trajectory:

**Manual prototype first**: A researcher acted as the AI for two days, reading documents and producing structured summaries by hand. This revealed that users expected **Action Items** and **Risk Flags** as separate sections — a distinction the initial prompt design did not make. Fixing this in the manual prototype took 20 minutes. Fixing it post-LLM-prototype would have required new prompt engineering, evaluation re-runs, and user testing.

**Evaluation rubric before automated prototype**: The `evaluation` skill was used to design the rubric before any LLM call was made:

| Dimension | Weight | Scoring Anchor (5/5) |
|-----------|--------|---------------------|
| Accuracy | 35% | All key decisions from source present; no hallucinations |
| Coherence | 25% | Summary reads fluently; logical structure throughout |
| Completeness | 20% | Action items and risk flags captured; no gaps |
| Format Compliance | 20% | All four sections present; correct heading structure |

Manual prototype baseline: **3.1/5**. LLM prototype result: **3.7/5** (above the 3.5 threshold). The rubric made the Alpha gate decision objective.

The `human-ai-collaboration` skill's HITL Map was tested with real users in Alpha. The draft from Discovery held — users confirmed they wanted human review for OFFICIAL-SENSITIVE documents and were comfortable with Level 2 for UNCLASSIFIED. Reviewers were given the source document alongside the AI summary and asked to confirm, edit, or reject.

## Beta

The `agent-observability` skill's prompt versioning pattern was implemented from the first Beta deployment. Each prompt version was tagged with a semantic version number, stored in `prompts/CHANGELOG.md`, and linked to before/after rubric scores.

In week 3 of Beta, a prompt change designed to improve factual density was deployed to 5% of traffic. The monitoring dashboard showed:
- Rubric score: 3.8 → 3.9 (improved)
- P95 latency: 18s → 25s (within threshold)
- Cost-per-summary: £0.038 → £0.041 (within budget)

In week 5, a second change targeting structure was deployed. This time:
- Rubric score: 3.9 → 4.0 (improved)
- P95 latency: 25s → 35s (**above the 30s threshold**)

Because the change was versioned and tracked, the team had the exact diff, the before/after scores, and a documented rollback path. The change was rolled back the same day. Without prompt versioning, identifying the cause would have taken days.

The `human-ai-collaboration` skill's HITL queue simulator (`scripts/hitl_simulator.py`) predicted peak wait times of 8 hours at projected OFFICIAL-SENSITIVE volume — double the 4-hour SLA. The team added a second reviewer pool (two part-time policy officers) before Beta launch. Post-launch, peak wait times averaged 2.4 hours.

## Live

Drift detection from the `agent-observability` skill runs weekly using a 30-day rolling baseline versus a 7-day current window.

Two months after launch, the rubric score drifted from 3.8 to 3.4 — below the 3.5 threshold. The drift detector flagged the regression. Investigation revealed the model provider had made an unannounced update to the base model. The ML Engineer adjusted the prompt within 48 hours. The regression was caught and resolved before users or service managers noticed.

**Without drift detection**: The regression would have persisted until a user complaint or a periodic manual audit — typically weeks.
