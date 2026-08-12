---
name: ai-delivery-process
description: "This skill should be used when the user asks to plan an AI project delivery, what phase are we in, what should we have at end of discovery, how do we staff an AI team, create a delivery plan for an agent system, what artefacts are required for alpha, define phase gate criteria for an AI project, or mentions agile phases, delivery process, sprint planning for AI, MVP for agent systems, project phase gates, or AI service delivery. Provides the full agile delivery process adapted for AI/agent systems."
---

# AI Delivery Process

## When to Activate

Activate this skill when:

- Planning a new AI agent or LLM-powered product or service
- Conducting a phase gate review (Alignment → Discovery → Alpha → Beta → Live)
- Staffing an AI delivery team and assigning roles
- Defining exit criteria for a phase
- Creating or reviewing Discovery, Alpha, or Beta artefacts for an AI system
- Asking what artefacts or activities are required at a given phase

Do not activate for: pure evaluation framework design (use `evaluation`), production monitoring setup (use `agent-observability`), human-in-the-loop workflow design (use `human-ai-collaboration`), or general context engineering questions (use `context-fundamentals`).

## Core Concepts

**The five phases**: Alignment (foundations) → Discovery (user research) → Alpha (prototyping) → Beta (build MVP) → Live (continuous improvement). The phases are the same for AI projects; the activities, artefacts, staffing, and exit criteria change.

**Evaluation-driven development**: Define the evaluation rubric before building. "Does it work well enough?" is answered by rubric-based scoring against a defined threshold — not by passing unit tests.

**Non-determinism as a design constraint**: AI systems are non-deterministic. Testing, monitoring, and quality gates must be statistical, not binary. A single wrong output is not a bug; a pattern is.

**Model as dependency**: Model providers update, deprecate, and change pricing on their own schedules. Version pin, change test, and deprecation plan are delivery requirements.

**Human-in-the-loop design**: Specifying which AI decisions require human review is a user research question (Discovery), a prototype test question (Alpha), a build requirement (Beta), and a monitoring concern (Live). See `human-ai-collaboration` skill.

## Phase-by-Phase AI Delivery

### Alignment
Standard focus: stakeholder alignment, funding, governance.

AI additions:
- Assess high-level problem fit for LLM/agent processing
- Identify data ownership and provenance constraints
- Establish which model vendors are within policy
- Initiate AI ethics or algorithmic accountability review

**Artefacts produced**: none specific to AI at this stage — constraints documented in project brief.

### Discovery
Standard focus: user research, needs identification, problem framing.

AI additions:
- Identify candidate tasks for AI automation
- Assess data availability for each candidate (Data Availability Matrix)
- Perform preliminary task-model fit assessment
- Draft the Human-in-the-Loop Map
- Research user comfort with AI-generated outputs and non-deterministic results

**Artefacts produced**:
- Data Availability Matrix
- Task-Model Fit Assessment (preliminary)
- Human-in-the-Loop Map (draft)

### Alpha
Standard focus: prototyping, hypothesis testing.

AI additions and ordering constraints:
1. Build manual prototypes first — a human acting as the model reveals tractability before automation investment
2. Define the evaluation rubric before building any automated prototype
3. Establish baseline scores using manual prototype outputs
4. Build and test at least one LLM-backed prototype with real users
5. Compare multiple model or prompt approaches before committing
6. Catalogue primary failure modes
7. Build the evaluation harness (test infrastructure) before Beta

**Critical rule**: The evaluation rubric is an Alpha output, not a Beta output. Defining success after the Beta build begins optimises for the wrong thing.

**Artefacts produced**:
- Evaluation Rubric (with baseline scores)
- Manual Prototype Log
- Failure Mode Catalogue
- Human-in-the-Loop Map (tested and validated)
- Technology decision and rationale

### Beta
Standard focus: build MVP, public release.

AI additions:
- Implement prompt versioning and change management from day one
- Establish production monitoring with rubric-based sampling
- Track cost-per-interaction
- Conduct bias and fairness review
- Document model deprecation plan
- A/B test prompt changes as deployments

**Critical rule**: Every prompt change in production must be treated as a deployment — versioned, tested against the evaluation rubric, and documented in a changelog.

**Artefacts produced**:
- Prompt Version History
- Model Deprecation Plan
- Production monitoring dashboard (metrics: latency, cost, rubric scores, error rate)

### Live
Standard focus: continuous improvement.

AI additions:
- Run evaluation sampling continuously (not as a one-time audit)
- Monitor for model drift, prompt drift, and data drift
- Monitor cost-per-interaction as a first-class metric
- Execute model deprecation plan when provider deprecates the model version

## Phase Gate Criteria for AI Projects

| Phase | Gate Criterion |
|-------|---------------|
| Alignment → Discovery | Data ownership identified; ethics review initiated; model vendor constraints established |
| Discovery → Alpha | Data Availability Matrix complete; candidate AI tasks identified; draft HITL Map created |
| Alpha → Beta | Evaluation rubric defined with baselines; LLM prototype user-tested; evaluation harness built; HITL Map validated |
| Beta → Live | Production monitoring active; prompt versioning in place; deprecation plan documented; accessibility and security reviews complete |

## Key Artefacts Summary

| Artefact | Phase | Owner | Purpose |
|----------|-------|-------|-------|
| Data Availability Matrix | Discovery | ML Engineer | What data exists; gaps; access agreements needed |
| Task-Model Fit Assessment | Discovery | ML Engineer | Which candidate tasks are tractable |
| Human-in-the-Loop Map | Discovery (draft), Alpha (validated) | Product Manager | Which AI decisions require human review |
| Manual Prototype Log | Alpha | UX / ML Engineer | Documents manual validation outcomes |
| Evaluation Rubric | Alpha | Evaluation Specialist | Defines dimensions, scoring, thresholds |
| Failure Mode Catalogue | Alpha | ML Engineer | Known failures and mitigations |
| Prompt Version History | Beta | ML Engineer | Changelog of prompt changes with rationale and scores |
| Model Deprecation Plan | Beta | Product Manager | Migration plan for when models are deprecated |
| Evaluation Sampling Report | Live | Evaluation Specialist | Periodic rubric scores from production sampling |

## Practical Guidance

**In Discovery**: Do not design AI features without knowing what data exists to support them. The Data Availability Matrix is a Discovery output. Discovering a data gap in Beta is expensive; discovering it in Discovery is cheap.

**In Alpha**: The first deliverable is the evaluation rubric, not the model. Define success criteria before building. Run manual prototypes before automated ones — they are faster, cheaper, and more revealing.

**In Beta**: Treat prompt changes as software deployments. Version them, test them against the rubric, stage them, and document them. An untracked prompt change is a production incident waiting to happen.

**In Live**: Model deprecation is an incident response scenario. Write the plan in Beta; execute it in Live when the provider announces deprecation. Cost-per-interaction monitoring catches prompt and usage pattern changes before they become budget surprises.

## AI Team Roles

| Role | Phase(s) | Key Responsibilities |
|------|----------|---------------------|
| AI/ML Systems Thinker | Alignment | Feasibility; data landscape; vendor constraints |
| Data Analyst / ML Engineer | Discovery | Data Availability Matrix; task-model fit |
| ML Engineer / Prompt Engineer | Alpha, Beta | Prototypes; prompt engineering; deployment |
| Evaluation Specialist | Alpha, Beta, Live | Rubric design; sampling; drift monitoring |
| AI Safety / Eval Lead | Beta, Live | Production monitoring; bias review; regression flags |
| MLOps / DevOps Engineer | Beta, Live | Model serving; CI/CD for prompt changes; cost monitoring |

## Examples

**Example 1: Alpha → Beta phase gate review (document summarisation project)**
| Criterion | Status | Evidence |
|-----------|--------|---------|
| Evaluation rubric defined with baseline scores | PASS | rubric-v1.md; baseline composite 0.84 |
| LLM prototype tested with real users | PASS | 12 user sessions; 8 rated useful |
| Evaluation harness built and passing | PASS | eval_harness.py; 47/50 golden set pass |
| HITL Map tested and validated | PASS | hitl-map-v2.md; validated by 3 subject-matter experts |
| Failure mode catalogue complete | PASS | failure-modes.md; 11 failure modes documented |

**Example 2: Data Availability Matrix (Discovery artefact)**
| Data Type | Exists | Format | Access | Gap |
|-----------|--------|--------|--------|-----|
| Policy documents | Yes | PDF, 2014–2026 | Internal share | Pre-2014 not digitised |
| User query logs | No | — | — | Must design collection from scratch |
| Manual expert decisions | Partial | Spreadsheet | — | Only 6 months of history available |

## Guidelines

1. Define the evaluation rubric before writing any automation code — if success cannot be measured, it cannot be achieved
2. Build manual prototypes in Alpha before automated ones — they reveal tractability constraints faster and at lower cost
3. Gate Alpha exit on a passing evaluation harness with a defined rubric score threshold, not just on a working prototype
4. Treat every prompt change in Beta and Live as a software deployment: version it, test it against the rubric, stage it, document it
5. Write the model deprecation plan in Beta; do not wait for a deprecation notice to start planning a migration
6. Complete the Data Availability Matrix in Discovery — a data gap discovered in Beta costs far more to resolve than one found in Discovery
7. Size the human review team for the HITL Map before Beta launch — an under-resourced review queue is a design failure, not a resourcing failure

## Gotchas

1. **Rubric defined after the prototype is built**: When success criteria are defined after building begins, teams optimise for what they built rather than what users need. The evaluation rubric must precede any automated prototype — it is a Discovery and Alpha output, not a Beta deliverable.

2. **Treating a prompt change as a configuration change**: Prompt changes significantly alter model behaviour. Teams that deploy prompt changes without rubric testing and staged rollout discover regressions in production rather than in evaluation. Every prompt change is a deployment: version it, test it, stage it.

3. **Underestimating model dependency risk**: A model version pinned in Alpha may be deprecated during Beta or Live. Teams without a deprecation plan scramble when the provider announces end-of-life with a 90-day window. Write the plan in Beta when planning is cheap.

4. **Skipping the manual prototype phase**: Teams that start directly with an LLM prototype discover intractable problems — ambiguous task definition, insufficient data, unacceptable non-determinism — after investing significantly more effort. The manual prototype phase is a rapid tractability test, not a waterfall holdover.

5. **HITL Map as an engineering artefact**: The HITL Map is a user research output, not an engineering output. Teams that design human review requirements based on their engineering model of risk, rather than on user research into trust and accountability needs, frequently discover that users require human review for legal or trust reasons even when the AI is accurate.

## Integration

This skill integrates with:
- `evaluation` — for designing the evaluation rubric and running the production sampling programme
- `agent-observability` — for setting up the production monitoring stack, drift detection, and prompt versioning
- `human-ai-collaboration` — for designing the Human-in-the-Loop Map and automation level decisions
- `project-development` — for task-model fit analysis and the manual prototype validation pattern
- `context-fundamentals` — context window constraints affect feature scoping in Discovery

## References

- [Phase Artefacts Reference](./references/phase-artefacts.md)
- [AI Team Roles Reference](./references/ai-team-roles.md)
- Related skills: evaluation, agent-observability, human-ai-collaboration, project-development
- Full process: https://github.com/ghostmachine-ai/agile-delivery-process

## Skill Metadata

- Created: 2026-07-09
- Last Updated: 2026-07-09
- Author: Agent Skills for Context Engineering Contributors
- Version: 1.0.0
