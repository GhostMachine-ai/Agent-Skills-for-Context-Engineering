# User Story Template — AI/Agent Features

## User Story

**As a** [type of user]  
**I want to** [action or capability]  
**So that** [outcome or benefit]

---

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [The AI-generated output is clearly labelled as AI-generated]
- [ ] [The user can identify which model version produced the output]

---

## AI/Agent Considerations

### Role of the AI Component

[Describe what the AI does in this story. Is it generating, classifying, summarising, or recommending? What data does it process?]

### Success Criteria

| Dimension | Threshold | Measurement Method |
|-----------|-----------|-------------------|
| [e.g., Accuracy] | [e.g., No hallucinations] | [e.g., Human annotation of 10% sample] |
| [e.g., Latency] | [e.g., ≤ 10s] | [e.g., P95 via monitoring] |

### Failure Modes

[What are the plausible ways the AI component fails in this user story? List 2–4.]

| Failure Mode | User Impact | Detection | Mitigation |
|--------------|-------------|-----------|------------|
| [e.g., Incorrect classification] | [Medium] | [Evaluation sampling] | [HITL review at low confidence] |

### Human Review Requirement

- [ ] This story requires human review of AI output before it reaches the user (HITL)
  - Reviewer: [Role]
  - Trigger: [When review is triggered]
  - SLA: [Maximum wait time]
- [ ] No human review required — user receives AI output directly
  - Rationale: [Why this is acceptable — consequence level, reversibility, user oversight]

### Non-determinism Acceptance

[AI outputs are non-deterministic. How does this story handle the fact that the same input may produce different outputs on different runs?]

- User is informed of non-determinism: [ ] Yes / [ ] No
- Quality gate for non-deterministic variation: [e.g., rubric score ≥ 3.5 on any run]

---

## Testing Notes

- **Evaluation**: How will AI output quality be tested? (rubric, human annotation, LLM-as-judge?)
- **Edge cases**: What inputs are likely to produce the worst-case AI outputs?
- **Regression**: How will a future model or prompt change be caught before reaching users?

---

## Dependencies

- Evaluation rubric defined: [ ] Yes / [ ] No (required before sprint)
- HITL Map entry created: [ ] Yes / [ ] No / [ ] N/A
- Monitoring instrumented for this feature: [ ] Yes / [ ] No (required before Beta)
