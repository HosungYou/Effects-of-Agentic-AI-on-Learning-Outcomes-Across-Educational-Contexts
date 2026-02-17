# ============================================================================
# 04_robust_variance.R
# Robust Variance Estimation for Dependent Effect Sizes
# ============================================================================
#
# Purpose:
#   Apply Robust Variance Estimation (RVE) via robumeta::robu() and compare
#   with the 3-level meta-analytic model (metafor::rma.mv) to handle
#   correlated effect sizes from studies contributing multiple outcomes.
#   Both approaches are standard for meta-analyses with dependent effects.
#
# Methods:
#   1. RVE with correlated effects weighting (robumeta::robu)
#   2. RVE with hierarchical effects weighting (robumeta::robu)
#   3. 3-level meta-analysis with nested random effects (metafor::rma.mv)
#   4. Cluster-robust inference via clubSandwich (applied to rma.mv)
#   5. Comparison of all approaches
#
# Input:
#   data/04_final/ma_data_clean.rds
#
# Output:
#   analysis/output/rve_results.txt
#   analysis/output/rve_comparison.csv
#   analysis/output/model_rve.rds
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 04: Robust Variance Estimation ==========\n")


# ============================================================================
# 1. LOAD DATA
# ============================================================================

dat <- readRDS(file.path(PATHS$data_final, "ma_data_clean.rds"))
message("Loaded ", nrow(dat), " effect sizes from ", n_distinct(dat$study_id), " studies")

# Summarize dependency structure
dep_summary <- dat %>%
  group_by(study_id) %>%
  summarise(n_es = n(), .groups = "drop")

n_single <- sum(dep_summary$n_es == 1)
n_multi  <- sum(dep_summary$n_es > 1)
total_es <- sum(dep_summary$n_es)

message("  Single-ES studies: ", n_single)
message("  Multi-ES studies:  ", n_multi)
message("  Total ES:          ", total_es)

if (n_multi == 0) {
  message("\n  No dependent effect sizes found.")
  message("  RVE is not required but will be fitted for completeness.")
}


# ============================================================================
# 2. RVE: CORRELATED EFFECTS MODEL (robumeta)
# ============================================================================
# The correlated effects model assumes a common correlation (rho) among
# effect sizes within the same study. Default rho = 0.8 is standard
# in educational research (Tanner-Smith & Tipton, 2014).

message("\n--- 2. RVE: Correlated Effects Model ---\n")

# Fit correlated effects model
res_rve_ce <- robu(
  formula   = hedges_g ~ 1,
  data      = dat,
  studynum  = study_id,
  var.eff.size = var_g,
  modelweights = "CORR",
  rho       = 0.8,           # Assumed within-study correlation
  small     = TRUE            # Small-sample correction (Tipton, 2015)
)

print(res_rve_ce)

# Extract key statistics
rve_ce_g     <- res_rve_ce$b.r
rve_ce_se    <- res_rve_ce$reg_table$SE
rve_ce_ci_lo <- res_rve_ce$reg_table$CI.L
rve_ce_ci_hi <- res_rve_ce$reg_table$CI.U
rve_ce_df    <- res_rve_ce$reg_table$dfs
rve_ce_t     <- res_rve_ce$reg_table$t
rve_ce_p     <- res_rve_ce$reg_table$prob
rve_ce_tau2  <- res_rve_ce$mod_info$tau.sq
rve_ce_I2    <- res_rve_ce$mod_info$I.2

message("  g = ", fmt(rve_ce_g, 4),
        " [", fmt(rve_ce_ci_lo, 4), ", ", fmt(rve_ce_ci_hi, 4), "]")
message("  t(", fmt(rve_ce_df, 1), ") = ", fmt(rve_ce_t, 3),
        ", p ", fmt_p(rve_ce_p))
message("  tau-squared = ", fmt(rve_ce_tau2, 4))
message("  I-squared = ", fmt(rve_ce_I2, 1), "%")


# ============================================================================
# 3. RVE: HIERARCHICAL EFFECTS MODEL (robumeta)
# ============================================================================
# The hierarchical effects model does not assume a common correlation
# among effect sizes but instead models within-study variance.

message("\n--- 3. RVE: Hierarchical Effects Model ---\n")

res_rve_hier <- robu(
  formula   = hedges_g ~ 1,
  data      = dat,
  studynum  = study_id,
  var.eff.size = var_g,
  modelweights = "HIER",
  small     = TRUE
)

print(res_rve_hier)

rve_hier_g     <- res_rve_hier$b.r
rve_hier_se    <- res_rve_hier$reg_table$SE
rve_hier_ci_lo <- res_rve_hier$reg_table$CI.L
rve_hier_ci_hi <- res_rve_hier$reg_table$CI.U
rve_hier_df    <- res_rve_hier$reg_table$dfs
rve_hier_p     <- res_rve_hier$reg_table$prob

message("  g = ", fmt(rve_hier_g, 4),
        " [", fmt(rve_hier_ci_lo, 4), ", ", fmt(rve_hier_ci_hi, 4), "]")
message("  df = ", fmt(rve_hier_df, 1), ", p ", fmt_p(rve_hier_p))


# ============================================================================
# 4. SENSITIVITY ANALYSIS: VARYING RHO
# ============================================================================
# Test sensitivity of results to the assumed within-study correlation rho.

message("\n--- 4. Sensitivity to Assumed Rho ---\n")

rho_values <- c(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
rho_sensitivity <- data.frame()

for (rho in rho_values) {
  tryCatch({
    res_rho <- robu(
      formula   = hedges_g ~ 1,
      data      = dat,
      studynum  = study_id,
      var.eff.size = var_g,
      modelweights = "CORR",
      rho       = rho,
      small     = TRUE
    )

    rho_sensitivity <- rbind(rho_sensitivity, data.frame(
      rho     = rho,
      g       = res_rho$b.r,
      se      = res_rho$reg_table$SE,
      ci_lo   = res_rho$reg_table$CI.L,
      ci_hi   = res_rho$reg_table$CI.U,
      df      = res_rho$reg_table$dfs,
      p       = res_rho$reg_table$prob,
      tau2    = res_rho$mod_info$tau.sq
    ))

    message("  rho = ", rho, ": g = ", fmt(res_rho$b.r, 4),
            " [", fmt(res_rho$reg_table$CI.L, 4), ", ",
            fmt(res_rho$reg_table$CI.U, 4), "]")

  }, error = function(e) {
    message("  rho = ", rho, ": Error - ", conditionMessage(e))
  })
}

# Check if results are robust across rho values
if (nrow(rho_sensitivity) >= 2) {
  g_range <- range(rho_sensitivity$g)
  message("\n  Effect size range across rho: [",
          fmt(g_range[1], 4), ", ", fmt(g_range[2], 4), "]")
  message("  Variation: ", fmt(diff(g_range), 4))

  if (diff(g_range) < 0.05) {
    message("  => Results are robust to assumed rho (variation < 0.05)")
  } else {
    message("  => Results show some sensitivity to assumed rho")
  }
}


# ============================================================================
# 5. THREE-LEVEL MODEL (metafor::rma.mv)
# ============================================================================
# Alternative to RVE: explicitly model the hierarchical structure with
# random effects at the effect-size level (Level 2) and study level (Level 3).

message("\n--- 5. Three-Level Meta-Analytic Model ---\n")

res_3lvl <- rma.mv(
  yi     = hedges_g,
  V      = var_g,
  random = ~ 1 | study_id / es_id,
  data   = dat,
  method = "REML"
)

print(summary(res_3lvl))

# Variance components
sigma2_within  <- res_3lvl$sigma2[2]
sigma2_between <- res_3lvl$sigma2[1]
total_hetero   <- sigma2_within + sigma2_between

# I-squared decomposition (Cheung, 2014)
typical_vi  <- mean(dat$var_g)
I2_total    <- total_hetero / (total_hetero + typical_vi) * 100
I2_level2   <- sigma2_within / (total_hetero + typical_vi) * 100
I2_level3   <- sigma2_between / (total_hetero + typical_vi) * 100

message("  g = ", fmt(coef(res_3lvl), 4),
        " [", fmt(res_3lvl$ci.lb, 4), ", ", fmt(res_3lvl$ci.ub, 4), "]")
message("  sigma2_within  (L2): ", fmt(sigma2_within, 4))
message("  sigma2_between (L3): ", fmt(sigma2_between, 4))
message("  I2_total:    ", fmt(I2_total, 1), "%")
message("  I2_level2:   ", fmt(I2_level2, 1), "% (within-study)")
message("  I2_level3:   ", fmt(I2_level3, 1), "% (between-study)")


# ============================================================================
# 6. CLUSTER-ROBUST INFERENCE (clubSandwich applied to rma.mv)
# ============================================================================
# Combine the 3-level model with cluster-robust variance estimation
# for the most rigorous handling of dependent effects.

message("\n--- 6. Cluster-Robust Inference (clubSandwich) ---\n")

# CR2 estimator (Tipton & Pustejovsky, 2015) with Satterthwaite df
cr_test <- tryCatch({
  coef_test(res_3lvl, vcov = "CR2", cluster = dat$study_id)
}, error = function(e) {
  message("  clubSandwich::coef_test failed: ", conditionMessage(e))
  message("  Falling back to CR1 estimator.")
  tryCatch(
    coef_test(res_3lvl, vcov = "CR1", cluster = dat$study_id),
    error = function(e2) {
      message("  CR1 also failed: ", conditionMessage(e2))
      NULL
    }
  )
})

if (!is.null(cr_test)) {
  print(cr_test)

  cr_g     <- cr_test$beta
  cr_se    <- cr_test$SE
  cr_df    <- cr_test$df
  cr_t     <- cr_test$tstat
  cr_p     <- cr_test$p_Satt

  # Compute CI from t-distribution
  t_crit    <- qt(1 - (1 - CONF_LEVEL) / 2, df = cr_df)
  cr_ci_lo  <- cr_g - t_crit * cr_se
  cr_ci_hi  <- cr_g + t_crit * cr_se

  message("\n  g = ", fmt(cr_g, 4),
          " [", fmt(cr_ci_lo, 4), ", ", fmt(cr_ci_hi, 4), "]")
  message("  t(", fmt(cr_df, 1), ") = ", fmt(cr_t, 3),
          ", p ", fmt_p(cr_p))
}


# ============================================================================
# 7. RVE MODERATOR TESTS
# ============================================================================
# Apply RVE to key moderator analyses for robust inference.

message("\n--- 7. RVE Moderator Tests ---\n")

run_rve_moderator <- function(data, moderator, label) {
  message("\n  RVE Moderator: ", label)

  d <- data[!is.na(data[[moderator]]), ]
  if (nrow(d) < 5) {
    message("    Insufficient data. Skipping.")
    return(NULL)
  }

  form <- as.formula(paste("hedges_g ~ factor(", moderator, ")"))

  tryCatch({
    res <- robu(
      formula      = form,
      data         = d,
      studynum     = study_id,
      var.eff.size = var_g,
      modelweights = "CORR",
      rho          = 0.8,
      small        = TRUE
    )

    # Wald-type test for moderator effect
    wald <- Wald_test(
      res,
      constraints = constrain_zero(2:length(res$b.r)),
      vcov = "CR2"
    )

    message("    Wald test: F = ", fmt(wald$Fstat, 3),
            ", df1 = ", wald$df_num, ", df2 = ", fmt(wald$df_denom, 1),
            ", p ", fmt_p(wald$p_val))

    return(list(
      model = res,
      wald  = wald,
      label = label
    ))
  }, error = function(e) {
    message("    Error: ", conditionMessage(e))
    return(NULL)
  })
}

# RQ2: Human oversight
rve_oversight <- run_rve_moderator(dat, "human_oversight", "Human Oversight (RQ2)")

# RQ3: Agent architecture
rve_arch <- run_rve_moderator(dat, "agent_architecture", "Agent Architecture (RQ3)")

# RQ4: Learning context
rve_context <- run_rve_moderator(dat, "learning_context", "Learning Context (RQ4)")

# Additional
rve_outcome <- run_rve_moderator(dat, "outcome_type", "Outcome Type")
rve_agency  <- run_rve_moderator(dat, "agency_level", "Agency Level (APCP)")
rve_blooms  <- run_rve_moderator(dat, "blooms_level", "Bloom's Level")


# ============================================================================
# 8. COMPARISON OF APPROACHES
# ============================================================================

message("\n--- 8. Comparison of All Approaches ---\n")

comparison <- tibble(
  Method = c(
    "Standard RE (rma)",
    "RVE Correlated Effects (rho=0.8)",
    "RVE Hierarchical Effects",
    "3-Level Model (rma.mv)",
    if (!is.null(cr_test)) "3-Level + clubSandwich (CR2)" else NULL
  ),
  g = c(
    {res_re_path <- file.path(PATHS$output, "model_re.rds")
     if (file.exists(res_re_path)) coef(readRDS(res_re_path))
     else coef(rma(yi = hedges_g, vi = var_g, data = dat, method = "REML"))},
    rve_ce_g,
    rve_hier_g,
    coef(res_3lvl),
    if (!is.null(cr_test)) cr_g else NULL
  ),
  CI_lower = c(
    {if (file.exists(res_re_path)) readRDS(res_re_path)$ci.lb
     else rma(yi = hedges_g, vi = var_g, data = dat, method = "REML")$ci.lb},
    rve_ce_ci_lo,
    rve_hier_ci_lo,
    res_3lvl$ci.lb,
    if (!is.null(cr_test)) cr_ci_lo else NULL
  ),
  CI_upper = c(
    {if (file.exists(res_re_path)) readRDS(res_re_path)$ci.ub
     else rma(yi = hedges_g, vi = var_g, data = dat, method = "REML")$ci.ub},
    rve_ce_ci_hi,
    rve_hier_ci_hi,
    res_3lvl$ci.ub,
    if (!is.null(cr_test)) cr_ci_hi else NULL
  )
)

comparison <- comparison %>%
  mutate(
    across(c(g, CI_lower, CI_upper), ~round(.x, 4)),
    CI_width = CI_upper - CI_lower
  )

print(comparison)

# Save comparison
comp_path <- file.path(PATHS$output, "rve_comparison.csv")
readr::write_csv(comparison, comp_path)
message("\nComparison table saved to: ", comp_path)


# ============================================================================
# 9. COMPREHENSIVE RESULTS REPORT
# ============================================================================

report_path <- file.path(PATHS$output, "rve_results.txt")
sink(report_path)

cat("=======================================================\n")
cat("Robust Variance Estimation Results\n")
cat(paste("Date:", Sys.Date()), "\n")
cat("=======================================================\n\n")

cat("--- Data Structure ---\n")
cat("  Total effect sizes:    ", total_es, "\n")
cat("  Single-ES studies:     ", n_single, "\n")
cat("  Multi-ES studies:      ", n_multi, "\n")
cat("  Total unique studies:  ", n_distinct(dat$study_id), "\n\n")

cat("--- RVE: Correlated Effects (rho = 0.8) ---\n")
print(res_rve_ce)

cat("\n--- RVE: Hierarchical Effects ---\n")
print(res_rve_hier)

cat("\n--- Sensitivity to Rho ---\n")
print(rho_sensitivity)

cat("\n--- Three-Level Model ---\n")
print(summary(res_3lvl))

cat("\nI2 Decomposition:\n")
cat("  I2_total:    ", fmt(I2_total, 2), "%\n")
cat("  I2_level2:   ", fmt(I2_level2, 2), "% (within-study)\n")
cat("  I2_level3:   ", fmt(I2_level3, 2), "% (between-study)\n")

if (!is.null(cr_test)) {
  cat("\n--- clubSandwich CR2 ---\n")
  print(cr_test)
}

cat("\n--- Comparison of Approaches ---\n")
print(as.data.frame(comparison))

cat("\n--- RVE Moderator Tests ---\n")
for (res_mod in list(rve_oversight, rve_arch, rve_context,
                     rve_outcome, rve_agency, rve_blooms)) {
  if (!is.null(res_mod)) {
    cat("\n", res_mod$label, ":\n")
    cat("  Wald F = ", fmt(res_mod$wald$Fstat, 3),
        ", p ", fmt_p(res_mod$wald$p_val), "\n")
  }
}

sink()
message("Full report saved to: ", report_path)

# Save model objects
saveRDS(res_rve_ce, file.path(PATHS$output, "model_rve_ce.rds"))
saveRDS(res_3lvl, file.path(PATHS$output, "model_3lvl_rve.rds"))
saveRDS(rho_sensitivity, file.path(PATHS$output, "rho_sensitivity.rds"))
message("Model objects saved.")

message("\n========== 04: Robust Variance Estimation Complete ==========\n")
