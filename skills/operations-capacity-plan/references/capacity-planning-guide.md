# Capacity Planning Guide — Detailed Reference

This reference provides formulas, worked examples, forecasting models, and runbook templates to complement the `operations-capacity-plan` skill.

---

## 1. Token Profiling Methodology

### Sampling Strategy

Profile tasks using stratified sampling across task types, not random sampling from the full task stream. Different task types can vary by 10-50× in token consumption.

**Minimum sample per type**: 50 tasks for P95 stability; 200 tasks for P99 stability.

**Recommended profiling instrumentation**:

```python
import anthropic

def profile_task(client, messages, system, tools):
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        system=system,
        tools=tools,
        messages=messages
    )
    return {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_read_tokens": getattr(response.usage, "cache_read_input_tokens", 0),
        "cache_write_tokens": getattr(response.usage, "cache_creation_input_tokens", 0),
    }
```

### Percentile Calculation

```python
import numpy as np

def compute_percentiles(samples: list[int]) -> dict:
    return {
        "p50": int(np.percentile(samples, 50)),
        "p75": int(np.percentile(samples, 75)),
        "p95": int(np.percentile(samples, 95)),
        "p99": int(np.percentile(samples, 99)),
        "max": max(samples),
    }
```

Use **P95** values for limit-based calculations (rate limits, context limits). Use **P50** values for cost projections.

---

## 2. Throughput Ceiling Formulas

### Single-Agent System

```
RPM_ceiling     = provider_RPM_limit / api_calls_per_task
TPM_ceiling     = provider_TPM_limit / task_input_tokens_p95
concurrency_max = provider_concurrency_limit  (if applicable)

throughput_ceiling = min(RPM_ceiling, TPM_ceiling, concurrency_max)
```

### Multi-Agent System (Orchestrator + Sub-agents)

All agents share the same rate limit pool. Calculate total token consumption per orchestrated workflow:

```
workflow_tokens_p95 = orchestrator_tokens_p95
                    + sum(subagent_i_tokens_p95 × subagent_i_calls_per_workflow)

TPM_ceiling = provider_TPM_limit / workflow_tokens_p95
```

Sub-agents that run in parallel consume TPM concurrently. Sub-agents that run serially consume TPM sequentially. Model accordingly.

### Effective Throughput with Retry Logic

Retries amplify token and request consumption. If the retry rate is R% and each retry consumes the same tokens:

```
effective_tokens_per_task = task_tokens_p50 × (1 + retry_rate)
effective_calls_per_task  = 1 + retry_rate
```

Cap retry attempts and use exponential backoff to prevent cascading rate limit exhaustion.

---

## 3. Cost Modeling

### Per-Task Cost Formula

```
cost_per_task =
    (non_cached_input_tokens × input_price)
  + (cache_write_tokens × cache_write_price)
  + (cache_read_tokens × cache_read_price)
  + (output_tokens × output_price)
```

**Reference pricing** (verify current pricing with your provider):

| Token Type | Approximate Price Range |
|-----------|------------------------|
| Input (non-cached) | $1–$15 per million tokens |
| Cache write | $1.25–$18.75 per million tokens |
| Cache read | $0.10–$1.50 per million tokens |
| Output | $5–$75 per million tokens |

### Cache Hit Rate Modeling

Cache hit rate depends on the stability of the prompt prefix. For a system with a fixed system prompt and tools definition:

```
cache_hit_rate ≈ (system_prompt_tokens + tools_tokens) / total_input_tokens
```

Cache hits only apply to **identical** prefixes. Any change to the system prompt or tool definitions resets the cache for that prefix.

Strategies to maximize cache hit rate:
1. Place static content (system prompt, tool definitions, few-shot examples) at the top of the prompt
2. Place dynamic content (user message, retrieved docs) at the bottom
3. Keep the static prefix as long as possible — more cached tokens = more savings

### Monthly Cost Projection Worksheet

```
daily_tasks           = [measured or projected]
cost_per_task_p50     = [calculated above]
monthly_tasks         = daily_tasks × 30
base_monthly_cost     = monthly_tasks × cost_per_task_p50
burst_buffer          = base_monthly_cost × 0.20     # 20% burst allowance
infra_costs           = warm_pool_count × sandbox_cost_per_hour × 720
total_monthly_budget  = base_monthly_cost + burst_buffer + infra_costs
```

---

## 4. Warm Pool Sizing

### Sizing Formula

```
peak_concurrent_tasks = [measured P95 concurrent tasks during peak hour]
burst_headroom        = 0.25   # 25% above peak
pool_size             = ceil(peak_concurrent_tasks × (1 + burst_headroom))
```

### Queue Depth Alert Threshold

```
cold_start_seconds    = [measured sandbox initialization time]
p95_latency_slo       = [latency SLO in seconds]
max_queue_wait        = p95_latency_slo - cold_start_seconds - p95_task_runtime

# If queue wait > max_queue_wait, SLO is at risk
alert_queue_depth     = ceil(max_queue_wait / avg_task_runtime × concurrency)
```

Trigger pool scale-out when queue depth exceeds `alert_queue_depth` for more than 60 seconds.

### Pool Scale-In Policy

Scale the pool down conservatively. Use a 15-minute trailing average of concurrent task count before releasing sandboxes. Premature scale-in causes cold-start penalty spikes.

```
scale_in_threshold    = pool_size × 0.40   # below 40% utilization
scale_in_delay        = 15 minutes         # sustained below threshold
```

---

## 5. SLA / SLO Templates

### Standard SLO Set for a Production Agent System

```yaml
slos:
  task_latency:
    p50_seconds: 8
    p95_seconds: 30
    p99_seconds: 90
    measurement_window: 5m rolling

  throughput:
    sustained_tasks_per_hour: 500
    peak_tasks_per_hour: 1000       # max 15-minute burst

  reliability:
    success_rate_target: 0.995      # 99.5%
    error_budget_per_month: 0.005 × (30 × 24 × 60) = 216 minutes

  rate_limit_compliance:
    throttle_rate_target: < 0.01    # < 1% of tasks throttled
```

### Error Budget Burn Rate Alerts

Alert when the error budget is being consumed faster than allowed:

```
burn_rate_1h  > 14.4   → page immediately (1h burn exhausts 30d budget)
burn_rate_6h  > 6.0    → urgent alert
burn_rate_24h > 3.0    → warning
burn_rate_72h > 1.0    → informational
```

---

## 6. Capacity Forecasting Models

### 30-Day Linear Extrapolation

```python
import numpy as np

def forecast_30d(daily_task_counts: list[int]) -> dict:
    """Fit linear trend to last 14 days, project 30 days forward."""
    x = np.arange(len(daily_task_counts))
    coeffs = np.polyfit(x, daily_task_counts, deg=1)
    slope, intercept = coeffs

    forecast = []
    for day in range(1, 31):
        projected = slope * (len(daily_task_counts) + day) + intercept
        forecast.append(max(0, projected))

    return {
        "day_30_tasks": round(forecast[-1]),
        "daily_growth_rate": slope,
        "forecast": forecast,
    }
```

### 90-Day Scenario Planning

Define three growth scenarios:

| Scenario | Monthly Growth Rate | Use Case |
|----------|-------------------|----------|
| Conservative | +10%/month | Steady organic growth |
| Base | +25%/month | Planned feature launches |
| Aggressive | +50%/month | Viral growth or large partnership |

```python
def scenario_projection(current_daily: float, months: int = 3) -> dict:
    scenarios = {"conservative": 0.10, "base": 0.25, "aggressive": 0.50}
    results = {}
    for name, monthly_rate in scenarios.items():
        projected = current_daily * ((1 + monthly_rate) ** months)
        results[name] = round(projected)
    return results
```

### Rate Limit Exhaustion Timeline

```python
def days_until_limit(current_tpm_utilization: float,
                     tpm_limit: float,
                     daily_growth_rate: float) -> int:
    """Return days until utilization hits 80% of TPM limit."""
    target = tpm_limit * 0.80
    if current_tpm_utilization >= target:
        return 0
    day = 0
    utilization = current_tpm_utilization
    while utilization < target:
        utilization *= (1 + daily_growth_rate)
        day += 1
        if day > 365:
            return -1  # won't hit limit within a year
    return day
```

---

## 7. Operational Runbooks

### Runbook: Context Window Overflow

**Trigger**: Task failure with error `context_length_exceeded` or token count approaching model limit.

**Immediate action**:
1. Check which context region is overflowing (use token profiling on recent failed tasks)
2. If history is the cause: lower compaction trigger from 70% to 60%
3. If retrieved content is the cause: reduce retrieval chunk size by 30%
4. If system prompt is the cause: audit for token bloat (verbose tool descriptions, redundant instructions)

**Root cause analysis**:
- Profile the last 50 failed tasks — identify common patterns (task type, session length, retrieval volume)
- If P95 input tokens grew >20% in the last 7 days: prompt or retrieval content may have changed

**Prevention**:
- Add monitoring for P95 context utilization per task type
- Alert when P95 exceeds 75% of the context limit

---

### Runbook: Rate Limit Exhaustion

**Trigger**: HTTP 429 responses from API provider, `rate_limit_error` in logs.

**Immediate action**:
1. Check whether RPM or TPM is exhausted (provider error message typically specifies)
2. If TPM: reduce concurrency by 25% immediately; enable request queuing with exponential backoff
3. If RPM: batch tool calls, reduce polling frequency, coalesce sub-agent invocations

**Medium-term**:
- Request higher rate limit tier from provider (typically requires 3-5 business days)
- Apply context-optimization to reduce tokens per task (see context-optimization skill)
- Implement token-aware request scheduler to smooth TPM usage across the minute window

**Prevention**:
- Alert at 70% sustained TPM utilization
- Review rate limit tier every 30 days against projected growth

---

### Runbook: Cost Spike

**Trigger**: Daily API cost exceeds budget threshold by >20%.

**Diagnosis**:
1. Compare today's input vs. output token breakdown to the 7-day average
2. Check cache hit rate — a drop in cache hit rate directly multiplies input cost
3. Check for new task types with higher token counts
4. Check for retry amplification (elevated error rate → retries → more tokens)

**Remediation**:
1. If cache hit rate dropped: investigate recent system prompt changes; restore stable prefix ordering
2. If output tokens spiked: add `max_tokens` cap appropriate for task type
3. If retries amplified: fix the root cause of errors before addressing cost

---

## 8. Capacity Review Checklist (Monthly)

Run this checklist every 30 days:

- [ ] Pull P50 and P95 token counts for each task type; compare to last month
- [ ] Calculate current TPM and RPM utilization as % of limit
- [ ] Compute days until 80% limit at current growth rate
- [ ] Review cache hit rate; identify opportunities to improve prefix stability
- [ ] Check warm pool utilization; adjust pool size if consistently above 80% or below 40%
- [ ] Review P95 task latency trend; flag if growing >5% month-over-month
- [ ] Review error budget burn rate for the past 30 days
- [ ] Update 90-day cost forecast with current actuals
- [ ] Identify top 3 optimization opportunities for next month

---

*This reference is maintained alongside the `operations-capacity-plan` skill. Submit improvements via the repository contribution guidelines.*
