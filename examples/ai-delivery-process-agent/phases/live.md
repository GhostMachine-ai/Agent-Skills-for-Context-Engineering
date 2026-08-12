# Live Phase: AI Document Summariser

## Retained Team

| Role | Allocation | AI-Specific |
|------|------------|-------------|
| Product Manager | Part-time | — |
| Developer | 1 FTE | — |
| ML Engineer | Part-time / on-call | Yes |
| AI Safety / Eval Lead | Part-time | Yes |
| MLOps Engineer | Part-time | Yes |

## Live Operations

### Evaluation Sampling Programme

- **Rate**: 5% of all summaries (reduced from 10% in Beta as quality stabilised)
- **Method**: Automated rubric (all sampled); human annotation (10% of sample = 0.5% overall)
- **Frequency**: Weekly report; daily alert check
- **Owner**: AI Safety / Eval Lead

### Drift Detection

- **Baseline window**: 30-day rolling average rubric score
- **Current window**: 7-day rolling average
- **Threshold**: Alert if current < baseline − 0.2
- **Tool**: `drift_detector.py` (see `agent-observability` skill)

### Cost Monitoring

- **Alert**: 2× baseline cost-per-summary
- **Review trigger**: Any week where cost-per-summary exceeds baseline by 20%
- **Owner**: MLOps Engineer

## Live Incidents

### Week 9: Model Drift Incident

**Detected**: Rubric score dropped from 3.8 (baseline) to 3.4 (below 3.5 threshold)  
**Cause**: Model provider made an unannounced update to base model (confirmed by provider)  
**Response**: Prompt adjusted by ML Engineer to restore score; re-evaluated against full test dataset  
**Resolution**: Score restored to 3.8 within 48 hours  
**Preventive action**: Added monthly check of provider changelog; escalation path formalized

### Week 22: Cost Spike

**Detected**: Cost-per-summary increased 35% over two days  
**Cause**: Spike in average document length (budget document season)  
**Response**: No action required; within policy budget allocation  
**Outcome**: Cost alert threshold reviewed; seasonal adjustment noted in runbook

## Live Metrics (Months 1–6)

| Metric | Target | Actual (P50) | Actual (P95) |
|--------|--------|-------------|-------------|
| Rubric score | ≥ 3.5 | 3.8 | 3.4 (week 9 incident) |
| P95 latency | ≤ 30s | 16s | 24s |
| Cost per summary | ≤ £0.05 | £0.038 | £0.051 |
| User satisfaction | ≥ 70% | 78% | — |
| HITL SLA compliance | ≥ 95% | 97% | — |

## Planned Next Steps

- Phase 2 scoping: OCR pipeline for scanned documents
- Evaluation rubric review (6-month mark): reassess dimension weights with domain experts
- Oversight fatigue assessment: review reviewer attention quality after 6 months
- Model upgrade evaluation: candidate replacement model to be tested
