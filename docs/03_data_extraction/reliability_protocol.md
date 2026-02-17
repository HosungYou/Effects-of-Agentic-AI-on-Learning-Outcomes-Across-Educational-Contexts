# Intercoder Reliability Protocol

## Overview

This document specifies the intercoder reliability (ICR) protocol for the two-coder meta-analysis coding process. Reliable coding is essential for the validity of meta-analytic findings. All reliability statistics will be reported in the published manuscript.

---

## 1. Reliability Framework

### 1.1 Standards

This protocol targets reliability standards consistent with best practices in meta-analysis (Pigott & Polanin, 2020; Card, 2012):

| Variable Type | Statistic | Minimum Acceptable | Target |
|---------------|-----------|:-----------------:|:------:|
| Categorical (nominal) | Cohen's kappa (κ) | κ ≥ 0.70 | κ ≥ 0.80 |
| Continuous (numeric) | Intraclass Correlation Coefficient (ICC) | ICC ≥ 0.85 | ICC ≥ 0.90 |
| Dichotomous | Cohen's kappa (κ) | κ ≥ 0.80 | κ ≥ 0.90 |

### 1.2 Roles

| Role | Responsibility |
|------|----------------|
| **Coder 1 (Primary)** | Hosung You — manages coding template, assigns study IDs, codes all studies, leads conflict resolution |
| **Coder 2 (Independent)** | Dr. Yang — independently codes all studies (or 20% reliability sample), participates in conflict resolution |
| **Arbitrator** | Project supervisor — resolves unresolvable conflicts; provides binding decisions |

---

## 2. Reliability Sample Design

### 2.1 Sample Size and Strategy

**Standard for ICR**: Code a minimum of **20% of the total included study set** for reliability.

If final study set = 40-80 studies, reliability sample = **8-16 studies**.

**Stratified random sampling** to ensure the reliability sample represents:

| Stratum | Criteria | Target Proportion |
|---------|----------|:-----------------:|
| Educational context | At least 1 study per context (K-12, HE, Workplace) | Proportional to full set |
| AI oversight level | At least 2 studies per oversight level | Proportional to full set |
| Study design | At least 1 RCT, 1 quasi-experimental, 1 pre-post | Proportional to full set |
| Publication year | Spread across 2018-2025 | Proportional to full set |

### 2.2 Random Selection Procedure

1. After full coding by Coder 1, generate random numbers in R:
   ```r
   set.seed(20250216)  # Use date of coding completion
   sample_ids <- sample(1:total_studies, size = ceiling(total_studies * 0.20))
   ```
2. Check stratification criteria — resample if any stratum is underrepresented
3. Send selected study IDs to Coder 2 without sharing Coder 1's decisions

### 2.3 Full vs. Sample Coding

| Option | Description | Recommendation |
|--------|-------------|----------------|
| **Full double-coding** | Both coders independently code ALL studies | Preferred for highest reliability; required if study set < 60 |
| **Sample double-coding** | Both coders independently code 20% sample; Coder 1 codes remaining 80% | Acceptable if study set ≥ 60 and resources limited |

**Decision**: If study set ≤ 60 studies → full double-coding. If study set > 60 → 20% stratified sample.

---

## 3. Training Procedure

### 3.1 Pre-Training Materials

Before any coding, both coders review:
1. `03_data_extraction/coding_manual.md` — complete coding manual
2. `03_data_extraction/effect_size_extraction_guide.md` — effect size procedures
3. `02_study_selection/inclusion_exclusion_criteria.md` — final inclusion criteria
4. 3-5 published educational AI studies as examples (provided in shared folder)

### 3.2 Training Session 1: Conceptual Review (90 minutes)

**Agenda**:
1. Review each coding variable definition (30 min)
2. Discuss borderline cases from inclusion/exclusion criteria (20 min)
3. Discuss anticipated ambiguous situations per variable (20 min)
4. Q&A and consensus building on decision rules (20 min)

**Output**: Updated decision rules documented in coding manual

### 3.3 Pilot Coding Round 1 (5 studies)

**Procedure**:
1. Select 5 diverse studies from included set (mix of contexts, designs, AI types)
2. Both coders independently code all variables for all 5 studies
3. No discussion during independent coding
4. Coders meet to compare decisions and compute kappa

**Meeting agenda**:
- Compare all categorical decisions (1-2 hours)
- Identify variables with lowest agreement
- Discuss each discrepancy with reference to the study text and coding manual
- Revise decision rules if needed (document all revisions)

### 3.4 Calibration Session After Pilot

**If kappa < 0.70 on any variable**:
- Rewrite the operational definition for that variable
- Add concrete decision examples to the coding manual
- Conduct another 5-study pilot round on NEW studies

**If 0.70 ≤ kappa < 0.80**:
- Review specific discrepancies
- Add clarifying examples to coding manual
- Proceed to independent coding with increased vigilance on weak variables

**If kappa ≥ 0.80 on all variables**:
- Proceed to full independent coding

### 3.5 Calibration Studies

Document which 5 studies were used for calibration (cannot be reused for reliability assessment):

| Calibration Study | Author | Year | Context | Design | Notes |
|-------------------|--------|------|---------|--------|-------|
| 1 | [TBD] | [TBD] | [TBD] | [TBD] | |
| 2 | [TBD] | [TBD] | [TBD] | [TBD] | |
| 3 | [TBD] | [TBD] | [TBD] | [TBD] | |
| 4 | [TBD] | [TBD] | [TBD] | [TBD] | |
| 5 | [TBD] | [TBD] | [TBD] | [TBD] | |

---

## 4. Independent Coding Phase

### 4.1 Independence Rules

During independent coding:
- **No discussion** of coding decisions between coders
- Each coder works from their own copy of the coding template
- Coders may ask clarifying questions about the coding MANUAL (not specific study decisions) via email — all Q&A documented
- Coders use the "notes" column to document rationale for ambiguous decisions

### 4.2 Timeline

| Activity | Coder 1 Deadline | Coder 2 Deadline |
|----------|:----------------:|:----------------:|
| Pilot round 1 (5 studies) | Week 13, Day 3 | Week 13, Day 3 |
| Calibration meeting | Week 13, Day 5 | Week 13, Day 5 |
| Pilot round 2 (if needed) | Week 14, Day 2 | Week 14, Day 2 |
| Full independent coding begins | Week 15 | Week 15 |
| Full independent coding complete | Week 16, end | Week 16, end |

### 4.3 Quality Checks During Coding

Coder 1 checks periodically:
- All required fields are completed (no blanks)
- Numerical data (n, M, SD) passes range checks
- Effect size calculations are verified with R code

---

## 5. Cohen's Kappa Calculation

### 5.1 Formula

```
κ = (Po - Pe) / (1 - Pe)
```

Where:
- **Po** = observed proportion of agreement = (agreements) / (total cases)
- **Pe** = expected proportion by chance = sum of (marginal proportion × marginal proportion) for each category

### 5.2 R Code for Kappa

```r
library(irr)

# For any categorical variable
# Create two vectors of coder decisions
coder1_oversight <- c(1, 2, 1, 3, 2, 1, 3, 2, 1, 1)  # example
coder2_oversight <- c(1, 2, 1, 3, 1, 1, 3, 2, 1, 2)  # example

# Cohen's kappa
kappa_result <- kappa2(cbind(coder1_oversight, coder2_oversight))
print(kappa_result)
# Output: Kappa statistic, z-value, p-value

# Weighted kappa (for ordinal variables like agency_level)
kappa_weighted <- kappa2(cbind(coder1_oversight, coder2_oversight),
                         weight = "equal")  # or "squared"
print(kappa_weighted)

# For all variables at once
coding_data <- data.frame(
  c1_oversight = coder1_oversight,
  c2_oversight = coder2_oversight
  # add other variables...
)

# Loop through all variable pairs
variables <- c("oversight_level", "architecture", "agency_level",
               "agent_role", "modality", "technology", "adaptivity",
               "context", "domain", "outcome_type", "blooms_level",
               "measurement_type", "timing", "design", "control_type")

kappa_results <- data.frame(variable = variables,
                             kappa = NA, z = NA, p = NA)
```

### 5.3 Kappa Calculation Schedule

| Checkpoint | When | Variables |
|------------|------|-----------|
| **Pilot kappa** | After 5-study pilot | All categorical variables |
| **Interim kappa** | After 20% of studies coded | All categorical variables |
| **Final kappa** | After all double-coded studies | All categorical variables |

---

## 6. Intraclass Correlation Coefficient (ICC) for Continuous Variables

### 6.1 Variables Requiring ICC

| Variable | Type | Rationale |
|----------|------|-----------|
| `duration_weeks` | Continuous | Judgment required in unit conversion |
| `n_treatment`, `n_control` | Integer | Should be identical; ICC verifies exact extraction |
| `mean_treatment`, `mean_control` | Continuous | Extracted from tables/figures |
| `sd_treatment`, `sd_control` | Continuous | Most variable in extraction |
| `hedges_g` | Continuous | Final computed effect size |
| `attrition_rate` | Continuous (0-1) | Requires calculation |

### 6.2 ICC Formula and Interpretation

Use **two-way mixed effects, absolute agreement, single rater** ICC:

```r
library(irr)
library(psych)

# ICC for effect size values
g_data <- data.frame(
  coder1 = c(0.45, 0.72, 0.31, 0.88, 0.52),  # example g values
  coder2 = c(0.47, 0.70, 0.33, 0.85, 0.55)
)

icc_result <- icc(g_data, model = "twoway", type = "agreement",
                  unit = "single")
print(icc_result)
# Look for: ICC estimate, 95% CI, F-test
```

| ICC Value | Interpretation |
|:---------:|----------------|
| < 0.50 | Poor |
| 0.50-0.75 | Moderate |
| 0.75-0.90 | Good |
| > 0.90 | Excellent |

**Target**: ICC > 0.90 for all continuous variables

---

## 7. Conflict Resolution Protocol

### 7.1 After Reliability Assessment

1. List all discrepancies (study × variable pairs where coders disagree)
2. Sort by variable (identify systematic vs. random discrepancy patterns)
3. For each discrepancy:
   a. Both coders re-read relevant section of paper independently
   b. Both coders write their rationale citing specific text
   c. Discuss until consensus or escalate

### 7.2 Resolution Decision Documentation

For each resolved discrepancy:

```
Study: [Author, Year], ES_ID: [id]
Variable: [variable name]
Coder 1 decision: [code] — Rationale: [text from paper]
Coder 2 decision: [code] — Rationale: [text from paper]
Resolution: [final code]
Method: [Discussion consensus / Third-party / Coin flip for truly ambiguous]
Notes: [any important context]
```

### 7.3 Revising Decision Rules

If a systematic pattern of disagreement reveals an ambiguous decision rule:
1. Both coders draft a revised decision rule
2. Apply the revised rule consistently to ALL studies (retroactively if needed)
3. Document the revision in `06_decisions/decision_log.md` with:
   - Old rule
   - New rule
   - Rationale for change
   - Date of revision

---

## 8. Reliability Reporting

### 8.1 In the Manuscript

Report the following in the Methods section:

1. Number of studies double-coded (or percentage if sample)
2. Cohen's kappa for each categorical variable (or range/average with minimum)
3. ICC for effect size data extraction
4. Number of discrepancies and resolution method
5. Variables with lowest reliability and explanation

**Example reporting text**:
> "Two independent coders coded all/20% of included studies. Cohen's kappa values ranged from κ = [min] to κ = [max] across categorical variables (mean κ = [M]), with the lowest agreement for [variable] (κ = [value]) and the highest for [variable] (κ = [value]). ICC for effect size extraction was [ICC] (95% CI: [lower, upper]). All discrepancies were resolved through discussion, with [N] cases requiring arbitration by a third reviewer."

### 8.2 Reliability Statistics Table

| Variable | κ | 95% CI | Discrepancies | Resolution |
|----------|:-:|:------:|:---:|---------|
| oversight_level | [TBD] | [TBD] | [TBD] | Discussion |
| architecture | [TBD] | [TBD] | [TBD] | Discussion |
| agency_level | [TBD] | [TBD] | [TBD] | Discussion |
| agent_role | [TBD] | [TBD] | [TBD] | Discussion |
| modality | [TBD] | [TBD] | [TBD] | Discussion |
| technology | [TBD] | [TBD] | [TBD] | Discussion |
| adaptivity | [TBD] | [TBD] | [TBD] | Discussion |
| context | [TBD] | [TBD] | [TBD] | Discussion |
| domain | [TBD] | [TBD] | [TBD] | Discussion |
| outcome_type | [TBD] | [TBD] | [TBD] | Discussion |
| blooms_level | [TBD] | [TBD] | [TBD] | Discussion |
| design | [TBD] | [TBD] | [TBD] | Discussion |
| **Effect size (ICC)** | **[TBD]** | **[TBD]** | **[TBD]** | **Discussion** |

---

## 9. Appendices

### Appendix A: Kappa Interpretation Reference

| κ Range | Interpretation | Action Required |
|---------|----------------|----------------|
| < 0.00 | Less than chance | Stop; completely revise criteria |
| 0.00-0.20 | Slight agreement | Stop; major revision needed |
| 0.21-0.40 | Fair agreement | Significant revision; additional training |
| 0.41-0.60 | Moderate agreement | Targeted revision; focused retraining |
| 0.61-0.80 | Substantial agreement | Minor clarification; proceed with caution |
| 0.81-1.00 | Almost perfect agreement | Proceed; report result |

*(Landis & Koch, 1977)*

### Appendix B: Variables by Reliability Difficulty

**High reliability expected** (objective, clearly defined):
- `year`, `n_treatment`, `n_control`, `pub_type`, `random_assignment`

**Moderate reliability expected** (requires judgment):
- `context`, `domain`, `modality`, `technology`, `outcome_type`, `measurement_type`

**Potentially lower reliability** (most subjective):
- `oversight_level`, `agency_level`, `agent_role`, `blooms_level`

Allocate more calibration time to variables in the "potentially lower reliability" category.

---

*References: Card (2012); Pigott & Polanin (2020); Landis & Koch (1977); Shrout & Fleiss (1979)*
