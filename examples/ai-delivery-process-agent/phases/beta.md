# Beta Phase: AI Document Summariser

## Team

| Role | Person | AI-Specific |
|------|--------|-------------|
| Product Manager | PM | — |
| UX Designer | UX | — |
| Developers | Dev 1, Dev 2 | — |
| DevOps / MLOps | MLOps Engineer | Yes |
| QA | QA | — |
| ML Engineer | ML Engineer | Yes |
| AI Safety / Eval Lead | Eval Specialist | Yes |
| User Researcher | UX Researcher (part-time) | — |

## Production Monitoring Setup

Full monitoring reference: `references/monitoring-setup.md`

| Metric | Threshold | Alert Condition | Collection |
|--------|-----------|-----------------|------------|
| P95 latency | ≤ 30s | > 30s for 5 mins | API gateway |
| Cost per summary | ≤ £0.05 | > £0.10 (2× baseline) | Cost API |
| Rubric score (sampled) | ≥ 3.5 | < 3.5 for 3 consecutive samples | Evaluation harness |
| Error rate | < 1% | > 5% | API gateway |
| HITL review wait time | ≤ 4h | > 4h P95 | Review queue |

**Evaluation sampling rate**: 10% of all summaries (both dimensions: automated rubric + 1% human annotation)

## Prompt Version History (Weeks 1–8)

Full changelog: `prompts/CHANGELOG.md` (not included in this example)

| Version | Date | Change | Rubric (before) | Rubric (after) | Latency P95 |
|---------|------|--------|-----------------|----------------|-------------|
| 1.0.0 | Week 1 | Initial production prompt | — | 3.7 | 18s |
| 1.1.0 | Week 3 | Improved factual density | 3.7 | 3.9 | 25s |
| 1.2.0 | Week 5 | Tighter structure enforcement | 3.9 | 4.0 | **35s** → rolled back |
| 1.1.1 | Week 5 | Rollback to 1.1.0 | 4.0 | 3.9 | 25s |
| 1.2.0-r | Week 6 | Structure enforcement with latency fix | 3.9 | 3.9 | 22s |

**All prompt changes**: staged at 5% → 25% → 100% with 24-hour hold at each stage, rubric re-run, and documented rollback path.

## HITL Implementation

**Review queue tool**: Internal web app with source document viewer, AI summary, edit interface, approve/reject.

**Reviewer pool**: 2 policy officers (part-time), 1 ML Engineer (escalation only)

**Queue performance (Beta weeks 1–8)**:

| Metric | Target | Actual |
|--------|--------|--------|
| Mean wait time | ≤ 4h | 1.8h |
| P95 wait time | ≤ 4h | 3.1h |
| Peak wait time | — | 3.7h |
| Reviewer capacity utilisation | < 80% | 62% |

**HITL queue simulator prediction** (run in Alpha): 8h peak wait time at projected volume with 1 reviewer. Actual with 2 reviewers: 3.7h. Simulator was pessimistic but directionally correct.

## Model Deprecation Plan

Owner: Product Manager  
Created: Week 2 of Beta

| Component | Detail |
|-----------|--------|
| Current model | [UK-sovereign provider], version 1.0 |
| Known EOL | Not announced; monitoring provider roadmap monthly |
| Deprecation signal | Provider deprecation notice or performance degradation > 10% |
| Evaluation plan | Run full test dataset against candidate replacement model; require ≥ 3.5/5 before switch |
| Rollout plan | Staged: 5% → 25% → 100%, same as prompt change process |
| Rollback plan | Revert to previous model version; 24h observation before removal |
| Cost impact | Document per-token pricing of replacement; update cost alerting threshold |

## Beta Gate Decision

**Decision**: Proceed to Live  
**Date**: End of week 10  
**Sign-off**: Service Owner, PM, AI Safety Lead

**Gate criteria met**:
- [x] Production monitoring active (all metrics instrumented)
- [x] Prompt versioning in place from first deployment
- [x] Model deprecation plan documented and reviewed
- [x] HITL queue implemented and SLA met
- [x] Accessibility audit complete (WCAG 2.1 AA)
- [x] Security threat and risk assessment complete
- [x] Privacy Impact Assessment (production) complete
