# Alignment Phase: AI Document Summariser

## Team

| Role | Person | AI-Specific |
|------|--------|-------------|
| Service Owner | Head of Digital Transformation | — |
| Product Manager | PM | — |
| Delivery Manager | DM | — |
| AI/ML Systems Thinker | Senior ML Architect (seconded) | Yes |
| Privacy Advisor | Data Protection Officer | — |

## Activities Completed

- [x] Stakeholder mapping and RACI agreed
- [x] Problem statement agreed with policy team
- [x] Funding confirmed for Discovery and Alpha
- [x] High-level feasibility assessment (AI/ML Systems Thinker)
- [x] Data sovereignty constraints identified
- [x] Approved model vendors list established
- [x] Ethics/algorithmic accountability review initiated
- [x] Privacy Impact Assessment submitted for Discovery activities

## AI Feasibility Assessment (Summary)

Performed by: Senior ML Architect  
Date: Week 2 of Alignment

**Assessment**: Document summarisation is tractable for current LLM capabilities. The task is well-bounded, has clear success criteria, and available models have demonstrated strong performance on comparable tasks in published benchmarks.

**Constraints identified**:

| Constraint | Severity | Resolution |
|------------|----------|------------|
| UK data sovereignty — no US-hosted API without DPA | High | Evaluate sovereign-cloud providers; UK Gov approved list |
| No fine-tuning on government documents without DPA | Medium | Use prompt engineering only for Phase 1 |
| No access to labelled government document dataset | Low | Use domain-expert annotation in Alpha |

**Recommendation**: Proceed to Discovery. Confirm sovereign-cloud provider selection in Discovery before committing to technical architecture.

## AI Constraints Document

Location: `docs/ai-constraints.md` (created in Alignment)

Key constraints captured:
1. Model provider must be on the approved vendor list or pass a security assessment
2. Documents may not leave UK jurisdiction for processing
3. Fine-tuning requires separate DPA and Data Ethics approval
4. All AI-generated content must be clearly labelled

## Gate Decision

**Decision**: Proceed to Discovery  
**Date**: End of week 3  
**Sign-off**: Head of Digital Transformation, DPO

**Gate criteria met**:
- [x] Data ownership identified
- [x] Ethics review initiated
- [x] Model vendor constraints established
- [x] Funding confirmed
