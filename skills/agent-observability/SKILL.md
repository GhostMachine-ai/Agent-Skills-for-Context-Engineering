---
name: agent-observability
description: "This skill should be used when the user asks to monitor agent in production, debug agent failures, trace agent decisions, detect prompt drift, set up agent logging, measure agent performance over time, track LLM costs, or mentions agent tracing, model drift, prompt regression, production agent monitoring, token cost tracking, or agent alerting. Provides the full observability stack for production AI agent systems."
---

# Agent Observability

## When to Activate

Activate this skill when:

- Setting up production monitoring for a deployed AI agent or LLM-powered service
- Debugging unexpected agent behaviour in a live environment
- Detecting or investigating model drift, prompt regression, or data drift
- Building alerting and alerting thresholds for agent failure modes
- Implementing cost tracking for a production agent workload
- Establishing the observability infrastructure as part of the Beta delivery phase

Do not activate for: evaluation rubric design (use `evaluation`), prompt engineering methodology (use `context-optimization`), general agent architecture decisions (use `multi-agent-patterns`), or delivery process planning (use `ai-delivery-process`).

## Core Concepts

**The observability triad, applied to agents**:
- **Metrics**: numeric measurements over time — latency, cost, rubric scores, error rates
- **Logs**: structured records of individual agent runs — prompt trace, tool call sequence, output sample
- **Traces**: full request-response chains including sub-agent calls, tool invocations, and timing per step

Three agent-specific concerns make traditional observability insufficient:

1. **Non-determinism**: the same input can produce different outputs. Anomaly detection requires statistical baselines, not exact thresholds.
2. **Prompt changes are deployments**: a change to a system prompt significantly alters model behaviour but leaves no artifact in standard deployment pipelines unless explicitly tracked.
3. **Model upgrades are silent breaking changes**: when a provider updates a model, prompts and evaluation scores may change without any action by the service team.

**Three observability failure modes unique to AI**:
- **Invisible failures**: the agent completes and returns a response, but the response is wrong. Only rubric-based sampling detects this.
- **Silent degradation**: quality decreases gradually below any single-point alert threshold. Only trend monitoring with statistical baselines detects this.
- **Cost explosions**: token usage spikes due to a prompt change or usage pattern shift. Only per-interaction cost monitoring with alerting detects this.

## Metric Taxonomy

### Latency

| Metric | Description | Alert |
|--------|-------------|-------|
| Time-to-first-token (TTFT) | Latency from request to first token | P95 > 2× baseline |
| Total latency | Full request-to-response time | P95 > 2× baseline for 10 min |
| Per-tool-call latency | Time per tool invocation | Any tool P95 > 5 seconds |

### Cost

| Metric | Description | Alert |
|--------|-------------|-------|
| Tokens in (per request) | Input tokens consumed | Component of cost calculation |
| Tokens out (per request) | Output tokens generated | Component of cost calculation |
| Cost per interaction | USD per complete agent turn | > 3× rolling 7-day avg |
| Cost per session | Cumulative cost for a multi-turn session | > 5× avg session cost |
| Daily cost total | Sum across all requests | > 150% of budget allocation |

### Quality

| Metric | Description | Alert |
|--------|-------------|-------|
| Rubric composite score (sampled) | Evaluation rubric score for a production sample | 7-day rolling avg drops > 0.3 from baseline |
| Human override rate | Rate at which humans override AI outputs | Week-over-week increase > 20% |
| Correction rate | Rate at which users edit or retry AI outputs | Week-over-week increase > 20% |

### Reliability

| Metric | Description | Alert |
|--------|-------------|-------|
| Error rate | Fraction of requests resulting in an error | > 2% over 15-minute window |
| Retry rate | Fraction of requests requiring a retry | > 10% (indicates rate limit pressure) |
| Tool call failure rate | Fraction of tool calls resulting in an error | > 5% over 15-minute window |

## Trace Design

A useful agent trace contains:

```json
{
  "trace_id": "...",
  "session_id": "...",
  "user_id_hash": "...",
  "timestamp": "...",
  "model": "...",
  "model_version": "...",
  "prompt_version": "...",
  "input_tokens": 1240,
  "output_tokens": 387,
  "cost_usd": 0.0041,
  "latency_ms": 2340,
  "ttft_ms": 480,
  "tool_calls": [
    {"tool": "web_search", "latency_ms": 890, "success": true}
  ],
  "rubric_score": null,
  "sampled_for_eval": false
}
```

**Never log raw user inputs that may contain PII.** Hash user identifiers. Treat logged content as sensitive data with restricted access and retention limits.

## Drift Detection

Three types of drift affect AI agents in production:

**Model Drift**: Same prompt, different model weights → different output distribution. Caused by provider updating a model version without changing the name.
- Detection: Compare rubric scores before and after a known model change; alert if composite score drops > 0.3 points.

**Prompt Drift**: Prompt changes over time degrade quality relative to the baseline.
- Detection: Compare current rubric scores against the Alpha baseline; alert on sustained 7-day rolling average decline > 0.2 points.

**Data Drift**: Content the agent retrieves or processes changes in character.
- Detection: Monitor input token distribution, query length distribution, and tool call rates; periodic re-evaluation against a stable golden test set.

## Sampling Strategy

| Phase | Evaluation Sampling Rate | Trigger for Full Trace |
|-------|--------------------------|----------------------|
| Alpha | 100% | N/A |
| Beta (early) | 20–30% | Any error or anomaly |
| Beta (stable) | 5–10% | Error, cost spike, or user complaint |
| Live | 2–5% | Error, cost spike, rubric drop alert, user complaint |

Always collect full traces for: any error, any cost > N× rolling average, any content safety flag, any explicit negative user feedback.

## Alerting Thresholds

| Metric | Alert Condition | Severity |
|--------|-----------------|---------|
| Rubric score (7-day rolling) | Drop > 0.3 from baseline | High |
| Error rate | > 2% over 15-minute window | High |
| P95 latency | > 2× baseline for 10 minutes | Medium |
| Cost per interaction | > 3× rolling 7-day average | High |
| Tool call failure rate | > 5% over 15-minute window | Medium |
| Rubric score (single day) | Drop > 0.5 from baseline | Critical |

## Prompt Versioning

Every system prompt in production must have:
1. A semantic version (major.minor.patch)
2. A changelog entry with what changed, why, and rubric scores before and after
3. A staged rollout (5–10% of traffic first; monitor 24–48 hours; then expand)

Treat prompt changes as code changes — same review, testing, and deployment pipeline.

## Practical Guidance

**Start logging from the first prototype in Alpha**: retroactively adding observability is painful. Establish the logging structure in Alpha even if only used for debugging.

**Establish baseline metrics in Alpha**: you cannot detect drift without a baseline. Alpha evaluation rubric scores are the initial baseline.

**Never alert on a single wrong output**: alert on statistical patterns over time windows, not individual outputs.

**Build a golden set of 20–50 representative inputs in Alpha**: re-run after every model or prompt change for a fast sanity check before full production monitoring catches a regression.

## Integration

This skill integrates with:
- `evaluation` — evaluation rubrics define which metrics matter and what scores mean
- `ai-delivery-process` — observability requirements belong in the Beta checklist; Live monitoring is part of the Live phase gate
- `context-optimization` — token cost monitoring informs context engineering decisions
- `hosted-agents` — sandboxed agent infrastructure must expose observability hooks

## References

- [Metric Taxonomy Reference](./references/metric-taxonomy.md)
- [Prompt Versioning Patterns Reference](./references/prompt-versioning-patterns.md)
- [Drift Detection Script](./scripts/drift_detector.py)
- Related skills: evaluation, ai-delivery-process, context-optimization

## Skill Metadata

- Created: 2026-07-09
- Last Updated: 2026-07-09
- Author: Agent Skills for Context Engineering Contributors
- Version: 1.0.0
