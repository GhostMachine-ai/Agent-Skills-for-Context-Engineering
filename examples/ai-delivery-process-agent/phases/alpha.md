# Alpha Phase: AI Document Summariser

## Team

| Role | Person | AI-Specific |
|------|--------|-------------|
| Product Manager | PM | — |
| UX Designer/Researcher | UX | — |
| Full-Stack Developer | Dev 1 | — |
| QA Lead | QA (part-time) | — |
| ML Engineer | ML Engineer | Yes |
| Evaluation Specialist | Eval Specialist (part-time) | Yes |

## Sequence of Activities

1. Manual prototype (weeks 1–2)
2. Evaluation rubric design (weeks 2–3, parallel with manual prototype)
3. Baseline scoring from manual prototype outputs (week 3)
4. LLM prototype build (weeks 3–5)
5. LLM prototype user testing (weeks 5–6)
6. HITL Map validation with users (week 6)
7. Evaluation harness build (weeks 5–7)
8. Failure mode catalogue (week 7)
9. Alpha gate review (week 8)

## Manual Prototype Log (Summary)

Full log: sessions were conducted by a UX researcher acting as the AI.

**Duration**: 2 days (8 documents across 4 participants)

**Key finding**: Users expected **Action Items** and **Risk Flags** as separate sections. The initial prompt design combined them under "Next Steps". This was discovered in 20 minutes of manual prototype work.

**Other findings**:
- Users wanted the Executive Summary to state the document's purpose, not just summarise its content
- Users in fast-turnaround teams preferred bullet format over prose for all sections
- Domain expert reviewers wanted source paragraph references alongside key decisions

**Recommendation**: Proceed with automated prototype. Revise four-section structure to make Action Items and Risk Flags explicit sections.

## Evaluation Rubric

Full rubric: `artefacts/evaluation-rubric-template.md`

| Dimension | Weight | Threshold | Scoring Anchor (5/5) |
|-----------|--------|-----------|---------------------|
| Accuracy | 35% | No hallucinations | All key decisions present; no citations invented; no fabricated data |
| Coherence | 25% | ≥ 3.0 | Summary reads fluently; no contradictions; logical flow |
| Completeness | 20% | ≥ 3.0 | All action items and risk flags captured; no material omissions |
| Format Compliance | 20% | ≥ 4.0 | All four sections present; correct headings; bullet format |

**Composite threshold**: ≥ 3.5/5 for Alpha gate

**Evaluation method**:
- Accuracy: Human annotation (10% sample) + LLM-as-judge (90%)
- Coherence: LLM-as-judge
- Completeness: LLM-as-judge with human calibration (10% overlap)
- Format Compliance: Automated rule check

**Baseline (manual prototype)**: 3.1/5

## LLM Prototype Results

**Model**: [UK-sovereign cloud provider, model version 1.0]

| Dimension | Score | vs. Baseline |
|-----------|-------|-------------|
| Accuracy | 3.8 | +0.7 |
| Coherence | 3.6 | +0.5 |
| Completeness | 3.5 | +0.4 |
| Format Compliance | 4.2 | +1.1 |
| **Composite** | **3.7** | **+0.6** |

**Alpha threshold met**: Yes (3.7 ≥ 3.5)

## User Testing (LLM Prototype)

**Participants**: 8 civil servants across 3 departments

**Key findings**:
- 7/8 rated the summary as "useful" or "very useful"
- 6/8 correctly identified which decisions required their action
- 2/8 trusted the AI summary without reading the source document (over-trust risk → confidence score display added)

**HITL Map validation**:
- Participants confirmed Level 2 is acceptable for UNCLASSIFIED documents
- Participants confirmed Level 1 is required for OFFICIAL-SENSITIVE: "I need to know a human checked this before it goes to the Minister"

## Failure Mode Catalogue (Summary)

Full catalogue: `artefacts/failure-modes.md`

| Failure Mode | Trigger | User Impact | Mitigation | Status |
|--------------|---------|-------------|------------|--------|
| Key decision omitted | Dense legislative language | High | Accuracy evaluation + human sampling | Accepted (score threshold) |
| Invented citation | Ambiguous source references | High | Hard constraint in prompt; accuracy evaluation | Mitigated |
| Risk flag missed | Subtle or implicit risks | Medium | Completeness evaluation | Accepted (score threshold) |
| Format breakdown | Very short documents (< 3 pages) | Low | Minimum length guardrail | Mitigated |
| Context window exceeded | Documents > 50 pages | High | Hard limit in API gateway; user notification | Mitigated (scope) |

## Evaluation Harness

Location: `scripts/` directory (not included in this example — see `scripts/` for tooling patterns)

**Components built**:
- `evaluate_batch.py`: runs rubric scoring across a dataset of document–summary pairs
- `accuracy_judge.py`: LLM-as-judge for accuracy with human-calibrated prompts
- `format_check.py`: automated rule check for four-section structure
- `harness_report.py`: generates HTML report with per-dimension scores and sample outputs

## Gate Decision

**Decision**: Proceed to Beta  
**Date**: End of week 8  
**Sign-off**: Service Owner, PM, Evaluation Specialist

**Gate criteria met**:
- [x] Evaluation rubric defined with baselines (3.1 manual, 3.7 LLM)
- [x] LLM prototype user-tested (8 participants)
- [x] Evaluation harness built and passing on test dataset
- [x] HITL Map validated with real users
- [x] Failure mode catalogue complete
- [x] Model/provider selected: [UK-sovereign cloud provider]
