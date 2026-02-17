# ============================================================================
# 02_overall_effect.R
# RQ1: Overall Effect of Agentic AI on Learning Outcomes
# ============================================================================
#
# Purpose:
#   Estimate the overall weighted mean effect size (Hedges' g) using a
#   random-effects model. Reports heterogeneity statistics (Q, I-squared,
#   tau-squared), prediction intervals, and generates a forest plot.
#   Supports both standard RE model (rma) and 3-level model (rma.mv)
#   for studies contributing multiple effect sizes.
#
# Input:
#   data/04_final/ma_data_clean.rds
#
# Output:
#   analysis/output/overall_effect_results.txt
#   analysis/output/forest_plots/forest_overall.png
#   analysis/output/forest_plots/forest_overall.pdf
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 02: Overall Effect (RQ1) ==========\n")


# ============================================================================
# 1. LOAD DATA
# ============================================================================

rds_path <- file.path(PATHS$data_final, "ma_data_clean.rds")

if (!file.exists(rds_path)) {
  stop("Clean data not found at: ", rds_path,
       "\nRun 01_data_preparation.R first.")
}

dat <- readRDS(rds_path)
message("Loaded ", nrow(dat), " effect sizes from ", n_distinct(dat$study_id), " studies")


# ============================================================================
# 2. STANDARD RANDOM-EFFECTS MODEL
# ============================================================================
# Uses a simple RE model with REML estimation. This is appropriate when
# each study contributes a single effect size, or as a baseline comparison.

message("\n--- 2.1 Standard Random-Effects Model (rma) ---\n")

# Fit the model using Hedges' g (yi) and its variance (var_g)
res_re <- rma(
  yi     = hedges_g,
  vi     = var_g,
  data   = dat,
  method = "REML",
  slab   = dat$study_label
)

# Print summary
print(summary(res_re))

# Extract key statistics
overall_g    <- coef(res_re)
overall_se   <- res_re$se
overall_ci   <- c(res_re$ci.lb, res_re$ci.ub)
overall_z    <- res_re$zval
overall_p    <- res_re$pval
Q_stat       <- res_re$QE
Q_df         <- res_re$k - 1
Q_p          <- res_re$QEp
I2           <- res_re$I2
tau2         <- res_re$tau2
tau          <- sqrt(tau2)
k            <- res_re$k

# Prediction interval
pi <- compute_prediction_interval(res_re)

message("\n  Overall effect (RE): ",
        fmt_es(overall_g, overall_ci[1], overall_ci[2], 3))
message("  Interpretation: ", interpret_g(overall_g))
message("  p ", fmt_p(overall_p))
message("  k = ", k, " effect sizes")
message("  Q(", Q_df, ") = ", fmt(Q_stat, 2), ", p ", fmt_p(Q_p))
message("  I-squared = ", fmt(I2, 1), "% (", interpret_i2(I2), ")")
message("  tau-squared = ", fmt(tau2, 4), " (tau = ", fmt(tau, 3), ")")
message("  Prediction interval: [", fmt(pi["pi_lower"], 3), ", ",
        fmt(pi["pi_upper"], 3), "]")


# ============================================================================
# 3. THREE-LEVEL META-ANALYTIC MODEL
# ============================================================================
# Accounts for dependent effect sizes nested within studies.
# Random effects: Level 2 (within-study) + Level 3 (between-study)

has_dependent <- any(dat$dependent_es, na.rm = TRUE)

if (has_dependent) {
  message("\n--- 3.1 Three-Level Model (rma.mv) ---\n")
  message("  Studies with multiple ES detected. Fitting 3-level model.")

  res_3lvl <- rma.mv(
    yi     = hedges_g,
    V      = var_g,
    random = ~ 1 | study_id / es_id,
    data   = dat,
    method = "REML",
    slab   = dat$study_label
  )

  print(summary(res_3lvl))

  # Extract variance components
  sigma2_within  <- res_3lvl$sigma2[2]  # Level 2: within-study

  sigma2_between <- res_3lvl$sigma2[1]  # Level 3: between-study
  total_var      <- sigma2_within + sigma2_between

  # Compute I-squared decomposition (Cheung, 2014)
  typical_vi <- mean(dat$var_g)
  I2_total   <- total_var / (total_var + typical_vi) * 100
  I2_within  <- sigma2_within / (total_var + typical_vi) * 100
  I2_between <- sigma2_between / (total_var + typical_vi) * 100

  # Prediction interval for 3-level model
  pi_3lvl <- compute_prediction_interval(res_3lvl)

  message("\n  Overall effect (3-level): ",
          fmt_es(coef(res_3lvl), res_3lvl$ci.lb, res_3lvl$ci.ub, 3))
  message("  sigma2_within  (Level 2): ", fmt(sigma2_within, 4))
  message("  sigma2_between (Level 3): ", fmt(sigma2_between, 4))
  message("  I2_total   = ", fmt(I2_total, 1), "%")
  message("  I2_within  = ", fmt(I2_within, 1), "%")
  message("  I2_between = ", fmt(I2_between, 1), "%")
  message("  Prediction interval: [", fmt(pi_3lvl["pi_lower"], 3), ", ",
          fmt(pi_3lvl["pi_upper"], 3), "]")

  # Likelihood ratio test comparing 3-level vs 2-level
  # Test if within-study variance is significant
  res_2lvl <- rma.mv(
    yi     = hedges_g,
    V      = var_g,
    random = ~ 1 | study_id,
    data   = dat,
    method = "REML"
  )

  lr_test <- anova(res_3lvl, res_2lvl)
  message("\n  Likelihood ratio test (3-level vs 2-level):")
  message("    LRT = ", fmt(lr_test$LRT, 3), ", p = ", fmt(lr_test$pval, 4))
  if (lr_test$pval < ALPHA) {
    message("    => 3-level model significantly improves fit. Use 3-level model.")
    primary_model <- res_3lvl
    model_label   <- "3-level RE"
  } else {
    message("    => No significant improvement. Standard RE model sufficient.")
    primary_model <- res_re
    model_label   <- "Standard RE"
  }
} else {
  message("\n  No dependent effect sizes. Using standard RE model.")
  primary_model <- res_re
  model_label   <- "Standard RE"
}


# ============================================================================
# 4. FOREST PLOT
# ============================================================================

message("\n--- 4. Forest Plot ---\n")

# --- 4.1 Standard metafor forest plot ---
forest_path_png <- file.path(PATHS$out_forest, "forest_overall.png")
forest_path_pdf <- file.path(PATHS$out_forest, "forest_overall.pdf")

# Determine plot height based on number of studies
plot_height <- max(8, k * 0.35 + 3)

# PNG version
png(forest_path_png, width = 10, height = plot_height, units = "in", res = 300)
par(mar = c(4, 4, 2, 2))
forest(
  res_re,
  xlim   = c(-4, 6),
  alim   = c(-2, 4),
  header = c("Study", "Hedges' g [95% CI]"),
  xlab   = "Hedges' g",
  mlab   = paste0(
    "RE Model (k = ", k,
    ", g = ", fmt(overall_g, 2),
    " [", fmt(overall_ci[1], 2), ", ", fmt(overall_ci[2], 2), "]",
    ", I\u00B2 = ", fmt(I2, 1), "%)"
  ),
  col    = "darkblue",
  border = "darkblue",
  fonts  = "Helvetica",
  cex    = 0.8,
  digits = 2
)
dev.off()
message("  Saved: ", forest_path_png)

# PDF version
pdf(forest_path_pdf, width = 10, height = plot_height)
par(mar = c(4, 4, 2, 2))
forest(
  res_re,
  xlim   = c(-4, 6),
  alim   = c(-2, 4),
  header = c("Study", "Hedges' g [95% CI]"),
  xlab   = "Hedges' g",
  mlab   = paste0(
    "RE Model (k = ", k,
    ", g = ", fmt(overall_g, 2),
    " [", fmt(overall_ci[1], 2), ", ", fmt(overall_ci[2], 2), "]",
    ", I\u00B2 = ", fmt(I2, 1), "%)"
  ),
  col    = "darkblue",
  border = "darkblue",
  cex    = 0.8,
  digits = 2
)
dev.off()
message("  Saved: ", forest_path_pdf)

# --- 4.2 ggplot-based forest plot (ordered by effect size) ---
forest_gg_path <- file.path(PATHS$out_forest, "forest_overall_ggplot.png")

dat_forest <- dat %>%
  filter(!is.na(hedges_g), !is.na(se_g)) %>%
  arrange(hedges_g) %>%
  mutate(
    ci_lo = hedges_g - qnorm(0.975) * se_g,
    ci_hi = hedges_g + qnorm(0.975) * se_g,
    study_label = factor(study_label, levels = study_label)
  )

# Add the overall estimate row
overall_row <- tibble(
  study_label = "Overall (RE)",
  hedges_g    = overall_g,
  se_g        = overall_se,
  ci_lo       = overall_ci[1],
  ci_hi       = overall_ci[2]
)
dat_forest_full <- bind_rows(dat_forest, overall_row) %>%
  mutate(study_label = factor(study_label,
                              levels = c(levels(dat_forest$study_label), "Overall (RE)")),
         is_overall = study_label == "Overall (RE)")

p_forest <- ggplot(dat_forest_full,
                   aes(x = hedges_g, y = study_label)) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "grey50") +
  geom_vline(xintercept = overall_g, linetype = "dotted", color = "steelblue",
             linewidth = 0.5) +
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi,
                     color = is_overall),
                 height = 0.3, linewidth = 0.5) +
  geom_point(aes(size = 1 / se_g^2, shape = is_overall, color = is_overall)) +
  scale_color_manual(values = c("FALSE" = "grey30", "TRUE" = "darkblue"),
                     guide = "none") +
  scale_shape_manual(values = c("FALSE" = 16, "TRUE" = 18), guide = "none") +
  scale_size_continuous(range = c(1, 5), guide = "none") +
  labs(
    title    = "Forest Plot: Effect of Agentic AI on Learning Outcomes",
    subtitle = paste0("Random-effects model (k = ", k, ")"),
    x        = "Hedges' g",
    y        = NULL
  ) +
  theme_meta() +
  theme(axis.text.y = element_text(size = 7))

ggsave(forest_gg_path, p_forest, width = 10,
       height = max(6, nrow(dat_forest_full) * 0.3 + 2),
       dpi = 300, bg = "white")
message("  Saved: ", forest_gg_path)


# ============================================================================
# 5. RESULTS SUMMARY TABLE
# ============================================================================

message("\n--- 5. Results Summary ---\n")

results_table <- tibble(
  Statistic = c(
    "Number of studies (k)",
    "Number of effect sizes",
    "Overall Hedges' g",
    "Standard error",
    "95% CI lower",
    "95% CI upper",
    "z-value",
    "p-value",
    "Q statistic",
    "Q df",
    "Q p-value",
    "I-squared (%)",
    "I-squared interpretation",
    "tau-squared",
    "tau",
    "Prediction interval lower",
    "Prediction interval upper",
    "Effect size interpretation",
    "Model"
  ),
  Value = c(
    n_distinct(dat$study_id),
    k,
    fmt(overall_g, 4),
    fmt(overall_se, 4),
    fmt(overall_ci[1], 4),
    fmt(overall_ci[2], 4),
    fmt(overall_z, 3),
    ifelse(overall_p < 0.001, "< 0.001", fmt(overall_p, 4)),
    fmt(Q_stat, 2),
    Q_df,
    ifelse(Q_p < 0.001, "< 0.001", fmt(Q_p, 4)),
    fmt(I2, 2),
    interpret_i2(I2),
    fmt(tau2, 4),
    fmt(tau, 4),
    fmt(pi["pi_lower"], 4),
    fmt(pi["pi_upper"], 4),
    interpret_g(overall_g),
    model_label
  )
)

# Add 3-level results if applicable
if (has_dependent && exists("res_3lvl")) {
  results_3lvl <- tibble(
    Statistic = c(
      "--- 3-Level Model ---",
      "Overall g (3-level)",
      "95% CI lower (3-level)",
      "95% CI upper (3-level)",
      "sigma2_within (Level 2)",
      "sigma2_between (Level 3)",
      "I2_total (%)",
      "I2_within (%)",
      "I2_between (%)",
      "LRT statistic",
      "LRT p-value"
    ),
    Value = c(
      "",
      fmt(coef(res_3lvl), 4),
      fmt(res_3lvl$ci.lb, 4),
      fmt(res_3lvl$ci.ub, 4),
      fmt(sigma2_within, 4),
      fmt(sigma2_between, 4),
      fmt(I2_total, 2),
      fmt(I2_within, 2),
      fmt(I2_between, 2),
      fmt(lr_test$LRT, 3),
      ifelse(lr_test$pval < 0.001, "< 0.001", fmt(lr_test$pval, 4))
    )
  )
  results_table <- bind_rows(results_table, results_3lvl)
}

print(results_table, n = 50)

# Save results
results_path <- file.path(PATHS$output, "overall_effect_results.txt")
sink(results_path)
cat("=======================================================\n")
cat("RQ1: Overall Effect of Agentic AI on Learning Outcomes\n")
cat(paste("Date:", Sys.Date()), "\n")
cat("=======================================================\n\n")
cat("--- Standard Random-Effects Model ---\n\n")
print(summary(res_re))
cat("\n\nPrediction Interval: [", fmt(pi["pi_lower"], 4), ", ",
    fmt(pi["pi_upper"], 4), "]\n")
if (has_dependent && exists("res_3lvl")) {
  cat("\n\n--- Three-Level Model ---\n\n")
  print(summary(res_3lvl))
  cat("\nI2 decomposition:\n")
  cat("  I2_total:   ", fmt(I2_total, 2), "%\n")
  cat("  I2_within:  ", fmt(I2_within, 2), "%\n")
  cat("  I2_between: ", fmt(I2_between, 2), "%\n")
  cat("\nLikelihood ratio test:\n")
  cat("  LRT = ", fmt(lr_test$LRT, 3), ", p = ", fmt(lr_test$pval, 4), "\n")
}
sink()
message("Results saved to: ", results_path)

# Save model objects for downstream scripts
saveRDS(res_re, file.path(PATHS$output, "model_re.rds"))
if (has_dependent && exists("res_3lvl")) {
  saveRDS(res_3lvl, file.path(PATHS$output, "model_3lvl.rds"))
}
saveRDS(primary_model, file.path(PATHS$output, "model_primary.rds"))
message("Model objects saved to: ", PATHS$output)

message("\n========== 02: Overall Effect Complete ==========\n")
