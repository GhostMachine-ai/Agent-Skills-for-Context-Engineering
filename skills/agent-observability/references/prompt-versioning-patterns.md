# Prompt Versioning Patterns Reference

Practical patterns for versioning, managing, and rolling back prompts in production AI agent systems.

## Why Prompt Versioning Matters

A prompt change in production changes the behaviour of every subsequent model call. Unlike a code change, a prompt change:
- Leaves no artifact in a standard deployment pipeline unless explicitly tracked
- Cannot be detected by static analysis
- May have no visible effect on metrics immediately, with degradation only detectable after days of sampling
- Is often made by non-engineers who may not have access to deployment tooling

Without prompt versioning, teams cannot answer: "When did the agent start behaving differently?" or "Which prompt change caused this regression?"

## Version Numbering Convention

Use semantic versioning: `v{major}.{minor}.{patch}`

| Increment | When to use |
|-----------|------------|
| Major | Structural change: sections added/removed, overall intent changed |
| Minor | Significant rewording; change to instructions or constraints |
| Patch | Small corrections, typos, minor clarifications |

Include the prompt version in every trace — this is the single most important metadata field for diagnosing quality regressions.

## Storage Pattern: Git-Versioned Prompt Files

```
prompts/
├── system-prompt.md        # Current production prompt
├── CHANGELOG.md            # Human-readable change log
└── archive/
    ├── v1.0.0-system-prompt.md
    └── v1.1.0-system-prompt.md
```

**CHANGELOG.md format**:
```markdown
## v1.3.0 — 2026-07-09
**Changed**: Added explicit instruction to cite sources for factual claims.
**Reason**: Rubric score for Groundedness was 3.1 vs. target of 4.0.
**Score before**: Composite 3.8, Groundedness 3.1
**Score after**: Composite 4.1, Groundedness 4.2
**Rollout**: 10% traffic from 2026-07-09, 100% from 2026-07-11
```

## Staged Rollout Pattern

Never switch 100% of production traffic to a new prompt version without staged rollout:

```
Stage 1: 5% of traffic — monitor 24 hours
  → If metrics within range: proceed
  → If any metric deteriorates: rollback immediately

Stage 2: 25% of traffic — monitor 48 hours
Stage 3: 100% of traffic — monitor 7 days; pin as new baseline
```

**Rollout decision criteria**:
- Error rate does not increase by more than 0.5%
- P95 latency does not increase by more than 20%
- Rubric scores do not decrease by more than 0.2 points on any dimension

## Rollback Playbook

1. Alert fires (rubric drop or error spike)
2. Identify the prompt version change in recent traces
3. Rollback decision < 30 minutes: flip production to previous stable version
4. Confirm recovery: monitor metrics for 1 hour post-rollback
5. Post-mortem: document what changed, why it regressed, what will be done differently

## Testing a New Prompt Version Before Rollout

1. Run against golden test set (20–50 representative inputs from Alpha)
2. Score outputs using evaluation rubric; compare against baseline
3. Flag any dimension where score drops > 0.2 from production baseline
4. Human spot-check a random sample before staged rollout
5. Document before/after scores in CHANGELOG before releasing
