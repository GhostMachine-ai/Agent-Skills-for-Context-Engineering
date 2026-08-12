# Agent Observability: Metric Taxonomy Reference

A complete reference for metrics that should be collected from a production AI agent system.

## 1. Latency

Collected at the client wrapper level (wrap the model API call).

| Metric | Unit | How to Collect | Alert |
|--------|------|---------------|-------|
| Time-to-first-token (TTFT) | ms | Timestamp at first streaming chunk vs. request sent | P95 TTFT > 2× baseline |
| Total generation latency | ms | Timestamp at last chunk vs. request sent | P95 > 2× baseline for 10 min |
| Full request latency | ms | Timestamp at response delivered vs. request received | P95 > SLA for 10 min |
| Per-tool-call latency | ms | Wrap tool execution; timestamp before and after | Any tool P95 > 5 seconds |

**Collection pattern (pseudocode)**:
```python
start = time.time()
first_chunk_time = None

for chunk in model.stream(prompt):
    if first_chunk_time is None:
        first_chunk_time = time.time()
    yield chunk

end = time.time()
metrics.record("ttft_ms", (first_chunk_time - start) * 1000)
metrics.record("request_latency_ms", (end - start) * 1000)
```

## 2. Cost

Collected from model API responses.

| Metric | Unit | How to Collect | Alert |
|--------|------|---------------|-------|
| Input tokens | count | API response `usage.input_tokens` | Component of cost |
| Output tokens | count | API response `usage.output_tokens` | Component of cost |
| Cost per request | USD | `input_tokens * input_price + output_tokens * output_price` | > 3× rolling 7-day avg |
| Cost per session | USD | Sum across all turns in a session | > 5× avg session cost |
| Daily cost total | USD | Sum across all requests in a day | > 150% of budget |

**Pricing constants**: Store in a config file, not hardcoded. Update when provider changes pricing.

```python
MODEL_PRICING = {
    "claude-sonnet-5": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
}

def calculate_cost(model, input_tokens, output_tokens):
    pricing = MODEL_PRICING.get(model, {"input": 0, "output": 0})
    return input_tokens * pricing["input"] + output_tokens * pricing["output"]
```

## 3. Quality

Collected by the evaluation pipeline.

| Metric | Unit | How to Collect | Alert |
|--------|------|---------------|-------|
| Rubric composite score | 1–5 float | Run rubric on sampled outputs | 7-day rolling avg drops > 0.3 from baseline |
| Per-dimension score | 1–5 float | Same as above, per dimension | Any dimension drops > 0.5 |
| Human override rate | percentage | HITL system: log approvals vs. overrides | Week-over-week increase > 20% |
| Correction rate | percentage | Log edits/retries of AI output | Week-over-week increase > 20% |

**Evaluation sampling pattern (pseudocode)**:
```python
def should_sample_for_eval(session_id, sample_rate=0.05):
    # Deterministic sampling based on session_id hash
    return int(session_id[-4:], 16) / 65535 < sample_rate
```

## 4. Reliability

| Metric | Unit | Alert |
|--------|------|-------|
| Error rate | percentage | > 2% over 15-minute window |
| Retry rate | percentage | > 10% (rate limit pressure) |
| Timeout rate | percentage | > 1% over 15-minute window |
| Tool call success rate | percentage | < 95% (> 5% failure rate) |
| Context window overflow rate | percentage | > 0.5% (context management issue) |

## Storage and Retention

| Data Type | Recommended Retention |
|-----------|----------------------|
| Aggregated metrics | 13 months |
| Structured trace logs | 90 days (PII-scrubbed) |
| Sampled evaluation outputs | 12 months |
| Raw prompt/output content | 30 days maximum (treat as sensitive) |
| Cost data | 13 months |

## Dashboard Layout

1. Error rate (15-minute window) — top of dashboard; red/yellow/green
2. P95 latency (1-hour window)
3. Cost today vs. budget
4. Rubric score trend (7-day rolling vs. baseline)
5. Evaluation sample count this week
6. Active alerts
