# Meta-Analysis Codebook

## Data Dictionary for All Coding Variables

**Study**: Effects of Agentic AI on Learning Outcomes Across Educational Contexts
**Version**: 1.0
**Date**: 2026-02-16
**Mirrors**: Excel coding template sheets (Study_Info, AI_Characteristics, Context, Outcomes, Effect_Sizes, Risk_of_Bias)

---

## Overview

This codebook defines every variable in the meta-analysis dataset. Each variable entry includes: variable name, data type, value range/codes, operational definition, and example.

**Dataset structure**: One row per effect size (long format). Multiple rows share the same `study_id` when a study reports multiple effect sizes.

---

## Sheet 1: Study Identification (`study_info`)

| Variable Name | Data Type | Values / Range | Definition | Example |
|---------------|-----------|---------------|------------|---------|
| `study_id` | String | "001"–"999" | Unique 3-digit study identifier, zero-padded | "042" |
| `es_id` | String | "[study_id].[seq]" | Unique effect size ID; sequential within study | "042.1", "042.2" |
| `author` | String | Text | First author last name only; add first initial if duplicate | "Smith" or "Smith_J" |
| `year` | Integer | 2018–2025 | Calendar year of publication (not data collection) | 2023 |
| `journal` | String | Text | Full journal/conference name; no abbreviations | "Computers & Education" |
| `country` | String | Text | Country where study was conducted; multiple separated by ";" | "USA" or "China;USA" |
| `pub_type` | Integer | 1–4 | Publication type: 1=Journal article, 2=Conference paper, 3=Dissertation, 4=Other | 1 |
| `doi` | String | Text or NA | Digital Object Identifier; "NA" if unavailable | "10.1016/j.compedu.2023.104700" |
| `notes_study` | String | Text | Any relevant notes about the study as a whole | "Companion paper to Smith (2022)" |

---

## Sheet 2: Study Design (`study_design`)

| Variable Name | Data Type | Values / Range | Definition | Example |
|---------------|-----------|---------------|------------|---------|
| `design` | Integer | 1–4 | Research design: 1=RCT, 2=Quasi-experimental, 3=Pre-post within-subjects, 4=Cross-over | 2 |
| `random_assignment` | Integer | 0–1 | 0=No random assignment, 1=Individual-level random assignment | 0 |
| `cluster_assignment` | Integer | 0–1 | 0=No, 1=Cluster-level random assignment (classrooms/schools) | 1 |
| `control_type` | Integer | 1–5 | Comparison condition: 1=No AI, 2=Non-agentic AI, 3=Different AI agency level, 4=Waitlist, 5=Active AI comparison | 1 |
| `duration_days` | Numeric | 1–999 | Intervention duration in days; convert to weeks in analysis | 42 |
| `duration_weeks` | Numeric | 0.14–142.9 | Intervention duration in weeks (computed from days or reported) | 6 |
| `n_treatment` | Integer | 1–9999 | Post-attrition treatment group sample size (use pre-attrition if post not reported) | 45 |
| `n_control` | Integer | 1–9999 | Post-attrition control group sample size | 43 |
| `n_total` | Integer | 2–99999 | Total sample size (treatment + control) | 88 |
| `attrition_rate` | Numeric | 0.00–1.00 | (Initial N – Final N) / Initial N; 999=Not reported | 0.08 |
| `attrition_n_used` | Integer | 0–1 | 0=Pre-attrition N used (initial), 1=Post-attrition N used (final) | 1 |

---

## Sheet 3: AI Agent Characteristics (`ai_characteristics`)

### Primary Moderator Variables

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `oversight_level` | Integer | 1–3 | Human oversight: 1=Fully autonomous, 2=AI-led with checkpoints, 3=Human-led with AI support | 2 |
| `oversight_notes` | String | Text | Evidence from paper supporting oversight_level code | "System emails instructor when learner fails 3 items" |
| `architecture` | Integer | 1–2 | Agent architecture: 1=Single agent, 2=Multi-agent system | 1 |
| `architecture_notes` | String | Text | Evidence from paper supporting architecture code | "Two distinct agents: tutor-bot and assess-bot" |

### APCP Agency Level

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `agency_level` | Integer | 1–4 | APCP level: 1=Adaptive, 2=Proactive, 3=Co-Learner, 4=Peer | 2 |
| `agency_level_notes` | String | Text | Evidence supporting agency level code | "System proactively suggests hints without request" |

### Agent Role

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `agent_role` | Integer | 1–6 | 1=Tutor, 2=Coach, 3=Assessor, 4=Collaborator, 5=Facilitator, 6=Multiple roles | 1 |
| `agent_role_multiple` | String | Text or NA | If agent_role=6, list all roles (e.g., "Tutor;Coach") | "Tutor;Assessor" |

### Modality and Technology

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `modality` | Integer | 1–4 | 1=Text-only, 2=Voice, 3=Embodied/Avatar, 4=Mixed | 1 |
| `technology` | Integer | 1–6 | 1=Rule-based, 2=ML (non-NLP), 3=NLP (pre-LLM), 4=LLM, 5=RL, 6=Hybrid | 4 |
| `technology_spec` | String | Text | Specific AI system/model mentioned in paper | "GPT-4" or "AutoTutor" |
| `adaptivity` | Integer | 1–5 | Adaptivity: 1=Static, 2=Performance, 3=Behavior, 4=Affect, 5=Multi-dimensional | 2 |
| `llm_model` | String | Text or NA | Specific LLM if identified; "NA" if not LLM | "GPT-4" or "NA" |

---

## Sheet 4: Learning Context (`learning_context`)

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `context` | Integer | 1–5 | 1=K-12, 2=Higher Ed, 3=Workplace, 4=Professional Ed, 5=Continuing/Adult Ed | 2 |
| `context_notes` | String | Text | Population description from paper | "Undergraduate CS students at a U.S. university" |
| `grade_level` | String | Text or NA | Specific grade(s) for K-12; "NA" otherwise | "Grade 5" or "NA" |
| `domain` | Integer | 1–7 | 1=STEM, 2=Language, 3=Medical/Health, 4=Business, 5=ICT/CS, 6=Social Sci/Humanities, 7=Other | 1 |
| `domain_spec` | String | Text | Specific subject within domain | "Introductory Python programming" |
| `mode` | Integer | 1–3 | 1=Formal, 2=Informal, 3=Blended | 1 |
| `format` | Integer | 1–3 | 1=Face-to-face with AI, 2=Fully online, 3=Hybrid | 2 |
| `learner_age_mean` | Numeric | 5–99 or 999 | Mean learner age; 999=Not reported | 21.3 |
| `learner_level` | String | Text | Novice/Intermediate/Advanced if reported; "NA" otherwise | "Novice" |

---

## Sheet 5: Learning Outcomes (`learning_outcomes`)

*Note: One row per effect size. Multiple outcomes from same study → multiple rows.*

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `outcome_type` | Integer | 1–4 | 1=Cognitive/Knowledge, 2=Skill-based, 3=Affective, 4=Performance/Transfer | 1 |
| `outcome_label` | String | Text | Brief label for the specific outcome measured | "Algebra post-test score" |
| `blooms_level` | Integer | 1–3 | 1=Remember-Understand, 2=Apply-Analyze, 3=Evaluate-Create | 2 |
| `measurement_type` | Integer | 1–6 | 1=Standardized test, 2=Researcher-developed test, 3=Performance assessment, 4=Self-report, 5=System-logged, 6=Mixed | 2 |
| `measurement_instrument` | String | Text or NA | Name of instrument if identified | "Mathematics Anxiety Rating Scale" or "NA" |
| `timing` | Integer | 1–3 | 1=Immediate post-test (<1 wk), 2=Delayed post-test (≥1 wk), 3=Transfer test | 1 |
| `timing_delay_weeks` | Numeric | 0–999 or NA | Weeks between intervention end and delayed post-test; "NA" if timing=1 | 4 |

---

## Sheet 6: Effect Size Data (`effect_sizes`)

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `es_type` | Integer | 1–9 | Statistic type: 1=M+SD, 2=t-stat, 3=F-stat (df=1), 4=r, 5=chi-square, 6=OR, 7=Pre-post (Morris), 8=Author-reported d/g, 9=Other | 1 |
| `mean_treatment` | Numeric | Any or NA | Treatment group post-test mean in original scale units | 82.4 |
| `sd_treatment` | Numeric | ≥0 or NA | Treatment group post-test SD | 12.1 |
| `n_treatment_es` | Integer | ≥2 or NA | Treatment group n for this specific effect size | 45 |
| `mean_control` | Numeric | Any or NA | Control group post-test mean | 74.6 |
| `sd_control` | Numeric | ≥0 or NA | Control group post-test SD | 13.8 |
| `n_control_es` | Integer | ≥2 or NA | Control group n for this specific effect size | 43 |
| `mean_pre_treatment` | Numeric | Any or NA | Treatment group pre-test mean; NA if not applicable | 61.2 |
| `sd_pre_treatment` | Numeric | ≥0 or NA | Treatment group pre-test SD | 11.8 |
| `mean_pre_control` | Numeric | Any or NA | Control group pre-test mean | 60.9 |
| `sd_pre_control` | Numeric | ≥0 or NA | Control group pre-test SD | 12.2 |
| `t_value` | Numeric | Any or NA | t-statistic if M+SD not available | 3.24 |
| `f_value` | Numeric | ≥0 or NA | F-statistic (df numerator=1 only) | 10.50 |
| `r_value` | Numeric | -1 to 1 or NA | Point-biserial correlation coefficient | 0.45 |
| `chi_sq` | Numeric | ≥0 or NA | Chi-square statistic | 8.12 |
| `odds_ratio` | Numeric | >0 or NA | Odds ratio | 2.35 |
| `p_value` | Numeric | 0–1 or NA | p-value if reported | 0.002 |
| `pre_post_r` | Numeric | -1 to 1 | Assumed or reported pre-post correlation; 0.70=default | 0.70 |
| `pre_post_r_source` | Integer | 1–3 | 1=Reported in paper, 2=Assumed (0.70 default), 3=Estimated from other statistics | 2 |
| `hedges_g` | Numeric | Any | Computed Hedges' g (positive = AI better) | 0.597 |
| `se_g` | Numeric | ≥0 | Standard error of Hedges' g | 0.218 |
| `var_g` | Numeric | ≥0 | Variance of Hedges' g | 0.048 |
| `ci_lower` | Numeric | Any | 95% CI lower bound | 0.170 |
| `ci_upper` | Numeric | Any | 95% CI upper bound | 1.024 |
| `g_direction` | Integer | 1 or -1 | 1=Positive coded as AI>Control, -1=Sign reversed | 1 |
| `g_notes` | String | Text | Any notes about extraction decisions | "Extracted from Fig. 3; SE converted to SD" |

---

## Sheet 7: Risk of Bias (`risk_of_bias`)

| Variable Name | Data Type | Values | Definition | Example |
|---------------|-----------|--------|------------|---------|
| `rob_random_seq` | Integer | 0–2 | Random sequence generation: 0=High risk, 1=Some concerns, 2=Low risk | 2 |
| `rob_random_seq_notes` | String | Text | Evidence from paper | "Computer-generated random numbers used" |
| `rob_allocation` | Integer | 0–2 | Allocation concealment: 0=High, 1=Some concerns, 2=Low risk | 1 |
| `rob_allocation_notes` | String | Text | Evidence | "Sealed envelopes used" |
| `rob_blind_part` | Integer | 0–2 | Blinding of participants: 0=High, 1=Some concerns (usually for ed research), 2=Low | 1 |
| `rob_blind_outcome` | Integer | 0–2 | Blinding of outcome assessors | 0 |
| `rob_incomplete` | Integer | 0–2 | Incomplete outcome data (attrition): 0=High, 1=Some concerns, 2=Low | 2 |
| `rob_incomplete_notes` | String | Text | Evidence | "ITT analysis conducted; 8% dropout balanced" |
| `rob_selective` | Integer | 0–2 | Selective reporting: 0=High, 1=Some concerns, 2=Low | 1 |
| `rob_other` | Integer | 0–2 | Other bias: contamination, expectancy effects | 1 |
| `rob_other_notes` | String | Text | Specific other bias concern | "Possible teacher enthusiasm effect" |
| `rob_overall` | Integer | 0–2 | Overall risk of bias: 0=High, 1=Moderate, 2=Low | 1 |

**Overall risk of bias decision rules**:
- Low (2): All individual domains rated Low
- Moderate (1): Some domains rated Some Concerns; no High risk domains
- High (0): At least one domain rated High risk

---

## Sheet 8: Computed Variables (`computed`)

*These are computed after data entry, not coded from papers*

| Variable Name | Data Type | Definition | Formula |
|---------------|-----------|------------|---------|
| `j_correction` | Numeric | Hedges' bias correction factor | 1 - (3 / (4 × df - 1)) |
| `cohens_d` | Numeric | Cohen's d before correction | (M_t - M_c) / SD_pooled |
| `sd_pooled` | Numeric | Pooled standard deviation | sqrt[((n_t-1)×SD_t² + (n_c-1)×SD_c²)/(n_t+n_c-2)] |
| `n_harmonic` | Numeric | Harmonic mean of n_t and n_c | 2×n_t×n_c/(n_t+n_c) |
| `weight_fe` | Numeric | Fixed-effect weight (1/Var_g) | 1/var_g |

---

## Missing Value Codes

| Code | Meaning | Usage |
|------|---------|-------|
| `NA` | Not applicable for this study/effect size | e.g., pre-test data for post-test-only design |
| `999` | Data not reported (could have been coded but wasn't) | e.g., attrition rate not mentioned in paper |
| `998` | Author contacted; data not provided | e.g., author did not respond or declined |
| `997` | Data exists but could not be extracted from figure | e.g., values on graph too imprecise to read |

---

## Variable Groups for Analysis

### For RQ1 (Overall Effect):
`study_id`, `es_id`, `hedges_g`, `var_g`, `n_total`

### For RQ2 (Oversight Moderation):
All RQ1 variables + `oversight_level`

### For RQ3 (Architecture Moderation):
All RQ1 variables + `architecture`

### For RQ4 (Context Moderation):
All RQ1 variables + `context`

### For Additional Moderators:
All RQ1 variables + `agency_level`, `agent_role`, `modality`, `technology`, `adaptivity`, `domain`, `outcome_type`, `blooms_level`, `measurement_type`, `timing`, `design`, `rob_overall`, `duration_weeks`, `year`

---

## Codebook Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-16 | Initial release |
| 1.1 | [TBD] | Updates after pilot coding calibration |

---

*This codebook mirrors the Excel coding template. Any changes to variable definitions during coding must be reflected in both this codebook and the coding manual (`03_data_extraction/coding_manual.md`), with the change logged in `06_decisions/decision_log.md`.*
