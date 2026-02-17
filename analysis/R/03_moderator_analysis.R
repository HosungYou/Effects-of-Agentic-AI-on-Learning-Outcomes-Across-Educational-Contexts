# ============================================================================
# 03_moderator_analysis.R
# RQ2-RQ4: Moderator Analyses (Subgroup and Meta-Regression)
# ============================================================================
#
# Purpose:
#   Examine how the effect of Agentic AI on learning outcomes varies
#   across moderator variables. Addresses:
#     RQ2: Human oversight level
#     RQ3: Agent architecture (single vs. multi-agent)
#     RQ4: Learning context
#     Additional: agent role, agency level, modality, AI technology,
#                 adaptivity, subject domain, outcome type, Bloom's level,
#                 study design, measurement timing
#   Also includes meta-regression for continuous moderators
#   (publication year, sample size, duration).
#
# Input:
#   data/04_final/ma_data_clean.rds
#   analysis/output/model_primary.rds    (from 02_overall_effect.R)
#
# Output:
#   analysis/output/moderator_analysis/subgroup_*.csv
#   analysis/output/moderator_analysis/moderator_summary.csv
#   analysis/output/moderator_analysis/meta_regression_results.txt
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 03: Moderator Analysis (RQ2-RQ4) ==========\n")


# ============================================================================
# 1. LOAD DATA
# ============================================================================

dat <- readRDS(file.path(PATHS$data_final, "ma_data_clean.rds"))
message("Loaded ", nrow(dat), " effect sizes from ", n_distinct(dat$study_id), " studies")

# Check whether we need 3-level models
has_dependent <- any(dat$dependent_es, na.rm = TRUE)

# Output directory
out_dir <- PATHS$out_mod
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)


# ============================================================================
# 2. SUBGROUP ANALYSIS FUNCTION
# ============================================================================
# Generic function for running subgroup (categorical moderator) analyses.
# Fits mixed-effects model with moderator as fixed effect.
# Handles both rma() and rma.mv() depending on data structure.

run_subgroup_analysis <- function(data, moderator_col, moderator_label,
                                  min_k = 3, use_3level = has_dependent) {
  # ---- Preparation ----
  message("\n--- Subgroup Analysis: ", moderator_label, " ---")

  # Remove rows with missing moderator
  idx <- !is.na(data[[moderator_col]])
  d <- data[idx, ]
  n_excluded <- sum(!idx)
  if (n_excluded > 0) {
    message("  Excluded ", n_excluded, " rows with missing ", moderator_col)
  }

  if (nrow(d) == 0) {
    message("  No data available for this moderator. Skipping.")
    return(NULL)
  }

  # Check minimum k per subgroup
  subgroup_k <- d %>%
    group_by(!!sym(moderator_col)) %>%
    summarise(k = n(), .groups = "drop")

  too_few <- subgroup_k %>% filter(k < min_k)
  if (nrow(too_few) > 0) {
    message("  Warning: Subgroups with < ", min_k, " effect sizes: ",
            paste(too_few[[moderator_col]], collapse = ", "))
  }

  # ---- Fit omnibus test (moderator as fixed effect) ----
  mod_formula <- as.formula(paste("~ factor(", moderator_col, ")"))

  tryCatch({
    if (use_3level) {
      res_mod <- rma.mv(
        yi     = hedges_g,
        V      = var_g,
        mods   = mod_formula,
        random = ~ 1 | study_id / es_id,
        data   = d,
        method = "REML"
      )
    } else {
      res_mod <- rma(
        yi   = hedges_g,
        vi   = var_g,
        mods = mod_formula,
        data = d,
        method = "REML"
      )
    }

    # Omnibus test for moderator
    QM       <- res_mod$QM
    QM_df    <- res_mod$m
    QM_p     <- res_mod$QMp

    message("  Omnibus test: QM(", QM_df, ") = ", fmt(QM, 2),
            ", p ", fmt_p(QM_p))

    # ---- Fit separate models per subgroup ----
    levels_present <- sort(unique(d[[moderator_col]]))
    subgroup_results <- list()

    for (lvl in levels_present) {
      d_sub <- d[d[[moderator_col]] == lvl, ]
      k_sub <- nrow(d_sub)

      if (k_sub < 2) {
        message("  Subgroup '", lvl, "': k = ", k_sub, " (too few, skipping)")
        next
      }

      tryCatch({
        if (use_3level && n_distinct(d_sub$study_id) > 1 &&
            any(d_sub$dependent_es, na.rm = TRUE)) {
          res_sub <- rma.mv(
            yi     = hedges_g,
            V      = var_g,
            random = ~ 1 | study_id / es_id,
            data   = d_sub,
            method = "REML"
          )
        } else {
          res_sub <- rma(
            yi   = hedges_g,
            vi   = var_g,
            data = d_sub,
            method = "REML"
          )
        }

        # Compute prediction interval
        pi_sub <- tryCatch(
          compute_prediction_interval(res_sub),
          error = function(e) c(pi_lower = NA, pi_upper = NA)
        )

        subgroup_results[[as.character(lvl)]] <- tibble(
          moderator       = moderator_label,
          level           = as.character(lvl),
          k               = k_sub,
          n_studies       = n_distinct(d_sub$study_id),
          g               = coef(res_sub),
          se              = res_sub$se,
          ci_lower        = res_sub$ci.lb,
          ci_upper        = res_sub$ci.ub,
          p_value         = res_sub$pval,
          interpretation  = interpret_g(coef(res_sub)),
          pi_lower        = pi_sub["pi_lower"],
          pi_upper        = pi_sub["pi_upper"]
        )

        message("  ", lvl, ": g = ", fmt(coef(res_sub), 3),
                " [", fmt(res_sub$ci.lb, 3), ", ", fmt(res_sub$ci.ub, 3), "]",
                ", k = ", k_sub)

      }, error = function(e) {
        message("  Error fitting subgroup '", lvl, "': ", conditionMessage(e))
      })
    }

    # Combine subgroup results
    if (length(subgroup_results) > 0) {
      subgroup_df <- bind_rows(subgroup_results) %>%
        mutate(
          QM          = QM,
          QM_df       = QM_df,
          QM_p        = QM_p,
          significant = QM_p < ALPHA
        )

      return(subgroup_df)
    } else {
      return(NULL)
    }

  }, error = function(e) {
    message("  Error in moderator model: ", conditionMessage(e))
    return(NULL)
  })
}


# ============================================================================
# 3. RQ2: HUMAN OVERSIGHT LEVEL
# ============================================================================

res_oversight <- run_subgroup_analysis(
  dat, "human_oversight_f", "Human Oversight Level (RQ2)")


# ============================================================================
# 4. RQ3: AGENT ARCHITECTURE
# ============================================================================

res_architecture <- run_subgroup_analysis(
  dat, "agent_architecture_f", "Agent Architecture (RQ3)")


# ============================================================================
# 5. RQ4: LEARNING CONTEXT
# ============================================================================

res_context <- run_subgroup_analysis(
  dat, "learning_context_f", "Learning Context (RQ4)")


# ============================================================================
# 6. ADDITIONAL CATEGORICAL MODERATORS
# ============================================================================

message("\n\n--- Additional Moderator Analyses ---\n")

# Agent role
res_role <- run_subgroup_analysis(
  dat, "agent_role_f", "Agent Role")

# Agency level (APCP)
res_agency <- run_subgroup_analysis(
  dat, "agency_level_f", "Agency Level (APCP)")

# Agent modality
res_modality <- run_subgroup_analysis(
  dat, "agent_modality_f", "Agent Modality")

# AI technology base
res_tech <- run_subgroup_analysis(
  dat, "ai_technology_f", "AI Technology")

# Adaptivity level
res_adaptivity <- run_subgroup_analysis(
  dat, "adaptivity_level_f", "Adaptivity Level")

# Subject domain
res_domain <- run_subgroup_analysis(
  dat, "subject_domain_f", "Subject Domain")

# Outcome type
res_outcome <- run_subgroup_analysis(
  dat, "outcome_type_f", "Outcome Type")

# Bloom's taxonomy level
res_blooms <- run_subgroup_analysis(
  dat, "blooms_level_f", "Bloom's Level")

# Study design
res_design <- run_subgroup_analysis(
  dat, "design_f", "Study Design")

# Measurement timing (if available)
if ("measurement_timing" %in% names(dat)) {
  timing_labels <- c("1" = "Immediate Post-test", "2" = "Delayed Post-test",
                     "3" = "Transfer Test")
  dat$measurement_timing_f <- factor(
    dat$measurement_timing,
    levels = 1:3, labels = timing_labels)
  res_timing <- run_subgroup_analysis(
    dat, "measurement_timing_f", "Measurement Timing")
} else {
  res_timing <- NULL
}


# ============================================================================
# 7. COMPILE ALL SUBGROUP RESULTS
# ============================================================================

message("\n\n--- Compiling Subgroup Results ---\n")

all_subgroup_results <- bind_rows(
  res_oversight,
  res_architecture,
  res_context,
  res_role,
  res_agency,
  res_modality,
  res_tech,
  res_adaptivity,
  res_domain,
  res_outcome,
  res_blooms,
  res_design,
  res_timing
)

if (nrow(all_subgroup_results) > 0) {
  # Save comprehensive CSV
  csv_path <- file.path(out_dir, "moderator_summary.csv")
  readr::write_csv(all_subgroup_results, csv_path)
  message("Saved all subgroup results to: ", csv_path)

  # Save individual moderator CSVs
  for (mod in unique(all_subgroup_results$moderator)) {
    mod_df <- all_subgroup_results %>% filter(moderator == mod)
    fname <- paste0("subgroup_",
                    tolower(gsub("[^a-zA-Z0-9]", "_", mod)),
                    ".csv")
    readr::write_csv(mod_df, file.path(out_dir, fname))
  }

  # Print summary table
  message("\n--- Moderator Summary Table ---\n")
  summary_print <- all_subgroup_results %>%
    select(moderator, level, k, g, ci_lower, ci_upper, p_value, QM_p) %>%
    mutate(across(c(g, ci_lower, ci_upper), ~fmt(.x, 3)),
           p_value = sapply(p_value, fmt_p),
           QM_p = sapply(QM_p, fmt_p))
  print(summary_print, n = 100)
}


# ============================================================================
# 8. META-REGRESSION (CONTINUOUS MODERATORS)
# ============================================================================

message("\n\n--- Meta-Regression: Continuous Moderators ---\n")

run_meta_regression <- function(data, predictor, label,
                                 use_3level = has_dependent) {
  message("\n  Meta-regression: ", label, " (", predictor, ")")

  idx <- !is.na(data[[predictor]])
  d <- data[idx, ]

  if (nrow(d) < 5) {
    message("    Too few observations (k = ", nrow(d), "). Skipping.")
    return(NULL)
  }

  mod_formula <- as.formula(paste("~", predictor))

  tryCatch({
    if (use_3level && any(d$dependent_es, na.rm = TRUE)) {
      res <- rma.mv(
        yi     = hedges_g,
        V      = var_g,
        mods   = mod_formula,
        random = ~ 1 | study_id / es_id,
        data   = d,
        method = "REML"
      )
    } else {
      res <- rma(
        yi   = hedges_g,
        vi   = var_g,
        mods = mod_formula,
        data = d,
        method = "REML"
      )
    }

    # Extract results
    coef_table <- data.frame(
      predictor   = label,
      variable    = predictor,
      intercept   = coef(res)[1],
      slope       = coef(res)[2],
      slope_se    = res$se[2],
      slope_ci_lo = res$ci.lb[2],
      slope_ci_hi = res$ci.ub[2],
      slope_z     = res$zval[2],
      slope_p     = res$pval[2],
      QM          = res$QM,
      QM_p        = res$QMp,
      k           = nrow(d),
      R2          = ifelse(!is.null(res$R2), res$R2, NA)
    )

    message("    Slope = ", fmt(coef(res)[2], 4),
            " [", fmt(res$ci.lb[2], 4), ", ", fmt(res$ci.ub[2], 4), "]",
            ", p ", fmt_p(res$pval[2]))
    if (!is.null(res$R2)) {
      message("    R-squared = ", fmt(res$R2, 2), "%")
    }

    return(list(model = res, results = coef_table))

  }, error = function(e) {
    message("    Error: ", conditionMessage(e))
    return(NULL)
  })
}

# Publication year
reg_year <- NULL
if ("year" %in% names(dat)) {
  # Center year for interpretability
  dat$year_centered <- dat$year - median(dat$year, na.rm = TRUE)
  reg_year <- run_meta_regression(dat, "year_centered", "Publication Year (centered)")
}

# Sample size (log-transformed)
reg_n <- NULL
if (all(c("n_treatment_es", "n_control_es") %in% names(dat))) {
  dat$n_total_es <- dat$n_treatment_es + dat$n_control_es
  dat$log_n <- log(dat$n_total_es)
  reg_n <- run_meta_regression(dat, "log_n", "Log(Total N)")
}

# Duration
reg_duration <- NULL
if ("duration_weeks" %in% names(dat)) {
  reg_duration <- run_meta_regression(dat, "duration_weeks", "Duration (weeks)")
}

# Compile meta-regression results
reg_results <- bind_rows(
  if (!is.null(reg_year)) reg_year$results,
  if (!is.null(reg_n)) reg_n$results,
  if (!is.null(reg_duration)) reg_duration$results
)

if (nrow(reg_results) > 0) {
  reg_path <- file.path(out_dir, "meta_regression_results.csv")
  readr::write_csv(reg_results, reg_path)
  message("\nMeta-regression results saved to: ", reg_path)
}


# ============================================================================
# 9. MODERATOR INTERACTIONS (EXPLORATORY)
# ============================================================================

message("\n\n--- Exploratory: Moderator Interactions ---\n")

# Test interaction between human oversight and learning context (RQ2 x RQ4)
if (all(c("human_oversight_f", "learning_context_f") %in% names(dat))) {

  # Check sufficient cell sizes
  cross_tab <- table(dat$human_oversight_f, dat$learning_context_f)
  sufficient_cells <- sum(cross_tab >= 2)

  if (sufficient_cells >= 4) {
    message("  Testing Oversight x Context interaction")

    tryCatch({
      # Main effects model
      if (has_dependent) {
        res_main <- rma.mv(
          yi     = hedges_g,
          V      = var_g,
          mods   = ~ factor(human_oversight) + factor(learning_context),
          random = ~ 1 | study_id / es_id,
          data   = dat,
          method = "REML"
        )
        # Interaction model
        res_interaction <- rma.mv(
          yi     = hedges_g,
          V      = var_g,
          mods   = ~ factor(human_oversight) * factor(learning_context),
          random = ~ 1 | study_id / es_id,
          data   = dat,
          method = "REML"
        )
      } else {
        res_main <- rma(
          yi   = hedges_g,
          vi   = var_g,
          mods = ~ factor(human_oversight) + factor(learning_context),
          data = dat,
          method = "REML"
        )
        res_interaction <- rma(
          yi   = hedges_g,
          vi   = var_g,
          mods = ~ factor(human_oversight) * factor(learning_context),
          data = dat,
          method = "REML"
        )
      }

      # Compare models
      interaction_test <- anova(res_main, res_interaction)
      message("  Interaction LRT: p = ",
              fmt(interaction_test$pval, 4))

      if (interaction_test$pval < ALPHA) {
        message("  => Significant interaction detected.")
      } else {
        message("  => No significant interaction.")
      }

    }, error = function(e) {
      message("  Could not test interaction: ", conditionMessage(e))
    })
  } else {
    message("  Insufficient cell sizes for Oversight x Context interaction")
  }
}

# Test interaction between oversight and outcome type (exploratory)
if (all(c("human_oversight_f", "outcome_type_f") %in% names(dat))) {
  cross_tab2 <- table(dat$human_oversight_f, dat$outcome_type_f)
  sufficient_cells2 <- sum(cross_tab2 >= 2)

  if (sufficient_cells2 >= 4) {
    message("  Testing Oversight x Outcome Type interaction")

    tryCatch({
      if (has_dependent) {
        res_ov_out <- rma.mv(
          yi     = hedges_g,
          V      = var_g,
          mods   = ~ factor(human_oversight) * factor(outcome_type),
          random = ~ 1 | study_id / es_id,
          data   = dat,
          method = "REML"
        )
      } else {
        res_ov_out <- rma(
          yi   = hedges_g,
          vi   = var_g,
          mods = ~ factor(human_oversight) * factor(outcome_type),
          data = dat,
          method = "REML"
        )
      }
      message("  Oversight x Outcome: QM(", res_ov_out$m, ") = ",
              fmt(res_ov_out$QM, 2), ", p ", fmt_p(res_ov_out$QMp))
    }, error = function(e) {
      message("  Could not test interaction: ", conditionMessage(e))
    })
  }
}


# ============================================================================
# 10. COMPREHENSIVE RESULTS REPORT
# ============================================================================

report_path <- file.path(out_dir, "moderator_analysis_report.txt")
sink(report_path)

cat("=======================================================\n")
cat("Moderator Analysis Report (RQ2-RQ4 + Additional)\n")
cat(paste("Date:", Sys.Date()), "\n")
cat("=======================================================\n\n")

# RQ2
cat("-------------------------------------------------------\n")
cat("RQ2: Human Oversight Level\n")
cat("-------------------------------------------------------\n")
if (!is.null(res_oversight) && nrow(res_oversight) > 0) {
  cat("Omnibus test: QM(", unique(res_oversight$QM_df), ") = ",
      fmt(unique(res_oversight$QM), 2), ", p ",
      fmt_p(unique(res_oversight$QM_p)), "\n\n")
  for (i in 1:nrow(res_oversight)) {
    cat("  ", res_oversight$level[i], ": g = ", fmt(res_oversight$g[i], 3),
        " [", fmt(res_oversight$ci_lower[i], 3), ", ",
        fmt(res_oversight$ci_upper[i], 3), "]",
        ", k = ", res_oversight$k[i], "\n")
  }
} else {
  cat("  Insufficient data for analysis.\n")
}

# RQ3
cat("\n-------------------------------------------------------\n")
cat("RQ3: Agent Architecture\n")
cat("-------------------------------------------------------\n")
if (!is.null(res_architecture) && nrow(res_architecture) > 0) {
  cat("Omnibus test: QM(", unique(res_architecture$QM_df), ") = ",
      fmt(unique(res_architecture$QM), 2), ", p ",
      fmt_p(unique(res_architecture$QM_p)), "\n\n")
  for (i in 1:nrow(res_architecture)) {
    cat("  ", res_architecture$level[i], ": g = ", fmt(res_architecture$g[i], 3),
        " [", fmt(res_architecture$ci_lower[i], 3), ", ",
        fmt(res_architecture$ci_upper[i], 3), "]",
        ", k = ", res_architecture$k[i], "\n")
  }
} else {
  cat("  Insufficient data for analysis.\n")
}

# RQ4
cat("\n-------------------------------------------------------\n")
cat("RQ4: Learning Context\n")
cat("-------------------------------------------------------\n")
if (!is.null(res_context) && nrow(res_context) > 0) {
  cat("Omnibus test: QM(", unique(res_context$QM_df), ") = ",
      fmt(unique(res_context$QM), 2), ", p ",
      fmt_p(unique(res_context$QM_p)), "\n\n")
  for (i in 1:nrow(res_context)) {
    cat("  ", res_context$level[i], ": g = ", fmt(res_context$g[i], 3),
        " [", fmt(res_context$ci_lower[i], 3), ", ",
        fmt(res_context$ci_upper[i], 3), "]",
        ", k = ", res_context$k[i], "\n")
  }
} else {
  cat("  Insufficient data for analysis.\n")
}

# Additional moderators
cat("\n-------------------------------------------------------\n")
cat("Additional Moderator Analyses\n")
cat("-------------------------------------------------------\n\n")
if (nrow(all_subgroup_results) > 0) {
  additional_mods <- all_subgroup_results %>%
    filter(!moderator %in% c("Human Oversight Level (RQ2)",
                             "Agent Architecture (RQ3)",
                             "Learning Context (RQ4)"))
  for (mod in unique(additional_mods$moderator)) {
    mod_df <- additional_mods %>% filter(moderator == mod)
    cat(mod, ":\n")
    cat("  Omnibus: QM = ", fmt(unique(mod_df$QM), 2),
        ", p ", fmt_p(unique(mod_df$QM_p)), "\n")
    for (j in 1:nrow(mod_df)) {
      cat("    ", mod_df$level[j], ": g = ", fmt(mod_df$g[j], 3),
          " [", fmt(mod_df$ci_lower[j], 3), ", ",
          fmt(mod_df$ci_upper[j], 3), "]",
          ", k = ", mod_df$k[j], "\n")
    }
    cat("\n")
  }
}

# Meta-regression
cat("-------------------------------------------------------\n")
cat("Meta-Regression (Continuous Moderators)\n")
cat("-------------------------------------------------------\n\n")
if (nrow(reg_results) > 0) {
  for (i in 1:nrow(reg_results)) {
    cat(reg_results$predictor[i], ":\n")
    cat("  Slope = ", fmt(reg_results$slope[i], 4),
        " [", fmt(reg_results$slope_ci_lo[i], 4), ", ",
        fmt(reg_results$slope_ci_hi[i], 4), "]",
        ", p ", fmt_p(reg_results$slope_p[i]), "\n")
    if (!is.na(reg_results$R2[i])) {
      cat("  R-squared = ", fmt(reg_results$R2[i], 2), "%\n")
    }
    cat("\n")
  }
}

sink()
message("\nFull report saved to: ", report_path)

message("\n========== 03: Moderator Analysis Complete ==========\n")
