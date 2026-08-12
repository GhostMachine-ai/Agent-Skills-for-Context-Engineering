# Human-in-the-Loop Map Template

Document which AI decisions require human review, what reviewers need, and how the review workflow operates.

Draft in Discovery (from user research); validate with real users in Alpha.

## AI Decisions Requiring Human Review

For each AI action or decision that affects a user, complete one row.

| AI Decision | Consequence Level | Automation Level | Reviewer | What Reviewer Needs | Review Trigger | SLA | On Approve | On Reject | Audit Required |
|-------------|------------------|-----------------|----------|-------------------|----------------|-----|------------|-----------|----------------|
| [e.g., Document summary — UNCLASSIFIED] | [Low] | [Level 2: AI draft, human edits] | [Requesting user] | [Source doc + AI summary] | [Any UNCLASSIFIED document] | [N/A — self-review] | [User uses/edits summary] | [User discards] | [No] |
| [e.g., Document summary — OFFICIAL-SENSITIVE] | [High] | [Level 1: human decides, AI informs] | [Designated policy reviewer] | [Source doc + AI summary + confidence score] | [Any OFFICIAL-SENSITIVE document] | [4 hours] | [Summary released to requestor] | [Human produces manual summary] | [Yes] |
| [e.g., Low-quality flag (score < 3.0)] | [Medium] | [Level 1: human reviews] | [ML Engineer] | [Input doc + output + rubric scores] | [Rubric composite < 3.0] | [2 hours] | [Reviewed output released] | [Output suppressed; error shown] | [Yes] |

**Automation levels** (from `human-ai-collaboration` skill):
- Level 1: Human decides; AI informs
- Level 2: AI draft; human reviews and edits before use
- Level 3: AI produces output; human spot-checks
- Level 4: AI acts; human monitors
- Level 5: Fully automated

---

## Consequence Level Guide

| Level | Description | Examples |
|-------|-------------|---------|
| High | Error could cause harm, legal liability, or accountability breach | Decisions affecting individuals; regulatory outputs |
| Medium | Error is embarrassing, recoverable, or detectable by user | Advisory summaries; internal briefings |
| Low | Error is easily spotted and has no downstream harm | Non-critical notifications; internal drafts |

---

## Oversight Fatigue Assessment

Review this table when the HITL Map is validated and after 3–6 months in Live.

| Review Decision | Volume (per day) | Avg Review Time | Reviewer Capacity | Risk |
|-----------------|-----------------|----------------|------------------|------|
| [e.g., OFFICIAL-SENSITIVE summaries] | [e.g., 12] | [e.g., 15 mins] | [e.g., 3h/day across 2 reviewers] | [Low / Medium / High] |

**SLA simulation result**: [Predicted peak wait time from `hitl_simulator.py`]

---

## Trust Calibration Plan

How the team will build and maintain appropriate user trust in the AI system.

| Phase | Trust Intervention | Owner |
|-------|-------------------|-------|
| Alpha | Show confidence score alongside summary | UX |
| Beta | Display model version and "AI-generated" label | Dev |
| Beta | Provide source paragraph references for key decisions | ML Engineer |
| Live | Monitor and report over-trust indicators (e.g., users never editing AI summaries) | Eval Lead |

---

## Graceful Degradation

What happens when the AI system is unavailable:

| Failure Mode | Fallback | User Experience |
|--------------|----------|----------------|
| Model API unavailable | Manual summary request routed to HITL queue | User notified; wait time communicated |
| Evaluation harness failure | Sampling paused; manual review rate increased | Transparent to users |
| Review queue SLA breach | Escalation to senior reviewer; notification to PM | SLA breach logged; user notified if impacted |
