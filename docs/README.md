# Documentation Index

## Project: Effects of Agentic AI on Learning Outcomes Across Educational Contexts

**A Meta-Analysis with Implications for Human-AI Learning Orchestration (HALO Framework)**

**Authors**: Hosung You & Dr. Yang
**Target Journals**: Educational Research Review (IF 11.8) | Computers & Education (IF 11.5)
**Protocol**: PRISMA 2020 | PROSPERO Pre-registration

---

## Directory Structure

```
docs/
├── README.md                          <- This file
├── research-proposal.md               <- Full research proposal
├── coding-scheme.md                   <- Coding scheme overview
├── search-strategy.md                 <- Search strategy summary
├── halo-framework.md                  <- HALO Framework specification
├── pitch-for-collaborator.md          <- Collaboration pitch document
├── timeline.md                        <- Project timeline (7 months)
├── references.md                      <- Key references
│
├── 01_literature_search/
│   ├── search_strategy.md             <- Detailed search strategy
│   └── database_coverage.md          <- Database coverage matrix
│
├── 02_study_selection/
│   ├── inclusion_exclusion_criteria.md <- Full I/E criteria with decision trees
│   └── screening_protocol.md          <- Two-phase screening protocol
│
├── 03_data_extraction/
│   ├── coding_manual.md               <- Comprehensive coding manual
│   ├── effect_size_extraction_guide.md <- Hedges' g computation guide
│   └── reliability_protocol.md        <- ICR protocol (kappa, ICC)
│
├── 04_methodology/
│   └── meta_analysis_method_guide.md  <- Complete analysis plan (R code)
│
├── 05_manuscript/
│   └── writing_timeline.md            <- Manuscript writing schedule
│
└── 06_decisions/
    └── decision_log.md                <- Methodological decision log
```

---

## Document Descriptions

### Core Documents (Root docs/)

| File | Purpose | Status |
|------|---------|--------|
| `research-proposal.md` | Full research proposal with RQs, method, theory, timeline | Complete |
| `coding-scheme.md` | Variable definitions and coding rules overview | Complete |
| `search-strategy.md` | Search databases, terms, screening process | Complete |
| `halo-framework.md` | HALO Framework 3-layer architecture | Complete |
| `pitch-for-collaborator.md` | Collaboration pitch for Dr. Yang | Complete |
| `timeline.md` | 7-month project timeline with milestones | Complete |
| `references.md` | Key references with annotations | Complete |

### Phase 1: Literature Search

| File | Purpose | Used In |
|------|---------|---------|
| `01_literature_search/search_strategy.md` | Full Boolean search strings for all 6 databases; execution protocol | Phase 1, Month 1 |
| `01_literature_search/database_coverage.md` | Database coverage matrix; journal lists; overlap rates | Phase 1, Month 1 |

### Phase 2: Study Selection

| File | Purpose | Used In |
|------|---------|---------|
| `02_study_selection/inclusion_exclusion_criteria.md` | Complete PICOS criteria with decision trees for borderline cases | Phase 2-3, Months 1-3 |
| `02_study_selection/screening_protocol.md` | Title/abstract and full-text screening procedures; kappa targets | Phase 2-3, Months 1-3 |

### Phase 3: Data Extraction

| File | Purpose | Used In |
|------|---------|---------|
| `03_data_extraction/coding_manual.md` | All variable definitions, codes, decision rules for systematic coding | Phase 4, Months 3-4 |
| `03_data_extraction/effect_size_extraction_guide.md` | Hedges' g formulas for all statistical formats; R code | Phase 4, Months 3-4 |
| `03_data_extraction/reliability_protocol.md` | 20% stratified sample ICR; Cohen's kappa and ICC procedures | Phase 4, Months 3-4 |

### Phase 4: Methodology

| File | Purpose | Used In |
|------|---------|---------|
| `04_methodology/meta_analysis_method_guide.md` | Complete analysis plan: RE model, 3-level, RVE, moderators, publication bias, sensitivity | Phase 5, Months 4-5 |

### Phase 5: Manuscript

| File | Purpose | Used In |
|------|---------|---------|
| `05_manuscript/writing_timeline.md` | Section-by-section writing schedule; word count budget; figure plan | Phase 6, Months 5-7 |

### Phase 6: Decisions

| File | Purpose | Used In |
|------|---------|---------|
| `06_decisions/decision_log.md` | Running log of all methodological decisions and protocol deviations | All phases |

---

## Quick Reference: Research Questions

| RQ | Question | Primary Analysis | Key Variable |
|----|----------|-----------------|--------------|
| **RQ1** | Overall effect of Agentic AI on learning outcomes | Random-effects meta-analysis | Hedges' g |
| **RQ2** | Does human oversight level moderate effects? | Subgroup analysis | `oversight_level` (1-3) |
| **RQ3** | Do single vs. multi-agent systems differ? | Subgroup analysis | `architecture` (1-2) |
| **RQ4** | Does educational context moderate effects? | Subgroup analysis | `context` (1-5) |
| **RQ5** | What design principles emerge? (HALO) | Moderator-to-principle mapping | All moderators |

---

## Quick Reference: Theoretical Framework

| Theory | Abbreviation | Role in Study | HALO Layer |
|--------|:---:|--------------|:-----------:|
| Affordance Actualization Theory | AAT | Explains context-specific actualization of AI affordances | Layer 3 |
| Event System Theory | EST | Grounds checkpoint trigger conditions | Layer 3 |
| Self-Determination Theory | SDT | Links oversight level to learner autonomy | Layers 1+3 |
| Dynamic Learner State | DLS | Informs multi-dimensional state tracking | Layer 2 |
| APCP Framework | APCP | Provides agency level taxonomy | Layer 1 |

---

## Quick Reference: Key Variables

### Primary Moderators

| Variable | Code Name | Values | Research Question |
|----------|-----------|--------|:-----------------:|
| Human oversight level | `oversight_level` | 1=Autonomous, 2=Checkpoint, 3=Human-led | RQ2 |
| Agent architecture | `architecture` | 1=Single, 2=Multi-agent | RQ3 |
| Learning context | `context` | 1=K-12, 2=HE, 3=Workplace, 4=Professional, 5=Continuing | RQ4 |

### Secondary Moderators

| Variable | Code Name | Values |
|----------|-----------|--------|
| Agency level (APCP) | `agency_level` | 1=Adaptive, 2=Proactive, 3=Co-Learner, 4=Peer |
| Agent role | `agent_role` | 1=Tutor, 2=Coach, 3=Assessor, 4=Collaborator, 5=Facilitator, 6=Multiple |
| AI technology | `technology` | 1=Rule-based, 2=ML, 3=NLP, 4=LLM, 5=RL, 6=Hybrid |
| Adaptivity | `adaptivity` | 1=Static, 2=Performance, 3=Behavior, 4=Affect, 5=Multi |
| Outcome type | `outcome_type` | 1=Cognitive, 2=Skill, 3=Affective, 4=Performance |
| Bloom's level | `blooms_level` | 1=Remember-Understand, 2=Apply-Analyze, 3=Evaluate-Create |

---

## Software Requirements

| Tool | Purpose | Version |
|------|---------|---------|
| R | Meta-analysis | ≥ 4.3.0 |
| metafor | Core analysis | ≥ 4.0.0 |
| robumeta | Robust Variance Estimation | Latest |
| clubSandwich | Small-sample RVE corrections | Latest |
| Covidence | Screening management | Web-based |
| Zotero | Reference management | Latest |

---

## Document Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-16 | Initial documentation package created |

---

*For questions about documentation, contact Hosung You (primary researcher). For questions about MCP-related theoretical components, contact Dr. Yang (co-author).*
