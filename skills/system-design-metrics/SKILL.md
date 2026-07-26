---
name: system-design-metrics
description: This skill should be used when the user asks to "estimate agent costs", "design latency budgets", "plan capacity", "set SLA targets", "measure throughput", or mentions cost-per-task modeling, error budgets, token economics, operational health metrics, or scalability analysis for agent systems.
---

# System Design Metrics for Agent Systems

Quantitative metrics for designing, sizing, and operating agent systems. This skill covers the non-functional requirements that determine whether an agent architecture is production-viable: latency budgets, cost modeling, reliability targets, throughput planning, and resource utilization. It complements evaluation skills (which measure output quality) by focusing on the engineering metrics that govern system economics and operational health.

## When to Activate

Activate this skill when:

- Estimating or optimizing the cost of an agent pipeline
- Designing latency budgets for agent workflows
- Setting SLA/SLO targets for agent-powered features
- Planning capacity for concurrent agent workloads
- Analyzing token economics or cost-per-task
- Choosing between model tiers based on cost/latency tradeoffs
- Building operational dashboards or alerts for agent systems
- Diagnosing throughput bottlenecks or rate-limit issues
- Sizing infrastructure for multi-agent deployments

**Do not activate** for:
- Measuring output quality, factual accuracy, or rubric-based scoring — use **evaluation**
- LLM-as-judge techniques, pairwise comparison, or bias mitigation — use **advanced-evaluation**
- Context window management or compression strategies — use **context-optimization** or **context-compression**

## Core Concepts

### Output Quality vs. System Metrics

Evaluation skills answer "how good is the output?" This skill answers "how fast, how cheap, how reliable, and how scalable is the system that produces it?" Both are necessary for production readiness; neither substitutes for the other.

### The Four Metric Families

| Family | Core Question | Key Units |
|--------|--------------|-----------|
| Latency | How fast? | ms, seconds, P50/P95/P99 |
| Cost | How expensive? | $/task, $/1K tokens, $/month |
| Reliability | How often does it work? | Success rate %, error budget remaining |
| Throughput | How much volume? | tasks/min, concurrent sessions, tokens/sec |

### Cost-Per-Task as North Star

The most actionable metric for agent economics is **cost-per-task**: the total cost of completing one end-user task, including all model calls, tool invocations, retries, and infrastructure. It collapses token costs, multi-step chains, and retry overhead into a single comparable unit.

```
cost_per_task = Σ (input_tokens × input_price + output_tokens × output_price
                   + cached_tokens × cache_price) across all calls per task
              + tool_execution_costs + infrastructure_overhead
```

## Detailed Topics

### Latency Analysis

**Latency Components in Agent Systems**

Agent latency is not a single API call. A typical task involves:

```
Total latency = TTFT₁ + generation₁ + tool_exec₁ + TTFT₂ + generation₂ + ... + TTFTₙ + generationₙ
```

- **TTFT (Time to First Token)**: Varies by model, prompt length, and provider load. Larger prompts increase TTFT due to prefill compute.
- **Generation time**: Proportional to output token count. Streaming mitigates perceived latency but not total latency.
- **Tool execution**: Network calls, database queries, or compute jobs between model turns. Often the dominant latency source.

**Serial vs. Parallel Latency Chains**

In multi-agent systems, latency depends on the orchestration pattern:
- **Serial chain**: Total = sum of all step latencies. A supervisor calling three workers sequentially pays 3× single-worker latency.
- **Parallel fan-out**: Total = max(worker latencies). Launching workers concurrently reduces wall-clock time to the slowest worker.
- **Hybrid**: Common pattern where a supervisor fans out to parallel workers, then aggregates results serially.

**Latency Budgets**

Allocate a total latency target, then partition across components:

```
User-facing SLA: T seconds
├── Orchestrator planning:     allocation_1
├── Worker A (parallel):       allocation_2
├── Worker B (parallel):       allocation_3
├── Result aggregation:        allocation_4
└── Buffer:                    allocation_5 (always reserve buffer)
```

**Percentile Thinking**

Averages hide tail latency. Track P50 (median experience), P95 (degraded experience), and P99 (worst realistic case). Agent systems exhibit high variance because tool calls and model generation lengths vary across tasks. Design for P95, alert on P99.

### Cost Modeling

**Token Cost Structure**

Model pricing has three tiers that directly affect agent economics:

| Token Type | Relative Cost | Optimization Lever |
|-----------|--------------|-------------------|
| Input (uncached) | Baseline | Reduce prompt size, remove redundant context |
| Input (cached) | Fraction of uncached | Maximize prefix cache hits via stable prefixes |
| Output | Multiple of input | Constrain output format, use structured responses |

**Cost Scaling with Context Length**

Cost grows linearly with input token count, but agent sessions accumulate context across turns. Multi-turn conversations with tool outputs grow the input significantly per request, making later turns dramatically more expensive than earlier ones.

**Cost Optimization Levers**

1. **Prefix caching**: Keep system prompts and stable context at the front of the prompt to maximize cache hits
2. **Context compression**: Summarize history before it inflates costs (see context-compression skill)
3. **Model tiering**: Use cheaper models for classification, routing, and simple extraction; reserve expensive models for reasoning
4. **Output constraints**: Structured output formats reduce output tokens vs. free-form prose
5. **Early termination**: Detect when a task is complete and stop generating

**Multi-Step Cost Accumulation**

Agent tasks compound costs across steps. A pipeline with N model calls costs roughly N× a single-call system. Multi-agent architectures multiply this further when supervisors maintain full conversation histories.

### Reliability and Error Budgets

**Success Rate Decomposition**

Agent failures have distinct root causes requiring different mitigations:

| Failure Type | Typical Rate | Mitigation |
|-------------|-------------|-----------|
| Model API errors (429, 500) | Low | Retry with exponential backoff |
| Tool execution failures | Low–moderate | Retry, fallback tools, error context |
| Malformed output (parse failures) | Low–moderate | Structured output, retry with correction |
| Incorrect reasoning | Moderate–high | Better prompts, evaluation gates, model upgrade |
| Timeout | Low | Latency budgets, circuit breakers |

**Error Budgets**

Borrowed from SRE practice: define a monthly error budget (e.g., 0.1% of tasks may fail = 99.9% target), then track consumption. When the budget is nearly exhausted, freeze deployments and prioritize reliability.

```
monthly_budget = total_expected_tasks × (1 - slo_target)
budget_remaining = monthly_budget - failures_this_month
budget_burn_rate = failures_last_hour × hours_remaining_in_month
```

**Cascade Failure in Multi-Agent Systems**

When agents depend on other agents, failures multiply. If each of N serial agents has reliability R, the pipeline's reliability is R^N (multiplicative). Mitigations: retry at each stage, circuit breakers to prevent retry storms, fallback paths that skip non-critical stages.

**Graceful Degradation**

Design systems to return partial results rather than failing completely. An agent that retrieves information from 5 sources should return what it found from 4 if one source times out, with a quality flag indicating incomplete coverage.

### Throughput and Scalability

**Rate Limit Awareness**

Model API rate limits (tokens/min, requests/min) are the primary throughput constraint for most agent systems. Track utilization against limits and implement request queuing before hitting hard limits.

**Concurrency Patterns**

- **Request-level parallelism**: Multiple independent tasks running simultaneously, each consuming its own rate-limit quota
- **Task-level parallelism**: A single task spawning parallel sub-agents (fan-out), sharing the rate-limit pool
- **Queue-based flow control**: Decouple task submission from execution to handle burst traffic without overloading

**Backpressure**

When downstream capacity is exhausted, propagate pressure upstream rather than buffering unboundedly. Strategies: reject new tasks with retry-after headers, reduce parallelism dynamically, degrade to simpler (faster) models under load.

**Scaling Dimensions**

| Dimension | Approach | When |
|-----------|----------|------|
| Horizontal | More agent instances | Independent tasks, stateless workers |
| Vertical | Larger context, more capable model | Complex tasks requiring more reasoning |
| Model tiering | Route by complexity | Mixed workloads with varying difficulty |

### Resource Utilization

**Context Window Utilization**

Track what fraction of the context window is consumed and how it breaks down:

```
utilization = total_tokens_in_context / model_max_context
breakdown:
  system_prompt:    [measured %]
  tool_definitions: [measured %]
  conversation:     [measured %]
  tool_outputs:     [measured %]
  available:        [remaining %]
```

When utilization is high, compression or context management strategies become urgent. Near-full utilization means the system is operating at the edge of failure.

**Cache Hit Rates**

For systems using prefix caching, track the ratio of cached vs. uncached input tokens. Low cache hit rates indicate prompt instability (system prompts or tool definitions changing between requests) or poor prefix ordering.

**Token Waste**

Tokens consumed that don't contribute to task completion: verbose tool outputs that get summarized anyway, repeated information across turns, tool calls that return errors. Track waste ratio and target reduction.

## Practical Guidance

### Metric Priority Framework

Not every system needs every metric. Prioritize based on system maturity:

**Phase 1 — Prototype**: Cost-per-task and success rate only. These determine viability.

**Phase 2 — Production**: Add P95 latency, throughput ceiling, and error budget tracking.

**Phase 3 — Scale**: Add resource utilization, cache hit rates, per-component cost breakdowns, and capacity planning models.

### Anti-Patterns

**Measuring averages instead of percentiles**: A low average latency can mask extreme tail latency. Always track percentiles for latency metrics.

**Ignoring cost until production**: Token costs compound fast. A cheap-seeming per-task cost multiplied by high daily volume produces significant annual spend. Model cost early.

**Vanity throughput metrics**: "Our system handles 1000 requests/minute" means nothing without specifying task complexity, quality thresholds, and error rates at that load.

**Optimizing the wrong component**: Profile before optimizing. If tool execution takes 80% of latency, optimizing prompt size for TTFT reduction is misplaced effort.

**Treating retries as free**: Each retry doubles (or more) the cost and latency of a task. High retry rates signal a design problem, not a normal operating condition.

## Examples

**Example 1: Cost-Per-Task Calculator**
```python
def calculate_cost_per_task(task_trace):
    total_cost = 0
    for call in task_trace.model_calls:
        input_cost = call.input_tokens * call.model.input_price_per_token
        cached_cost = call.cached_tokens * call.model.cached_price_per_token
        output_cost = call.output_tokens * call.model.output_price_per_token
        total_cost += input_cost + cached_cost + output_cost

    for tool_call in task_trace.tool_calls:
        total_cost += tool_call.compute_cost

    total_cost += total_cost * task_trace.retry_overhead_ratio
    return total_cost
```

**Example 2: Latency Budget for Supervisor-Worker Pattern**
```python
def check_latency_budget(task_result, budget):
    components = {
        "planning": task_result.planning_latency_ms,
        "worker_max": max(w.latency_ms for w in task_result.workers),
        "aggregation": task_result.aggregation_latency_ms,
    }
    total = sum(components.values())
    budget_remaining = budget.total_ms - total

    violations = {k: v for k, v in components.items()
                  if v > budget.component_limits[k]}

    return {
        "total_ms": total,
        "within_budget": budget_remaining >= 0,
        "component_breakdown": components,
        "violations": violations,
    }
```

**Example 3: Error Budget Tracker**
```python
def check_error_budget(slo_target, period_tasks, period_failures):
    budget_total = period_tasks * (1 - slo_target)
    budget_consumed = period_failures
    budget_remaining = budget_total - budget_consumed
    burn_rate = period_failures / max(budget_total, 1)

    return {
        "slo_target": slo_target,
        "budget_total": budget_total,
        "budget_consumed": budget_consumed,
        "budget_remaining_pct": max(0, budget_remaining / budget_total * 100),
        "burn_rate": burn_rate,
        "alert": burn_rate > 0.8,
    }
```

## Guidelines

1. Track cost-per-task from day one — it is the single most important metric for agent economics
2. Use percentiles (P50, P95, P99) for latency, never averages alone
3. Decompose end-to-end latency into per-component budgets before optimizing
4. Set explicit SLOs for success rate and latency before launching to production
5. Model cost scaling before scaling traffic — a 10× traffic increase may require model tiering to remain viable
6. Track retry rates separately from success rates — high retries inflate cost and latency even when the final success rate looks healthy
7. Monitor context window utilization and trigger compression before hitting capacity
8. Profile before optimizing — measure where time and money actually go before changing architecture
9. Design multi-agent pipelines with cascade failure math: serial reliability = product of individual reliabilities
10. Implement backpressure rather than unbounded queuing when approaching rate limits

## Gotchas

1. **Token cost surprises from long contexts**: Input costs scale linearly with token count. Agent sessions that accumulate context across many turns can silently reach expensive input sizes.
2. **Latency variance from provider queuing**: Model API latency can spike substantially during peak hours. Design for P99, not P50.
3. **Retry storms in multi-agent systems**: A supervisor retrying a failing worker, which itself retries a failing tool, creates exponential request amplification. Use per-layer retry limits and circuit breakers.
4. **Cache invalidation costs**: Changing system prompts, tool definitions, or their ordering invalidates prefix caches, causing sudden cost increases.
5. **Output token costs dominate for generative tasks**: When agents produce long-form content, output tokens (priced higher than input) become the primary cost driver, not input context.
6. **Rate limits are shared across agents**: Multiple agent instances sharing the same API key compete for the same rate-limit pool. A burst from one agent can throttle all others.

## Integration

- **evaluation** — System metrics complement output quality metrics; both are needed for production readiness
- **advanced-evaluation** — Cost and latency constraints inform evaluation pipeline design (e.g., choosing cheaper judges for high-volume evaluation)
- **context-optimization** — Compression and caching techniques directly affect cost and latency metrics
- **context-compression** — Compression strategies reduce token costs and latency at the expense of potential quality loss
- **multi-agent-patterns** — Orchestration pattern choice (serial vs. parallel, supervisor vs. peer) determines latency and reliability profiles
- **tool-design** — Tool response format and error handling affect both latency (payload size) and reliability (parse failures)
- **hosted-agents** — Infrastructure choices (warm pools, pre-built images, sandbox sizing) affect throughput and latency

## References

Internal skills:
- evaluation — Output quality measurement (complements this skill)
- context-optimization — Token efficiency techniques that reduce cost metrics
- multi-agent-patterns — Architecture patterns with distinct metric profiles

External resources:
- Google SRE Book — Error budgets, SLOs, and reliability engineering principles
- Anthropic token counting documentation — Accurate cost modeling for Claude models
- OpenAI rate limits documentation — Rate limit management patterns

---

## Skill Metadata

**Created**: 2026-07-26
**Last Updated**: 2026-07-26
**Author**: Agent Skills for Context Engineering Contributors
**Version**: 1.0.0
