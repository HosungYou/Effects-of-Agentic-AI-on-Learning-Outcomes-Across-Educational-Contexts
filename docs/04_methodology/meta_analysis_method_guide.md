# Meta-Analysis Method Guide

## Overview

This guide specifies the complete analytical strategy for the meta-analysis of Agentic AI effects on learning outcomes. All analyses will be conducted in R using the `metafor`, `robumeta`, and `clubSandwich` packages. This document serves as the pre-registered analysis plan and reporting reference.

---

## 1. Software and Packages

```r
# Required packages
install.packages(c("metafor",      # Core meta-analysis engine
                   "robumeta",     # Robust Variance Estimation
                   "clubSandwich", # RVE with small-sample corrections
                   "dmetar",       # Meta-analysis helper functions
                   "ggplot2",      # Visualization
                   "dplyr",        # Data manipulation
                   "readxl",       # Data import from Excel
                   "meta",         # Additional meta-analysis tools
                   "puniform",     # Publication bias methods
                   "weightr"))     # Weighted regression for pub bias

# Load packages
library(metafor)
library(robumeta)
library(clubSandwich)
library(dmetar)
library(ggplot2)
library(dplyr)
```

**R version**: ≥ 4.3.0
**metafor version**: ≥ 4.0.0
**All analysis scripts stored in**: `/analysis/R/`

---

## 2. Data Structure

### 2.1 Primary Dataset Format

One row per effect size (multiple rows per study when multiple outcomes reported):

| Column | Type | Description |
|--------|------|-------------|
| `study_id` | Character | Unique study identifier (e.g., "001") |
| `es_id` | Character | Effect size ID (e.g., "001.1") |
| `author` | Character | First author last name |
| `year` | Integer | Publication year |
| `hedges_g` | Numeric | Effect size (positive = AI better) |
| `var_g` | Numeric | Variance of Hedges' g |
| `se_g` | Numeric | Standard error of Hedges' g |
| `n_total` | Integer | Total sample size |
| `oversight_level` | Integer | 1=Autonomous, 2=Checkpoint, 3=Human-led |
| `architecture` | Integer | 1=Single, 2=Multi-agent |
| `agency_level` | Integer | 1=Adaptive, 2=Proactive, 3=Co-learner, 4=Peer |
| `agent_role` | Integer | 1-6 (see coding manual) |
| `modality` | Integer | 1-4 (see coding manual) |
| `technology` | Integer | 1-6 (see coding manual) |
| `adaptivity` | Integer | 1-5 (see coding manual) |
| `context` | Integer | 1=K-12, 2=HE, 3=Workplace, 4=Professional, 5=Continuing |
| `domain` | Integer | 1-7 (see coding manual) |
| `outcome_type` | Integer | 1=Cognitive, 2=Skill, 3=Affective, 4=Performance |
| `blooms_level` | Integer | 1=Lower, 2=Middle, 3=Higher |
| `design` | Integer | 1=RCT, 2=Quasi, 3=Pre-post |
| `rob_overall` | Integer | 0=High, 1=Moderate, 2=Low risk |
| `duration_weeks` | Numeric | Intervention duration in weeks |

---

## 3. Step 1: Overall Effect Size (RQ1)

### 3.1 Random-Effects Model

The random-effects model (REM) assumes that the true effect size varies across studies (heterogeneity). This is the appropriate choice for educational meta-analyses where study characteristics differ.

**Model specification**:
```
g_i = mu + u_i + e_i
```
Where:
- `mu` = overall mean effect size (population parameter)
- `u_i` ~ N(0, τ²) = random effect for study i (between-study variance)
- `e_i` ~ N(0, σ²_i) = within-study sampling error

**Estimator**: Restricted Maximum Likelihood (REML) — the default and recommended estimator in `metafor`.

### 3.2 R Code: Overall Random-Effects Model

```r
# Load data
dat <- read.csv("analysis/data/master_dataset.csv")

# IMPORTANT: For dependent effect sizes, do NOT use standard RE model
# Use a single effect size per study for this primary analysis
# OR use 3-level model / RVE (see Section 5)

# Option A: One effect size per study (most conservative)
dat_primary <- dat %>%
  group_by(study_id) %>%
  slice(1)  # Take first/primary effect size per study

# Fit random-effects model
res_overall <- rma(yi = hedges_g,
                   vi = var_g,
                   data = dat_primary,
                   method = "REML",
                   slab = paste(author, year))

# Results summary
summary(res_overall)
```

### 3.3 Heterogeneity Statistics

| Statistic | Formula | Interpretation |
|-----------|---------|---------------|
| **Q-statistic** | Sum of weighted squared deviations | Tests whether all studies share a common effect; p < .05 = significant heterogeneity |
| **I²** | (Q - df) / Q × 100% | % of variance due to heterogeneity (not sampling error); 25% = low, 50% = moderate, 75% = high |
| **τ²** | Between-study variance | Absolute heterogeneity; scale depends on effect size metric |
| **τ** | sqrt(τ²) | SD of true effect size distribution |
| **H²** | Q / df | Ratio of total to within-study variance |
| **Prediction interval** | mu ± 1.96 × τ | Range of true effects across 95% of hypothetical studies |

```r
# Extract heterogeneity statistics
cat("Q =", res_overall$QE, "(df =", res_overall$k-1, "), p =",
    formatC(res_overall$QEp, format = "e"), "\n")
cat("I² =", round(res_overall$I2, 1), "%\n")
cat("τ² =", round(res_overall$tau2, 4), "\n")
cat("τ =", round(sqrt(res_overall$tau2), 4), "\n")

# Prediction interval
predict(res_overall, digits = 3)
```

### 3.4 Forest Plot

```r
# Basic forest plot
forest(res_overall,
       xlim = c(-3, 4),
       ilab = cbind(dat_primary$n_treatment, dat_primary$n_control),
       ilab.xpos = c(-2.5, -2.0),
       header = c("Author (Year)", "g [95% CI]"),
       xlab = "Hedges' g",
       refline = 0,
       cex = 0.8)

# Add column headers
text(c(-2.5, -2.0), res_overall$k + 2,
     c("n(AI)", "n(Ctrl)"), font = 2, cex = 0.8)

# Save
pdf("analysis/figures/forest_plot_overall.pdf", width = 12, height = 14)
forest(res_overall, ...)
dev.off()
```

---

## 4. Step 2: Publication Bias Assessment

### 4.1 Funnel Plot

```r
# Funnel plot
funnel(res_overall,
       main = "Funnel Plot: Overall Effect",
       xlab = "Hedges' g",
       ylab = "Standard Error",
       pch = 19)

# Contour-enhanced funnel plot
funnel(res_overall,
       level = c(90, 95, 99),
       shade = c("white", "gray55", "gray75"),
       refline = 0,
       legend = TRUE,
       main = "Contour-Enhanced Funnel Plot")
```

### 4.2 Egger's Test (Linear Regression Test)

```r
# Egger's test for funnel plot asymmetry
egger_test <- regtest(res_overall, model = "rma", predictor = "sei")
print(egger_test)
# p < .10 suggests potential publication bias
```

### 4.3 Trim-and-Fill

```r
# Trim-and-fill method (Duval & Tweedie, 2000)
res_tf_left <- trimfill(res_overall, side = "left")
res_tf_right <- trimfill(res_overall, side = "right")

summary(res_tf_left)
print(res_tf_left)

# Funnel plot with imputed studies
funnel(res_tf_left,
       pch = c(19, 17),  # filled circles = real, triangles = imputed
       legend = TRUE)
```

### 4.4 PET-PEESE (Stanley & Doucouliagou, 2012)

```r
# PET: Precision-Effect Test
pet <- rma(yi = hedges_g, vi = var_g, mods = ~ se_g,
           data = dat_primary, method = "REML")

# PEESE: Precision-Effect Estimate with Standard Error
peese <- rma(yi = hedges_g, vi = var_g, mods = ~ var_g,
             data = dat_primary, method = "REML")

# Use PET intercept to test if true effect ≠ 0
# If PET intercept significant, use PEESE estimate as bias-corrected effect
```

### 4.5 Selection Models (Vevea & Woods, 2005)

```r
library(weightr)
# Step function selection model
res_selection <- weightfunct(effect = dat_primary$hedges_g,
                             v = dat_primary$var_g,
                             steps = c(0.025, 0.10, 0.50, 1.00))
summary(res_selection)
```

---

## 5. Step 3: Handling Dependent Effect Sizes

### 5.1 The Dependency Problem

Most studies in educational AI report multiple outcomes (e.g., cognitive + affective; immediate + delayed post-test). Standard meta-analysis assumes independence — violation of this assumption inflates precision and Type I error.

**Solutions** (both will be applied):

### 5.2 Option A: Three-Level Meta-Analysis

The 3-level model nests effect sizes within studies (Van den Noortgate et al., 2013):

```
Level 1: Sampling variance within effect sizes (σ²_e_i)
Level 2: Variance between effect sizes within studies (σ²_within)
Level 3: Variance between studies (σ²_between)
```

```r
# 3-level meta-analysis
res_3level <- rma.mv(yi = hedges_g,
                     V = var_g,
                     random = ~ 1 | study_id / es_id,
                     data = dat,
                     method = "REML",
                     slab = paste(author, year))

summary(res_3level)

# Variance components
res_3level$sigma2  # [1] = within-study; [2] = between-study

# Likelihood ratio test comparing models
anova(rma.mv(yi = hedges_g, V = var_g, random = ~ 1 | study_id, data = dat),
      res_3level)
```

### 5.3 Option B: Robust Variance Estimation (RVE)

RVE (Hedges, Tipton & Johnson, 2010) provides valid inference without requiring correct specification of the covariance structure:

```r
library(robumeta)

# RVE with correlated effects working model
res_rve <- robu(hedges_g ~ 1,
                var.eff.size = var_g,
                studynum = study_id,
                data = dat,
                rho = 0.80,  # Assumed correlation between outcomes
                small = TRUE)  # Small sample correction

print(res_rve)

# Sensitivity analysis: vary rho
for (rho in c(0.50, 0.70, 0.80, 0.90)) {
  res_rho <- robu(hedges_g ~ 1,
                  var.eff.size = var_g,
                  studynum = study_id,
                  data = dat,
                  rho = rho,
                  small = TRUE)
  cat("rho =", rho, ": g =", round(res_rho$reg_table$b.r, 3),
      "[", round(res_rho$reg_table$CI.L, 3), ",",
      round(res_rho$reg_table$CI.U, 3), "]\n")
}
```

### 5.4 Primary Reporting Strategy

- **Primary analysis**: 3-level model with RVE corrections via `clubSandwich`
- **Sensitivity check**: Standard RE model on one primary effect size per study
- **Both approaches** reported in supplementary materials

---

## 6. Step 4: Moderator Analyses (RQ2-4)

### 6.1 Categorical Moderators (Subgroup Analysis)

**Variables**: oversight_level, architecture, context, agent_role, outcome_type, blooms_level, technology, design

```r
# RQ2: Human oversight level as moderator
res_oversight <- rma.mv(yi = hedges_g,
                        V = var_g,
                        mods = ~ factor(oversight_level),
                        random = ~ 1 | study_id / es_id,
                        data = dat,
                        method = "REML")

summary(res_oversight)

# Omnibus test for moderator
anova(res_oversight, btt = 2:3)  # Test both oversight level coefficients

# With RVE via clubSandwich for robust inference
library(clubSandwich)
coef_test(res_oversight,
          vcov = "CR2",
          cluster = dat$study_id)

# Subgroup-specific estimates (for forest plot)
res_auto <- rma(yi = hedges_g, vi = var_g,
                data = dat[dat$oversight_level == 1, ], method = "REML")
res_check <- rma(yi = hedges_g, vi = var_g,
                 data = dat[dat$oversight_level == 2, ], method = "REML")
res_human <- rma(yi = hedges_g, vi = var_g,
                 data = dat[dat$oversight_level == 3, ], method = "REML")
```

**RQ3: Agent architecture**:
```r
res_arch <- rma.mv(yi = hedges_g, V = var_g,
                   mods = ~ factor(architecture),
                   random = ~ 1 | study_id / es_id,
                   data = dat, method = "REML")
```

**RQ4: Learning context**:
```r
res_context <- rma.mv(yi = hedges_g, V = var_g,
                      mods = ~ factor(context),
                      random = ~ 1 | study_id / es_id,
                      data = dat, method = "REML")
```

### 6.2 Continuous Moderators (Meta-Regression)

**Variables**: duration_weeks, year, n_total

```r
# Duration as continuous moderator
res_duration <- rma.mv(yi = hedges_g, V = var_g,
                       mods = ~ duration_weeks,
                       random = ~ 1 | study_id / es_id,
                       data = dat, method = "REML")

# Center continuous predictors for interpretability
dat$duration_c <- scale(dat$duration_weeks, center = TRUE, scale = FALSE)
dat$year_c <- dat$year - 2021  # Center at midpoint

res_meta_reg <- rma.mv(yi = hedges_g, V = var_g,
                       mods = ~ duration_c + year_c,
                       random = ~ 1 | study_id / es_id,
                       data = dat, method = "REML")
```

### 6.3 Interaction Effects

Planned interactions (if sufficient k per cell, minimum k = 4 per subgroup):

```r
# Oversight × Context interaction
res_interact <- rma.mv(yi = hedges_g, V = var_g,
                       mods = ~ factor(oversight_level) * factor(context),
                       random = ~ 1 | study_id / es_id,
                       data = dat, method = "REML")

# Test interaction term
anova(res_main, res_interact)
```

**Minimum cell size rule**: Only test interactions if each cell contains ≥ 4 independent studies. Report cells with k < 4 as "insufficient data."

### 6.4 Multiple Testing Correction

With multiple moderator analyses, apply Benjamini-Hochberg FDR correction:

```r
# Collect all moderator p-values
p_values <- c(p_oversight, p_arch, p_context, p_role, p_outcome_type,
              p_blooms, p_technology)

# FDR correction
p_adjusted <- p.adjust(p_values, method = "BH")
names(p_adjusted) <- c("oversight", "architecture", "context", "role",
                       "outcome_type", "blooms", "technology")
print(p_adjusted)
```

---

## 7. Step 5: Sensitivity Analyses

### 7.1 Leave-One-Out Analysis

```r
# Influence analysis
inf <- influence(res_overall)
plot(inf)

# Leave-one-out
res_loo <- leave1out(res_overall)
forest(res_loo, xlab = "Hedges' g", refline = coef(res_overall))
```

### 7.2 Outlier Detection

```r
# Standardized residuals
rstudent_vals <- rstudent(res_overall)
plot(1:length(rstudent_vals$z), rstudent_vals$z,
     type = "b", xlab = "Study", ylab = "Studentized Residual",
     main = "Outlier Detection")
abline(h = c(-3.29, 3.29), lty = 2, col = "red")  # p < .001 threshold

# Identify outliers
outliers <- which(abs(rstudent_vals$z) > 3.29)
cat("Potential outliers:", outliers, "\n")
```

### 7.3 Risk of Bias Sensitivity Analysis

```r
# Restrict to low risk of bias studies only
dat_low_rob <- dat[dat$rob_overall == 2, ]
res_low_rob <- rma(yi = hedges_g, vi = var_g,
                   data = dat_low_rob, method = "REML")

# Compare: all studies vs. low risk of bias only
cat("All studies: g =", round(coef(res_overall), 3), "\n")
cat("Low RoB only: g =", round(coef(res_low_rob), 3), "\n")
```

### 7.4 Assumed Pre-Post Correlation Sensitivity

For studies using pre-post designs with assumed r = 0.70:

```r
# Recompute effect sizes with r = 0.50 and r = 0.90
# Compare overall effect across assumptions
for (r_assumed in c(0.50, 0.70, 0.90)) {
  # Recompute g for pre-post studies using different r
  # (see effect_size_extraction_guide.md for formula)
  # Run meta-analysis and compare
}
```

### 7.5 Funnel Plot Asymmetry Correction

Compare effect sizes before and after trim-and-fill correction. If substantial difference (>0.10 g units), investigate potential publication bias more thoroughly.

---

## 8. Step 6: Additional Moderator Analyses

### 8.1 Priority Order for Additional Moderators

Conduct in this priority order (based on theoretical importance):

| Priority | Variable | Rationale |
|:--------:|----------|-----------|
| 1 | `agent_role` | Role-effectiveness matching theory |
| 2 | `outcome_type` | Cognitive vs. affective differential effects |
| 3 | `blooms_level` | Higher-order vs. lower-order cognitive demands |
| 4 | `technology` | Rule-based vs. LLM effect differences |
| 5 | `adaptivity` | Adaptivity level as efficacy driver |
| 6 | `modality` | Text vs. embodied agent differences |
| 7 | `domain` | Subject domain specificity |
| 8 | `design` | Design quality as moderator |
| 9 | `duration_weeks` | Dose-response relationship |
| 10 | `year` | Historical trend (improving AI effectiveness?) |

### 8.2 Reporting Threshold

Report moderator results only if: **k ≥ 10 studies in at least one subgroup** (for categorical moderators) or **k ≥ 20 total studies** (for meta-regression). Otherwise, report as "insufficient data for [moderator] analysis."

---

## 9. Reporting Standards

### 9.1 Effect Size Tables

For each analysis, report:
- k (number of studies), K (number of effect sizes)
- Hedges' g with 95% CI
- Q-statistic and p-value
- I² (with 95% CI using Q-profile method)
- τ²
- 95% prediction interval

### 9.2 Forest Plot Standards

All forest plots must include:
- Individual study effect sizes with 95% CIs
- Overall pooled estimate with 95% CI and prediction interval
- Study sample sizes (n_treatment, n_control)
- I² and heterogeneity statistics
- Reference line at g = 0

### 9.3 GRADE Assessment (Optional)

If required by target journal: apply GRADE framework to assess certainty of evidence:
- Risk of bias
- Inconsistency (heterogeneity)
- Indirectness
- Imprecision
- Publication bias

---

## 10. HALO Framework Derivation (RQ5)

### 10.1 Mapping Meta-Analytic Results to Design Principles

After completing all analyses, map findings to HALO Framework:

| Finding | If AI-led > Human-led | If Human-led > AI-led | If No Difference |
|---------|----------------------|----------------------|------------------|
| **RQ2: Oversight** | Reduce checkpoint frequency; favor automation | Increase checkpoint frequency; default to human-led | Context-specific configuration |
| **RQ3: Architecture** | Recommend multi-agent; invest in MCP | Simplify to single-agent; avoid complexity | Either works; choose based on cost |
| **RQ4: Context** | Context X gets higher agency | Context X gets more oversight | Universal design acceptable |

### 10.2 Effect Size Thresholds for Design Recommendations

| g Difference | Recommendation Strength |
|:------------:|------------------------|
| < 0.10 | No recommendation; effects equivalent |
| 0.10 – 0.20 | Weak preference; consider other factors |
| 0.21 – 0.40 | Moderate recommendation |
| > 0.40 | Strong recommendation |

---

*All analysis scripts will be made available as supplementary materials (R scripts). Analysis was pre-registered on PROSPERO [registration number].*

*References: Viechtbauer (2010); Hedges, Tipton & Johnson (2010); Van den Noortgate et al. (2013); Pustejovsky & Tipton (2022); Stanley & Doucouliagou (2012)*
