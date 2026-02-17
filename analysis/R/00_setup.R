# ============================================================================
# 00_setup.R
# Project Setup: Package Management, Configuration, and Utility Functions
# ============================================================================
#
# Purpose:
#   Initialize the analysis environment for the meta-analysis of
#   "Effects of Agentic AI on Learning Outcomes Across Educational Contexts."
#   This script installs/loads required packages, sets project paths,
#   defines coding variable levels, and provides utility functions for
#   computing Hedges' g and associated statistics.
#
# Usage:
#   Source this script at the beginning of every analysis script:
#     source("analysis/R/00_setup.R")
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================


# ============================================================================
# 1. PACKAGE MANAGEMENT
# ============================================================================

# Define required packages
required_packages <- c(

  # --- Meta-analysis core ---
  "metafor",        # Primary meta-analysis engine (rma, rma.mv, escalc, funnel, etc.)
  "robumeta",       # Robust variance estimation (robu)
  "clubSandwich",   # Cluster-robust standard errors for meta-analysis

  # --- Data manipulation ---
  "dplyr",          # Data wrangling

  "tidyr",          # Data reshaping
  "readxl",         # Read Excel files
  "readr",          # Read CSV/delimited files
  "tibble",         # Modern data frames
  "stringr",        # String manipulation

  # --- Visualization ---
  "ggplot2",        # Grammar of graphics
  "forestplot",     # Forest plot generation
  "patchwork",      # Combine ggplot panels

  # --- Reporting ---
  "writexl",        # Write Excel files
  "knitr",          # Dynamic report generation
  "kableExtra",     # Enhanced tables for knitr
  "flextable"       # Publication-quality tables
)

# Optional packages (installed if available; analysis proceeds without them)
optional_packages <- c(
  "weightr",          # Weight-function models for publication bias
  "PublicationBias",  # Sensitivity analysis for publication bias
  "ggrepel",          # Non-overlapping text labels
  "scales",           # Axis scale formatting
  "RColorBrewer",     # Color palettes
  "DiagrammeR"        # Flow diagrams (PRISMA)
)

# Install missing required packages
install_if_missing <- function(pkgs, required = TRUE) {
  missing <- pkgs[!sapply(pkgs, requireNamespace, quietly = TRUE)]
  if (length(missing) > 0) {
    if (required) {
      message("Installing required packages: ", paste(missing, collapse = ", "))
      install.packages(missing, repos = "https://cloud.r-project.org")
    } else {
      message("Optional packages not installed (install manually if needed): ",
              paste(missing, collapse = ", "))
    }
  }
}

install_if_missing(required_packages, required = TRUE)
install_if_missing(optional_packages, required = FALSE)

# Load required packages
invisible(lapply(required_packages, library, character.only = TRUE))

# Load optional packages silently
for (pkg in optional_packages) {
  if (requireNamespace(pkg, quietly = TRUE)) {
    library(pkg, character.only = TRUE)
  }
}

message("All required packages loaded successfully.")


# ============================================================================
# 2. PROJECT CONFIGURATION
# ============================================================================

# Detect project root (works when sourced from any subdirectory)
if (!exists("PROJECT_ROOT")) {
  # Try to find the project root by looking for README.md
  candidate <- getwd()
  while (!file.exists(file.path(candidate, "README.md")) && candidate != dirname(candidate)) {
    candidate <- dirname(candidate)
  }
  if (file.exists(file.path(candidate, "README.md"))) {
    PROJECT_ROOT <- candidate
  } else {
    PROJECT_ROOT <- getwd()
    warning("Could not auto-detect project root. Using working directory: ", PROJECT_ROOT)
  }
}

# --- Directory paths ---
PATHS <- list(
  root        = PROJECT_ROOT,
  data_raw    = file.path(PROJECT_ROOT, "data", "00_raw"),
  data_screen = file.path(PROJECT_ROOT, "data", "01_screened"),
  data_extract= file.path(PROJECT_ROOT, "data", "02_extracted"),
  data_coded  = file.path(PROJECT_ROOT, "data", "03_coded"),
  data_final  = file.path(PROJECT_ROOT, "data", "04_final"),
  templates   = file.path(PROJECT_ROOT, "data", "templates"),
  analysis_r  = file.path(PROJECT_ROOT, "analysis", "R"),
  output      = file.path(PROJECT_ROOT, "analysis", "output"),
  out_figures = file.path(PROJECT_ROOT, "analysis", "output", "figures"),
  out_forest  = file.path(PROJECT_ROOT, "analysis", "output", "forest_plots"),
  out_mod     = file.path(PROJECT_ROOT, "analysis", "output", "moderator_analysis"),
  out_pub     = file.path(PROJECT_ROOT, "analysis", "output", "publication_bias"),
  figures     = file.path(PROJECT_ROOT, "figures", "output"),
  manuscript  = file.path(PROJECT_ROOT, "manuscript")
)

# Create output directories if they do not exist
invisible(lapply(PATHS, function(p) {
  if (!dir.exists(p)) dir.create(p, recursive = TRUE, showWarnings = FALSE)
}))

# --- Analysis parameters ---
CONF_LEVEL   <- 0.95       # Confidence level for CIs
ALPHA        <- 0.05       # Significance threshold
SEED         <- 20260216   # Random seed for reproducibility
DIGITS       <- 3          # Decimal places for reporting

set.seed(SEED)

message("Project paths configured. Root: ", PROJECT_ROOT)


# ============================================================================
# 3. CODING VARIABLE DEFINITIONS
# ============================================================================
# These correspond to the coding scheme in docs/coding-scheme.md.
# Labels are used for display; values are used for filtering and modeling.

# --- C1. Human Oversight Level (RQ2) ---
HUMAN_OVERSIGHT_LEVELS <- c(

  "fully_autonomous"     = 1,
  "ai_led_checkpoints"   = 2,
  "human_led_ai_support" = 3
)
HUMAN_OVERSIGHT_LABELS <- c(
  "1" = "Fully Autonomous",
  "2" = "AI-Led with Checkpoints",
  "3" = "Human-Led with AI Support"
)

# --- C2. Agent Architecture (RQ3) ---
AGENT_ARCHITECTURE <- c(
  "single_agent" = 1,
  "multi_agent"  = 2
)
AGENT_ARCHITECTURE_LABELS <- c(
  "1" = "Single Agent",
  "2" = "Multi-Agent System"
)

# --- C3. Agent Agency Level (Yan 2025 APCP Framework) ---
AGENCY_LEVELS <- c(
  "adaptive"   = 1,
  "proactive"  = 2,
  "co_learner" = 3,
  "peer"       = 4
)
AGENCY_LEVEL_LABELS <- c(
  "1" = "Adaptive",
  "2" = "Proactive",
  "3" = "Co-Learner",
  "4" = "Peer"
)

# --- C4. Agent Role ---
AGENT_ROLES <- c(
  "tutor"        = 1,
  "coach"        = 2,
  "assessor"     = 3,
  "collaborator" = 4,
  "facilitator"  = 5,
  "multiple"     = 6
)
AGENT_ROLE_LABELS <- c(
  "1" = "Tutor",
  "2" = "Coach",
  "3" = "Assessor",
  "4" = "Collaborator",
  "5" = "Facilitator",
  "6" = "Multiple Roles"
)

# --- C5. Agent Modality ---
AGENT_MODALITY <- c(
  "text_only"  = 1,
  "voice"      = 2,
  "embodied"   = 3,
  "mixed"      = 4
)
AGENT_MODALITY_LABELS <- c(
  "1" = "Text-Only",
  "2" = "Voice",
  "3" = "Embodied (Avatar)",
  "4" = "Mixed"
)

# --- C6. AI Technology Base ---
AI_TECHNOLOGY <- c(
  "rule_based"     = 1,
  "ml"             = 2,
  "nlp_pre_llm"    = 3,
  "llm"            = 4,
  "rl"             = 5,
  "hybrid"         = 6
)
AI_TECHNOLOGY_LABELS <- c(
  "1" = "Rule-Based",
  "2" = "Machine Learning",
  "3" = "NLP (Pre-LLM)",
  "4" = "Large Language Model",
  "5" = "Reinforcement Learning",
  "6" = "Hybrid"
)

# --- C7. Adaptivity Level ---
ADAPTIVITY_LEVELS <- c(
  "static"           = 1,
  "performance"      = 2,
  "behavior"         = 3,
  "affect"           = 4,
  "multi_dimensional"= 5
)
ADAPTIVITY_LABELS <- c(
  "1" = "Static",
  "2" = "Performance-Adaptive",
  "3" = "Behavior-Adaptive",
  "4" = "Affect-Adaptive",
  "5" = "Multi-Dimensional"
)

# --- D1. Learning Context (RQ4) ---
LEARNING_CONTEXTS <- c(
  "k12"                   = 1,
  "higher_education"      = 2,
  "workplace_training"    = 3,
  "professional_education"= 4,
  "continuing_education"  = 5
)
LEARNING_CONTEXT_LABELS <- c(
  "1" = "K-12",
  "2" = "Higher Education",
  "3" = "Workplace Training",
  "4" = "Professional Education",
  "5" = "Continuing Education"
)

# --- D2. Subject Domain ---
SUBJECT_DOMAINS <- c(
  "stem"        = 1,
  "language"    = 2,
  "medical"     = 3,
  "business"    = 4,
  "ict_cs"      = 5,
  "social_sci"  = 6,
  "other"       = 7
)
SUBJECT_DOMAIN_LABELS <- c(
  "1" = "STEM",
  "2" = "Language",
  "3" = "Medical/Health Sciences",
  "4" = "Business/Management",
  "5" = "ICT/Computer Science",
  "6" = "Social Sciences/Humanities",
  "7" = "Other"
)

# --- E1. Outcome Type ---
OUTCOME_TYPES <- c(
  "cognitive"    = 1,
  "skill_based"  = 2,
  "affective"    = 3,
  "performance"  = 4
)
OUTCOME_TYPE_LABELS <- c(
  "1" = "Cognitive (Knowledge)",
  "2" = "Skill-Based",
  "3" = "Affective",
  "4" = "Performance"
)

# --- E2. Bloom's Taxonomy Level ---
BLOOMS_LEVELS <- c(
  "remember_understand"  = 1,
  "apply_analyze"        = 2,
  "evaluate_create"      = 3
)
BLOOMS_LABELS <- c(
  "1" = "Remember-Understand",
  "2" = "Apply-Analyze",
  "3" = "Evaluate-Create"
)

# --- E3. Measurement Type ---
MEASUREMENT_TYPES <- c(
  "standardized"     = 1,
  "researcher_dev"   = 2,
  "performance_rubric"= 3,
  "self_report"      = 4,
  "system_logged"    = 5
)

# --- Study Design ---
STUDY_DESIGNS <- c(
  "rct"              = 1,
  "quasi_experimental"= 2,
  "pre_post"         = 3
)
STUDY_DESIGN_LABELS <- c(
  "1" = "RCT",
  "2" = "Quasi-Experimental",
  "3" = "Pre-Post Within-Subjects"
)

# --- Risk of Bias ---
ROB_LEVELS <- c(
  "high_risk"      = 0,
  "some_concerns"  = 1,
  "low_risk"       = 2
)


# ============================================================================
# 4. UTILITY FUNCTIONS
# ============================================================================

# ----------------------------------------------------------------------------
# 4.1 Compute Hedges' g from group means and SDs
# ----------------------------------------------------------------------------
#' @title Compute Hedges' g (standardized mean difference with small-sample correction)
#' @param m1 Mean of the treatment group
#' @param m2 Mean of the control group
#' @param sd1 SD of the treatment group
#' @param sd2 SD of the control group
#' @param n1 Sample size of the treatment group
#' @param n2 Sample size of the control group
#' @return Named numeric vector: hedges_g, se_g, var_g, ci_lower, ci_upper
compute_hedges_g <- function(m1, m2, sd1, sd2, n1, n2) {

  # Pooled standard deviation (Cohen's d denominator)
  sd_pooled <- sqrt(((n1 - 1) * sd1^2 + (n2 - 1) * sd2^2) / (n1 + n2 - 2))

  # Cohen's d
  d <- (m1 - m2) / sd_pooled

  # Small-sample correction factor J (Hedges & Olkin, 1985)
  df <- n1 + n2 - 2
  J <- 1 - (3 / (4 * df - 1))

  # Hedges' g
  g <- d * J

  # Variance of g (Borenstein et al., 2009, Eq. 4.24)
  var_g <- (n1 + n2) / (n1 * n2) + g^2 / (2 * (n1 + n2))

  # Standard error
  se_g <- sqrt(var_g)

  # 95% CI
  z_crit <- qnorm(1 - (1 - CONF_LEVEL) / 2)
  ci_lower <- g - z_crit * se_g
  ci_upper <- g + z_crit * se_g

  return(c(
    hedges_g = g,
    se_g     = se_g,
    var_g    = var_g,
    ci_lower = ci_lower,
    ci_upper = ci_upper
  ))
}


# ----------------------------------------------------------------------------
# 4.2 Compute SE of Hedges' g directly
# ----------------------------------------------------------------------------
#' @title Compute the standard error of Hedges' g
#' @param g Hedges' g value
#' @param n1 Treatment group sample size
#' @param n2 Control group sample size
#' @return Numeric: standard error of g
compute_se_g <- function(g, n1, n2) {
  sqrt((n1 + n2) / (n1 * n2) + g^2 / (2 * (n1 + n2)))
}


# ----------------------------------------------------------------------------
# 4.3 Compute effect size using metafor::escalc (wrapper)
# ----------------------------------------------------------------------------
#' @title Compute Hedges' g using metafor::escalc
#' @description Wrapper around escalc() for computing standardized mean
#'   differences (Hedges' g) from summary statistics. Handles both
#'   post-test only and gain-score designs.
#' @param data Data frame with columns: mean_treatment, sd_treatment,
#'   n_treatment_es, mean_control, sd_control, n_control_es
#' @param measure Character. Effect size measure: "SMD" for Hedges' g (default)
#' @return Data frame with yi (effect size) and vi (variance) appended
escalc_from_summary <- function(data, measure = "SMD") {

  # Validate required columns

  required_cols <- c("mean_treatment", "sd_treatment", "n_treatment_es",
                     "mean_control", "sd_control", "n_control_es")
  missing_cols <- setdiff(required_cols, names(data))
  if (length(missing_cols) > 0) {
    stop("Missing columns for escalc: ", paste(missing_cols, collapse = ", "))
  }

  # Use metafor::escalc to compute Hedges' g
  data <- metafor::escalc(
    measure = measure,
    m1i     = mean_treatment,
    sd1i    = sd_treatment,
    n1i     = n_treatment_es,
    m2i     = mean_control,
    sd2i    = sd_control,
    n2i     = n_control_es,
    data    = data
  )

  return(data)
}


# ----------------------------------------------------------------------------
# 4.4 Convert other statistics to Hedges' g
# ----------------------------------------------------------------------------
#' @title Convert t-value to Hedges' g
#' @param t t-statistic
#' @param n1 Treatment group sample size
#' @param n2 Control group sample size
#' @return Named vector with hedges_g and se_g
t_to_g <- function(t, n1, n2) {
  d <- t * sqrt((n1 + n2) / (n1 * n2))
  df <- n1 + n2 - 2
  J <- 1 - (3 / (4 * df - 1))
  g <- d * J
  se_g <- compute_se_g(g, n1, n2)
  return(c(hedges_g = g, se_g = se_g))
}

#' @title Convert F-value (one-way, df1=1) to Hedges' g
#' @param f F-statistic (with df1 = 1)
#' @param n1 Treatment group sample size
#' @param n2 Control group sample size
#' @return Named vector with hedges_g and se_g
f_to_g <- function(f, n1, n2) {
  t <- sqrt(f)
  t_to_g(t, n1, n2)
}

#' @title Convert correlation (r) to Hedges' g
#' @param r Correlation coefficient
#' @param n Total sample size
#' @return Named vector with hedges_g and se_g
r_to_g <- function(r, n) {
  d <- (2 * r) / sqrt(1 - r^2)
  n1 <- n / 2
  n2 <- n / 2
  df <- n - 2
  J <- 1 - (3 / (4 * df - 1))
  g <- d * J
  se_g <- compute_se_g(g, n1, n2)
  return(c(hedges_g = g, se_g = se_g))
}


# ----------------------------------------------------------------------------
# 4.5 Formatting helpers
# ----------------------------------------------------------------------------
#' @title Format a number for reporting
fmt <- function(x, digits = DIGITS) {
  formatC(x, format = "f", digits = digits)
}

#' @title Format effect size with 95% CI for inline reporting
fmt_es <- function(g, ci_lo, ci_hi, digits = 2) {
  paste0("g = ", fmt(g, digits),
         " [", fmt(ci_lo, digits), ", ", fmt(ci_hi, digits), "]")
}

#' @title Format a p-value for reporting
fmt_p <- function(p, digits = 3) {
  if (p < 0.001) {
    return("< .001")
  } else {
    return(paste0("= ", sub("^0", "", fmt(p, digits))))
  }
}


# ----------------------------------------------------------------------------
# 4.6 Heterogeneity interpretation helpers
# ----------------------------------------------------------------------------
#' @title Interpret I-squared values (Higgins et al., 2003)
interpret_i2 <- function(i2) {
  case_when(
    i2 < 25  ~ "Low",
    i2 < 50  ~ "Low-to-Moderate",
    i2 < 75  ~ "Moderate-to-Substantial",
    TRUE     ~ "Substantial"
  )
}

#' @title Interpret effect size magnitude (Cohen, 1988; Hattie, 2009 for education)
interpret_g <- function(g) {
  g_abs <- abs(g)
  case_when(
    g_abs < 0.20 ~ "Negligible",
    g_abs < 0.40 ~ "Small",
    g_abs < 0.60 ~ "Medium",
    g_abs < 0.80 ~ "Large",
    TRUE          ~ "Very Large"
  )
}


# ----------------------------------------------------------------------------
# 4.7 Risk-of-bias summary score
# ----------------------------------------------------------------------------
#' @title Compute overall quality category from individual RoB ratings
#' @param rob_df Data frame with rob_* columns (values: 0, 1, 2)
#' @return Character vector: "High", "Some Concerns", or "Low"
compute_rob_overall <- function(rob_df) {
  rob_cols <- grep("^rob_", names(rob_df), value = TRUE)
  rob_cols <- setdiff(rob_cols, "rob_overall")

  apply(rob_df[, rob_cols, drop = FALSE], 1, function(row) {
    if (any(row == 0, na.rm = TRUE)) {
      return("High")
    } else if (any(row == 1, na.rm = TRUE)) {
      return("Some Concerns")
    } else {
      return("Low")
    }
  })
}


# ----------------------------------------------------------------------------
# 4.8 Prediction interval for random-effects model
# ----------------------------------------------------------------------------
#' @title Compute prediction interval (Riley et al., 2011)
#' @param model A fitted rma or rma.mv object from metafor
#' @return Named vector: pi_lower, pi_upper
compute_prediction_interval <- function(model) {
  k <- model$k
  tau2 <- ifelse(is.null(model$tau2), sum(model$sigma2), model$tau2)
  se_pred <- sqrt(tau2 + model$se^2)
  t_crit <- qt(1 - (1 - CONF_LEVEL) / 2, df = max(k - 2, 1))
  pi_lower <- model$b[1] - t_crit * se_pred
  pi_upper <- model$b[1] + t_crit * se_pred
  return(c(pi_lower = as.numeric(pi_lower), pi_upper = as.numeric(pi_upper)))
}


# ----------------------------------------------------------------------------
# 4.9 Theme for publication-quality ggplot figures
# ----------------------------------------------------------------------------
theme_meta <- function(base_size = 12) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title       = element_text(face = "bold", size = base_size + 2, hjust = 0),
      plot.subtitle    = element_text(size = base_size, color = "grey40"),
      axis.title       = element_text(face = "bold"),
      legend.position  = "bottom",
      legend.title     = element_text(face = "bold"),
      panel.grid.minor = element_blank(),
      panel.border     = element_rect(color = "grey80", fill = NA, linewidth = 0.5),
      strip.text       = element_text(face = "bold", size = base_size)
    )
}


# ============================================================================
# 5. SESSION INFO
# ============================================================================

message("\n--- Session Info ---")
message("R version: ", R.version.string)
message("metafor:   ", packageVersion("metafor"))
message("robumeta:  ", packageVersion("robumeta"))
message("clubSandwich: ", packageVersion("clubSandwich"))
message("Analysis date: ", Sys.Date())
message("-------------------\n")
