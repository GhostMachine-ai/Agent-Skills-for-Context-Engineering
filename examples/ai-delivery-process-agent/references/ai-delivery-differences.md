# Why AI Delivery Is Different

Four fundamental differences that change how AI projects should be run compared to standard digital delivery.

## 1. Non-determinism as a Design Constraint

Standard software: a given input produces a deterministic output. Testing is binary: pass or fail.

AI systems: the same input may produce different outputs on different runs. Testing must be statistical:

- Quality gates are score thresholds, not pass/fail assertions
- Regression detection requires statistical comparison of score distributions, not exact output matching
- Production monitoring must track score distributions over time, not just error rates

**Delivery implication**: Binary acceptance criteria ("it works") are replaced by rubric-based thresholds ("it scores ≥ 3.5/5"). The evaluation rubric must be designed before the system is built.

## 2. Evaluation-Driven Development

Standard software: "does it work?" is answered by unit tests and functional tests.

AI systems: "does it work?" is answered by measuring behaviour against a rubric on a representative dataset.

- The rubric defines what "good" means for this task
- A test dataset represents the distribution of real inputs
- Baseline scores are established before automation (manual prototype)
- Alpha exit requires meeting a rubric threshold, not passing unit tests

**Delivery implication**: The evaluation rubric is an Alpha output, not a Beta output. Defining success criteria after the build begins optimises for the wrong outcome.

## 3. Model as Dependency

Standard software dependencies: libraries, APIs, databases. These change on a schedule you largely control.

AI model dependencies: model providers update, deprecate, and change pricing on their own schedules, with varying notice periods. A model that performs at 3.8/5 today may perform at 3.4/5 after an unannounced provider update.

**Delivery implication**: Three artefacts are required that have no standard-software equivalent:
- **Model deprecation plan**: What do we do when the provider deprecates our model version?
- **Prompt version history**: Every prompt change is a deployment; every deployment is tracked with before/after scores.
- **Drift detection**: Automated comparison of current score distribution vs. historical baseline.

## 4. Human-in-the-Loop Design

Standard software: human oversight of outputs is a business process concern, not a product design concern.

AI systems: which outputs require human review before reaching a user is a user research question, a design requirement, a build requirement, and a monitoring concern. The answer must be grounded in:

- The consequence of an incorrect AI output
- The reversibility of acting on an incorrect AI output
- User expectations and trust (a user research finding, not a design assumption)
- Regulatory and accountability requirements

**Delivery implication**: The Human-in-the-Loop Map is a Discovery artefact (drafted from user research) and an Alpha artefact (validated with users). It is a product design document, not an engineering afterthought.

---

## Summary Table

| Aspect | Standard Delivery | AI Delivery |
|--------|------------------|-------------|
| Testing | Deterministic pass/fail | Statistical rubric scoring |
| Success definition | Functional acceptance criteria | Rubric threshold on evaluation dataset |
| Quality gate | Unit tests + UAT | Rubric score ≥ threshold at Alpha gate |
| Dependency management | Library/API versioning | Model versioning + deprecation plan |
| Output change management | Code release | Prompt versioning + staged rollout |
| Production monitoring | Error rates + latency | Error rates + latency + rubric score + cost-per-interaction |
| Human oversight | Business process concern | Product design concern (HITL Map) |
