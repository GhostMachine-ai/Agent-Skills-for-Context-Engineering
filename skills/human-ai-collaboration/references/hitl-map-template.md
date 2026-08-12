# Human-in-the-Loop Map Template

A structured template for documenting human review requirements for every AI decision in a service.

## Overview

**Service:**
**Version:**
**Last updated:**
**Owner:** [Product Manager]
**Phase status:**
- [ ] Draft (Discovery)
- [ ] Validated with users (Alpha)
- [ ] Implemented (Beta)
- [ ] Monitoring live (Live)

## AI Decision Template

Copy and complete for each AI decision or action in the service.

---

### Decision: [Name]

**Description**: [What the AI is doing — be specific]

**Automation Level**: [ ] 1-Manual [ ] 2-Assisted [ ] 3-HITL [ ] 4-HOTL [ ] 5-Automated

**Rationale**: [Why this level was chosen — reference accuracy evidence, consequence assessment, human capacity]

**Consequence if wrong**:
- Severity: High / Medium / Low
- Description: [Impact on user or system if AI output is wrong and goes uncorrected]

**Who reviews**:
- Primary reviewer: [role]
- Escalation reviewer: [role]

**What the reviewer needs**: [Information required — not just the AI output; also source material, context, decision criteria]

**Trigger for review**:
- [ ] All outputs route to review
- [ ] Route when AI confidence < [threshold]
- [ ] Route when consequence score ≥ [threshold]
- [ ] Route when flagged by safety/quality filter
- [ ] Batch review: [N] outputs per [period]

**Review SLA**: [time]

**SLA miss handling**: [Escalate / Proceed / Notify user of delay]

**On approval**: [What happens]

**On rejection**: [What happens; what does the user see]

**Audit requirements**:
- [ ] Log who approved and when
- [ ] Log reviewer modifications to AI output
- [ ] Log reason for rejection

---

## Oversight Fatigue Risk Assessment

| Decision | Volume/day (est.) | Reviewer capacity/day | Fatigue Risk |
|----------|------------------|----------------------|-------------|
| | | | High/Med/Low |

**Assessment**: [Is total review load sustainable?]

## Trust Calibration Plan

**Starting automation levels**: [Summary and rationale]

**Trust signals to monitor**: [correction rate, reviewer agreement rates, user satisfaction]

**Criteria for expanding automation**:
- [ ] Reviewer agreement rate > 95% sustained 3 months
- [ ] User correction rate < 5% sustained 3 months
- [ ] Zero High-severity errors in previous month

**Review schedule**: [Quarterly review of automation levels against trust signal data]
