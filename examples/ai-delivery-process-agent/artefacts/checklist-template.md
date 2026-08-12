# Phase Gate Checklist Template

Use at the end of each phase to confirm readiness to proceed. The gate review should produce a signed-off version of this document.

## Phase: [Alignment / Discovery / Alpha / Beta / Live]

**Project**: [Project Name]  
**Review Date**: [Date]  
**Reviewers**: [Names and roles]

---

## Standard Criteria

- [ ] User research evidence reviewed
- [ ] Artefacts complete (no TBD sections)
- [ ] Technical feasibility confirmed
- [ ] Governance and compliance items resolved
- [ ] Outstanding risks documented with owners and mitigations

## AI-Specific Criteria

*Complete only for AI/agent projects.*

### Alignment Gate

- [ ] Data ownership and provenance constraints identified
- [ ] Ethics/algorithmic accountability review initiated
- [ ] Approved model vendor list established
- [ ] AI/ML feasibility assessment completed

### Discovery Gate

- [ ] Data Availability Matrix complete (no "TBD" on severity ratings)
- [ ] Candidate AI tasks identified and scoped
- [ ] Draft Human-in-the-Loop Map created (based on user research)
- [ ] Task-Model Fit Assessment complete

### Alpha Gate

- [ ] Manual prototype conducted and logged
- [ ] Evaluation rubric defined with domain expert approval
- [ ] Baseline scores established from manual prototype
- [ ] LLM prototype user-tested with real users
- [ ] HITL Map validated with users
- [ ] Failure mode catalogue complete
- [ ] Evaluation harness built and passing on test dataset
- [ ] Model/provider selected

### Beta Gate

- [ ] Production monitoring active (latency, cost, rubric score)
- [ ] Prompt versioning in place from first deployment
- [ ] Model deprecation plan documented
- [ ] HITL queue implemented with SLA confirmation
- [ ] Accessibility audit complete
- [ ] Security threat and risk assessment complete
- [ ] Privacy Impact Assessment (production) complete

---

## Evidence

| Criterion | Evidence | Owner | Status |
|-----------|----------|-------|--------|
| [e.g., Evaluation rubric] | [Link to rubric document] | [Eval Specialist] | [Complete] |

---

## Gate Decision

- [ ] Proceed to next phase
- [ ] Proceed with conditions: [list conditions]
- [ ] Return to current phase: [specify what must change]

**Decision**: _______________  
**Rationale**: _______________

## Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Service Owner | | | |
| Product Manager | | | |
| [AI Safety Lead (Beta+)] | | | |
