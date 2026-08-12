# AI Team Roles Reference

Detailed descriptions of each role on an AI delivery team.

## Core Delivery Roles (all phases)

### Product Manager

**Active in**: All phases

**AI-specific responsibilities**:
- Owns the Human-in-the-Loop Map
- Makes build-vs-buy-vs-fine-tune decisions
- Manages the model deprecation plan
- Translates evaluation rubric scores into product decisions
- Balances feature scope against model cost-per-interaction

### Delivery Manager

**Active in**: All phases

**AI-specific responsibilities**:
- Tracks evaluation harness completion as a Beta prerequisite
- Manages prompt change deployment complexity
- Coordinates model upgrade testing cycles

## AI-Specific Roles

### ML Engineer / Prompt Engineer

**Active in**: Discovery (part-time), Alpha (full-time), Beta (full-time), Live (part-time / on-call)

**Primary responsibilities**:
- Discovery: Data Availability Matrix; task-model fit assessment
- Alpha: Manual prototype validation; prompt engineering; model comparison; evaluation harness
- Beta: Production model integration; prompt version control; A/B testing; performance tuning
- Live: Model upgrade testing; prompt incident response; cost monitoring

**Skills**: LLM API integration; prompt design; evaluation framework development; MLOps; Python.

**Common mistake**: ML Engineers hired only for Beta who were not present in Discovery and Alpha. They arrive without the context they should have helped create.

### Evaluation Specialist

**Active in**: Alpha (full-time), Beta (part-time), Live (part-time)

**Primary responsibilities**:
- Designs the evaluation rubric in Alpha
- Creates evaluation test dataset
- Establishes baseline scores from Alpha prototype testing
- Sets up rubric-based sampling for Beta production
- Runs ongoing evaluation sampling programme in Live
- Monitors for rubric score drift and reports regressions

**Skills**: Evaluation methodology; LLM-as-judge techniques; statistical sampling; inter-rater reliability.

**Note on separation of concerns**: In smaller teams the ML Engineer and Evaluation Specialist may be the same person. The risk is motivated reasoning — the person building is also defining success. In higher-stakes services, keep these roles separate.

### AI Safety / Evaluation Lead

**Active in**: Beta (part-time), Live (part-time)

**Primary responsibilities**:
- Monitors model behaviour in production for safety and quality
- Runs or oversees rubric-based sampling programme
- Conducts bias and fairness review
- Flags regressions to Product Manager
- Owns process for escalating outputs that trigger human review

### AI/ML Systems Thinker

**Active in**: Alignment (part-time)

**Primary responsibilities**:
- Credible assessment of whether the problem is tractable for AI/agent processing
- Identifies data landscape constraints before Discovery
- Flags model vendor policy issues and infrastructure constraints

**Note**: Not a builder — a consultant to Alignment. A senior ML Engineer or AI architect from another team is often appropriate.

### MLOps / DevOps Engineer

**Active in**: Beta (full-time), Live (part-time)

**Primary responsibilities**:
- Manages model serving infrastructure
- Implements CI/CD pipelines with prompt testing and rubric evaluation
- Sets up observability stack (metrics, logs, traces)
- Manages cost monitoring and alerting
- Handles capacity planning and rate limit management

## Team Composition by Phase

| Phase | Minimum Team | AI Project Additions |
|-------|-------------|---------------------|
| Alignment | Service Owner, Product Manager, Delivery Manager | AI/ML Systems Thinker (pt) |
| Discovery | PM, User Researcher, Service Designer, Technical Lead (pt) | Data Analyst / ML Engineer (pt) |
| Alpha | PM, UX Designer/Researcher, Full-Stack Dev (1–2), QA Lead (pt) | ML Engineer (ft), Evaluation Specialist (pt) |
| Beta | PM, UX Designer, Developers (2–4), DevOps, QA, User Researcher (pt) | ML Engineer (ft), AI Safety Lead (pt), MLOps (ft) |
| Live | PM, Developer (1–2), User Researcher (pt) | ML Engineer (pt/on-call), AI Safety Lead (pt) |
