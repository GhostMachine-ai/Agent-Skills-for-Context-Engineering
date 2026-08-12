# Skills Mapping: AI Document Summariser

Maps every significant design decision to the skill that informed it.

## Delivery Process Decisions

| Decision | Skill | Phase | Without the Skill |
|----------|-------|-------|-------------------|
| AI/ML Systems Thinker in Alignment team | `ai-delivery-process` | Alignment | Data sovereignty gap found in Beta |
| Data Availability Matrix completed before feature design | `ai-delivery-process` | Discovery | Scanned-document gap found in Alpha or Beta |
| Manual prototype before automated prototype | `ai-delivery-process` | Alpha | Structural output gap found after prompt engineering investment |
| Evaluation rubric before LLM prototype | `ai-delivery-process` | Alpha | Success criteria defined after build, optimised for wrong thing |
| Evaluation harness as Alpha exit criterion | `ai-delivery-process` | Alpha | No automated quality gate in Beta |
| Prompt change treated as software deployment | `ai-delivery-process` | Beta | Untracked prompt changes; no rollback path |
| Model deprecation plan before Beta | `ai-delivery-process` | Beta | Unplanned incident when provider deprecates model version |

## Observability Decisions

| Decision | Skill | Phase | Outcome |
|----------|-------|-------|---------|
| Latency, cost, rubric score instrumented from day one | `agent-observability` | Beta | Prompt regression caught in 24h in week 5 |
| Semantic prompt versioning with before/after scores | `agent-observability` | Beta | Rollback completed same day as regression detected |
| Cost alerting at 2× baseline per summary | `agent-observability` | Beta | Budget overrun caught in simulation before launch |
| Drift detection (30-day baseline vs 7-day current) | `agent-observability` | Live | Model provider silent update caught in 48h |
| Sampling rate: 10% in Beta, 5% in Live | `agent-observability` | Beta, Live | Evaluation cost within budget; coverage sufficient for regression detection |

## Human-AI Collaboration Decisions

| Decision | Skill | Phase | Outcome |
|----------|-------|-------|---------|
| Level 2 (AI draft, human edits) for UNCLASSIFIED | `human-ai-collaboration` | Discovery | Accepted by governance; users satisfied |
| Level 1 (human decides, AI informs) for OFFICIAL-SENSITIVE | `human-ai-collaboration` | Discovery | Regulatory requirement met; accountability clear |
| 4-hour SLA for human review | `human-ai-collaboration` | Discovery | SLA met with 2-reviewer pool (predicted by simulator) |
| Confidence score display on AI summaries | `human-ai-collaboration` | Alpha | User testing showed reduced over-trust of low-quality outputs |
| Graceful degradation when API unavailable | `human-ai-collaboration` | Beta | Service remains usable (manual fallback) during model outages |
| Oversight fatigue review after 3 months Live | `human-ai-collaboration` | Live | Reviewer attention quality monitored; intervention planned if needed |

## Evaluation Decisions

| Decision | Skill | Phase | Outcome |
|----------|-------|-------|---------|
| Four dimensions, accuracy-weighted | `evaluation` | Alpha | Reflects domain priority (no hallucinations > format) |
| LLM-as-judge for coherence and completeness | `evaluation` | Alpha | Scalable evaluation without full human annotation cost |
| Human annotation for accuracy (10% sample) | `evaluation` | Alpha, Live | Ground truth for calibrating LLM judge |
| 3.5/5 threshold for Alpha gate | `evaluation` | Alpha | LLM prototype scored 3.7; gate passed |
| Weekly evaluation sampling in Live | `evaluation` | Live | Drift detected at 3.4 (week 9); resolved at 3.8 (week 10) |
