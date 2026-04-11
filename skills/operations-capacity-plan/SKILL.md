---
name: operations-capacity-plan
description: This skill should be used when planning compute and context capacity for AI agent systems, estimating token budgets, forecasting API costs, sizing warm agent pools, setting throughput targets, designing SLAs for production agent deployments, or analyzing rate limits and concurrency constraints. Activate when a user asks to "plan capacity", "estimate costs", "size my agent fleet", "set throughput targets", "design SLAs", or mentions running out of tokens, hitting rate limits, or scaling an agent system.
---

# Operations Capacity Planning for AI Agent Systems

Capacity planning for AI agent systems differs fundamentally from traditional software capacity planning. The key resource is not CPU or memory alone — it is **context window tokens**, **API throughput**, and **concurrency slots**. A well-formed capacity plan translates business requirements (tasks per day, response latency, cost per task) into concrete resource allocations and operational guardrails.

Capacity planning is not a one-time exercise. It is a continuous loop: measure baselines, model growth, allocate budgets, observe actuals, and recalibrate.

## When to Activate

Activate this skill when:

- Designing a new production agent deployment and need to set resource budgets upfront
- Hitting API rate limits or context overflows in an existing system and need to diagnose root cause
- Forecasting monthly API costs before a system scales or before a business commitment
- Sizing warm agent pools (sandbox pre-warm counts, concurrency slots) for a hosted agent infrastructure
- Writing SLAs or SLOs that include latency, throughput, or error-rate guarantees
- Planning capacity for multi-agent systems where parent and sub-agents share rate limits
- Estimating how much headroom to maintain before triggering context optimization

## Core Concepts

**Token economy model**: Every agent task consumes tokens across four buckets — system prompt, tool definitions, conversation history, and output generation. Planning starts by profiling these buckets for a representative task sample, not averages across all tasks.

**Throughput ceiling**: The maximum sustainable task rate is determined by the binding constraint: tokens-per-minute limit, requests-per-minute limit, or concurrency slot count. Identify which constraint binds first; optimizing non-binding constraints yields no improvement.

**Concurrency vs. latency tradeoff**: Higher concurrency increases throughput but adds queuing delay. The goal is to find the concurrency level that saturates the API limit without causing queue buildup that violates latency SLOs.

**Cost-per-task decomposition**: Total cost per task = (input tokens × input price) + (output tokens × output price) − (cache-hit tokens × cache discount). Cache hit rate is the single largest lever for cost reduction in stable workloads.

**Headroom principle**: Always plan to operate at 70-80% of theoretical limits. The remaining 20-30% absorbs burst traffic, model output variability, and unexpected prompt growth.

## Detailed Topics

### Context Window Budget Planning

Every agent task has a context window budget defined by the model's maximum context length. Allocate this budget explicitly across four regions:

| Region | Typical Allocation | Notes |
|--------|-------------------|-------|
| System prompt + tools | 10-20% | Fixed per deployment; optimize once |
| Conversation history | 20-40% | Grows with turns; trigger compaction at 70% |
| Retrieved / injected content | 20-30% | Variable; compress before injection |
| Output generation buffer | 15-25% | Reserve based on max expected output length |

Profile 50-100 representative tasks to establish P50 and P95 token counts per region. Set the compaction trigger at 70% of the model's context limit to preserve a safety margin.

When P95 input tokens exceed 80% of the context limit, the system is under context pressure. Apply context-optimization techniques (compaction, masking, partitioning) before scaling horizontally.

### API Rate Limit and Throughput Ceiling

API providers enforce limits on two dimensions simultaneously:

- **Requests per minute (RPM)**: Number of API calls regardless of size
- **Tokens per minute (TPM)**: Total tokens consumed across all calls

The effective throughput ceiling is:

```
max_tasks_per_minute = min(RPM / calls_per_task, TPM / tokens_per_task_p95)
```

Use P95 token counts (not averages) to avoid underestimating load. A single P99 task consuming 5× the average can exhaust the TPM budget for an entire minute.

For multi-agent systems, the orchestrator and all sub-agents share the same rate limit pool. Budget as a unified system, not per-agent.

**Rate limit headroom rule**: Target 70% utilization of the binding limit. At 80%+ sustained utilization, burst traffic will cause throttling.

### Cost Modeling

Cost per task follows this formula:

```
cost_per_task = (input_tokens_p50 × input_price_per_token)
              + (output_tokens_p50 × output_price_per_token)
              - (cached_input_tokens × cache_discount_per_token)
```

Key inputs to measure:
- **Input token P50 and P95**: Profile across representative task types
- **Output token P50 and P95**: Profile outputs; highly variable across task types
- **Cache hit rate**: For stable system prompts and tool definitions, expect 60-80% cache hits after warm-up

Monthly cost projection:

```
monthly_cost = cost_per_task × tasks_per_day × 30
             + fixed_infra_costs (sandboxes, warm pools, storage)
```

Include a 20% buffer for cost overruns during peak periods or prompt growth from feature additions.

### Warm Pool Sizing

Hosted agent systems that pre-warm sandbox environments incur fixed costs proportional to pool size. Size the warm pool using:

```
pool_size = ceil(peak_concurrent_tasks × (1 + burst_headroom))
burst_headroom = 0.25  # 25% above expected peak
```

Cold-start penalty (time to provision a new sandbox) defines the maximum acceptable task queue depth before user-facing latency degrades. If cold-start takes 10 seconds and the SLO allows 15 seconds of queue wait, the pool must be replenished before queue depth exceeds 1.5× concurrency slots.

Scale the warm pool proactively, not reactively. Monitor queue depth; trigger pool expansion when queue depth exceeds 50% of pool size for more than 60 seconds.

### SLA and SLO Design

Define SLOs across three dimensions:

**Latency**:
- P50 (median) task completion time
- P95 task completion time (primary SLO target)
- P99 task completion time (alerting threshold)

**Throughput**:
- Sustained tasks per hour under normal load
- Peak tasks per hour during burst

**Reliability**:
- Error rate (% of tasks ending in unrecoverable failure)
- Throttle rate (% of tasks delayed by rate limits)

Error budget = (1 − reliability_target) × time_window. Spend error budget on planned changes; halt changes when budget is exhausted.

Set alerting thresholds at 80% of SLO breach to allow time for remediation before users are affected.

### Capacity Forecasting

Forecast growth using a three-horizon model:

| Horizon | Method | Confidence |
|---------|--------|------------|
| 30 days | Linear extrapolation from current trend | High |
| 90 days | Trend + planned feature launches | Medium |
| 12 months | Scenario planning (low/base/high) | Low |

Identify growth drivers: new users, new task types, increased task complexity (more turns, longer outputs), or new sub-agent deployments. Each driver has a different token multiplier.

Trigger a capacity review when any of these thresholds are crossed:
- Sustained API utilization > 70% of TPM limit for 7+ days
- Monthly cost growth > 20% month-over-month for 2+ consecutive months
- P95 task latency growth > 15% over 30 days

## Practical Guidance

### Phase I Capacity Plan Checklist

Use this checklist when producing an initial capacity plan for a new or existing system:

1. **Baseline measurement**
   - Profile 100+ representative tasks for input and output token counts
   - Record P50, P95, and P99 values per task type
   - Measure current API utilization (RPM and TPM) if system is live

2. **Constraint identification**
   - Calculate throughput ceiling for RPM and TPM separately
   - Identify which limit binds first at current and projected load
   - Check concurrency slot limits if using hosted agents

3. **Budget allocation**
   - Assign token budgets per context region (system prompt, history, content, output)
   - Set compaction trigger threshold (recommended: 70% of context limit)
   - Calculate cost-per-task at P50 and P95

4. **Growth projection**
   - Project 30-day and 90-day task volume growth
   - Calculate when current limits will be exhausted at projected growth rate
   - Identify the next rate-limit tier to request from the API provider

5. **SLO definition**
   - Set P95 latency target based on user-facing requirements
   - Set reliability target (recommended: 99.5% for production)
   - Calculate error budget

6. **Operational guardrails**
   - Set alerting thresholds at 80% of each SLO
   - Define runbooks for: context overflow, rate limit exhaustion, cold-start surge
   - Schedule next capacity review (recommended: monthly)

### Scaling vs. Optimizing Decision

When approaching a limit, choose between scaling (higher API tier) and optimizing (use existing capacity more efficiently):

- **Optimize first** if cache hit rate < 60%, context utilization is dominated by retrievals, or output tokens are highly variable (optimization via better prompting)
- **Scale** if utilization is uniformly high across all task types, cache hit rate is already > 70%, and optimization has been applied

Optimization is always cheaper short-term; scaling has no ceiling but grows cost linearly with load.

## Examples

**Example: 100-task/day agent deployment**

Baseline measurements:
- Input tokens P50: 8,000 / P95: 22,000
- Output tokens P50: 1,200 / P95: 3,500
- Cache hit rate: 65% (system prompt + tools cached)
- API tier: 60,000 TPM / 500 RPM

Throughput ceiling:
```
RPM constraint:  500 RPM / 1 call/task = 500 tasks/min = 720,000 tasks/day
TPM constraint:  60,000 TPM / 22,000 tokens (P95) = 2.7 tasks/min = 3,888 tasks/day
```
TPM is the binding constraint. At 100 tasks/day (0.07 tasks/min), current capacity provides 39× headroom — well within budget.

Cost per task (at P50):
```
Input:  8,000 × 0.35% cache miss × $3/M  = $0.0084
Cached: 8,000 × 65% cache hit × $0.30/M  = $0.00156
Output: 1,200 × $15/M                     = $0.018
Total:  ~$0.028 per task
Monthly (100 tasks/day × 30): ~$84/month
```

**Example: Warm pool sizing for 10 concurrent tasks**

```
pool_size = ceil(10 × 1.25) = 13 sandboxes
cold_start_penalty = 12 seconds
P95 latency SLO = 30 seconds
max_queue_depth_before_breach = (30 - 12) / average_task_time = depends on task
```

## Guidelines

1. Profile real task traffic — never plan from token averages alone; use P95 values for limit calculations
2. Identify the binding constraint before optimizing — TPM, RPM, and concurrency each require different remediation
3. Reserve 20-30% headroom on all limits to absorb burst traffic and prompt growth
4. Set context compaction triggers at 70% of the context window limit, not at the limit itself
5. Cache hit rate is the primary cost lever — invest in stable system prompt and tool definition ordering
6. Define SLOs before launch, not after the first incident
7. Forecast 90 days ahead and trigger a rate-limit tier upgrade request when projected to hit 80% of the binding limit within 45 days
8. Revisit the capacity plan after every significant feature launch or traffic step-change

## Integration

This skill connects to the following skills in the collection:

- context-optimization — Apply compaction, masking, and partitioning when context budgets are under pressure
- hosted-agents — Warm pool sizing, sandbox lifecycle, and concurrency slot management
- evaluation — Measure baseline task performance metrics that feed into capacity calculations
- project-development — Embed capacity planning into the production pipeline design phase

## References

Internal reference:
- [Capacity Planning Guide](./references/capacity-planning-guide.md) — Detailed formulas, forecasting models, and runbook templates

Related skills in this collection:
- context-optimization — Token budget management and compaction strategies
- hosted-agents — Infrastructure sizing for sandboxed agent deployments
- evaluation — Measurement frameworks for establishing baselines

---

## Skill Metadata

**Created**: 2026-04-11
**Last Updated**: 2026-04-11
**Author**: Agent Skills for Context Engineering Contributors
**Version**: 1.0.0
