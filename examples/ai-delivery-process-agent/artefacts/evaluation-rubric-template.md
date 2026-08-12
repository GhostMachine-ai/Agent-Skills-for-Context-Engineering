# Evaluation Rubric Template

Use this template to define evaluation criteria before building the automated prototype in Alpha.

## Task Description

**Task name**: [e.g., Document Summarisation]  
**Task description**: [What the AI component does]  
**Composite threshold for Alpha gate**: [e.g., ≥ 3.5/5]  
**Rubric owner**: [Evaluation Specialist]  
**Domain expert approval**: [Name, date]

---

## Evaluation Dimensions

Weights must sum to 100%. Assign higher weight to dimensions where failure has the highest user impact.

| Dimension | Weight | Description | Threshold |
|-----------|--------|-------------|-----------|
| [e.g., Accuracy] | [e.g., 35%] | [What accuracy means for this task] | [e.g., No hallucinations; hard constraint] |
| [e.g., Coherence] | [e.g., 25%] | [What coherence means for this task] | [e.g., ≥ 3.0] |
| [e.g., Completeness] | [e.g., 20%] | [What completeness means for this task] | [e.g., ≥ 3.0] |
| [e.g., Format Compliance] | [e.g., 20%] | [What compliance means for this task] | [e.g., ≥ 4.0] |

---

## Scoring Guide

### [Dimension 1: e.g., Accuracy]

| Score | Anchor |
|-------|--------|
| 5 | All required information present; no hallucinations; no invented citations |
| 4 | All required information present; minor inaccuracies that do not mislead |
| 3 | Most required information present; one factual error that is detectable |
| 2 | Key information missing or contains significant factual errors |
| 1 | Output is substantially inaccurate or fabricated |

### [Dimension 2: e.g., Coherence]

| Score | Anchor |
|-------|--------|
| 5 | Reads fluently; logical structure throughout; no contradictions |
| 4 | Mostly fluent; one or two awkward transitions |
| 3 | Understandable but requires effort; some structural issues |
| 2 | Difficult to follow; significant structural problems |
| 1 | Incoherent or self-contradictory |

*[Add scoring guide for each dimension.]*

---

## Test Cases

Representative inputs and expected output characteristics. Used for manual review and LLM-as-judge calibration.

| Case ID | Input Description | Expected Output Characteristics | Difficulty |
|---------|------------------|--------------------------------|------------|
| TC-001 | [e.g., 10-page policy memo] | [e.g., 3 key decisions; 2 action items; no risk flags] | Medium |
| TC-002 | [e.g., Dense legislative text] | [e.g., All decisions present; risk of omission] | Hard |
| TC-003 | [e.g., Short executive brief] | [e.g., All four sections present; completeness easy] | Easy |

---

## Failure Mode Catalogue

| Failure Mode | Trigger | User Impact | Mitigation | Detection |
|--------------|---------|-------------|------------|-----------|
| [e.g., Decision omitted] | [e.g., Dense text] | [High/Medium/Low] | [e.g., Prompt instruction; accuracy eval] | [e.g., Accuracy score < 3] |

---

## Baseline and Targets

| Source | Composite Score | Notes |
|--------|----------------|-------|
| Manual prototype | [e.g., 3.1] | Human-as-model baseline |
| Alpha LLM prototype | [Score] | Must meet threshold |
| Beta target | [e.g., 3.8] | Post-prompt-tuning |
| Live steady-state | [e.g., 3.8] | Monitored via sampling |

---

## Evaluation Method

| Dimension | Method | Sampling Rate | Human Calibration |
|-----------|--------|--------------|------------------|
| [Dimension 1] | [Human annotation / LLM-as-judge / Automated rule] | [e.g., 100%] | [e.g., 10% overlap] |
| [Dimension 2] | [Human annotation / LLM-as-judge / Automated rule] | [e.g., 10%] | [e.g., 5% overlap] |

---

## Human Review Criteria

Outputs routed to human review if:
- [ ] Composite score < [threshold]
- [ ] Any hard-constraint dimension fails (e.g., accuracy = 1 or 2)
- [ ] Confidence score < [threshold]
- [ ] Document classification is OFFICIAL-SENSITIVE or above (project-specific)
