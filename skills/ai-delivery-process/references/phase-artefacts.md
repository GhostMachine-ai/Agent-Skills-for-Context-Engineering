# Phase Artefacts Reference: AI Delivery Process

Detailed descriptions of every artefact produced during an AI agent delivery project, organised by phase.

## Discovery Artefacts

### Data Availability Matrix

**Purpose**: Establish whether sufficient data exists to support candidate AI features before Alpha investment begins.

**Owner**: Data Analyst or ML Engineer

**Contents**:
- Inventory of all data types required by candidate AI features
- For each data type: source, format, volume, quality assessment, access status, privacy classification
- Gap analysis: required data that does not currently exist or is not accessible
- Data agreements required
- Preliminary task-model fit assessment per candidate feature

**Quality criteria**:
- All candidate AI features covered
- Each data type has a documented source (not "TBD")
- Privacy classification documented for all personal data
- Gap severity rated (High / Medium / Low impact if unresolved)
- Path to resolution documented for every gap

**Common failure mode**: Teams rate all gaps as "Medium" to avoid difficult conversations. Gaps that block Alpha or Beta should be rated High regardless of discomfort.

### Task-Model Fit Assessment (preliminary)

**Purpose**: Identify which candidate AI tasks are tractable given available data, model capabilities, and acceptable failure modes.

**Owner**: ML Engineer

**Assessment criteria**:

| Criterion | Fit Implication |
|-----------|----------------|
| Task is well-defined and bounded | Strong fit |
| Sufficient labelled data exists | Strong fit |
| Task has clear, measurable success criteria | Strong fit |
| Failure is low-consequence or easily detectable | Acceptable |
| Data requires significant cleaning or labelling | Moderate; budget time |
| No data exists; requires collection programme | Weak; significant pre-work |
| Failure could harm users; hard to detect | Not recommended without robust HITL |
| Task requires precise, auditable reasoning | Consider rule-based alternative |

### Human-in-the-Loop Map (draft)

**Purpose**: Identify which AI decisions must be reviewed by a human before affecting a user. Drafted in Discovery from user research; tested and validated in Alpha.

**Owner**: Product Manager (with input from User Researcher)

**Contents**: For each AI action or decision — description, consequence level, who reviews, what information they need, threshold for review, what happens on approval or rejection, review SLA.

**Common failure mode**: HITL Maps created by engineers without user research input. The question "which decisions must a human make?" is a user research question — users of high-stakes services often require human accountability even when the AI output is technically correct.

## Alpha Artefacts

### Manual Prototype Log

**Purpose**: Document outcomes of manual (human-as-model) prototype validation sessions before automation investment.

**Owner**: UX Designer or ML Engineer

**Contents**: Session dates, participant descriptions, inputs provided, outputs produced, user reactions, patterns and failure modes observed, recommendation on whether to proceed with automation.

### Evaluation Rubric

**Purpose**: Define how AI/agent behaviour is measured and what threshold must be met before Beta.

**Owner**: Evaluation Specialist

**Contents**:
- Evaluation dimensions with weights (must sum to 100%)
- Scoring guide with concrete anchors per score point
- Representative test cases with expected output characteristics
- Failure mode catalogue
- Baseline scores from Alpha prototype testing
- Targets for Beta launch and Live steady-state
- Evaluation method (human annotation, LLM-as-judge, or hybrid)
- Human review criteria

**Critical rule**: Rubric is finalized before the Beta build begins.

### Failure Mode Catalogue

**Purpose**: Document all known ways the AI system can fail, trigger conditions, and mitigations.

**Owner**: ML Engineer

**Contents**: For each failure mode — description, trigger conditions, user impact (High / Medium / Low), mitigation, detection method, status (Mitigated / Accepted / Open).

## Beta Artefacts

### Prompt Version History

**Purpose**: Maintain a changelog of all changes to production prompts.

**Owner**: ML Engineer

**Required fields per entry**: version, date, author, change summary, rubric score before, rubric score after, rollback path.

**Requirements**:
- Every production prompt change must be documented
- Rubric scores recorded before and after each change
- Rollback path documented for every change
- Staged rollouts recorded (percentage of traffic, dates)

### Model Deprecation Plan

**Purpose**: Document what the team will do when the model provider deprecates the model version the service depends on.

**Owner**: Product Manager

**Contents**: Current model versions and known end-of-life dates, deprecation monitoring approach, evaluation plan for replacement model, rollout plan for the switch, rollback plan if replacement performs worse, cost impact assessment.
