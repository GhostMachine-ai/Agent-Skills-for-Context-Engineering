---
name: human-ai-collaboration
description: "This skill should be used when the user asks to design a human-in-the-loop workflow, when should agents escalate to humans, build trust in AI outputs, design agent oversight, calibrate automation level, create a human review process, define HITL requirements, or mentions human-in-the-loop, HITL, AI oversight, automation level, trust calibration, escalation paths, human-agent teaming, or oversight fatigue. Provides frameworks for designing workflows where humans and AI collaborate effectively."
---

# Human-AI Collaboration

## When to Activate

Activate this skill when:

- Designing a workflow where humans and AI agents work together
- Deciding which AI decisions require human review or approval
- Building escalation logic into an agent system
- Establishing trust between users and an AI-generated output
- Conducting a human-in-the-loop risk assessment (Discovery phase)
- Designing the human review interface for an AI-assisted service

Do not activate for: general agent architecture decisions (use `multi-agent-patterns`), production monitoring setup (use `agent-observability`), evaluation rubric design (use `evaluation`), or delivery process planning (use `ai-delivery-process`).

## Core Concepts

**The automation spectrum**:

| Level | Name | Description | When appropriate |
|-------|------|-------------|----------------|
| 1 | Fully manual | Human does everything; AI not involved | High-stakes; no AI data; regulatory requirement |
| 2 | AI-assisted | AI provides information; human decides and acts | High consequence; variable AI confidence |
| 3 | Human-in-the-loop | AI proposes; human approves before execution | Moderate consequence; good AI accuracy |
| 4 | Human-on-the-loop | AI acts; human monitors and can override | Lower consequence; high AI accuracy |
| 5 | Fully automated | AI acts; humans review outcomes periodically | Low consequence; very high AI accuracy |

**Calibration principle**: the right automation level is not determined by what is technically possible. It is determined by:

`consequence magnitude × (1 - AI confidence) × (1 / human capacity to review)`

A high-consequence decision requires human-in-the-loop even with high AI confidence. A low-consequence decision with a capacity-constrained review team may justify human-on-the-loop even at moderate AI confidence.

**Trust debt**: deploying agents with more autonomy than users trust them to have creates trust debt. Trust debt is expensive to recover. Calibrate conservatively, earn trust, then expand autonomy.

**The three escalation triggers**:
1. **Uncertainty escalation**: agent confidence is below a threshold; it routes to human review rather than guessing
2. **Consequence escalation**: the action exceeds the agent's authorised authority level
3. **Anomaly escalation**: the agent's output is outside the expected distribution; routes to human review even if confidence is high

## The Human-in-the-Loop Map

The HITL Map specifies, for every AI decision or action in a service, the human review requirements. It is:
- **Drafted in Discovery** from user research about trust and stakes
- **Tested as a hypothesis in Alpha** alongside prototype testing
- **Implemented in Beta** as part of the service build
- **Monitored in Live** for oversight fatigue and coverage gaps

### HITL Map Fields

For each AI action or decision:

| Field | Description |
|-------|-------------|
| Decision / Action | What the AI is doing |
| Automation Level | 1–5 |
| Consequence if Wrong | High / Medium / Low; user/system impact |
| Who Reviews | Role, not individual; include escalation chain |
| What They Need | Information required for a meaningful review |
| Trigger for Review | When does this route to review vs. proceed |
| Review SLA | How long can review take; what happens if missed |
| On Approval | What happens |
| On Rejection | What happens; does the user see a fallback? |

### Common HITL Map Failure Modes

**"Just in case" human review**: review added to every AI decision without specifying who reviews, at what latency, with what information. Creates review queues no one is resourced to process.

**Engineer-designed without user research**: created by engineering team based on their model of risk, not from user research. Users of high-stakes services often require human accountability for legal and trust reasons even when the AI is accurate.

**No oversight fatigue design**: if reviewers are asked to approve too many low-stakes decisions, they approve reflexively. Filter to surface only decisions where a human can add genuine value.

## Trust Calibration Patterns

### Progressive Trust Expansion

Start with more human oversight than you think you need. Measure reviewer agreement rates. When consistently > 90% over a sustained period, consider reducing the human review requirement.

Never expand autonomy without expanding monitoring simultaneously.

### Confidence Display

Show users the model's uncertainty to help them calibrate trust. Design principles:
- Be honest about uncertainty; do not suppress low-confidence signals
- Express uncertainty in terms the user understands (not "confidence: 0.73")
- Provide a clear path for users who disagree with the output

### Explanation Surfacing

For high-stakes decisions, show users *why* the agent made a recommendation:
- "Based on these 3 documents..." — helpful
- "This is consistent with the last 5 cases of this type..." — helpful
- "AI can make mistakes" — not helpful (generic disclaimer)
- Attention weights or logit values — not helpful (technical internals)

## Designing for Oversight Fatigue

Symptoms of oversight fatigue:
- Reviewers approve AI outputs without reading them
- Review SLAs consistently missed
- Reviewers report the review process as burdensome
- Error rates in reviewed items are not lower than in non-reviewed items

Prevention:
- Reserve human review for decisions where a human genuinely adds value
- Design the review interface to show only information needed for a meaningful decision
- Monitor reviewer agreement rates — sustained high agreement signals automation level should be increased
- Audit review quality periodically

## Designing for Graceful Degradation

Plan for:
- **AI failure**: route to manual process; inform the user of the delay
- **Review SLA missed**: escalate to the next reviewer tier; log the SLA miss
- **User rejection of all AI suggestions**: provide a path to human-assisted completion

## Practical Guidance

**In Discovery**: research which decisions users require human accountability for — not just which ones the AI might get wrong. Some decisions require human accountability for legal or trust reasons even when the AI is accurate.

**In Alpha**: test human reviewers, not just AI outputs. The review interface is part of the product. A reviewer who cannot complete a meaningful review within the SLA is a design failure, not a resourcing failure.

**In Beta**: instrument reviewer agreement rates, SLA compliance, and rejection rates from day one. These are leading indicators of oversight fatigue.

**In Live**: periodically audit review quality. A queue with 95% approval rates over an extended period is either a signal to increase automation level, or evidence that reviewers are no longer reading what they approve.

## Examples

**Example 1: HITL Map entry for a high-consequence eligibility decision**
| Field | Value |
|-------|-------|
| Decision | AI recommends benefit eligibility outcome |
| Automation Level | 3 — Human-in-the-loop |
| Consequence if Wrong | High — applicant denied legitimate benefit |
| Who Reviews | Senior caseworker (escalation: team lead → service manager) |
| What They Need | AI recommendation, confidence score, top 3 supporting documents, 6-month history summary |
| Trigger for Review | All recommendations (100% review in Beta) |
| Review SLA | 2 business days; escalate to team lead if missed |
| On Approval | System records outcome, notifies applicant |
| On Rejection | Caseworker records manual decision; correction logged for rubric learning |

**Example 2: Progressive trust expansion cadence**
```
Week 1–4:  100% human review — establish agreement rate baseline
Week 5–8:  Review only cases where AI confidence < 0.85 (est. 30% of volume)
Week 9–12: Review only cases where AI confidence < 0.75 (est. 15% of volume)
Trigger for next expansion: reviewer agreement rate > 90% sustained over 4 weeks
```

## Guidelines

1. Start at a more conservative automation level than analysis alone suggests — earning trust is cheaper than recovering it after a visible failure
2. Never expand automation level without simultaneously expanding monitoring coverage
3. Specify in the HITL Map exactly who reviews, what information they see, and how long they have — vague "human review" entries are placeholders, not designs
4. Test the review interface with actual reviewers before Beta launch — an interface that cannot be completed within SLA is a product failure
5. Instrument reviewer agreement rates, SLA compliance, and rejection rates from day one in Beta — these are leading indicators, not lagging ones
6. Design escalation chains before they are needed; a missed SLA with no escalation path becomes an invisible failure
7. Conduct user research to determine which decisions require human accountability for legal or trust reasons — do not rely solely on AI accuracy estimates

## Gotchas

1. **"Human review" as a liability shield without resources**: Teams add human review to high-stakes decisions for legal compliance, then do not resource the review queue. Reviewers approve AI outputs reflexively without reading them. This creates the worst outcome: nominal human oversight with no actual human judgment. Design the review queue as a product with its own SLA, tooling, and staffing capacity.

2. **Automation level determined by technical capability alone**: The automation level is calibrated by consequence magnitude × (1 - AI confidence) × (1 / reviewer capacity). Teams that set automation levels based solely on AI accuracy over-automate high-consequence decisions and under-automate low-consequence ones where reviewer capacity is the binding constraint.

3. **Oversight fatigue onset is invisible at first**: Reviewer agreement rates rising toward very high levels feel like success. They are a leading indicator of oversight fatigue — reviewers approving outputs without reading them. Monitor agreement rates as a two-tailed metric: sustained very-low rates (genuine disagreement warranting investigation) and sustained very-high rates (reflexive approval) both require action.

4. **Confidence score as the only escalation trigger**: Uncertainty escalation (agent confidence below threshold) is one of three escalation triggers. Teams that implement only confidence-based escalation miss consequence escalation (action exceeds authorised authority level) and anomaly escalation (output outside expected distribution despite high confidence).

5. **Trust debt from premature autonomy**: Deploying agents with more autonomy than users trust them to have generates trust debt. A single high-profile error from an over-automated decision can take months of careful, conservative operation to recover from. Start conservatively; expand autonomy as reviewer agreement data supports it.

## Integration

This skill integrates with:
- `ai-delivery-process` — the HITL Map is a Discovery artefact in the AI delivery process
- `evaluation` — reviewer agreement rates are a measurable quality metric
- `agent-observability` — anomaly-triggered escalation requires observability infrastructure to detect the anomaly
- `bdi-mental-states` — formal BDI models can make agent uncertainty and belief state explicit, enabling principled confidence thresholds for escalation

## References

- [Automation Level Framework Reference](./references/automation-level-framework.md)
- [HITL Map Template](./references/hitl-map-template.md)
- [HITL Queue Simulator](./scripts/hitl_simulator.py)
- Related skills: ai-delivery-process, evaluation, agent-observability, bdi-mental-states

## Skill Metadata

- Created: 2026-07-09
- Last Updated: 2026-07-09
- Author: Agent Skills for Context Engineering Contributors
- Version: 1.0.0
