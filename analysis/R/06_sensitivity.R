# ============================================================================
# 06_sensitivity.R
# Sensitivity and Influence Analyses
# ============================================================================
#
# Purpose:
#   Evaluate the robustness of the overall meta-analytic findings by
#   systematically examining how results change when excluding individual
#   studies, subsets of studies, or applying alternative analytic decisions.
#
# Analyses:
#   1. Leave-one-out analysis (influence of each study)
#   2. Influence diagnostics (Cook's distance, hat values, DFFITS, etc.)
#   3. Outlier detection and removal
#   4. Quality-based sensitivity (high-quality studies only)
#   5. Design-based sensitivity (RCT only, experimental only)
#   6. Outcome type sensitivity (cognitive only, skill only, etc.)
#   7. Pre-post vs. experimental design sensitivity
#   8. Cumulative meta-analysis by year
#   9. Sensitivity to model specification (REML, DL, PM, EB)
#
# Input:
#   data/04_final/ma_data_clean.rds
#   analysis/output/model_re.rds
#
# Output:
#   analysis/output/sensitivity_analysis_report.txt
#   analysis/output/figures/influence_plot.png
#   analysis/output/figures/leave_one_out.png
#   analysis/output/figures/cumulative_ma.png
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 06: Sensitivity Analysis ==========\n")


# ============================================================================
# 1. LOAD DATA AND MODEL
# ============================================================================

dat <- readRDS(file.path(PATHS$data_final, "ma_data_clean.rds"))

re_path <- file.path(PATHS$output, "model_re.rds")
if (file.exists(re_path)) {
  res_re <- readRDS(re_path)
} else {
  res_re <- rma(yi = hedges_g, vi = var_g, data = dat, method = "REML",
                slab = dat$study_label)
}

k <- res_re$k
original_g <- coef(res_re)
original_ci <- c(res_re$ci.lb, res_re$ci.ub)

message("Loaded ", k, " effect sizes")
message("Original estimate: ", fmt_es(original_g, original_ci[1], original_ci[2], 3))

# Ensure output directories exist
fig_dir <- PATHS$out_figures
if (!dir.exists(fig_dir)) dir.create(fig_dir, recursive = TRUE)

# Results collector
sensitivity_results <- list()


# ============================================================================
# 2. LEAVE-ONE-OUT ANALYSIS
# ============================================================================
# Sequentially remove each effect size and re-estimate the model.
# Identifies studies that exert disproportionate influence on the results.

message("\n--- 2. Leave-One-Out Analysis ---\n")

loo <- leave1out(res_re)

# Find most influential studies
loo_df <- data.frame(
  study      = res_re$slab,
  g_without  = loo$estimate,
  ci_lo      = loo$ci.lb,
  ci_hi      = loo$ci.ub,
  p_without  = loo$pval,
  Q_without  = loo$Q,
  I2_without = loo$I2,
  tau2_without = loo$tau2
)
loo_df$g_change <- loo_df$g_without - original_g
loo_df$abs_change <- abs(loo_df$g_change)

# Sort by influence
loo_df <- loo_df[order(-loo_df$abs_change), ]

message("  Top 5 most influential studies:")
for (i in 1:min(5, nrow(loo_df))) {
  message("    ", loo_df$study[i],
          ": g changes by ", fmt(loo_df$g_change[i], 4),
          " (to ", fmt(loo_df$g_without[i], 3), ")")
}

# Check if any single study changes significance
sig_changes <- loo_df[loo_df$p_without >= ALPHA & original_g != 0, ]
if (nrow(sig_changes) > 0) {
  message("\n  WARNING: Removing these studies makes the overall effect non-significant:")
  for (i in 1:nrow(sig_changes)) {
    message("    ", sig_changes$study[i], " (p = ", fmt(sig_changes$p_without[i], 4), ")")
  }
  sensitivity_results$loo_fragile <- TRUE
} else {
  message("\n  Overall significance is robust to removing any single study.")
  sensitivity_results$loo_fragile <- FALSE
}

# --- Leave-one-out plot ---
loo_plot_path <- file.path(fig_dir, "leave_one_out.png")

loo_plot_df <- loo_df %>%
  arrange(g_without) %>%
  mutate(study = factor(study, levels = study))

p_loo <- ggplot(loo_plot_df, aes(x = g_without, y = study)) +
  geom_vline(xintercept = original_g, linetype = "dashed", color = "steelblue") +
  geom_vline(xintercept = 0, linetype = "dotted", color = "grey60") +
  geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi), height = 0.3,
                 color = "grey40", linewidth = 0.3) +
  geom_point(aes(color = abs_change), size = 2) +
  scale_color_gradient(low = "grey60", high = "red3",
                       name = "|Change in g|") +
  labs(
    title    = "Leave-One-Out Sensitivity Analysis",
    subtitle = paste0("Original g = ", fmt(original_g, 3),
                      " (dashed line)"),
    x = "Hedges' g (with study removed)",
    y = NULL
  ) +
  theme_meta() +
  theme(axis.text.y = element_text(size = 6))

ggsave(loo_plot_path, p_loo, width = 10,
       height = max(6, k * 0.25 + 2), dpi = 300, bg = "white")
message("  Saved: ", loo_plot_path)


# ============================================================================
# 3. INFLUENCE DIAGNOSTICS
# ============================================================================
# metafor provides comprehensive influence measures analogous to
# regression diagnostics.

message("\n--- 3. Influence Diagnostics ---\n")

inf <- influence(res_re)

# Cook's distance: measures overall influence of each observation
cooks_d   <- inf$inf$cook.d
hat_vals  <- inf$inf$hat
dffits    <- inf$inf$dffits
rstudent  <- inf$inf$rstudent

# Identify influential cases
# Cook's distance > 4/k is a common threshold
cooks_threshold <- 4 / k
influential_cooks <- which(cooks_d > cooks_threshold)

# Studentized residuals > |3| suggest outliers
outlier_resid <- which(abs(rstudent) > 3)

# Hat values > 2*(p+1)/k suggest leverage points
hat_threshold <- 2 * 2 / k
high_leverage <- which(hat_vals > hat_threshold)

message("  Cook's distance threshold (4/k): ", fmt(cooks_threshold, 4))
message("  Influential cases (Cook's d): ",
        ifelse(length(influential_cooks) > 0,
               paste(res_re$slab[influential_cooks], collapse = "; "),
               "None"))
message("  Outliers (|rstudent| > 3): ",
        ifelse(length(outlier_resid) > 0,
               paste(res_re$slab[outlier_resid], collapse = "; "),
               "None"))
message("  High leverage: ",
        ifelse(length(high_leverage) > 0,
               paste(length(high_leverage), "cases"), "None"))

# --- Influence diagnostic plots ---
inf_plot_path <- file.path(fig_dir, "influence_plot.png")
png(inf_plot_path, width = 12, height = 10, units = "in", res = 300)
plot(inf, layout = c(8, 1))
dev.off()
message("  Saved: ", inf_plot_path)

# --- Baujat plot (contribution to Q vs. influence on estimate) ---
baujat_path <- file.path(fig_dir, "baujat_plot.png")
png(baujat_path, width = 8, height = 6, units = "in", res = 300)
baujat(res_re, main = "Baujat Plot: Contribution to Heterogeneity vs. Influence")
dev.off()
message("  Saved: ", baujat_path)

# --- GOSH plot (graphical display of study heterogeneity) ---
# Only run for small k due to computational cost (2^k subsets)
if (k <= 20) {
  message("\n  Running GOSH analysis (k = ", k, "; this may take a moment)...")
  gosh_path <- file.path(fig_dir, "gosh_plot.png")
  gosh_res <- gosh(res_re, subsets = min(2^k, 10000))
  png(gosh_path, width = 8, height = 6, units = "in", res = 300)
  plot(gosh_res, main = "GOSH Plot")
  dev.off()
  message("  Saved: ", gosh_path)
} else {
  message("  Skipping GOSH plot (k = ", k, " > 20; too many subsets)")
}


# ============================================================================
# 4. OUTLIER REMOVAL SENSITIVITY
# ============================================================================
# Re-estimate after removing statistical outliers.

message("\n--- 4. Outlier Removal Sensitivity ---\n")

# Method 1: Remove studies with |rstudent| > 2
outliers_2 <- which(abs(rstudent) > 2)

if (length(outliers_2) > 0) {
  message("  Removing ", length(outliers_2), " outliers (|rstudent| > 2):")
  for (i in outliers_2) {
    message("    ", res_re$slab[i], " (rstudent = ", fmt(rstudent[i], 2), ")")
  }

  dat_no_outliers <- dat[-outliers_2, ]
  res_no_outliers <- rma(yi = hedges_g, vi = var_g, data = dat_no_outliers,
                          method = "REML")

  message("  Without outliers: g = ", fmt(coef(res_no_outliers), 3),
          " [", fmt(res_no_outliers$ci.lb, 3), ", ",
          fmt(res_no_outliers$ci.ub, 3), "]",
          ", k = ", res_no_outliers$k)
  message("  Change: ", fmt(coef(res_no_outliers) - original_g, 4))

  sensitivity_results$no_outliers <- list(
    g = coef(res_no_outliers),
    ci = c(res_no_outliers$ci.lb, res_no_outliers$ci.ub),
    k = res_no_outliers$k,
    n_removed = length(outliers_2)
  )
} else {
  message("  No outliers detected (|rstudent| > 2)")
  sensitivity_results$no_outliers <- list(g = original_g, k = k, n_removed = 0)
}

# Method 2: Remove influential studies (Cook's distance)
if (length(influential_cooks) > 0) {
  dat_no_influential <- dat[-influential_cooks, ]
  res_no_influential <- rma(yi = hedges_g, vi = var_g, data = dat_no_influential,
                             method = "REML")
  message("\n  Without influential (Cook's d): g = ",
          fmt(coef(res_no_influential), 3),
          " [", fmt(res_no_influential$ci.lb, 3), ", ",
          fmt(res_no_influential$ci.ub, 3), "]")
}


# ============================================================================
# 5. QUALITY-BASED SENSITIVITY
# ============================================================================
# Restrict to studies rated as high or moderate quality.

message("\n--- 5. Quality-Based Sensitivity ---\n")

if ("quality" %in% names(dat) && !all(is.na(dat$quality))) {
  # High quality only
  dat_high_q <- dat %>% filter(quality == "High Quality")
  if (nrow(dat_high_q) >= 3) {
    res_high_q <- rma(yi = hedges_g, vi = var_g, data = dat_high_q,
                       method = "REML")
    message("  High quality only: g = ", fmt(coef(res_high_q), 3),
            " [", fmt(res_high_q$ci.lb, 3), ", ", fmt(res_high_q$ci.ub, 3), "]",
            ", k = ", res_high_q$k)
    sensitivity_results$high_quality <- list(
      g = coef(res_high_q), k = res_high_q$k)
  } else {
    message("  Too few high-quality studies (k = ", nrow(dat_high_q), ")")
  }

  # High + moderate quality
  dat_hm_q <- dat %>% filter(quality %in% c("High Quality", "Moderate Quality"))
  if (nrow(dat_hm_q) >= 3) {
    res_hm_q <- rma(yi = hedges_g, vi = var_g, data = dat_hm_q,
                     method = "REML")
    message("  High + moderate quality: g = ", fmt(coef(res_hm_q), 3),
            " [", fmt(res_hm_q$ci.lb, 3), ", ", fmt(res_hm_q$ci.ub, 3), "]",
            ", k = ", res_hm_q$k)
    sensitivity_results$hm_quality <- list(
      g = coef(res_hm_q), k = res_hm_q$k)
  }
} else {
  message("  Quality variable not available. Skipping.")

  # Alternative: use rob_overall if available
  if ("rob_overall" %in% names(dat) && !all(is.na(dat$rob_overall))) {
    dat_low_rob <- dat %>% filter(rob_overall >= 1)  # Exclude high risk
    if (nrow(dat_low_rob) >= 3) {
      res_low_rob <- rma(yi = hedges_g, vi = var_g, data = dat_low_rob,
                          method = "REML")
      message("  Low/some-concern RoB only: g = ", fmt(coef(res_low_rob), 3),
              ", k = ", res_low_rob$k)
    }
  }
}


# ============================================================================
# 6. DESIGN-BASED SENSITIVITY
# ============================================================================

message("\n--- 6. Design-Based Sensitivity ---\n")

if ("design" %in% names(dat)) {
  # RCT only
  dat_rct <- dat %>% filter(design == 1)
  if (nrow(dat_rct) >= 3) {
    res_rct <- rma(yi = hedges_g, vi = var_g, data = dat_rct, method = "REML")
    message("  RCT only: g = ", fmt(coef(res_rct), 3),
            " [", fmt(res_rct$ci.lb, 3), ", ", fmt(res_rct$ci.ub, 3), "]",
            ", k = ", res_rct$k)
    sensitivity_results$rct_only <- list(g = coef(res_rct), k = res_rct$k)
  } else {
    message("  Too few RCTs (k = ", nrow(dat_rct), ")")
  }

  # Experimental only (RCT + quasi-experimental, excluding pre-post)
  dat_exp <- dat %>% filter(design %in% c(1, 2))
  if (nrow(dat_exp) >= 3) {
    res_exp <- rma(yi = hedges_g, vi = var_g, data = dat_exp, method = "REML")
    message("  Experimental only (RCT + quasi): g = ", fmt(coef(res_exp), 3),
            " [", fmt(res_exp$ci.lb, 3), ", ", fmt(res_exp$ci.ub, 3), "]",
            ", k = ", res_exp$k)
    sensitivity_results$experimental_only <- list(g = coef(res_exp), k = res_exp$k)
  }
}

# Pre-post sensitivity
if ("pre_post" %in% names(dat)) {
  # Post-test only designs
  dat_post <- dat %>% filter(pre_post == 0)
  if (nrow(dat_post) >= 3) {
    res_post <- rma(yi = hedges_g, vi = var_g, data = dat_post, method = "REML")
    message("  Post-test only: g = ", fmt(coef(res_post), 3),
            ", k = ", res_post$k)
  }

  # Gain score designs
  dat_gain <- dat %>% filter(pre_post == 1)
  if (nrow(dat_gain) >= 3) {
    res_gain <- rma(yi = hedges_g, vi = var_g, data = dat_gain, method = "REML")
    message("  Gain scores only: g = ", fmt(coef(res_gain), 3),
            ", k = ", res_gain$k)
  }
}


# ============================================================================
# 7. OUTCOME TYPE SENSITIVITY
# ============================================================================

message("\n--- 7. Outcome Type Sensitivity ---\n")

if ("outcome_type" %in% names(dat)) {
  for (ot in sort(unique(dat$outcome_type[!is.na(dat$outcome_type)]))) {
    dat_ot <- dat %>% filter(outcome_type == ot)
    if (nrow(dat_ot) >= 3) {
      res_ot <- rma(yi = hedges_g, vi = var_g, data = dat_ot, method = "REML")
      label <- OUTCOME_TYPE_LABELS[as.character(ot)]
      message("  ", label, ": g = ", fmt(coef(res_ot), 3),
              " [", fmt(res_ot$ci.lb, 3), ", ", fmt(res_ot$ci.ub, 3), "]",
              ", k = ", res_ot$k)
    }
  }
}


# ============================================================================
# 8. CUMULATIVE META-ANALYSIS BY YEAR
# ============================================================================
# Shows how the overall estimate evolves as studies are added chronologically.

message("\n--- 8. Cumulative Meta-Analysis ---\n")

if ("year" %in% names(dat)) {
  # Sort by publication year
  dat_sorted <- dat %>% arrange(year)
  res_sorted <- rma(yi = hedges_g, vi = var_g, data = dat_sorted,
                     method = "REML", slab = dat_sorted$study_label)

  cum_res <- cumul(res_sorted, order = dat_sorted$year)

  # Plot cumulative forest
  cum_path <- file.path(fig_dir, "cumulative_ma.png")
  png(cum_path, width = 10, height = max(6, k * 0.3 + 2),
      units = "in", res = 300)
  par(mar = c(4, 8, 2, 2))
  forest(cum_res, xlab = "Cumulative Hedges' g",
         main = "Cumulative Meta-Analysis by Publication Year",
         digits = 3, cex = 0.7)
  dev.off()
  message("  Saved: ", cum_path)

  # ggplot version
  cum_gg_path <- file.path(fig_dir, "cumulative_ma_ggplot.png")
  cum_df <- tibble(
    study = cum_res$slab,
    year  = dat_sorted$year,
    g     = cum_res$estimate,
    ci_lo = cum_res$ci.lb,
    ci_hi = cum_res$ci.ub,
    k     = 1:length(cum_res$estimate)
  )

  p_cum <- ggplot(cum_df, aes(x = k, y = g)) +
    geom_hline(yintercept = original_g, linetype = "dashed", color = "steelblue") +
    geom_hline(yintercept = 0, linetype = "dotted", color = "grey60") +
    geom_ribbon(aes(ymin = ci_lo, ymax = ci_hi), fill = "steelblue", alpha = 0.2) +
    geom_line(color = "darkblue", linewidth = 0.8) +
    geom_point(color = "darkblue", size = 1.5) +
    labs(
      title    = "Cumulative Meta-Analysis",
      subtitle = "Studies added chronologically by publication year",
      x        = "Number of Studies Added",
      y        = "Cumulative Hedges' g"
    ) +
    theme_meta()

  ggsave(cum_gg_path, p_cum, width = 8, height = 5, dpi = 300, bg = "white")
  message("  Saved: ", cum_gg_path)
}


# ============================================================================
# 9. MODEL SPECIFICATION SENSITIVITY
# ============================================================================
# Compare results across different RE estimators.

message("\n--- 9. Model Specification Sensitivity ---\n")

estimators <- c("REML", "DL", "PM", "EB", "SJ", "ML")
est_results <- data.frame()

for (est in estimators) {
  tryCatch({
    res_est <- rma(yi = hedges_g, vi = var_g, data = dat, method = est)
    est_results <- rbind(est_results, data.frame(
      estimator = est,
      g         = coef(res_est),
      se        = res_est$se,
      ci_lo     = res_est$ci.lb,
      ci_hi     = res_est$ci.ub,
      tau2      = res_est$tau2,
      I2        = res_est$I2
    ))
    message("  ", est, ": g = ", fmt(coef(res_est), 4),
            " [", fmt(res_est$ci.lb, 4), ", ", fmt(res_est$ci.ub, 4), "]",
            ", tau2 = ", fmt(res_est$tau2, 4))
  }, error = function(e) {
    message("  ", est, ": Error - ", conditionMessage(e))
  })
}

# Check consistency
if (nrow(est_results) >= 2) {
  g_range <- range(est_results$g)
  message("\n  Effect size range across estimators: [",
          fmt(g_range[1], 4), ", ", fmt(g_range[2], 4), "]")
  message("  Variation: ", fmt(diff(g_range), 4))

  if (diff(g_range) < 0.05) {
    message("  => Results are highly robust to estimator choice")
  } else if (diff(g_range) < 0.10) {
    message("  => Results are moderately robust to estimator choice")
  } else {
    message("  => Some sensitivity to estimator choice detected")
  }
}

sensitivity_results$estimator_range <- if (nrow(est_results) >= 2) diff(range(est_results$g)) else NA


# ============================================================================
# 10. COMPILE AND SAVE RESULTS
# ============================================================================

message("\n\n--- 10. Sensitivity Analysis Summary ---\n")

# Build summary table
summary_rows <- list()
summary_rows[[1]] <- tibble(Analysis = "Original", g = original_g, k = k, Note = "Baseline")

if (!is.null(sensitivity_results$no_outliers)) {
  summary_rows[[length(summary_rows) + 1]] <- tibble(
    Analysis = "Without outliers",
    g = sensitivity_results$no_outliers$g,
    k = sensitivity_results$no_outliers$k,
    Note = paste0(sensitivity_results$no_outliers$n_removed, " removed"))
}
if (!is.null(sensitivity_results$high_quality)) {
  summary_rows[[length(summary_rows) + 1]] <- tibble(
    Analysis = "High quality only",
    g = sensitivity_results$high_quality$g,
    k = sensitivity_results$high_quality$k,
    Note = "RoB = Low")
}
if (!is.null(sensitivity_results$rct_only)) {
  summary_rows[[length(summary_rows) + 1]] <- tibble(
    Analysis = "RCT only",
    g = sensitivity_results$rct_only$g,
    k = sensitivity_results$rct_only$k,
    Note = "Design = RCT")
}
if (!is.null(sensitivity_results$experimental_only)) {
  summary_rows[[length(summary_rows) + 1]] <- tibble(
    Analysis = "Experimental only",
    g = sensitivity_results$experimental_only$g,
    k = sensitivity_results$experimental_only$k,
    Note = "RCT + quasi-exp")
}

sens_summary <- bind_rows(summary_rows) %>%
  mutate(
    change = g - original_g,
    g = round(g, 4),
    change = round(change, 4)
  )

print(sens_summary)

# Save
sens_path <- file.path(PATHS$output, "sensitivity_summary.csv")
readr::write_csv(sens_summary, sens_path)
message("Saved: ", sens_path)

# Save estimator comparison
if (nrow(est_results) > 0) {
  est_path <- file.path(PATHS$output, "estimator_comparison.csv")
  readr::write_csv(est_results, est_path)
  message("Saved: ", est_path)
}

# Save leave-one-out results
loo_path <- file.path(PATHS$output, "leave_one_out.csv")
readr::write_csv(loo_df, loo_path)
message("Saved: ", loo_path)

# Comprehensive report
report_path <- file.path(PATHS$output, "sensitivity_analysis_report.txt")
sink(report_path)

cat("=======================================================\n")
cat("Sensitivity Analysis Report\n")
cat(paste("Date:", Sys.Date()), "\n")
cat("=======================================================\n\n")
cat("Original: ", fmt_es(original_g, original_ci[1], original_ci[2], 4), "\n\n")

cat("--- Leave-One-Out ---\n")
cat("Fragile to single-study removal: ",
    ifelse(sensitivity_results$loo_fragile, "YES", "NO"), "\n")
cat("Top 5 most influential:\n")
for (i in 1:min(5, nrow(loo_df))) {
  cat("  ", loo_df$study[i], ": change = ", fmt(loo_df$g_change[i], 4), "\n")
}

cat("\n--- Influence Diagnostics ---\n")
cat("Influential (Cook's d > ", fmt(cooks_threshold, 4), "): ",
    length(influential_cooks), "\n")
cat("Outliers (|rstudent| > 3): ", length(outlier_resid), "\n")

cat("\n--- Sensitivity Summary ---\n")
print(as.data.frame(sens_summary))

cat("\n--- Estimator Comparison ---\n")
if (nrow(est_results) > 0) print(as.data.frame(est_results))

cat("\n--- Conclusion ---\n")
if (!is.null(sensitivity_results$estimator_range) && !is.na(sensitivity_results$estimator_range)) {
  if (sensitivity_results$estimator_range < 0.05 && !sensitivity_results$loo_fragile) {
    cat("Overall: Results are robust across multiple sensitivity analyses.\n")
  } else {
    cat("Overall: Some sensitivity detected. Interpret with appropriate caution.\n")
  }
}

sink()
message("Report saved to: ", report_path)

message("\n========== 06: Sensitivity Analysis Complete ==========\n")
