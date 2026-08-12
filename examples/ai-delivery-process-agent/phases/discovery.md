# Discovery Phase: AI Document Summariser

## Team

| Role | Person | AI-Specific |
|------|--------|-------------|
| Product Manager | PM | — |
| User Researcher | UX Researcher | — |
| Service Designer | Service Designer | — |
| Technical Lead | Senior Developer | — |
| Data Analyst / ML Engineer | ML Engineer | Yes |

## Key Discovery Findings

**User needs**:
- Civil servants want summaries structured around decisions and required actions, not narrative recaps
- Users in fast-moving policy teams need summaries within minutes, not hours
- Users in accountability roles (senior civil servants) need to know the AI produced the summary and which model version

**Data landscape**:
- Most documents are machine-readable PDFs or Word files: suitable for direct processing
- 28% of documents are scanned images: require OCR (deferred to Phase 2)
- Documents range from 3 to 120 pages; 92% under 50 pages (in-scope for Phase 1)

## Data Availability Matrix (Summary)

Full matrix: `artefacts/data-availability-matrix.md`

| Data Type | Source | Status | Gap | Severity |
|-----------|--------|--------|-----|----------|
| Machine-readable PDFs | SharePoint | Available | None | — |
| Word documents (.docx) | SharePoint | Available | None | — |
| Scanned image PDFs | Legacy archive | Not accessible | No OCR pipeline | High (Phase 2) |
| Documents > 50 pages | Various | Available | Context window constraint | Medium (Phase 2) |
| Classification labels | Document metadata | Partially present | 40% unlabelled | Medium; manual labelling needed |
| Domain expert annotations | Must be created | Not available | No labelled dataset exists | Low; create in Alpha |

## Task-Model Fit Assessment (Summary)

Full assessment: `artefacts/task-model-fit.md`

| Task Component | Fit | Notes |
|----------------|-----|-------|
| Identify key decisions | Strong | Well-bounded; clear criteria |
| Identify action items | Strong | Well-bounded; tested in comparable domains |
| Identify risk flags | Moderate | Subjective; requires evaluation rubric definition |
| Summarise in structured format | Strong | Prompt engineering well-understood |
| Classify document sensitivity level | Weak | Requires training data; deferred |

**Recommendation**: Proceed with summarisation task. Exclude automatic sensitivity classification from Phase 1 scope.

## Human-in-the-Loop Map (Draft)

Full map: `artefacts/hitl-map-template.md`

| AI Decision | Classification | Automation Level | Reviewer | SLA |
|-------------|---------------|-----------------|----------|-----|
| Summary of UNCLASSIFIED document | UNCLASSIFIED | Level 2: AI draft, human edits | Requesting civil servant | N/A (self-review) |
| Summary of OFFICIAL-SENSITIVE document | OFFICIAL-SENSITIVE | Level 1: human decides, AI informs | Designated reviewer (policy team) | 4 hours |
| Summary quality flag (score < 3.0) | Any | Level 1: human review | ML Engineer (escalation) | 2 hours |

**HITL Map status**: Draft — to be validated with users in Alpha.

## Gate Decision

**Decision**: Proceed to Alpha  
**Date**: End of week 8  
**Sign-off**: Service Owner, PM

**Gate criteria met**:
- [x] Data Availability Matrix complete
- [x] AI tasks identified and scoped
- [x] Draft HITL Map created
- [x] Scanned documents explicitly deferred to Phase 2
- [x] Sovereign-cloud provider shortlisted (2 options)
