# Product Requirements Document: AI Document Summariser

## Problem Statement

Civil servants spend significant time reading lengthy policy documents to extract key decisions and action items. The average policy document is 45 pages; a team of 20 reads 3–5 documents per week each. High cognitive load leads to missed action items and inconsistent summaries across teams.

## Proposed Solution

An LLM-powered document summarisation service that accepts uploaded PDF or Word documents and returns a structured four-section summary:

1. **Executive Summary** (3–5 sentences)
2. **Key Decisions** (bulleted list)
3. **Action Items** (bulleted list with owners where stated)
4. **Risk Flags** (bulleted list with severity where determinable)

## Success Criteria (Alpha Gate)

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| Evaluation rubric score | ≥ 3.5/5 | Rubric with human + LLM judges |
| P95 latency | ≤ 30s | Production monitoring |
| Cost per summary | ≤ £0.05 | Cost tracking dashboard |
| User satisfaction | ≥ 70% positive | Post-use survey |
| Hallucinated citations | 0 | Accuracy review (human annotation) |

## Constraints

- All documents contain potentially sensitive government data; model provider must be UK-sovereign or approved equivalent
- No fine-tuning on government documents without Data Processing Agreement
- Summaries must clearly indicate AI generation and model version used
- OFFICIAL-SENSITIVE documents require human review before summary is delivered

## Out of Scope — Phase 1

- Scanned image PDFs (requires OCR; deferred to Phase 2)
- Documents longer than 50 pages
- Languages other than English
- Audio or video transcripts

## AI-Specific Requirements

| Requirement | Phase | Owner |
|-------------|-------|-------|
| Human review for OFFICIAL-SENSITIVE documents | Beta | PM, UX |
| Evaluation rubric approved by domain expert | Alpha | Evaluation Specialist |
| Prompt version history from first Beta deployment | Beta | ML Engineer |
| Model deprecation plan before Beta gate | Beta | PM |
| Drift detection active at Live launch | Live | MLOps |
| Cost alerting at 2× baseline | Beta | MLOps |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Model provider changes API or pricing | Medium | High | Model deprecation plan; cost alerting |
| Accuracy insufficient for OFFICIAL-SENSITIVE documents | Medium | High | Level 1 HITL for all OFFICIAL-SENSITIVE |
| Latency too high for acceptable UX | Low | Medium | Async processing with notification |
| User over-trust of AI summaries | Medium | Medium | Confidence score display; clear AI labelling |
