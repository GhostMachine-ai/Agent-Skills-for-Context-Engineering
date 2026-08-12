# Phase Exit Criteria: AI Projects

Detailed exit criteria for each phase gate on an AI delivery project. Use this alongside the phase gate checklist.

## Alignment → Discovery

All of the following must be true:

| Criterion | Evidence | Notes |
|-----------|----------|-------|
| Problem statement agreed | Signed problem statement document | |
| Funding confirmed for Discovery | Budget approval | |
| Data ownership constraints identified | AI Constraints Document | Who owns the data; what agreements are needed |
| Model vendor constraints established | AI Constraints Document | Approved vendor list or assessment criteria |
| Ethics/accountability review initiated | Review submission acknowledgement | Not complete — initiated |
| Privacy Impact Assessment submitted for Discovery activities | PIA submission | |
| AI feasibility assessment complete | Assessment document | Signed off by AI/ML Systems Thinker |

**Anti-pattern**: Proceeding to Discovery without knowing data sovereignty constraints. This regularly surfaces in Beta and causes delays or architectural rework.

---

## Discovery → Alpha

All of the following must be true:

| Criterion | Evidence | Notes |
|-----------|----------|-------|
| Data Availability Matrix complete | Matrix document — no "TBD" severity ratings | All gaps rated High/Medium/Low with resolution path |
| Candidate AI tasks identified and scoped | Task-Model Fit Assessment | Clear in-scope / out-of-scope decision for each task |
| Draft HITL Map created from user research | HITL Map document | Must reflect user research findings, not engineering assumptions |
| User research complete | Research report | Covers user needs and attitudes to AI-generated outputs |
| Problem statement validated with users | Research report | Confirms problem is real and AI is appropriate solution |

**Anti-pattern**: Task-Model Fit Assessment created by ML Engineer without user research input. The key question — which tasks are appropriate for AI automation — requires understanding user consequence and tolerance, not just technical feasibility.

---

## Alpha → Beta

All of the following must be true:

| Criterion | Evidence | Notes |
|-----------|----------|-------|
| Manual prototype conducted and logged | Manual Prototype Log | Documents what the human-as-model revealed |
| Evaluation rubric defined and approved | Rubric document — domain expert sign-off | Weights and scoring guide; domain expert has reviewed |
| Baseline scores from manual prototype | Rubric document | Establishes what "human level" looks like |
| LLM prototype scored ≥ composite threshold | Evaluation results | Must be on a held-out test set, not the rubric design set |
| LLM prototype user-tested with real users | User testing report | Minimum 5 participants from target population |
| HITL Map validated with users | Updated HITL Map | Automation levels confirmed with users, not assumed |
| Failure Mode Catalogue complete | Catalogue document | Covers trigger, impact, mitigation, detection for each mode |
| Evaluation harness built and passing | Test results | Must run on representative dataset without manual intervention |
| Model/provider selection made | Decision document | Provider cleared through security and legal |

**Anti-pattern**: Evaluation rubric defined after the LLM prototype is built. This leads to rubric design being influenced by what the model happens to do well — optimising for the build, not for user need.

---

## Beta → Live

All of the following must be true:

| Criterion | Evidence | Notes |
|-----------|----------|-------|
| Production monitoring active | Dashboard link | Latency, cost, rubric score, error rate all instrumented |
| Prompt versioning in place from first deployment | CHANGELOG.md | At least one version entry with before/after scores |
| Model deprecation plan documented | Deprecation plan document | Reviewed by PM and ML Engineer |
| HITL queue live and SLA met | Queue metrics | P95 wait time within SLA target during Beta |
| Accessibility audit complete | Audit report | WCAG 2.1 AA minimum |
| Security threat and risk assessment complete | STRA document | Signed off by security team |
| Privacy Impact Assessment (production) complete | PIA document | Covers production data flows including model API |
| Rubric score stable over Beta period | Monitoring dashboard | No unresolved regressions below threshold |

**Anti-pattern**: Treating prompt changes as code deployments without separate versioning. A prompt change that improves quality on the rubric but degrades latency or cost is a regression — caught only if before/after metrics are tracked.

---

## Live: Ongoing Quality Gate

The live quality gate runs continuously, not as a one-time review.

| Trigger | Action |
|---------|--------|
| Rubric score < threshold for 3 consecutive weekly samples | ML Engineer investigates; PM notified within 24h |
| Drift alert (current window < baseline − 0.2) | ML Engineer investigates cause; fix deployed within 5 business days |
| Cost-per-interaction > 2× baseline | MLOps investigates; PM notified same day |
| HITL SLA breach (> 10% of reviews) | Reviewer capacity review; PM notified same day |
| Model provider deprecation notice | Model deprecation plan activated; timeline confirmed with PM |
