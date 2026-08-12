# Automation Level Framework Reference

A detailed framework for selecting the right level of AI automation for each decision or action in a service.

## The Five Automation Levels

### Level 1: Fully Manual
AI is not involved. A human does everything.

**Use when**: Life/safety consequences; regulation requires human decision-making; no training data; task requires embodied judgment.

### Level 2: AI-Assisted
AI provides information, context, or analysis; the human decides and takes action.

**Use when**: High consequence; AI confidence is variable or unpredictable; building trust in a new AI capability before expanding automation.

**Design requirement**: The AI's analysis must be shown in a form the human can evaluate. "RISK: HIGH" with no explanation is a black box, not AI-assisted.

### Level 3: Human-in-the-Loop
AI proposes an action; a human approves it before execution.

**Use when**: Good AI accuracy but not high enough to trust fully; regulatory or audit requirements demand a human approval trail; users expect human review.

**Design requirements**: Review must be meaningful; SLA must be achievable; fallback if SLA missed; audit trail of who approved what with timestamp.

### Level 4: Human-on-the-Loop
AI acts autonomously; a human monitors and can intervene.

**Use when**: High accuracy well-evidenced; actions are reversible or consequences are moderate; volume exceeds practical Level 3 capacity; trust has been established through extended Level 3 operation.

**Risk**: Oversight can become nominal. Monitor reviewer engagement as an oversight quality signal.

### Level 5: Fully Automated
AI acts without human review. Outcomes audited periodically.

**Use when**: Very high accuracy (typically > 98%) with long production history; low-consequence errors; failure modes well-understood and detectable; reversal of incorrect actions is fast.

**Important**: Level 5 requires MORE robust observability than Levels 1–4 because there is no human reviewer catching systematic errors.

## Decision Framework

**Step 1: Assess consequence**
If an AI error goes undetected for 24 hours, what is the impact?
- Life/safety/legal → Start at Level 1 or 2
- Significant financial or welfare consequence → Level 3
- Moderate consequence; reversible → Level 3 or 4
- Low consequence; easily reversible → Level 4 or 5

**Step 2: Assess AI accuracy evidence**
What is the accuracy on a representative sample?
- No evidence → Level 2 (gather evidence)
- < 90% → Level 2 or 3
- 90–95% → Level 3 or 4
- > 95% sustained 6+ months → Level 4 or 5

**Step 3: Assess human capacity**
Can reviewers handle the queue volume at the required SLA?
- Queue would exceed capacity → Consider Level 4 only if accuracy justifies it
- SLA would be unacceptable to users → Increase reviewer capacity; do not skip steps

**Step 4: Assess reversibility**
- Detection > 24 hours or correction difficult → Lower automation level
- Detection < 1 hour and correction easy → Higher automation level is lower risk

**Step 5: Check regulatory constraints**
Are there requirements that mandate human decision-making regardless of accuracy? If yes, automation level is bounded.
