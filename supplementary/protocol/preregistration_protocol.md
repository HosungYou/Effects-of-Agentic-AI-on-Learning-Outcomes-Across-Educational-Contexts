# PROSPERO Pre-Registration Protocol

## Systematic Review Registration

**Registry**: PROSPERO (International prospective register of systematic reviews)
**URL**: https://www.crd.york.ac.uk/prospero/

---

## Section 1: Review Title

**Title**: Effects of Agentic AI on Learning Outcomes Across Educational Contexts: A Meta-Analysis with Implications for Human-AI Learning Orchestration

**Anticipated or Actual Start Date**: [Month 1, 2026]
**Anticipated Completion Date**: [Month 7, 2026]

---

## Section 2: Reviewers

### 2.1 Contact Person for This Review

**Name**: Hosung You
**Institution**: [Institution Name]
**Address**: [Address]
**Email**: [Email]
**ORCID**: [ORCID ID]

### 2.2 Review Team Members

| Name | Role | Institution | ORCID |
|------|------|-------------|-------|
| Hosung You | Lead researcher; Coder 1; Meta-analyst | [Institution] | [ORCID] |
| Dr. Yang | Co-investigator; Coder 2; Theory lead | [Institution] | [ORCID] |

---

## Section 3: Funding Sources/Sponsors

**Funding**: [Specify funding sources, or "No external funding"]
**Sponsor**: [Institution name if applicable]
**Role of funder**: [Description, or "N/A"]

---

## Section 4: Conflicts of Interest

**Declaration**: [None declared / Specify any conflicts]

---

## Section 5: Review Question

### 5.1 Primary Research Questions

1. **(RQ1)** What is the overall effect of Agentic AI interventions on learning outcomes in educational contexts (Hedges' g)?

2. **(RQ2)** How does the level of human oversight (fully autonomous vs. AI-led with checkpoints vs. human-led with AI support) moderate the effect of Agentic AI on learning outcomes?

3. **(RQ3)** What is the difference in learning outcome effect sizes between single-agent and multi-agent AI systems?

4. **(RQ4)** How do learning contexts (K-12, higher education, workplace training, professional education, continuing education) moderate the effectiveness of Agentic AI interventions?

5. **(RQ5)** What evidence-based design principles for AI agent-based learning support systems (HALO Framework) are implied by the meta-analytic findings?

### 5.2 PICOS Framework

| Element | Specification |
|---------|--------------|
| **Population** | Learners in formal and informal educational contexts (K-12, higher education, workplace, professional, continuing education) |
| **Intervention** | AI agent systems with autonomous action capability (adaptive response, proactive intervention, automated assessment, recommendation generation, dialogue management, or multi-agent coordination) |
| **Comparison** | No AI agent; non-agentic AI; traditional instruction; or different AI agency level |
| **Outcomes** | Cognitive learning outcomes (knowledge, comprehension); skill-based outcomes (procedural, problem-solving); affective outcomes (motivation, self-efficacy, engagement); performance outcomes (transfer, job performance) |
| **Study Design** | Randomized controlled trials, quasi-experimental studies, pre-post comparison designs |

---

## Section 6: Searches

### 6.1 Databases

The following databases will be searched:

1. Web of Science (Core Collection)
2. Scopus
3. ERIC (Education Resources Information Center)
4. PsycINFO (via APA PsycNet or EBSCOhost)
5. IEEE Xplore
6. ACM Digital Library

### 6.2 Search Terms

**Block 1: AI Agent Intervention**
```
"AI agent*" OR "intelligent agent*" OR "virtual agent*" OR "agentic AI"
OR "intelligent tutoring system*" OR "AI-powered agent*"
OR "pedagogical agent*" OR "conversational agent*"
OR "AI chatbot*" OR "multi-agent system*" OR "AI assistant*" OR "AI tutor*"
```

**Block 2: Learning Outcome**
```
"learning outcome*" OR "academic achievement" OR "academic performance"
OR "knowledge gain*" OR "skill acquisition" OR "learning gain*"
OR "test score*" OR "assessment" OR "motivation" OR "self-efficacy"
OR "engagement" OR "performance"
```

**Block 3: Educational Context**
```
"education*" OR "training" OR "learning" OR "instruction" OR "teaching"
OR "workplace" OR "professional development" OR "K-12"
OR "higher education" OR "university" OR "college" OR "workforce"
```

**Combined**: Block 1 AND Block 2 AND Block 3

### 6.3 Date Range

**Publication years**: 2018-2025

**Rationale**: 2018 marks the beginning of practical AI agent implementation in education following the transformer era (Vaswani et al., 2017). This range captures the shift from rule-based to AI/ML-powered agents and excludes the pre-agentic era covered by Ma et al. (2014).

### 6.4 Additional Searches

- Backward citation tracking from all included studies
- Forward citation tracking of key seed articles (Dai et al., 2024; Ma et al., 2014; Yang, 2025; Yan, 2025)
- Hand search of: *Computers & Education*, *International Journal of AI in Education*, *Educational Psychology Review*
- Grey literature: ProQuest Dissertations; Google Scholar; EdArXiv; SSRN

---

## Section 7: Study Selection Criteria

### 7.1 Inclusion Criteria

| Criterion | Description |
|-----------|-------------|
| **IC1: Study Design** | Experimental (RCT), quasi-experimental, or pre-post designs that allow quantitative effect size calculation |
| **IC2: Intervention** | AI agent with at least one of six autonomous capabilities (adaptive response, proactive intervention, automated assessment, recommendation, dialogue management, multi-agent coordination) |
| **IC3: Comparison** | Includes a valid comparison: no AI, non-agentic AI, traditional instruction, or different AI agency level |
| **IC4: Outcome** | Reports at least one quantitative learning outcome (cognitive, skill, affective, or performance) |
| **IC5: Context** | K-12, higher education, workplace training, professional education, or continuing education |
| **IC6: Data** | Sufficient statistics to compute or estimate Hedges' g |
| **IC7: Language** | Published in English |
| **IC8: Publication** | Peer-reviewed journal article or full-text conference proceedings |

### 7.2 Exclusion Criteria

| Criterion | Description |
|-----------|-------------|
| **EC1** | Purely qualitative; case study; survey without intervention |
| **EC2** | AI intervention is not agentic (static content; simple FAQ; non-adaptive) |
| **EC3** | No comparison condition |
| **EC4** | Satisfaction/usability outcomes only |
| **EC5** | Laboratory experiment without educational context |
| **EC6** | Insufficient data even after author contact |
| **EC7** | Non-English publication |
| **EC8** | Non-peer-reviewed source |

---

## Section 8: Study Selection

### 8.1 Screening Process

**Phase 1: Title and Abstract Screening**
- Two independent reviewers
- Platform: Covidence
- Conflict resolution: Discussion; third reviewer if unresolved
- Inter-rater reliability: Cohen's kappa calculated; target κ ≥ 0.80

**Phase 2: Full-Text Screening**
- Two independent reviewers
- All inclusion criteria systematically applied
- Exclusion reason documented for each excluded study
- Inter-rater reliability: Cohen's kappa; target κ ≥ 0.80

**Pilot screening**: 50 records screened jointly before independent screening begins.

---

## Section 9: Data Extraction

### 9.1 Data Items

Data will be extracted for:

**Study Characteristics**: Author, year, journal, country, publication type

**Study Design**: Research design, random assignment, control condition type, duration, sample sizes, attrition

**AI Agent Characteristics** (Key Moderators):
- Human oversight level (1=Fully autonomous, 2=AI-led with checkpoints, 3=Human-led with AI support)
- Agent architecture (1=Single agent, 2=Multi-agent system)
- Agency level — APCP Framework (1=Adaptive, 2=Proactive, 3=Co-Learner, 4=Peer)
- Agent role (1=Tutor, 2=Coach, 3=Assessor, 4=Collaborator, 5=Facilitator, 6=Multiple)
- Agent modality (1=Text, 2=Voice, 3=Embodied, 4=Mixed)
- AI technology (1=Rule-based, 2=ML, 3=NLP, 4=LLM, 5=RL, 6=Hybrid)
- Adaptivity level (1=Static, 2=Performance, 3=Behavior, 4=Affect, 5=Multi-dimensional)

**Learning Context**: Context type, subject domain, learning mode, delivery format

**Learning Outcome**: Outcome type, Bloom's taxonomy level, measurement type, measurement timing

**Effect Size Data**: Means, SDs, sample sizes, t/F/r/OR statistics, computed Hedges' g

**Risk of Bias**: 7-domain assessment per Cochrane RoB 2.0 (adapted)

### 9.2 Data Extraction Process

- Two independent coders
- Standardized Excel/Google Sheets template
- Pilot coding (5 studies) before full independent coding
- 20% stratified random sample for intercoder reliability (Cohen's kappa ≥ 0.80)
- All discrepancies resolved through discussion; arbitrator if needed
- Authors contacted for missing data (one email; 2-week window)

---

## Section 10: Risk of Bias Assessment

**Tool**: Cochrane Risk of Bias 2.0 adapted for educational intervention research

**Domains Assessed**:
1. Randomization process
2. Allocation concealment
3. Blinding of participants
4. Blinding of outcome assessors
5. Incomplete outcome data
6. Selective reporting
7. Other sources of bias

**Assessment**: Both coders independently; disagreements resolved by consensus.

---

## Section 11: Strategy for Data Synthesis

### 11.1 Effect Size Metric

**Primary metric**: Hedges' g (bias-corrected standardized mean difference)

**Direction**: Positive g = AI agent condition outperforms comparison

**Computation**:
- From M and SD: pooled SD formula with J correction
- From t, F, r, OR: established conversion formulas (Morris & DeShon, 2002)
- Pre-post designs: Morris & DeShon (2002) Equation 8

### 11.2 Synthesis Model

**Primary**: Random-effects model (REML estimator) with 3-level extension for dependent effect sizes (Van den Noortgate et al., 2013)

**Robustness check**: Robust Variance Estimation with clubSandwich small-sample corrections (Pustejovsky & Tipton, 2022)

**Heterogeneity**: Q-statistic, I², τ², prediction interval

### 11.3 Moderator Analysis Plan

| Moderator | Type | Method |
|-----------|------|--------|
| Human oversight level | Categorical (3 levels) | Subgroup analysis; omnibus test |
| Agent architecture | Categorical (2 levels) | Subgroup analysis |
| Learning context | Categorical (5 levels) | Subgroup analysis; omnibus test |
| Agent role | Categorical (6 levels) | Subgroup analysis |
| Outcome type | Categorical (4 levels) | Subgroup analysis |
| Bloom's level | Ordinal (3 levels) | Subgroup analysis |
| AI technology | Categorical (6 levels) | Subgroup analysis |
| Duration (weeks) | Continuous | Meta-regression |
| Publication year | Continuous | Meta-regression |

**Minimum cell size**: k ≥ 4 per subgroup for valid inference.

**Multiple testing**: Benjamini-Hochberg FDR correction applied across moderator tests.

### 11.4 Publication Bias Assessment

- Funnel plot visual inspection
- Egger's test for funnel plot asymmetry
- Trim-and-fill method (Duval & Tweedie, 2000)
- PET-PEESE (Stanley & Doucouliagou, 2012)
- Step function selection models (Vevea & Woods, 2005)

### 11.5 Sensitivity Analyses

- Leave-one-out influence analysis
- Restriction to low risk of bias studies (rob_overall = 2)
- Alternative assumed pre-post correlation (r = 0.50, 0.70, 0.90)
- Alternative assumed RVE working correlation (ρ = 0.50, 0.70, 0.80, 0.90)

### 11.6 Software

R (≥ 4.3.0); packages: `metafor`, `robumeta`, `clubSandwich`, `dmetar`

---

## Section 12: Expected Number of Studies

**Expected total hits (pre-deduplication)**: 7,500-13,000
**Expected after deduplication**: 4,000-8,000
**Expected after title/abstract screening**: 200-400
**Expected included studies**: 40-80
**Expected effect sizes**: 100-200

**Rationale**: Dai et al. (2024) found k=22 for AI agents in simulations only; Ma et al. (2014) extracted 107 effect sizes for ITS alone. Our broader scope and 7-year window (2018-2025) during rapid growth of AI education research justifies higher estimates.

---

## Section 13: Amendments

Any amendments to the protocol after registration will be:
1. Logged in PROSPERO with date and rationale
2. Documented in `06_decisions/decision_log.md`
3. Reported as deviations in the published manuscript

---

## Section 14: Dissemination Plans

**Primary**: Peer-reviewed journal article in Educational Research Review or Computers & Education

**Secondary**:
- Pre-print on SSRN or EdArXiv after submission
- Conference presentation at AIED, LAK, or AERA
- Open data and materials on OSF or Zenodo

---

*This pre-registration template follows PROSPERO guidelines. Complete the registration at https://www.crd.york.ac.uk/prospero/ before conducting the systematic search.*
