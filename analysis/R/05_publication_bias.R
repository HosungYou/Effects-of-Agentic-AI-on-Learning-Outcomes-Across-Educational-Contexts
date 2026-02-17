# ============================================================================
# 05_publication_bias.R
# Publication Bias Assessment
# ============================================================================
#
# Purpose:
#   Conduct a comprehensive assessment of publication bias using multiple
#   complementary methods. No single test is sufficient; convergence across
#   methods strengthens confidence in the conclusions.
#
# Methods:
#   1. Funnel plot (visual inspection for asymmetry)
#   2. Egger's regression test (regression-based asymmetry test)
#   3. Trim-and-fill (Duval & Tweedie, 2000)
#   4. PET-PEESE (Stanley & Doucouliagos, 2014)
#   5. Selection models (Vevea & Hedges, 1995; via weightr package)
#   6. Sensitivity analysis (PublicationBias package; Mathur & VanderWeele)
#   7. Fail-safe N (Rosenthal, 1979; Orwin, 1983)
#
# Input:
#   data/04_final/ma_data_clean.rds
#   analysis/output/model_primary.rds
#
# Output:
#   analysis/output/publication_bias/funnel_plot.png
#   analysis/output/publication_bias/funnel_plot_trimfill.png
#   analysis/output/publication_bias/egger_test.txt
#   analysis/output/publication_bias/publication_bias_report.txt
#   analysis/output/publication_bias/pub_bias_summary.csv
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 05: Publication Bias Assessment ==========\n")


# ============================================================================
# 1. LOAD DATA AND MODELS
# ============================================================================

dat <- readRDS(file.path(PATHS$data_final, "ma_data_clean.rds"))

# Load primary model (standard RE for publication bias tests)
primary_path <- file.path(PATHS$output, "model_primary.rds")
re_path      <- file.path(PATHS$output, "model_re.rds")

if (file.exists(re_path)) {
  res_re <- readRDS(re_path)
} else {
  message("Fitting standard RE model for publication bias tests...")
  res_re <- rma(yi = hedges_g, vi = var_g, data = dat, method = "REML",
                slab = dat$study_label)
}

k <- res_re$k
message("Loaded ", k, " effect sizes for publication bias assessment")

out_dir <- PATHS$out_pub
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Initialize results collector
bias_results <- list()


# ============================================================================
# 2. FUNNEL PLOT
# ============================================================================

message("\n--- 2. Funnel Plot ---\n")

# --- 2.1 Standard funnel plot ---
funnel_path <- file.path(out_dir, "funnel_plot.png")
png(funnel_path, width = 8, height = 6, units = "in", res = 300)
par(mar = c(5, 5, 3, 2))
funnel(
  res_re,
  xlab   = "Hedges' g",
  ylab   = "Standard Error",
  main   = "Funnel Plot: Agentic AI Effects on Learning",
  back   = "white",
  shade  = c("white", "gray90", "gray75"),
  hlines = "grey80",
  level  = c(90, 95, 99),
  legend = TRUE,
  digits = 2
)
dev.off()
message("  Saved: ", funnel_path)

# --- 2.2 Contour-enhanced funnel plot ---
contour_path <- file.path(out_dir, "funnel_contour.png")
png(contour_path, width = 8, height = 6, units = "in", res = 300)
par(mar = c(5, 5, 3, 2))
funnel(
  res_re,
  xlab    = "Hedges' g",
  ylab    = "Standard Error",
  main    = "Contour-Enhanced Funnel Plot",
  level   = c(0.90, 0.95, 0.99),
  shade   = c("gray90", "gray70", "gray50"),
  refline = 0,
  legend  = TRUE
)
dev.off()
message("  Saved: ", contour_path)

# --- 2.3 ggplot funnel ---
funnel_gg_path <- file.path(out_dir, "funnel_ggplot.png")

dat_funnel <- tibble(
  g  = dat$hedges_g,
  se = dat$se_g,
  study = if ("study_label" %in% names(dat)) dat$study_label else paste("Study", dat$study_id)
)
overall_est <- coef(res_re)

p_funnel <- ggplot(dat_funnel, aes(x = g, y = se)) +
  # Significance regions
  geom_ribbon(
    data = tibble(
      se  = seq(0, max(dat_funnel$se) * 1.1, length.out = 100),
      lo  = overall_est - qnorm(0.975) * se,
      hi  = overall_est + qnorm(0.975) * se
    ),
    aes(x = NULL, y = se, xmin = lo, xmax = hi),
    fill = "gray90", alpha = 0.8
  ) +
  geom_vline(xintercept = overall_est, linetype = "dashed", color = "steelblue") +
  geom_vline(xintercept = 0, linetype = "dotted", color = "grey50") +
  geom_point(aes(size = 1/se^2), alpha = 0.7, color = "darkblue") +
  scale_y_reverse() +
  scale_size_continuous(range = c(1, 5), guide = "none") +
  labs(
    title    = "Funnel Plot: Agentic AI Effects on Learning Outcomes",
    subtitle = paste0("Overall g = ", fmt(overall_est, 3),
                      " (dashed line); k = ", k),
    x        = "Hedges' g",
    y        = "Standard Error"
  ) +
  theme_meta()

ggsave(funnel_gg_path, p_funnel, width = 8, height = 6, dpi = 300, bg = "white")
message("  Saved: ", funnel_gg_path)


# ============================================================================
# 3. EGGER'S REGRESSION TEST
# ============================================================================
# Tests for funnel plot asymmetry via regression of effect sizes on their
# precision (1/SE). A significant intercept suggests small-study effects.

message("\n--- 3. Egger's Regression Test ---\n")

egger <- regtest(res_re, model = "lm", predictor = "sei")
print(egger)

egger_z <- egger$zval
egger_p <- egger$pval

message("  Egger's test: z = ", fmt(egger_z, 3), ", p ", fmt_p(egger_p))

if (egger_p < ALPHA) {
  message("  => Significant funnel plot asymmetry detected (p < ", ALPHA, ")")
  bias_results$egger <- "Significant asymmetry"
} else {
  message("  => No significant asymmetry detected")
  bias_results$egger <- "No significant asymmetry"
}

# Also try rank correlation test (Begg & Mazumdar, 1994)
rank_test <- ranktest(res_re)
message("\n  Rank correlation test (Begg & Mazumdar):")
message("  Kendall's tau = ", fmt(rank_test$tau, 3),
        ", p ", fmt_p(rank_test$pval))


# ============================================================================
# 4. TRIM-AND-FILL
# ============================================================================
# Estimates the number of missing studies and adjusts the overall estimate.

message("\n--- 4. Trim-and-Fill ---\n")

# Left side (looking for suppressed small/null effects)
tf_left <- trimfill(res_re, side = "left")
print(tf_left)

n_filled_left <- tf_left$k0
tf_left_g     <- coef(tf_left)
tf_left_ci    <- c(tf_left$ci.lb, tf_left$ci.ub)

message("  Left side: ", n_filled_left, " studies imputed")
message("  Adjusted estimate: g = ", fmt(tf_left_g, 4),
        " [", fmt(tf_left_ci[1], 4), ", ", fmt(tf_left_ci[2], 4), "]")
message("  Original estimate: g = ", fmt(coef(res_re), 4))

# Right side (looking for suppressed negative effects -- less common)
tf_right <- trimfill(res_re, side = "right")
n_filled_right <- tf_right$k0
message("  Right side: ", n_filled_right, " studies imputed")

# Plot trim-and-fill funnel
tf_path <- file.path(out_dir, "funnel_plot_trimfill.png")
png(tf_path, width = 8, height = 6, units = "in", res = 300)
par(mar = c(5, 5, 3, 2))
funnel(tf_left,
       xlab  = "Hedges' g",
       ylab  = "Standard Error",
       main  = "Trim-and-Fill Funnel Plot",
       legend = TRUE)
dev.off()
message("  Saved: ", tf_path)

bias_results$trimfill <- paste0(
  n_filled_left, " studies imputed; adjusted g = ", fmt(tf_left_g, 3))


# ============================================================================
# 5. PET-PEESE
# ============================================================================
# Precision-Effect Test (PET): regress ES on SE. If PET intercept is
# significant, use PEESE (regress ES on variance) for corrected estimate.
# Stanley & Doucouliagos (2014)

message("\n--- 5. PET-PEESE ---\n")

# PET: yi ~ SE
res_pet <- rma(
  yi   = hedges_g,
  vi   = var_g,
  mods = ~ se_g,
  data = dat,
  method = "REML"
)

pet_intercept   <- coef(res_pet)[1]
pet_intercept_p <- res_pet$pval[1]
pet_slope       <- coef(res_pet)[2]
pet_slope_p     <- res_pet$pval[2]

message("  PET (yi ~ SE):")
message("    Intercept (bias-corrected estimate): ",
        fmt(pet_intercept, 4), ", p ", fmt_p(pet_intercept_p))
message("    Slope (small-study effect): ",
        fmt(pet_slope, 4), ", p ", fmt_p(pet_slope_p))

# PEESE: yi ~ variance
res_peese <- rma(
  yi   = hedges_g,
  vi   = var_g,
  mods = ~ var_g,
  data = dat,
  method = "REML"
)

peese_intercept   <- coef(res_peese)[1]
peese_intercept_p <- res_peese$pval[1]

message("\n  PEESE (yi ~ Var):")
message("    Intercept (bias-corrected estimate): ",
        fmt(peese_intercept, 4), ", p ", fmt_p(peese_intercept_p))

# Decision rule: Use PET if PET intercept is non-significant; else use PEESE
if (pet_intercept_p >= ALPHA) {
  petpeese_est   <- pet_intercept
  petpeese_label <- "PET (non-significant intercept)"
  message("\n  => PET intercept non-significant. Using PET estimate.")
} else {
  petpeese_est   <- peese_intercept
  petpeese_label <- "PEESE (PET intercept significant)"
  message("\n  => PET intercept significant. Using PEESE estimate.")
}

message("  PET-PEESE corrected estimate: g = ", fmt(petpeese_est, 4))
bias_results$petpeese <- paste0(petpeese_label, "; corrected g = ", fmt(petpeese_est, 3))


# ============================================================================
# 6. SELECTION MODELS (weightr package)
# ============================================================================
# Vevea & Hedges (1995) weight-function models for publication bias.

message("\n--- 6. Selection Models ---\n")

if (requireNamespace("weightr", quietly = TRUE)) {
  tryCatch({
    # Three-parameter selection model (one cut-point at p = 0.05)
    res_sel <- weightr::weightfunct(
      effect = dat$hedges_g,
      v      = dat$var_g,
      steps  = c(0.05, 1),
      table  = TRUE
    )

    print(res_sel)

    # Extract results
    sel_unadj_g <- res_sel[[1]]$par[1]
    sel_adj_g   <- res_sel[[2]]$par[1]

    message("  Unadjusted estimate:   g = ", fmt(sel_unadj_g, 4))
    message("  Selection-adjusted:    g = ", fmt(sel_adj_g, 4))

    # Likelihood ratio test for selection
    lr_stat <- -2 * (res_sel[[1]]$value - res_sel[[2]]$value)
    lr_df   <- length(res_sel[[2]]$par) - length(res_sel[[1]]$par)
    lr_p    <- pchisq(lr_stat, df = lr_df, lower.tail = FALSE)
    message("  LRT for selection: chi2 = ", fmt(lr_stat, 3),
            ", df = ", lr_df, ", p ", fmt_p(lr_p))

    bias_results$selection_model <- paste0(
      "Adjusted g = ", fmt(sel_adj_g, 3),
      "; LRT p ", fmt_p(lr_p))

  }, error = function(e) {
    message("  Selection model error: ", conditionMessage(e))
    bias_results$selection_model <- "Could not fit"
  })
} else {
  message("  weightr package not available. Skipping selection models.")
  bias_results$selection_model <- "Package not installed"
}


# ============================================================================
# 7. PUBLICATION BIAS SENSITIVITY ANALYSIS (PublicationBias package)
# ============================================================================
# Mathur & VanderWeele (2020): How severe would publication bias need to be
# to nullify the results?

message("\n--- 7. Sensitivity Analysis (PublicationBias) ---\n")

if (requireNamespace("PublicationBias", quietly = TRUE)) {
  tryCatch({
    # Significance funnel: what selection ratio would reduce the
    # meta-analytic estimate to a target value (e.g., 0)?
    sval <- PublicationBias::svalue(
      yi   = dat$hedges_g,
      vi   = dat$var_g,
      q    = 0,             # Target: null effect
      clustervar = dat$study_id,
      model = "robust"
    )

    message("  S-value for q = 0 (null effect):")
    message("    To shift the estimate to 0, significant results would need")
    message("    to be ", fmt(sval$sval, 1), "x more likely to be published")
    message("    than non-significant results.")

    if (sval$sval > 5) {
      message("    => Robust to substantial publication bias (S > 5)")
    } else if (sval$sval > 2) {
      message("    => Moderately robust to publication bias (2 < S < 5)")
    } else {
      message("    => Sensitive to publication bias (S < 2)")
    }

    bias_results$sensitivity <- paste0("S-value = ", fmt(sval$sval, 2))

  }, error = function(e) {
    message("  PublicationBias analysis error: ", conditionMessage(e))
    bias_results$sensitivity <- "Error in computation"
  })
} else {
  message("  PublicationBias package not available. Skipping.")
  bias_results$sensitivity <- "Package not installed"
}


# ============================================================================
# 8. FAIL-SAFE N
# ============================================================================
# How many studies with null results would be needed to render the overall
# effect non-significant? Computed for reference but recognized as limited.

message("\n--- 8. Fail-Safe N ---\n")

# Rosenthal's fail-safe N
fsn_rosenthal <- fsn(yi = hedges_g, vi = var_g, data = dat, type = "Rosenthal")
message("  Rosenthal's fail-safe N: ", fsn_rosenthal$fsnum)
message("    (5k + 10 threshold = ", 5 * k + 10, ")")
if (fsn_rosenthal$fsnum > 5 * k + 10) {
  message("    => Exceeds threshold. Result is robust.")
} else {
  message("    => Below threshold. Interpret with caution.")
}

# Orwin's fail-safe N (how many null studies to reduce g to 0.10)
fsn_orwin <- fsn(yi = hedges_g, vi = var_g, data = dat, type = "Orwin",
                  target = 0.10)
message("  Orwin's fail-safe N (to reduce g to 0.10): ", fsn_orwin$fsnum)

bias_results$failsafe_rosenthal <- fsn_rosenthal$fsnum
bias_results$failsafe_orwin     <- fsn_orwin$fsnum


# ============================================================================
# 9. SUMMARY OF ALL BIAS ASSESSMENTS
# ============================================================================

message("\n\n--- 9. Publication Bias Summary ---\n")

pub_bias_summary <- tibble(
  Method = c(
    "Egger's Regression Test",
    "Begg & Mazumdar Rank Test",
    "Trim-and-Fill (left)",
    "PET-PEESE",
    "Selection Model",
    "Sensitivity Analysis (S-value)",
    "Rosenthal Fail-Safe N",
    "Orwin Fail-Safe N (to g=0.10)"
  ),
  Result = c(
    paste0("z = ", fmt(egger_z, 3), ", p ", fmt_p(egger_p)),
    paste0("tau = ", fmt(rank_test$tau, 3), ", p ", fmt_p(rank_test$pval)),
    paste0(n_filled_left, " studies imputed; adjusted g = ", fmt(tf_left_g, 3)),
    paste0("Corrected g = ", fmt(petpeese_est, 3), " (", petpeese_label, ")"),
    ifelse(!is.null(bias_results$selection_model),
           bias_results$selection_model, "N/A"),
    ifelse(!is.null(bias_results$sensitivity),
           bias_results$sensitivity, "N/A"),
    paste0("N = ", fsn_rosenthal$fsnum, " (threshold: ", 5 * k + 10, ")"),
    paste0("N = ", fsn_orwin$fsnum)
  ),
  Interpretation = c(
    ifelse(egger_p < ALPHA, "Significant asymmetry detected",
           "No significant asymmetry"),
    ifelse(rank_test$pval < ALPHA, "Significant correlation detected",
           "No significant correlation"),
    ifelse(n_filled_left > 0,
           paste0("Possible bias; estimate changes by ",
                  fmt(abs(coef(res_re) - tf_left_g), 3)),
           "No adjustment needed"),
    ifelse(abs(petpeese_est - coef(res_re)) > 0.10,
           "Substantial correction suggests bias",
           "Minor correction; results likely robust"),
    "",
    "",
    ifelse(fsn_rosenthal$fsnum > 5 * k + 10,
           "Robust (exceeds 5k+10 threshold)", "Potentially fragile"),
    ""
  )
)

print(pub_bias_summary, n = 20, width = 120)

# Save summary
summary_path <- file.path(out_dir, "pub_bias_summary.csv")
readr::write_csv(pub_bias_summary, summary_path)
message("Summary saved to: ", summary_path)


# ============================================================================
# 10. COMPREHENSIVE REPORT
# ============================================================================

report_path <- file.path(out_dir, "publication_bias_report.txt")
sink(report_path)

cat("=======================================================\n")
cat("Publication Bias Assessment Report\n")
cat(paste("Date:", Sys.Date()), "\n")
cat("=======================================================\n\n")

cat("Original RE estimate: g = ", fmt(coef(res_re), 4),
    " [", fmt(res_re$ci.lb, 4), ", ", fmt(res_re$ci.ub, 4), "]\n")
cat("k = ", k, " effect sizes from ",
    n_distinct(dat$study_id), " studies\n\n")

cat("--- Egger's Regression Test ---\n")
print(egger)
cat("\nRank correlation test:\n")
print(rank_test)

cat("\n--- Trim-and-Fill ---\n")
cat("Left side:\n")
print(tf_left)
cat("\nRight side: ", n_filled_right, " studies imputed\n")

cat("\n--- PET-PEESE ---\n")
cat("PET intercept:  g = ", fmt(pet_intercept, 4),
    ", p ", fmt_p(pet_intercept_p), "\n")
cat("PEESE intercept: g = ", fmt(peese_intercept, 4),
    ", p ", fmt_p(peese_intercept_p), "\n")
cat("Decision: ", petpeese_label, "\n")
cat("Corrected estimate: g = ", fmt(petpeese_est, 4), "\n")

cat("\n--- Fail-Safe N ---\n")
cat("Rosenthal's: ", fsn_rosenthal$fsnum,
    " (threshold 5k+10 = ", 5 * k + 10, ")\n")
cat("Orwin's (to g=0.10): ", fsn_orwin$fsnum, "\n")

cat("\n--- Overall Summary ---\n\n")
print(as.data.frame(pub_bias_summary))

# Overall assessment
cat("\n\n--- Overall Assessment ---\n\n")
n_sig_tests <- sum(c(egger_p < ALPHA, rank_test$pval < ALPHA,
                     n_filled_left > 0))

if (n_sig_tests == 0) {
  cat("No significant evidence of publication bias across all tests.\n")
  cat("The overall effect estimate appears trustworthy.\n")
} else if (n_sig_tests <= 1) {
  cat("Limited evidence of publication bias (1 of 3 asymmetry tests significant).\n")
  cat("Results should be interpreted with some caution.\n")
} else {
  cat("Multiple indicators suggest publication bias may be present.\n")
  cat("Consider the trim-and-fill and PET-PEESE corrected estimates as\n")
  cat("lower bounds for the true effect.\n")
}

sink()
message("Report saved to: ", report_path)

message("\n========== 05: Publication Bias Assessment Complete ==========\n")
