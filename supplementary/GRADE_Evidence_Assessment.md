# GRADE Evidence Quality Assessment

## Overview

The GRADE (Grading of Recommendations, Assessment, Development and Evaluations) approach provides a systematic methodology for assessing the certainty of evidence in meta-analyses and systematic reviews. GRADE evaluates evidence quality by considering study limitations, consistency of results, directness of evidence, precision of effect estimates, and likelihood of publication bias.

For this meta-analysis examining the effects of Agentic AI on learning outcomes, GRADE assessments are conducted per outcome across studies using random-effects meta-analysis with Hedges' g as the effect size metric. Evidence starts at "High" certainty and may be downgraded based on specific criteria, or upgraded in cases of exceptionally strong evidence.

---

## GRADE Assessment Criteria

### Downgrade Factors (Each can lower certainty by 1-2 levels)

| Factor | Description | Assessment Method | Thresholds |
|--------|-------------|-------------------|-----------|
| **Risk of Bias** | Study-level methodological quality and risk of bias | RoB 2.0 (for RCTs); ROBINS-I (for quasi-experimental); Cochrane risk of bias tool | <25% studies high risk = no downgrade; 25-50% = -1 level; >50% = -2 levels |
| **Inconsistency** | Unexplained heterogeneity in effect estimates across studies | I² statistic; prediction intervals; subgroup consistency; visual inspection of forest plot | I² <50% = no downgrade; I² 50-75% = -1 level; I² >75% = -2 levels; or PI excludes null/benefit |
| **Indirectness** | Mismatch between study population/intervention/outcome and research question | Comparison of PICOS (Population, Intervention, Comparator, Outcome, Study design) across studies | Direct evidence for all PICOS = no downgrade; partially indirect = -1 level; substantially indirect = -2 levels |
| **Imprecision** | Wide confidence intervals or insufficient sample size to detect clinically important effects | 95% CI width; optimal information size (OIS); sample size calculations | CI excludes both null and minimally important difference (MID) = no downgrade; CI includes null OR MID = -1 level; narrow N or very wide CI = -2 levels |
| **Publication Bias** | Suspected non-random publication of studies, favoring positive results | Funnel plot visual inspection; Egger's test (p < 0.05); trim-and-fill analysis; PET-PEESE regression | No asymmetry = no downgrade; possible asymmetry = -1 level; strong evidence of bias = -2 levels |

### Upgrade Factors (Each can raise certainty by 1 level; max +2)

| Factor | Description | Assessment Method | Threshold |
|--------|-------------|-------------------|-----------|
| **Large Effect Size** | Observed effect is large and clinically/educationally meaningful | Cohen's d interpretation: small (0.2), medium (0.5), large (0.8) | Hedges' g ≥ 0.80 = +1; Hedges' g ≥ 1.20 = +2 |
| **Dose-Response Gradient** | Monotonic relationship between intervention intensity/duration and outcome magnitude | Visual inspection of dose-response plot; meta-regression on dose/duration variable | Clear monotonic relationship = +1 |
| **Plausible Confounding** | Known confounders would likely bias results *away* from observed effect, strengthening true effect | Narrative review of unmeasured confounders in study contexts; direction of potential bias | Plausible residual confounding would reduce effect = +1 |

---

## Evidence Profile Template

Use this table to record GRADE assessments for each outcome. Each row represents a unique outcome with associated meta-analytic summary.

### Template Structure

| Outcome | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|---------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| [Outcome Name] | [k] | [N] | [–/–1/–2] | [–/–1/–2] | [–/–1/–2] | [–/–1/–2] | [–/–1/–2] | High/Moderate/Low/Very Low | [g, 95% CI] | High/Moderate/Low/Very Low |

### Primary Outcomes

#### Overall Learning Outcomes
| Outcome | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|---------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| Overall learning outcomes (all contexts, all measures) | [k] | [N] | | | | | | | | |

#### Cognitive Outcomes (Knowledge & Academic Performance)
| Outcome | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|---------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| Knowledge retention/comprehension | [k] | [N] | | | | | | | | |
| Academic test performance | [k] | [N] | | | | | | | | |
| Problem-solving accuracy | [k] | [N] | | | | | | | | |

#### Skill-Based Outcomes
| Outcome | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|---------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| Complex skill development | [k] | [N] | | | | | | | | |
| Critical thinking/analysis | [k] | [N] | | | | | | | | |
| Collaborative skills | [k] | [N] | | | | | | | | |

#### Affective Outcomes
| Outcome | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|---------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| Student motivation/engagement | [k] | [N] | | | | | | | | |
| Self-efficacy | [k] | [N] | | | | | | | | |
| Attitude toward learning | [k] | [N] | | | | | | | | |

### Secondary Outcomes (Subgroup Analyses)

#### RQ2: Effect of Human Oversight Level
| Oversight Level | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|-----------------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| High oversight (human-in-the-loop) | [k] | [N] | | | | | | | | |
| Moderate oversight (human monitoring) | [k] | [N] | | | | | | | | |
| Low oversight (autonomous) | [k] | [N] | | | | | | | | |
| No oversight (baseline/control) | [k] | [N] | | | | | | | | |

#### RQ3: Effect by Agent Architecture
| Architecture Type | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|------------------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| Retrieval-augmented generation (RAG) | [k] | [N] | | | | | | | | |
| Reinforcement learning from human feedback (RLHF) | [k] | [N] | | | | | | | | |
| Chain-of-thought / reasoning agents | [k] | [N] | | | | | | | | |
| Multi-agent systems | [k] | [N] | | | | | | | | |
| Tool-use / agentic action agents | [k] | [N] | | | | | | | | |

#### RQ4: Effect by Learning Context
| Context | # Studies | N Participants | Risk of Bias | Inconsistency | Indirectness | Imprecision | Pub Bias | Overall Quality | Hedges' g (95% CI) | GRADE Rating |
|---------|-----------|----------------|--------------|---------------|--------------|-------------|----------|-----------------|-------------------|--------------|
| K-12 education | [k] | [N] | | | | | | | | |
| Higher education | [k] | [N] | | | | | | | | |
| Professional/corporate training | [k] | [N] | | | | | | | | |
| Online/distance learning | [k] | [N] | | | | | | | | |
| In-person/classroom learning | [k] | [N] | | | | | | | | |
| Hybrid learning environments | [k] | [N] | | | | | | | | |

---

## GRADE Rating Scale

### Certainty of Evidence Levels

**HIGH:** Very confident that the true effect is close to the estimate of the effect. Further research is very unlikely to change the conclusion.
- Typically based on: RCTs with minimal risk of bias, consistent results, direct evidence, precise estimates, no publication bias.
- May be downgraded if concerns exist for any of the five domains.

**MODERATE:** Moderately confident in the effect estimate. The true effect is likely to be close to the estimate, but there is a possibility it is substantially different. Further research may change the conclusion.
- Typically based on: RCTs with some concerns, or observational studies with particularly strong designs and/or effects.
- Usually one downgrade factor (e.g., –1 for risk of bias or inconsistency).

**LOW:** Limited confidence in the effect estimate. The true effect may be substantially different from the estimate. Further research is likely to have an important impact on the confidence in the estimate and may change the conclusion.
- Typically based on: Observational studies, RCTs with serious limitations, or indirect evidence.
- Usually two downgrade factors (e.g., –1 for risk of bias and –1 for inconsistency).

**VERY LOW:** Very little confidence in the effect estimate. The true effect is likely to be substantially different from the estimate. Any estimate of effect is very uncertain.
- Typically based on: Case studies, non-comparative observational data, or evidence with multiple serious limitations.
- Usually three or more downgrade factors, or studies rated as high risk across multiple domains.

---

## Decision Rules for Downgrade/Upgrade Assessment

### Risk of Bias Decision Rule

1. **No Downgrade (0 levels):** ≤25% of studies rated high risk of bias on summary across all domains (selection, performance, detection, attrition, reporting).
2. **Downgrade 1 Level:** 25–50% of studies high risk; or one critical domain with >50% high risk.
3. **Downgrade 2 Levels:** >50% of studies high risk; or multiple critical domains with high risk; or detection bias + attrition bias co-occurring.

**Tools:**
- RCTs: Cochrane RoB 2.0 (randomization process, deviations from intended intervention, missing outcome data, measurement of outcome, selection of reported result)
- Quasi-experimental: ROBINS-I (confounding, selection bias, classification of intervention, deviations, missing data, measurement, reporting)

### Inconsistency Decision Rule

1. **No Downgrade (0 levels):** I² <50%; prediction interval includes the null effect but not the point estimate; subgroups agree on direction and magnitude.
2. **Downgrade 1 Level:** I² 50–75%; prediction interval heterogeneity explains some but not all variance; one subgroup diverges substantially.
3. **Downgrade 2 Levels:** I² >75%; prediction interval wide and excludes point estimate; multiple subgroups diverge; conflicting directions of effect.

**Tools:**
- I² calculation (% variance explained by heterogeneity)
- Prediction intervals (95% range of true effects in future studies)
- Visual inspection: Q-test and tau² estimates
- Subgroup consistency: test for subgroup interaction (p < 0.05 suggests inconsistency)

### Indirectness Decision Rule

1. **No Downgrade (0 levels):** All studies directly address PICOS; population, intervention, comparator, and outcomes match research questions closely.
2. **Downgrade 1 Level:** Some studies address PICOS indirectly (e.g., proxy population, surrogate outcome, slightly different intervention); or mixture of direct and indirect evidence.
3. **Downgrade 2 Levels:** Most or all studies are indirect (e.g., learning context differs markedly, outcome is surrogate, agent architecture differs substantially from research question).

**Assessment:**
- Population: Educational stage, learner characteristics
- Intervention: Agent autonomy level, architecture type, mode of integration
- Comparator: Baseline/control condition (e.g., traditional instruction, no AI)
- Outcome: Measured constructs match outcome domains (knowledge, skills, affect)
- Study design: Experimental vs. observational

### Imprecision Decision Rule

1. **No Downgrade (0 levels):** 95% CI excludes both the null effect (0) and minimally important difference (MID); optimal information size (OIS) met; N ≥ 400 total across studies.
2. **Downgrade 1 Level:** 95% CI includes the null effect OR crosses the MID; or OIS not met (N = 100–400); sample size marginal.
3. **Downgrade 2 Levels:** 95% CI very wide (includes null AND MID, or CI ratio >2); OIS seriously unmet (N < 100); single small study.

**Determination of MID:**
- Effect sizes: Small MID = 0.2 (Cohen's d); Medium MID = 0.5; Large MID = 0.8
- Educational context: Consensus-based or stakeholder engagement to define educationally meaningful effect size (e.g., g ≥ 0.5 = meaningful improvement in learning)

**OIS Calculation:**
- For continuous outcomes: OIS = (2 × Z_α/2 + Z_β)² × (σ₁² + σ₂²) / (μ₁ – μ₂)²
- Typical threshold for meta-analyses: N ≥ 400 overall

### Publication Bias Decision Rule

1. **No Downgrade (0 levels):** Funnel plot symmetric; Egger's test p > 0.10; no evidence of selective reporting; prospective protocol available.
2. **Downgrade 1 Level:** Funnel plot mildly asymmetric; Egger's test 0.05 < p ≤ 0.10; trim-and-fill suggests up to 10% missing studies; selective outcome reporting suspected.
3. **Downgrade 2 Levels:** Funnel plot strongly asymmetric; Egger's test p < 0.05; trim-and-fill suggests >10% missing studies; PET-PEESE suggests substantial bias.

**Tools:**
- Funnel plot: Scatter plot of effect size vs. precision (1/SE); asymmetry suggests bias
- Egger's test: Linear regression of standardized effect size on precision (H₀: no bias; p < 0.05 suggests bias)
- Trim-and-fill: Nonparametric method to estimate number of missing studies; recalculates effect excluding imputed studies
- PET-PEESE: Precision-Effect Test and Precision-Effect Estimate with Standard Error; meta-regression to assess bias-adjusted effect

### Large Effect Size Upgrade Rule

1. **Upgrade 1 Level:** Hedges' g ≥ 0.80 (large effect by Cohen's conventions); statistically significant; 95% CI excludes null.
2. **Upgrade 2 Levels:** Hedges' g ≥ 1.20 (very large effect); consistent across studies; narrow 95% CI; high certainty despite other concerns.

**Interpretation:**
- 0.2 = small effect
- 0.5 = medium effect
- 0.8 = large effect
- 1.2+ = very large effect

### Dose-Response Gradient Upgrade Rule

1. **Upgrade 1 Level:** Clear monotonic relationship between intervention intensity (e.g., agent autonomy level, training duration, interaction frequency) and outcome effect size; meta-regression p < 0.05; visual inspection shows linear trend across subgroups.

**Assessment:**
- Plot effect size (Hedges' g) vs. dose variable (e.g., weeks of intervention, level of autonomy on ordinal scale)
- Conduct meta-regression with dose as predictor; test significance of slope
- Examine subgroup effects ordered by dose; confirm monotonicity

### Plausible Confounding Upgrade Rule

1. **Upgrade 1 Level:** Narrative review identifies plausible residual confounders that would bias results *away from* the observed effect (e.g., selection bias toward more motivated learners, unmeasured prior knowledge). Direction and magnitude of potential bias support genuine protective/beneficial effect.

**Assessment:**
- Identify unmeasured confounders from study contexts (e.g., learner motivation, prior knowledge, teacher quality)
- Evaluate direction of bias: Would confounding inflate or reduce observed effect?
- If confounding would reduce effect, true effect is likely larger than estimate → upgrade feasible
- Document in Evidence Profile with rationale

---

## Summary Assessment Workflow

1. **Extract Data:** For each outcome, extract study characteristics, risk of bias ratings, effect sizes (Hedges' g with 95% CI), heterogeneity statistics (I², tau²), and sample size.

2. **Assess Risk of Bias:** Use RoB 2.0 (RCTs) or ROBINS-I (quasi-experimental) for each study; summarize proportion high risk.

3. **Check Consistency:** Calculate I²; compute prediction interval; visually inspect forest plot; examine subgroup agreement.

4. **Evaluate Directness:** Compare PICOS across studies to research questions; flag indirect evidence.

5. **Examine Precision:** Compute 95% CI width; determine MID; check OIS; assess CI crossing null or MID.

6. **Inspect Publication Bias:** Create funnel plot; conduct Egger's test; consider trim-and-fill; check trial registries for unpublished studies.

7. **Consider Upgrades:** Assess effect size magnitude, dose-response relationships, and direction of residual confounding.

8. **Assign GRADE Rating:** Start at High; apply downgrades (max –2 per domain); apply upgrades (max +2 total); assign final certainty rating.

9. **Document Justification:** Record specific threshold values and reasoning in Evidence Profile notes column.

---

## References

1. Guyatt, G. H., Oxman, A. D., Vist, G. E., et al. (2008). GRADE: An emerging consensus on rating quality of evidence and strength of recommendations. *British Medical Journal*, 336(7650), 924–926.

2. Schünemann, H., Brożek, J., Guyatt, G., & Oxman, A. (Eds.). (2013). *GRADE handbook for grading quality of evidence and strength of recommendations*. Retrieved from https://gdt.gradepro.org/app/handbook/handbook.html

3. Higgins, J. P. T., & Green, S. (Eds.). (2011). *Cochrane handbook for systematic reviews of interventions* (Version 5.1.0). Cochrane Collaboration.

4. Sterne, J. A. C., Savović, J., Page, M. J., et al. (2019). RoB 2: A revised tool for assessing risk of bias in randomised trials. *BMJ*, 366, l4898.

5. Sterne, J. A. C., Hernán, M. A., Reeves, B. C., et al. (2016). ROBINS-I: A tool for assessing risk of bias in non-randomised studies of interventions. *BMJ*, 355, i4919.

6. Borenstein, M., Hedges, L. V., Higgins, J. P. T., & Rothstein, H. R. (2009). *Introduction to meta-analysis*. John Wiley & Sons.

7. Egger, M., Davey Smith, G., Schneider, M., & Minder, C. (1997). Bias in meta-analysis detected by a simple, graphical test. *BMJ*, 315(7109), 629–634.

8. Duval, S., & Tweedie, R. (2000). Trim and fill: A simple funnel-plot-based method of testing and adjusting for publication bias in meta-analysis. *Biometrics*, 56(2), 455–463.

9. Stanley, T. D., & Doucouliagos, H. (2014). Meta-regression approximations to reduce publication bias. *Research Synthesis Methods*, 5(2), 111–125.

10. Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Lawrence Erlbaum Associates.

---

**Document Version:** 1.0
**Date Created:** 2026-02-16
**Purpose:** Standardized GRADE assessment for meta-analysis of Agentic AI effects on learning outcomes
