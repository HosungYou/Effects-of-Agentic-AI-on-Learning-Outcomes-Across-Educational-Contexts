# Effect Size Extraction Guide: Computing Hedges' g

## Overview

This guide provides step-by-step procedures for extracting and computing Hedges' g from all commonly reported statistical formats in educational AI research. All effect sizes must be converted to Hedges' g (bias-corrected standardized mean difference) for meta-analytic synthesis.

**Effect size interpretation** (Cohen, 1988, adapted):
- Small: g ≈ 0.20
- Medium: g ≈ 0.50
- Large: g ≈ 0.80

---

## 1. Core Formula: Hedges' g

### 1.1 From Independent Groups (Treatment vs. Control)

**Step 1**: Compute Cohen's d:

```
d = (M_treatment - M_control) / SD_pooled
```

Where the pooled standard deviation is:

```
SD_pooled = sqrt[ ((n_t - 1) × SD_t² + (n_c - 1) × SD_c²) / (n_t + n_c - 2) ]
```

**Step 2**: Apply the Hedges' bias correction factor J:

```
J = 1 - (3 / (4 × df - 1))
  where df = n_t + n_c - 2
```

**Step 3**: Compute Hedges' g:

```
g = J × d
```

**Step 4**: Compute variance and standard error:

```
Var(g) = (n_t + n_c) / (n_t × n_c) + g² / (2 × (n_t + n_c))

SE(g) = sqrt(Var(g))
```

**Step 5**: Compute 95% confidence interval:

```
CI_lower = g - 1.96 × SE(g)
CI_upper = g + 1.96 × SE(g)
```

### 1.2 Example Calculation

Study reports: M_t = 82.4, SD_t = 12.1, n_t = 45; M_c = 74.6, SD_c = 13.8, n_c = 43

```
SD_pooled = sqrt[ (44 × 12.1² + 42 × 13.8²) / (45 + 43 - 2) ]
           = sqrt[ (44 × 146.41 + 42 × 190.44) / 86 ]
           = sqrt[ (6442.04 + 7998.48) / 86 ]
           = sqrt[ 14440.52 / 86 ]
           = sqrt[167.913]
           = 12.958

d = (82.4 - 74.6) / 12.958 = 7.8 / 12.958 = 0.602

df = 45 + 43 - 2 = 86
J = 1 - (3 / (4 × 86 - 1)) = 1 - (3/343) = 1 - 0.00875 = 0.991

g = 0.991 × 0.602 = 0.597

Var(g) = (45 + 43)/(45 × 43) + 0.597²/(2 × 88)
       = 88/1935 + 0.356/176
       = 0.0455 + 0.00202
       = 0.0475

SE(g) = sqrt(0.0475) = 0.218

CI: [0.597 - 1.96 × 0.218, 0.597 + 1.96 × 0.218] = [0.170, 1.024]
```

---

## 2. Pre-Post Designs (Morris & DeShon, 2002)

### 2.1 When to Use This Formula

Use when the study has a pre-post design (same participants measured before and after), either:
- Single-group pre-post (no control)
- Two-group with both pre- and post-test data available

### 2.2 Two-Group Pre-Post (Preferred)

When both groups have pre- and post-test data, compute gain score effect size:

**Step 1**: Compute gain scores for each group:

```
Gain_treatment = M_post_t - M_pre_t
Gain_control   = M_post_c - M_pre_c
```

**Step 2**: Estimate SD of change scores (if not directly reported):

```
SD_change = sqrt(SD_pre² + SD_post² - 2 × r × SD_pre × SD_post)
```

Where r = pre-post correlation (assume r = 0.70 if not reported; conduct sensitivity analysis with r = 0.50 and r = 0.90)

**Step 3**: Compute d from gain scores using pooled SD of change:

```
d_gain = (Gain_treatment - Gain_control) / SD_change_pooled
```

**Step 4**: Apply J correction → Hedges' g (same as Section 1.1, Step 2-5)

### 2.3 Single-Group Pre-Post (Morris & DeShon, 2002, Equation 8)

When only one group with pre and post data:

```
d_rm = (M_post - M_pre) / SD_pre × sqrt(2 × (1 - r))
```

Where:
- SD_pre = pre-test standard deviation (use as standardizer)
- r = pre-post correlation (assume r = 0.70 if unreported)

Apply J correction → Hedges' g.

**Variance**:

```
Var(d_rm) = (1/n) + d_rm²/(2n)
```

### 2.4 Sensitivity Analysis for Assumed r

When r is assumed (not reported), conduct sensitivity analysis:
- Report g with r = 0.50, 0.70, 0.90
- Use r = 0.70 as the primary estimate
- Report in sensitivity analysis table

---

## 3. Conversion from Other Statistics

### 3.1 From t-statistic (Independent Groups)

```
d = t × sqrt(1/n_t + 1/n_c)

OR equivalently:

d = t × sqrt((n_t + n_c) / (n_t × n_c))
```

Then apply J correction → Hedges' g.

**Example**: t = 3.24, n_t = 35, n_c = 33

```
d = 3.24 × sqrt((35 + 33) / (35 × 33))
  = 3.24 × sqrt(68 / 1155)
  = 3.24 × sqrt(0.0589)
  = 3.24 × 0.2427
  = 0.786

df = 35 + 33 - 2 = 66
J = 1 - 3/(4 × 66 - 1) = 1 - 3/263 = 0.989
g = 0.989 × 0.786 = 0.777
```

### 3.2 From F-statistic (Between Groups, df_numerator = 1)

When F has df numerator = 1 (one degree of freedom for the group effect):

```
d = sqrt(F × (n_t + n_c) / (n_t × n_c))

OR equivalently:

t = sqrt(F)
then use the t formula above
```

**Note**: This conversion is ONLY valid when df_numerator = 1. For F with df_numerator > 1 (e.g., ANOVA with 3+ groups), use a different approach or contact authors for pairwise statistics.

### 3.3 From Point-Biserial Correlation r

```
d = 2r / sqrt(1 - r²)
```

Or alternatively using the exact formula:

```
d = r × sqrt((n_t + n_c - 2) / (n_t × n_c / (n_t + n_c)))
      × sqrt((n_t + n_c) / (n_t × n_c))
```

Simpler approximation (adequate for most uses):

```
d ≈ 2r / sqrt(1 - r²)
```

Apply J correction → Hedges' g.

### 3.4 From Chi-Square (2×2 Contingency Tables)

For binary outcomes (pass/fail, mastered/not mastered):

**Step 1**: Compute phi coefficient:

```
phi = sqrt(chi² / N)
```

**Step 2**: Convert phi to d:

```
d = 2 × phi / sqrt(1 - phi²)
```

Apply J correction → Hedges' g.

**Note**: Only appropriate for binary outcomes. If the underlying construct is continuous (e.g., test score dichotomized at cutoff), this may underestimate the true effect.

### 3.5 From Odds Ratio (OR)

```
d = ln(OR) × sqrt(3) / pi
  = ln(OR) × 0.5513
```

Apply J correction → Hedges' g.

**Note**: Less precise than other conversions. Flag these effect sizes in the dataset.

### 3.6 From Eta-Squared or Partial Eta-Squared (η² or η²_p)

```
d = 2 × sqrt(eta²) / sqrt(1 - eta²)

OR from partial eta-squared:

d = 2 × sqrt(eta²_p) / sqrt(1 - eta²_p)
```

Apply J correction → Hedges' g.

**Note**: Partial eta-squared from ANCOVA includes covariate adjustment. Note whether covariates were included.

---

## 4. Handling Multiple Outcomes per Study

### 4.1 The Dependency Problem

When a study reports multiple outcomes from the same sample, the effect sizes are statistically dependent. This violates the independence assumption of standard meta-analysis.

**Solutions** (applied hierarchically):

1. **Primary approach**: Extract all effect sizes; handle dependency with Robust Variance Estimation (RVE) or 3-level meta-analysis (see `04_methodology/meta_analysis_method_guide.md`)

2. **Secondary approach for simple analyses**: Compute one composite effect size per study using the formulas below

3. **Subgroup analyses**: Use only the effect size matching the subgroup outcome category

### 4.2 Composite Effect Size (When Needed)

If multiple outcomes of the SAME TYPE are reported for the same sample:

```
g_composite = (sum of all g values) / k

Var(g_composite) = (1/k²) × [sum of Var(g_i) + 2 × sum over pairs of Cov(g_i, g_j)]
```

Where Cov(g_i, g_j) = r_ij × sqrt(Var(g_i)) × sqrt(Var(g_j)) and r_ij is the correlation between outcomes (assume r = 0.50 if not reported).

### 4.3 Decision Rules for Multiple Outcomes

| Situation | Action |
|-----------|--------|
| Multiple cognitive outcomes (same construct) | Composite or choose most comprehensive |
| Multiple outcome types (cognitive + affective) | Extract separately; code outcome_type for each |
| Multiple time points (immediate + delayed) | Extract both; code timing for each |
| Multiple subgroups (different learner types) | Extract for full sample; note subgroup splits |
| Pre-test + post-test + delayed test | Extract post-test and delayed separately |

---

## 5. Special Statistical Situations

### 5.1 ANCOVA-Adjusted Means

When the study uses ANCOVA (pre-test as covariate) and reports adjusted means:

**Preferred**: Use adjusted means with the ANCOVA error term for SD (pooled within-group SD)

If only adjusted means reported without SD:
1. Attempt to extract unadjusted SDs from descriptive statistics
2. Use ANCOVA F-statistic conversion if available
3. If neither available, contact authors

### 5.2 Gain Scores as Dependent Variable

When a study analyzes gain scores (post - pre) as the DV:

- If both pre and post means are available: prefer the two-group pre-post formula (Section 2.2)
- If only gain means and SDs are reported: use gain SD as the denominator

```
d = (M_gain_treatment - M_gain_control) / SD_gain_pooled
```

### 5.3 Multilevel Data (Students Nested in Classes/Schools)

When students are nested in classrooms or schools and the study uses multilevel modeling:

- If ICC and design effect are reported: apply design effect correction
- Design Effect = 1 + (cluster_size - 1) × ICC
- Effective N = total N / Design Effect
- Use Effective N in all effect size calculations

If not reported: use total N but flag as potentially inflated (high risk of bias for this item).

### 5.4 Standardized vs. Raw Score Means

**Standardized (z-score, percentile rank, T-score)**:
- Compute d using reported M and SD in standardized units
- Note that z-scores have SD = 1 by definition (verify SD ≈ 1)

**Raw scores**:
- Use pooled SD from treatment and control groups

**Percent correct**:
- Use raw means and SDs (treat as continuous)
- Check for floor/ceiling effects (mean > 90% or < 10%)

---

## 6. Quality Control for Effect Size Extraction

### 6.1 Double-Entry Verification

For all extracted effect sizes:
1. Coder 1 extracts all statistical data
2. Coder 2 independently extracts the same data
3. Compare all numerical values
4. Calculate ICC for continuous variables (target: ICC ≥ 0.95)
5. Resolve discrepancies by re-reading source paper

### 6.2 Outlier Detection

After computing all Hedges' g values:
1. Compute z-score for each g within the overall distribution
2. Flag g values where |z| > 3.29 (p < 0.001) as potential outliers
3. Re-verify extraction for flagged values
4. Include in sensitivity analysis (see methodology guide)

### 6.3 Common Extraction Errors

| Error Type | Prevention |
|------------|-----------|
| Using N per cell from factorial design | Use only the relevant groups' n |
| Ignoring attrition (using initial N) | Always check for post-attrition n |
| Confusing SE for SD | Check: SE = SD / sqrt(n); if SE is small relative to M, it's likely SE |
| Wrong sign convention | Verify: positive g = AI better; reverse if comparison group listed first |
| Using effect size from wrong outcome | Double-check outcome variable description matches target variable |
| ANOVA with 3+ groups: wrong F conversion | F with df_numerator > 1 requires pairwise extraction |

### 6.4 Missing Data Protocol

When statistics are missing or insufficient:

| Step | Action | Timeline |
|------|--------|----------|
| 1 | Check supplementary materials and appendices | Immediate |
| 2 | Extract from figures using WebPlotDigitizer | Immediate |
| 3 | Contact corresponding author via email | Day 1 |
| 4 | Send follow-up if no response | Day 14 |
| 5 | Document as "data not available" and exclude | Day 21 |

**Email template** (stored in project folder):
```
Subject: Data request for meta-analysis - [Author, Year]
Dear Dr. [Name],
We are conducting a systematic meta-analysis of Agentic AI in education...
We are unable to extract effect size data from [specific result in paper].
Could you provide: [specific statistics needed]?
...
```

---

## 7. R Code for Effect Size Computation

```r
# Load required packages
library(metafor)
library(dplyr)

# Function: Hedges' g from means and SDs (independent groups)
compute_hedges_g <- function(m_t, sd_t, n_t, m_c, sd_c, n_c) {
  # Pooled SD
  sd_pool <- sqrt(((n_t - 1) * sd_t^2 + (n_c - 1) * sd_c^2) / (n_t + n_c - 2))
  # Cohen's d
  d <- (m_t - m_c) / sd_pool
  # Hedges' J correction
  df <- n_t + n_c - 2
  j <- 1 - (3 / (4 * df - 1))
  # Hedges' g
  g <- j * d
  # Variance
  var_g <- (n_t + n_c) / (n_t * n_c) + g^2 / (2 * (n_t + n_c))
  se_g <- sqrt(var_g)
  ci_lower <- g - 1.96 * se_g
  ci_upper <- g + 1.96 * se_g
  return(list(g = g, se = se_g, var = var_g,
              ci_lower = ci_lower, ci_upper = ci_upper))
}

# Function: d from t-statistic
t_to_d <- function(t_val, n_t, n_c) {
  d <- t_val * sqrt((n_t + n_c) / (n_t * n_c))
  return(d)
}

# Function: d from F-statistic (df_num = 1 only)
f_to_d <- function(f_val, n_t, n_c) {
  t_val <- sqrt(f_val)
  return(t_to_d(t_val, n_t, n_c))
}

# Function: d from correlation r
r_to_d <- function(r, n_t = NULL, n_c = NULL) {
  d <- 2 * r / sqrt(1 - r^2)
  return(d)
}

# Function: Hedges' g for pre-post single group (Morris & DeShon, 2002)
prepost_hedges_g <- function(m_pre, m_post, sd_pre, n, r = 0.70) {
  d_rm <- (m_post - m_pre) / sd_pre * sqrt(2 * (1 - r))
  df <- n - 1
  j <- 1 - (3 / (4 * df - 1))
  g <- j * d_rm
  var_g <- 1/n + g^2/(2*n)
  se_g <- sqrt(var_g)
  return(list(g = g, se = se_g, var = var_g))
}

# Use metafor's escalc() for systematic computation
# Example using metafor
data_example <- data.frame(
  m_t = c(82.4, 75.2),
  sd_t = c(12.1, 10.5),
  n_t = c(45, 38),
  m_c = c(74.6, 68.9),
  sd_c = c(13.8, 11.2),
  n_c = c(43, 40)
)

results <- escalc(measure = "SMD",  # SMD = Hedges' g with correction
                  m1i = m_t, sd1i = sd_t, n1i = n_t,
                  m2i = m_c, sd2i = sd_c, n2i = n_c,
                  data = data_example)
```

---

## 8. Reporting Standards

In the manuscript methods section, report:
- Which statistics were used for effect size computation (M/SD, t, F, r, OR)
- Proportion of effect sizes from each type
- Assumed pre-post correlation value and sensitivity range
- How multiple outcomes were handled
- Number of studies where authors were contacted and response rate

---

*References: Cohen (1988), Morris & DeShon (2002), Borenstein et al. (2009), Viechtbauer (2010).*
