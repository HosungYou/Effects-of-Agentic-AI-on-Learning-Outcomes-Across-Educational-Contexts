# Master Integration Document

## Effects of Agentic AI on Learning Outcomes Across Educational Contexts: A Meta-Analysis with Implications for Human-AI Learning Orchestration

**Authors**: Hosung You & Dr. Yang
**Version**: 1.1
**Date**: 2026-02-16
**Status**: Active — Phase 1 (Protocol & Pilot)
**Study Type**: Standard Random-Effects Meta-Analysis (Hedges' g)
**Framework**: HALO (Human-AI Learning Orchestration)

---

## 1. Project Purpose and Scope

This document serves as the central integration point for all components of the meta-analysis project. It maps relationships between documents, tracks project status, and provides quick-reference access to all key decisions, materials, and procedures.

This is a **standard random-effects meta-analysis** synthesizing empirical evidence on the effects of agentic AI systems on learning outcomes across K-12, higher education, and workplace training contexts. The study uses Hedges' g and robust variance estimation (RVE) to examine the overall magnitude of agentic AI effects and the moderating role of human oversight, agent architecture, and learning context. The analysis culminates in the empirically-grounded HALO Framework for principled AI agent design in education.

### 1.1 Core Research Questions

| ID | Question | Status | Analysis Method | Key Document |
|----|----------|:------:|-----------------|-------------|
| **RQ1** | Overall effect of Agentic AI on learning outcomes | Pending | Random-effects meta-analysis (Hedges' g) | `docs/04_methodology/meta_analysis_method_guide.md` |
| **RQ2** | Human oversight level as moderator | Pending | Subgroup analysis + RVE | `docs/03_data_extraction/coding_manual.md` §C1 |
| **RQ3** | Single vs. multi-agent architecture | Pending | Subgroup analysis | `docs/03_data_extraction/coding_manual.md` §C2 |
| **RQ4** | Learning context as moderator (K-12 / HE / Workplace) | Pending | Subgroup analysis | `docs/03_data_extraction/coding_manual.md` §D1 |
| **RQ5** | HALO Framework design principles derivation | Pending | Moderator-to-principle mapping | `docs/halo-framework.md` |

---

## 1.2 Theoretical Foundations

| Theory | Abbreviation | Relevance |
|--------|-------------|-----------|
| Affordance Actualization Theory | AAT | Context-dependent effectiveness of AI agents; affordance realization |
| Event System Theory | EST | Grounds checkpoint trigger conditions; oversight event salience |
| Self-Determination Theory | SDT | Autonomy, competence, and relatedness as mediators of AI agent effects |
| Dynamic Learner State Model | DLS | Yang (2025) — learner state as dynamic multi-dimensional input to agent adaptation |
| Adaptive/Proactive/Co-Learner/Peer Framework | APCP | Yan (2025) — taxonomy of AI agency levels in educational contexts |

---

## 1.3 Moderator Variable Registry

All moderators are coded at the effect-size level. Categorical moderators use dummy coding unless otherwise specified; continuous moderators are mean-centered.

### Primary Moderators (RQ2–RQ4)

| Moderator | Variable Name | Levels | Coding Notes |
|-----------|--------------|--------|--------------|
| **Human Oversight Level** | `oversight_level` | (1) Fully Autonomous — AI acts without human review; (2) AI-Led with Checkpoints — human reviews at defined intervals; (3) Human-Led with AI Support — human retains primary control | Primary moderator for RQ2; must be coded for all included studies |
| **Agent Architecture** | `agent_architecture` | (1) Single-Agent — one AI agent per learner interaction; (2) Multi-Agent — two or more AI agents coordinate or interact | Primary moderator for RQ3; if ambiguous, code as single-agent and flag |
| **Learning Context** | `learning_context` | (1) K-12; (2) Higher Education; (3) Workplace Training | Primary moderator for RQ4; use participant population, not platform |

### Secondary Moderators (Exploratory)

| Moderator | Variable Name | Levels / Range | Coding Notes |
|-----------|--------------|----------------|--------------|
| **Agency Level (APCP)** | `agency_level_apcp` | (1) Adaptive — responds to learner input; (2) Proactive — initiates without learner prompt; (3) Co-Learner — engages as co-constructor; (4) Peer — treated as social equal | Based on Yan (2025) APCP taxonomy |
| **AI Agent Role** | `agent_role` | (1) Tutor; (2) Assistant; (3) Facilitator; (4) Evaluator; (5) Peer | Code primary functional role; multiple roles → code dominant role |
| **Agent Modality** | `agent_modality` | (1) Text; (2) Voice; (3) Embodied (avatar/robot); (4) Multimodal | Code modality of learner-facing interaction |
| **Outcome Type** | `outcome_type` | (1) Cognitive; (2) Skill-based; (3) Affective; (4) Behavioral | Can have multiple effect sizes per study if multiple outcome types reported |
| **Bloom's Taxonomy Level** | `blooms_level` | (1) Remember; (2) Understand; (3) Apply; (4) Analyze; (5) Evaluate; (6) Create | Code the highest Bloom's level the outcome targets |

### Methodological Moderators (Sensitivity)

| Moderator | Variable Name | Type | Notes |
|-----------|--------------|------|-------|
| Study design | `study_design` | Categorical: RCT / Quasi-experiment / Pre-post | Used in sensitivity analysis |
| Publication status | `pub_status` | Categorical: Published / Unpublished / Preprint | Used in publication bias assessment |
| Sample size | `n_total` | Continuous | Used in Egger's test and PET-PEESE |
| Publication year | `pub_year` | Continuous | Used in meta-regression for temporal trends |
| Study duration (weeks) | `duration_weeks` | Continuous | Coded from reported study length |

---

## 1.4 Analysis Module Cross-Reference

All scripts reside in `analysis/R/`. Run sequentially unless otherwise noted.

| Module | File | Purpose | Input | Output | Dependencies |
|--------|------|---------|-------|--------|--------------|
| 00 | `00_setup.R` | Load packages, set global options, configure paths | None | Environment | None |
| 01 | `01_data_preparation.R` | Import coded data, compute Hedges' g, validate, create analysis dataset | `data/04_final/master_effect_sizes.xlsx` | `data/05_analysis/analysis_dataset.rds` | 00 |
| 02 | `02_overall_effect.R` | Random-effects model (REML), overall g, heterogeneity (Q, I², τ²) | analysis_dataset.rds | Table 2 outputs, model objects | 01 |
| 03 | `03_moderator_analysis.R` | Subgroup analyses and meta-regression for RQ2–RQ4 moderators | analysis_dataset.rds | Table 3 outputs, QM statistics | 01 |
| 04 | `04_robust_variance.R` | RVE (correlated effects model), 3-level meta-analysis comparison | analysis_dataset.rds | Table 4 outputs, RVE model | 01 |
| 05 | `05_publication_bias.R` | Funnel plot, Egger's test, PET-PEESE, trim-and-fill, p-curve | analysis_dataset.rds | Table 5 outputs, Figure 4 | 01 |
| 06 | `06_sensitivity.R` | Leave-one-out, influence diagnostics, design-subgroup sensitivity | analysis_dataset.rds | Sensitivity tables | 02, 03 |
| 07 | `07_visualization.R` | Forest plots (overall + moderators), funnel plot, bubble plots | analysis_dataset.rds, model objects | Figures 2, 3, 4 | 02, 03, 05 |
| 08 | `08_halo_mapping.R` | HALO Framework derivation: pattern extraction from moderator results | analysis_dataset.rds, Table 3 outputs | Figure 5, HALO specification table | 03 |

---

## 1.5 Data Pipeline (AI-Assisted Coding)

```
PDFs
  │
  ▼
Phase 0: RAG Preprocessing
  └── Chunk PDFs, build vector index, extract metadata
  │
  ▼
Phase 1: Study Information Extraction
  └── Title, authors, year, journal, country, design, N, context
  │
  ▼
Phase 2: Effect Size Extraction
  └── Outcome measure, means, SDs, n per group → compute Hedges' g
  │
  ▼
Phase 3: Agent Characteristics Coding
  └── Oversight level, architecture, agency level (APCP), role, modality
  │
  ▼
Phase 4: 3-Model Consensus
  └── Claude Sonnet 4.5 + GPT-4o + Groq → majority vote / flag disagreements
  │
  ▼
Phase 5: Inter-Coder Reliability (ICR)
  └── Human coders verify flagged items; compute κ (≥.85) and ICC (≥.90)
  │
  ▼
Phase 6: Quality Assurance
  └── Bounds checking (|g| < 5), cross-validation, provenance logging
  │
  ▼
data/04_final/master_effect_sizes.xlsx
  │
  ▼
R Analysis Pipeline (Modules 00–08)
```

### Data Directory Structure

```
data/
├── 00_raw/          # Original PDFs (not committed to git)
├── 01_screened/     # PRISMA screening outputs
├── 02_extracted/    # Per-phase extraction CSVs
├── 03_coded/        # ICR files and consensus outputs
├── 04_final/        # master_effect_sizes.xlsx (source of truth)
└── 05_analysis/     # analysis_dataset.rds (generated by 01_data_preparation.R)
```

---

## 1.6 Quality Gates

Quality gates must be verified before proceeding to the next analysis phase. Failures are logged in `logs/quality_gate_failures.log`.

| Gate | ID | Criterion | Action if Failed |
|------|----|-----------|-----------------|
| Effect Size Bounds | G1 | All Hedges' g values satisfy \|g\| < 5.0 | Flag for human review; exclude if coding error confirmed |
| Inter-Coder Reliability | G2 | κ ≥ .85 for categorical moderators; ICC ≥ .90 for continuous variables | Re-code discrepant items; do not proceed until threshold met |
| Model Convergence | G3 | Random-effects REML model converges without warnings | Check for sparse cells, consider aggregation or fixed effects |
| Heterogeneity Diagnostics | G4 | I², τ², and Q statistic reported; outlier influence assessed | Conduct additional sensitivity analyses; report in limitations |
| Publication Bias | G5 | Egger's test, trim-and-fill, and PET-PEESE all run and reported | Report all results regardless of significance; adjust if indicated |

---

## 1.7 Manuscript Mapping

### Tables

| Table | Title | Source Module(s) | Notes |
|-------|-------|-----------------|-------|
| Table 1 | Characteristics of Included Studies | 01_data_preparation.R | Descriptive summary: N, context, design, year, outcome type |
| Table 2 | Overall Effect Size and Heterogeneity | 02_overall_effect.R | g, 95% CI, Q, df, p, I², τ², τ |
| Table 3 | Moderator Analysis Results (RQ2–RQ4) | 03_moderator_analysis.R | Subgroup g per level, QM statistic, between-group p |
| Table 4 | Robust Variance Estimation and 3-Level Comparison | 04_robust_variance.R | RVE correlated-effects model vs. standard RE model |
| Table 5 | Publication Bias Diagnostics | 05_publication_bias.R | Egger's b, trim-and-fill k, PET-PEESE intercept |

### Figures

| Figure | Title | Source Module(s) | Notes |
|--------|-------|-----------------|-------|
| Figure 1 | PRISMA 2020 Flow Diagram | Manual / screening pipeline | Records identified, screened, excluded, included |
| Figure 2 | Forest Plot: Overall Effect | 07_visualization.R | Ordered by effect size; includes RE summary diamond |
| Figure 3 | Moderator Forest Plots | 07_visualization.R | Three panels: Human Oversight, Agent Architecture, Learning Context |
| Figure 4 | Funnel Plot with Trim-and-Fill | 07_visualization.R | Egger's regression line; imputed studies marked |
| Figure 5 | HALO Framework Diagram | 08_halo_mapping.R | 3-layer architecture: Orchestration / Agency / Grounding |

---

## 1.8 Key Decision Log

| # | Date | Decision | Rationale | Alternatives Considered |
|---|------|----------|-----------|------------------------|
| D-01 | 2026-02-16 | Use Hedges' g (not Cohen's d) as primary effect size metric | Hedges' g provides small-sample correction; standard in educational meta-analysis | Cohen's d (rejected: biased for small N); log odds ratio (rejected: incompatible with continuous outcomes) |
| D-02 | 2026-02-16 | Adopt random-effects model (REML estimator) as primary model | Assumes true effect heterogeneity across studies; appropriate given expected variance in agentic AI implementations | Fixed-effects (rejected: implausible homogeneity assumption); Bayesian (deferred to sensitivity) |
| D-03 | 2026-02-16 | Apply RVE (correlated effects) to handle multiple effect sizes per study | Studies may report multiple outcomes; RVE preserves all effect sizes without arbitrary selection | Average within study (rejected: information loss); multilevel meta-analysis (reported as comparison in Table 4) |
| D-04 | 2026-02-16 | Define search window as 2018–2025 | Agentic AI in education emerged primarily post-2018; earlier studies predate the concept of agent-like AI in learning | 2015–2025 (considered; 2015–2017 literature is AI-assistive, not agentic) |
| D-05 | 2026-02-16 | Code oversight level as the primary moderator (RQ2) | Human oversight is the theoretically and practically most critical design dimension for safe AI deployment in education | Learning context (retained as RQ4); agent architecture (retained as RQ3) |
| D-06 | 2026-02-16 | This is a standard meta-analysis (not MASEM) | Research questions concern moderating variables and effect sizes, not structural paths between latent constructs | MASEM (rejected: not testing a structural model; construct covariance matrix not estimable from available literature) |

---

## 2. Document Map

### 2.1 Complete Document Inventory

#### Core Documentation (`docs/`)

| Document | Phase | Purpose | Status |
|----------|:-----:|---------|:------:|
| `docs/research-proposal.md` | All | Master research proposal | Complete |
| `docs/coding-scheme.md` | 4 | Coding variable overview | Complete |
| `docs/search-strategy.md` | 1 | Search strategy summary | Complete |
| `docs/halo-framework.md` | 5 | HALO Framework specification | Complete (initial) |
| `docs/pitch-for-collaborator.md` | Pre | Collaboration pitch | Complete |
| `docs/timeline.md` | All | 7-month project timeline | Complete |
| `docs/references.md` | All | Annotated key references | Complete |
| `docs/README.md` | All | Documentation index | Complete |

#### Phase 1: Literature Search (`docs/01_literature_search/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `search_strategy.md` | Full Boolean strings for all 6 databases | Complete |
| `database_coverage.md` | Coverage matrix; journal lists; overlap | Complete |

#### Phase 2: Study Selection (`docs/02_study_selection/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `inclusion_exclusion_criteria.md` | PICOS criteria + decision trees | Complete |
| `screening_protocol.md` | Two-phase screening + kappa | Complete |

#### Phase 3: Data Extraction (`docs/03_data_extraction/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `coding_manual.md` | All variable definitions + decision rules | Complete |
| `effect_size_extraction_guide.md` | Hedges' g formulas + R code | Complete |
| `reliability_protocol.md` | ICR kappa + ICC + training | Complete |

#### Phase 4: Methodology (`docs/04_methodology/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `meta_analysis_method_guide.md` | Full analysis plan with R code | Complete |

#### Phase 5: Manuscript (`docs/05_manuscript/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `writing_timeline.md` | Writing schedule + section assignments | Complete |

#### Phase 6: Decisions (`docs/06_decisions/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `decision_log.md` | Running log of all methodological decisions | Active |

#### Supplementary Materials (`supplementary/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `prisma/PRISMA_2020_Checklist.md` | 30-item PRISMA 2020 compliance checklist | Template ready |
| `protocol/preregistration_protocol.md` | PROSPERO registration template | Template ready |
| `codebook/meta_analysis_codebook.md` | Data dictionary for all variables | Complete |
| `risk_of_bias/Risk_of_Bias_Assessment.md` | RoB assessment tool (Cochrane adapted) | Complete |
| `Search_Strategy_Appendix.md` | Verbatim search strings for all databases | Template ready |

#### Manuscript (`manuscript/`)

| Document | Purpose | Status |
|----------|---------|:------:|
| `abstract.md` | Structured abstract template | Template ready |

#### Root Directory

| Document | Purpose | Status |
|----------|---------|:------:|
| `MASTER_INTEGRATION_DOCUMENT.md` | This file | Active |
| `CHANGELOG.md` | Version history | Active |
| `README.md` | [To be created] Project overview | Pending |

---

## 3. Theoretical Integration Map

### 3.1 Theory-to-Variable Mapping

| Theory | Theoretical Role | Coded Variable | RQ Connection | HALO Layer |
|--------|-----------------|---------------|:---:|:---------:|
| Affordance Actualization Theory (AAT) | Explains context-dependent effectiveness | `context`, `agent_role` | RQ4 | Layer 3 |
| Event System Theory (EST) | Grounds checkpoint trigger conditions | `oversight_level` | RQ2 | Layer 3 |
| Self-Determination Theory (SDT) | Links oversight to learner autonomy | `oversight_level`, `context` | RQ2, RQ4 | Layers 1+3 |
| Dynamic Learner State (DLS; Yang, 2025) | Multi-dimensional state tracking | `adaptivity` | Additional | Layer 2 |
| APCP Framework (Yan, 2025) | Agency level taxonomy | `agency_level` | Additional | Layer 1 |

### 3.2 Theory-to-HALO Mapping

| HALO Layer | Governing Theory | Meta-Analysis Input | Design Output |
|------------|-----------------|--------------------:|---------------|
| Layer 1: Foundation | APCP + SDT | RQ4 context effects; agency_level moderator | Agency level calibration per context |
| Layer 2: Protocol | DLS (Yang, 2025) | Adaptivity level moderator | Multi-dimensional state tracking spec |
| Layer 3: Orchestration | EST + AAT + SDT | RQ2 oversight effects; RQ3 architecture | Checkpoint calibration; role assignment |

---

## 4. Variable-to-Analysis Mapping

### 4.1 Variables by Research Question

| Variable | Code | RQ | Analysis Method | Expected Direction |
|----------|------|----|-----------------|-------------------|
| `oversight_level` | 1-3 | RQ2 | Subgroup analysis | Checkpoint-based > Fully autonomous (hypothesis) |
| `architecture` | 1-2 | RQ3 | Subgroup analysis | Multi-agent > Single agent (hypothesis) |
| `context` | 1-5 | RQ4 | Subgroup analysis | Varies by context (hypothesis) |
| `agency_level` | 1-4 | Additional | Subgroup analysis | Higher agency > lower in advanced contexts |
| `agent_role` | 1-6 | Additional | Subgroup analysis | Tutor role most effective for cognitive outcomes |
| `outcome_type` | 1-4 | Additional | Subgroup analysis | Cognitive > Affective effects |
| `blooms_level` | 1-3 | Additional | Subgroup analysis | Lower Bloom's → larger AI effect |
| `technology` | 1-6 | Additional | Subgroup analysis | LLM > Rule-based |
| `adaptivity` | 1-5 | Additional | Subgroup analysis | Multi-dim > Single-dim |
| `duration_weeks` | Continuous | Additional | Meta-regression | Dose-response (longer = larger?) |
| `year` | Continuous | Additional | Meta-regression | Increasing over time? |
| `rob_overall` | 0-2 | Sensitivity | Restriction analysis | High RoB studies inflate effect? |

### 4.2 Effect Size Dependency Structure

| Dependency Type | Handling Method | Priority |
|----------------|-----------------|:--------:|
| Multiple outcomes from same sample | 3-level RE model (primary) + RVE (check) | 1 |
| Multiple time points from same sample | Extract separately; code timing variable | 2 |
| Multiple subgroups from same paper | Extract for full sample primary; subgroup secondary | 3 |
| Multiple papers from same study | Merge data; use most complete dataset | 4 |

---

## 5. Role Distribution

### 5.1 Author Responsibilities

| Area | Hosung You | Dr. Yang |
|------|:---:|:---:|
| Research design + HALO Framework | Lead | Support |
| MCP theory + Dynamic Learner State | Support | Lead |
| Search strategy + Covidence management | Lead | Support |
| Independent screening (Coder 1) | Lead | Support |
| Independent screening (Coder 2) | — | Lead |
| Coding scheme management | Lead | Support |
| Independent coding (Coder 1) | Lead | — |
| Independent coding (Coder 2) | — | Lead |
| Meta-analysis execution (R) | Lead | Support |
| Data validation + robustness checks | Support | Lead |
| Writing: Framework + Discussion | Lead | Support |
| Writing: Theory + Method | Support | Lead |
| HALO Layer 3 (Orchestration, Checkpoints) | Lead | Support |
| HALO Layer 2 (Protocol, State Tracking) | Support | Lead |

### 5.2 Third-Party Resources

| Resource | Purpose | Contact/Access |
|----------|---------|----------------|
| Covidence | Screening management | [Institutional subscription] |
| Zotero | Reference management | Shared group library |
| PROSPERO | Protocol registration | https://www.crd.york.ac.uk/prospero/ |
| R (metafor, robumeta) | Meta-analysis | https://cran.r-project.org/ |
| OSF/Zenodo | Data/materials sharing | [Create project page] |

---

## 6. Project Timeline Integration

### 6.1 Phase-Document Mapping

| Phase | Months | Key Documents | Key Deliverables |
|-------|:------:|--------------|-----------------|
| **Phase 1**: Protocol & Pilot | 1 | `preregistration_protocol.md`; `search_strategy.md` | PROSPERO registration; finalized search strings |
| **Phase 2**: Search & Screening (T/A) | 1-2 | `database_coverage.md`; `screening_protocol.md` | 6 database exports; deduplicated set |
| **Phase 3**: Full-Text Screening | 2-3 | `inclusion_exclusion_criteria.md`; `screening_protocol.md` | Included study list; PRISMA flow |
| **Phase 4**: Coding & Extraction | 3-4 | `coding_manual.md`; `effect_size_extraction_guide.md`; `reliability_protocol.md` | Master dataset; ICR statistics |
| **Phase 5**: Analysis | 4-5 | `meta_analysis_method_guide.md` | All forest plots; tables; HALO refined |
| **Phase 6**: Writing | 5-7 | `writing_timeline.md`; `abstract.md` | Complete manuscript draft |
| **Phase 7**: Submission | 7 | `PRISMA_2020_Checklist.md`; `Search_Strategy_Appendix.md` | Submitted manuscript |

### 6.2 Milestone Tracker

| Milestone | Target | Status | Date Completed |
|-----------|:------:|:------:|:--------------:|
| Protocol registered (PROSPERO) | End Month 1 | Pending | |
| Pilot search complete | Week 3-4 | Pending | |
| All database searches complete | End Month 2 | Pending | |
| Title/abstract screening complete | End Month 2 | Pending | |
| Full-text screening complete | End Month 3 | Pending | |
| Pilot coding complete (kappa ≥ 0.80) | Week 13-14 | Pending | |
| Full independent coding complete | End Month 4 | Pending | |
| Master dataset verified | Week 17 | Pending | |
| Overall meta-analysis (RQ1) complete | Week 18-19 | Pending | |
| Moderator analyses (RQ2-4) complete | Week 21 | Pending | |
| HALO refined version complete | Week 22 | Pending | |
| Full manuscript draft complete | End Month 6 | Pending | |
| Manuscript submitted | End Month 7 | Pending | |

---

## 7. Quality Assurance Checklist

### 7.1 Pre-Submission Verification

Before submitting the manuscript, verify all of the following:

#### Search Quality
- [ ] All 6 databases searched with locked search strings
- [ ] Search dates documented for all databases
- [ ] Citation tracking completed for 5 seed articles
- [ ] Hand search of 3 key journals completed
- [ ] Grey literature sources searched

#### Screening Quality
- [ ] Pilot screening kappa ≥ 0.80 before independent screening
- [ ] Phase 1 kappa calculated and reported
- [ ] Phase 2 kappa calculated and reported
- [ ] All exclusion reasons documented at full-text stage
- [ ] PRISMA flow diagram counts verified

#### Coding Quality
- [ ] Pilot coding kappa ≥ 0.80 before full coding
- [ ] 20% reliability sample coded by both coders
- [ ] All variables with kappa < 0.80 resolved and re-coded
- [ ] Effect size extraction verified (ICC ≥ 0.90)
- [ ] All discrepancies resolved and documented

#### Analysis Quality
- [ ] All Hedges' g values computed and verified in R
- [ ] Forest plots generated for all analyses
- [ ] Heterogeneity statistics reported (Q, I², τ², PI)
- [ ] Publication bias assessed with ≥ 3 methods
- [ ] Sensitivity analyses conducted and reported
- [ ] Moderator analyses with k < 4 per cell excluded

#### Reporting Quality
- [ ] PRISMA 2020 checklist completed (all 30 items)
- [ ] Pre-registration number included in abstract and methods
- [ ] All tables and figures labeled and cited in text
- [ ] All claims in discussion supported by results
- [ ] Supplementary materials package complete

#### HALO Framework Quality
- [ ] All design principles mapped to specific meta-analytic findings
- [ ] Effect size thresholds applied consistently
- [ ] Framework acknowledges null/unexpected findings
- [ ] Limitations of framework appropriately noted

---

## 8. Data Management

### 8.1 File Naming Conventions

| File Type | Convention | Example |
|-----------|-----------|---------|
| Database exports | `[db]_search_[YYYYMMDD].[ext]` | `wos_search_20260301.ris` |
| Coding sheets | `coding_[version]_[coder]_[YYYYMMDD].xlsx` | `coding_v1_HY_20260415.xlsx` |
| Analysis scripts | `analysis_[rq]_[YYYYMMDD].R` | `analysis_rq1_overall_20260501.R` |
| Figures | `fig[N]_[description].pdf` | `fig2_forest_overall.pdf` |
| Manuscript drafts | `manuscript_v[N]_[YYYYMMDD].docx` | `manuscript_v3_20260615.docx` |

### 8.2 Version Control

All project files are maintained in the shared repository at:
`/Users/hosung/Effects-of-Agentic-AI-on-Learning-Outcomes-Across-Educational-Contexts/`

Key subdirectories:
```
/data/          - Coding sheets, master dataset (sensitive; not for public sharing pre-publication)
/analysis/R/    - R scripts for all analyses
/analysis/figures/ - All generated figures
/manuscript/    - Manuscript drafts
/docs/          - All methodology documentation (this document set)
/supplementary/ - Supplementary materials for submission
```

### 8.3 Data Sharing Plan

Upon acceptance:
- Anonymized coding dataset → OSF or Zenodo (DOI-assigned)
- R analysis scripts (annotated) → GitHub public repository
- PRISMA flow diagram → OSF
- Pre-registration → PROSPERO (already public upon registration)

---

## 9. Key Reference Integration

### 9.1 Foundation Studies

| Reference | Role | How Used |
|-----------|------|---------|
| Dai et al. (2024) | Predecessor meta-analysis | Comparison benchmark; seed for citation tracking |
| Ma et al. (2014) | ITS precedent | Historical comparison; coding precedent |
| Yang (2025) | HALO Layer 2 theory | DLS coding; MCP framework basis |
| Yan (2025) | Agency level taxonomy | APCP coding scheme (C3) |
| Page et al. (2021) | PRISMA 2020 guideline | Reporting standard throughout |
| Viechtbauer (2010) | metafor package | Primary analysis software |
| Hedges, Tipton & Johnson (2010) | RVE method | Dependent effect size handling |
| Van den Noortgate et al. (2013) | 3-level meta-analysis | Alternative to RVE |
| Morris & DeShon (2002) | Pre-post ES formula | Effect size computation for pre-post designs |

---

## 10. Contact and Communication

### 10.1 Team Communication Protocol

| Communication Type | Method | Frequency |
|-------------------|--------|-----------|
| Status updates | Email | Weekly |
| Conflict resolution | Video call | As needed |
| Document sharing | Shared cloud folder | Ongoing |
| Decision logging | `06_decisions/decision_log.md` | Immediately after decision |
| Milestone check-ins | Video call | Monthly |

### 10.2 External Communication

| Party | Purpose | Protocol |
|-------|---------|---------|
| Study authors (data requests) | Missing effect size data | One email; 2-week response window |
| PROSPERO | Protocol registration and amendments | Online submission |
| Target journal editors | Submission and revision | Via journal submission system |

---

*This document is the master reference for the project. It is updated at each major milestone. Last updated: 2026-02-16.*
