# ============================================================================
# 01_data_preparation.R
# Data Preparation: Import, Clean, Validate, and Compute Effect Sizes
# ============================================================================
#
# Purpose:
#   Read the coded meta-analysis data from the Excel coding template,
#   perform validation checks, compute Hedges' g where raw summary
#   statistics are provided, handle multiple effect sizes per study,
#   and produce a clean, analysis-ready dataset.
#
# Input:
#   data/templates/Agentic_AI_Learning_MA_Coding_v1.xlsx
#   OR data/04_final/*.csv (if previously exported)
#
# Output:
#   data/04_final/ma_data_clean.csv       -- Full cleaned dataset
#   data/04_final/ma_data_clean.rds       -- R binary for fast loading
#   analysis/output/data_summary.txt      -- Descriptive summary report
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 01: Data Preparation ==========\n")


# ============================================================================
# 1. DATA IMPORT
# ============================================================================

# --- Try Excel template first, then CSV fallback ---
excel_path <- file.path(PATHS$templates, "Agentic_AI_Learning_MA_Coding_v1.xlsx")
csv_path   <- file.path(PATHS$data_final, "ma_data_raw.csv")

if (file.exists(excel_path)) {
  message("Reading data from Excel template: ", excel_path)

  # Read the main coding sheet (assumes first sheet or named "Coding")
  sheet_names <- readxl::excel_sheets(excel_path)
  coding_sheet <- if ("Coding" %in% sheet_names) "Coding" else sheet_names[1]

  raw_data <- readxl::read_excel(
    excel_path,
    sheet = coding_sheet,
    na    = c("", "NA", "N/A", "n/a", ".")
  )
  message("  Sheet: '", coding_sheet, "' | Rows: ", nrow(raw_data),
          " | Columns: ", ncol(raw_data))

} else if (file.exists(csv_path)) {
  message("Reading data from CSV: ", csv_path)
  raw_data <- readr::read_csv(csv_path, show_col_types = FALSE)
  message("  Rows: ", nrow(raw_data), " | Columns: ", ncol(raw_data))

} else {
  stop("No data file found. Expected:\n",
       "  ", excel_path, "\n  OR\n  ", csv_path, "\n",
       "Please place the coded data file in one of these locations.")
}


# ============================================================================
# 2. COLUMN NAME STANDARDIZATION
# ============================================================================

# Standardize column names to snake_case
names(raw_data) <- names(raw_data) %>%
  tolower() %>%
  str_replace_all("[^a-z0-9]+", "_") %>%
  str_replace_all("^_|_$", "")

# Define expected column mappings (flexible matching)
expected_cols <- c(
  # Study identification
  "study_id", "es_id", "author", "year", "journal", "country",
  "publication_type",
  # Study design
  "design", "random_assignment", "control_type",
  "duration_weeks", "n_treatment", "n_control", "n_total",
  "attrition_rate",
  # AI agent characteristics
  "human_oversight", "agent_architecture", "agency_level",
  "agent_role", "agent_modality", "ai_technology", "adaptivity_level",
  # Learning context
  "learning_context", "subject_domain", "learning_mode",
  "delivery_format",
  # Outcome characteristics
  "outcome_type", "blooms_level", "measurement_type",
  "measurement_timing",
  # Effect size data
  "es_type", "mean_treatment", "sd_treatment", "mean_control",
  "sd_control", "n_treatment_es", "n_control_es",
  "t_value", "f_value", "p_value",
  "hedges_g", "se_g", "var_g", "ci_lower", "ci_upper",
  "pre_post",
  # Quality assessment
  "rob_randomization", "rob_allocation", "rob_blinding_participants",
  "rob_blinding_outcome", "rob_incomplete_data", "rob_selective_reporting",
  "rob_other", "rob_overall",
  # Notes
  "notes"
)

# Report which expected columns are present
present_cols <- intersect(expected_cols, names(raw_data))
missing_cols <- setdiff(expected_cols, names(raw_data))

message("\nColumn check:")
message("  Expected: ", length(expected_cols))
message("  Present:  ", length(present_cols))
if (length(missing_cols) > 0) {
  message("  Missing:  ", paste(missing_cols, collapse = ", "))
}


# ============================================================================
# 3. DATA CLEANING
# ============================================================================

dat <- as_tibble(raw_data)

# --- 3.1 Ensure numeric types for key variables ---
numeric_vars <- c(
  "study_id", "es_id", "year", "publication_type", "design",
  "random_assignment", "control_type", "duration_weeks",
  "n_treatment", "n_control", "n_total", "attrition_rate",
  "human_oversight", "agent_architecture", "agency_level",
  "agent_role", "agent_modality", "ai_technology", "adaptivity_level",
  "learning_context", "subject_domain", "learning_mode", "delivery_format",
  "outcome_type", "blooms_level", "measurement_type", "measurement_timing",
  "es_type", "mean_treatment", "sd_treatment", "mean_control", "sd_control",
  "n_treatment_es", "n_control_es", "t_value", "f_value", "p_value",
  "hedges_g", "se_g", "var_g", "ci_lower", "ci_upper", "pre_post",
  "rob_randomization", "rob_allocation", "rob_blinding_participants",
  "rob_blinding_outcome", "rob_incomplete_data", "rob_selective_reporting",
  "rob_other", "rob_overall"
)

for (v in intersect(numeric_vars, names(dat))) {
  dat[[v]] <- suppressWarnings(as.numeric(dat[[v]]))
}

# --- 3.2 Remove rows with no study_id (empty rows from Excel) ---
if ("study_id" %in% names(dat)) {
  n_before <- nrow(dat)
  dat <- dat %>% filter(!is.na(study_id))
  n_removed <- n_before - nrow(dat)
  if (n_removed > 0) {
    message("Removed ", n_removed, " rows with missing study_id")
  }
}

# --- 3.3 Create es_id if not present ---
if (!"es_id" %in% names(dat) || all(is.na(dat$es_id))) {
  dat <- dat %>%
    group_by(study_id) %>%
    mutate(es_id = row_number()) %>%
    ungroup()
  message("Generated es_id (effect size identifier within studies)")
}

# --- 3.4 Compute n_total if missing ---
if ("n_total" %in% names(dat)) {
  dat <- dat %>%
    mutate(n_total = if_else(
      is.na(n_total) & !is.na(n_treatment) & !is.na(n_control),
      n_treatment + n_control,
      n_total
    ))
}

# --- 3.5 Use study-level sample sizes for effect-size-level if missing ---
if ("n_treatment_es" %in% names(dat) && "n_treatment" %in% names(dat)) {
  dat <- dat %>%
    mutate(
      n_treatment_es = if_else(is.na(n_treatment_es), n_treatment, n_treatment_es),
      n_control_es   = if_else(is.na(n_control_es),   n_control,   n_control_es)
    )
}


# ============================================================================
# 4. COMPUTE EFFECT SIZES
# ============================================================================

message("\nComputing effect sizes...")

# --- 4.1 Identify rows that need effect size computation ---
# Rows with means and SDs but no Hedges' g
needs_computation <- !is.na(dat$mean_treatment) &
                     !is.na(dat$sd_treatment) &
                     !is.na(dat$mean_control) &
                     !is.na(dat$sd_control) &
                     !is.na(dat$n_treatment_es) &
                     !is.na(dat$n_control_es) &
                     is.na(dat$hedges_g)

n_compute_ms <- sum(needs_computation, na.rm = TRUE)
message("  Rows needing computation from M/SD: ", n_compute_ms)

if (n_compute_ms > 0) {
  # Use metafor::escalc for standardized computation
  computed <- escalc_from_summary(dat[needs_computation, ])
  dat$hedges_g[needs_computation] <- as.numeric(computed$yi)
  dat$var_g[needs_computation]    <- as.numeric(computed$vi)
  dat$se_g[needs_computation]     <- sqrt(as.numeric(computed$vi))
  message("  Computed ", n_compute_ms, " effect sizes from means/SDs via escalc()")
}

# --- 4.2 Convert t-values to Hedges' g ---
needs_t_conv <- is.na(dat$hedges_g) &
                !is.na(dat$t_value) &
                !is.na(dat$n_treatment_es) &
                !is.na(dat$n_control_es)

n_compute_t <- sum(needs_t_conv, na.rm = TRUE)
if (n_compute_t > 0) {
  for (i in which(needs_t_conv)) {
    res <- t_to_g(dat$t_value[i], dat$n_treatment_es[i], dat$n_control_es[i])
    dat$hedges_g[i] <- res["hedges_g"]
    dat$se_g[i]     <- res["se_g"]
    dat$var_g[i]    <- res["se_g"]^2
  }
  message("  Converted ", n_compute_t, " t-values to Hedges' g")
}

# --- 4.3 Convert F-values to Hedges' g ---
needs_f_conv <- is.na(dat$hedges_g) &
                !is.na(dat$f_value) &
                !is.na(dat$n_treatment_es) &
                !is.na(dat$n_control_es)

n_compute_f <- sum(needs_f_conv, na.rm = TRUE)
if (n_compute_f > 0) {
  for (i in which(needs_f_conv)) {
    res <- f_to_g(dat$f_value[i], dat$n_treatment_es[i], dat$n_control_es[i])
    dat$hedges_g[i] <- res["hedges_g"]
    dat$se_g[i]     <- res["se_g"]
    dat$var_g[i]    <- res["se_g"]^2
  }
  message("  Converted ", n_compute_f, " F-values to Hedges' g")
}

# --- 4.4 Compute SE/variance if g exists but SE is missing ---
missing_se <- !is.na(dat$hedges_g) & is.na(dat$se_g) &
              !is.na(dat$n_treatment_es) & !is.na(dat$n_control_es)

if (sum(missing_se) > 0) {
  dat$se_g[missing_se] <- mapply(
    compute_se_g,
    dat$hedges_g[missing_se],
    dat$n_treatment_es[missing_se],
    dat$n_control_es[missing_se]
  )
  dat$var_g[missing_se] <- dat$se_g[missing_se]^2
  message("  Computed SE for ", sum(missing_se), " effect sizes with known g but missing SE")
}

# --- 4.5 Compute confidence intervals if missing ---
if ("ci_lower" %in% names(dat)) {
  missing_ci <- !is.na(dat$hedges_g) & !is.na(dat$se_g) & is.na(dat$ci_lower)
  if (sum(missing_ci) > 0) {
    z_crit <- qnorm(1 - (1 - CONF_LEVEL) / 2)
    dat$ci_lower[missing_ci] <- dat$hedges_g[missing_ci] - z_crit * dat$se_g[missing_ci]
    dat$ci_upper[missing_ci] <- dat$hedges_g[missing_ci] + z_crit * dat$se_g[missing_ci]
    message("  Computed 95% CIs for ", sum(missing_ci), " effect sizes")
  }
}


# ============================================================================
# 5. DATA VALIDATION
# ============================================================================

message("\nRunning validation checks...")

# --- 5.1 Check for complete effect size data ---
valid_es <- !is.na(dat$hedges_g) & !is.na(dat$se_g)
n_valid <- sum(valid_es)
n_invalid <- sum(!valid_es)
message("  Valid effect sizes:   ", n_valid)
message("  Missing effect sizes: ", n_invalid)

if (n_invalid > 0) {
  warning(n_invalid, " rows have missing effect sizes after all conversions.\n",
          "  These rows will be excluded from analysis.\n",
          "  Study IDs: ", paste(unique(dat$study_id[!valid_es]), collapse = ", "))
}

# --- 5.2 Check for extreme values ---
if (n_valid > 0) {
  extreme_g <- which(abs(dat$hedges_g) > 5 & valid_es)
  if (length(extreme_g) > 0) {
    warning("Extreme Hedges' g values (|g| > 5) found in rows: ",
            paste(extreme_g, collapse = ", "),
            "\n  Review these entries for data entry errors.")
    for (i in extreme_g) {
      message("    Study ", dat$study_id[i], " ES ", dat$es_id[i],
              ": g = ", fmt(dat$hedges_g[i], 3))
    }
  }

  # Check for negative variances
  neg_var <- which(dat$var_g < 0 & valid_es)
  if (length(neg_var) > 0) {
    warning("Negative variance found in rows: ", paste(neg_var, collapse = ", "))
  }
}

# --- 5.3 Check moderator coding validity ---
validate_coding <- function(dat, var_name, valid_values, label) {
  if (var_name %in% names(dat)) {
    vals <- dat[[var_name]][!is.na(dat[[var_name]])]
    invalid <- vals[!vals %in% valid_values]
    if (length(invalid) > 0) {
      warning(label, ": Invalid codes found: ",
              paste(unique(invalid), collapse = ", "),
              "\n  Valid codes: ", paste(valid_values, collapse = ", "))
    }
  }
}

validate_coding(dat, "human_oversight",    1:3, "Human oversight level")
validate_coding(dat, "agent_architecture", 1:2, "Agent architecture")
validate_coding(dat, "agency_level",       1:4, "Agency level (APCP)")
validate_coding(dat, "agent_role",         1:6, "Agent role")
validate_coding(dat, "learning_context",   1:5, "Learning context")
validate_coding(dat, "outcome_type",       1:4, "Outcome type")
validate_coding(dat, "blooms_level",       1:3, "Bloom's level")
validate_coding(dat, "design",             1:3, "Study design")
validate_coding(dat, "ai_technology",      1:6, "AI technology")
validate_coding(dat, "adaptivity_level",   1:5, "Adaptivity level")
validate_coding(dat, "agent_modality",     1:4, "Agent modality")


# ============================================================================
# 6. ADD FACTOR LABELS
# ============================================================================

message("\nApplying factor labels...")

# Helper function to create labeled factor
label_factor <- function(x, labels_vec) {
  factor(x, levels = as.numeric(names(labels_vec)), labels = labels_vec)
}

if ("human_oversight" %in% names(dat)) {
  dat$human_oversight_f <- label_factor(dat$human_oversight, HUMAN_OVERSIGHT_LABELS)
}
if ("agent_architecture" %in% names(dat)) {
  dat$agent_architecture_f <- label_factor(dat$agent_architecture, AGENT_ARCHITECTURE_LABELS)
}
if ("agency_level" %in% names(dat)) {
  dat$agency_level_f <- label_factor(dat$agency_level, AGENCY_LEVEL_LABELS)
}
if ("agent_role" %in% names(dat)) {
  dat$agent_role_f <- label_factor(dat$agent_role, AGENT_ROLE_LABELS)
}
if ("agent_modality" %in% names(dat)) {
  dat$agent_modality_f <- label_factor(dat$agent_modality, AGENT_MODALITY_LABELS)
}
if ("ai_technology" %in% names(dat)) {
  dat$ai_technology_f <- label_factor(dat$ai_technology, AI_TECHNOLOGY_LABELS)
}
if ("adaptivity_level" %in% names(dat)) {
  dat$adaptivity_level_f <- label_factor(dat$adaptivity_level, ADAPTIVITY_LABELS)
}
if ("learning_context" %in% names(dat)) {
  dat$learning_context_f <- label_factor(dat$learning_context, LEARNING_CONTEXT_LABELS)
}
if ("subject_domain" %in% names(dat)) {
  dat$subject_domain_f <- label_factor(dat$subject_domain, SUBJECT_DOMAIN_LABELS)
}
if ("outcome_type" %in% names(dat)) {
  dat$outcome_type_f <- label_factor(dat$outcome_type, OUTCOME_TYPE_LABELS)
}
if ("blooms_level" %in% names(dat)) {
  dat$blooms_level_f <- label_factor(dat$blooms_level, BLOOMS_LABELS)
}
if ("design" %in% names(dat)) {
  dat$design_f <- label_factor(dat$design, STUDY_DESIGN_LABELS)
}

# --- Compute overall risk of bias if individual domains exist ---
rob_cols <- grep("^rob_(?!overall)", names(dat), value = TRUE, perl = TRUE)
if (length(rob_cols) >= 3 && !"rob_overall" %in% names(dat)) {
  dat$rob_overall <- NA
}
if (length(rob_cols) >= 3) {
  missing_rob <- is.na(dat$rob_overall)
  if (sum(missing_rob) > 0) {
    dat$rob_overall_f[!missing_rob] <- compute_rob_overall(dat[!missing_rob, ])
  }
} else {
  dat$rob_overall_f <- NA_character_
}

# Create quality category
if ("rob_overall" %in% names(dat)) {
  dat$quality <- case_when(
    dat$rob_overall == 2 ~ "High Quality",
    dat$rob_overall == 1 ~ "Moderate Quality",
    dat$rob_overall == 0 ~ "Low Quality",
    TRUE                  ~ NA_character_
  )
  dat$quality <- factor(dat$quality,
                        levels = c("High Quality", "Moderate Quality", "Low Quality"))
}

# --- Create study label for forest plots ---
if (all(c("author", "year") %in% names(dat))) {
  dat$study_label <- paste0(dat$author, " (", dat$year, ")")
}


# ============================================================================
# 7. HANDLE MULTIPLE EFFECT SIZES PER STUDY
# ============================================================================

message("\nChecking for dependent effect sizes...")

# Count effect sizes per study
es_per_study <- dat %>%
  filter(!is.na(hedges_g)) %>%
  group_by(study_id) %>%
  summarise(n_es = n(), .groups = "drop")

n_multi <- sum(es_per_study$n_es > 1)
n_single <- sum(es_per_study$n_es == 1)
n_total_es <- sum(es_per_study$n_es)

message("  Total studies with valid ES: ", nrow(es_per_study))
message("  Studies with single ES:      ", n_single)
message("  Studies with multiple ES:     ", n_multi)
message("  Total effect sizes:           ", n_total_es)

if (n_multi > 0) {
  message("\n  Multi-ES studies:")
  multi_studies <- es_per_study %>% filter(n_es > 1) %>% arrange(desc(n_es))
  for (i in 1:nrow(multi_studies)) {
    sid <- multi_studies$study_id[i]
    lbl <- dat$study_label[dat$study_id == sid][1]
    message("    ", lbl, " (study_id=", sid, "): ",
            multi_studies$n_es[i], " effect sizes")
  }
}

# Add a flag for dependent ES
dat <- dat %>%
  left_join(es_per_study, by = "study_id") %>%
  mutate(dependent_es = n_es > 1)


# ============================================================================
# 8. FILTER TO ANALYSIS-READY DATASET
# ============================================================================

# Keep only rows with valid effect sizes
dat_analysis <- dat %>%
  filter(!is.na(hedges_g) & !is.na(se_g) & se_g > 0)

n_excluded <- nrow(dat) - nrow(dat_analysis)
if (n_excluded > 0) {
  message("\nExcluded ", n_excluded, " rows without valid effect sizes")
}

message("Final analysis dataset: ", nrow(dat_analysis), " effect sizes from ",
        n_distinct(dat_analysis$study_id), " studies")


# ============================================================================
# 9. DESCRIPTIVE SUMMARY
# ============================================================================

message("\n--- Descriptive Summary ---\n")

summary_lines <- c(
  "=======================================================",
  "Meta-Analysis Data Summary",
  paste("Date:", Sys.Date()),
  "=======================================================",
  "",
  paste("Total effect sizes:     ", nrow(dat_analysis)),
  paste("Total unique studies:   ", n_distinct(dat_analysis$study_id)),
  ""
)

# Effect size distribution
if (nrow(dat_analysis) > 0) {
  summary_lines <- c(summary_lines,
    "--- Effect Size Distribution ---",
    paste("  Mean g:   ", fmt(mean(dat_analysis$hedges_g), 3)),
    paste("  Median g: ", fmt(median(dat_analysis$hedges_g), 3)),
    paste("  SD g:     ", fmt(sd(dat_analysis$hedges_g), 3)),
    paste("  Min g:    ", fmt(min(dat_analysis$hedges_g), 3)),
    paste("  Max g:    ", fmt(max(dat_analysis$hedges_g), 3)),
    ""
  )

  # Sample size distribution
  if ("n_total" %in% names(dat_analysis) || all(c("n_treatment_es", "n_control_es") %in% names(dat_analysis))) {
    n_col <- if ("n_total" %in% names(dat_analysis)) {
      dat_analysis$n_total
    } else {
      dat_analysis$n_treatment_es + dat_analysis$n_control_es
    }
    summary_lines <- c(summary_lines,
      "--- Sample Size Distribution ---",
      paste("  Total N:  ", sum(n_col, na.rm = TRUE)),
      paste("  Mean N:   ", fmt(mean(n_col, na.rm = TRUE), 1)),
      paste("  Median N: ", fmt(median(n_col, na.rm = TRUE), 1)),
      paste("  Min N:    ", min(n_col, na.rm = TRUE)),
      paste("  Max N:    ", max(n_col, na.rm = TRUE)),
      ""
    )
  }

  # Publication year distribution
  if ("year" %in% names(dat_analysis)) {
    summary_lines <- c(summary_lines,
      "--- Publication Year ---",
      paste("  Range:", min(dat_analysis$year, na.rm = TRUE), "-",
            max(dat_analysis$year, na.rm = TRUE)),
      ""
    )
    year_tab <- table(dat_analysis$year)
    for (y in names(year_tab)) {
      summary_lines <- c(summary_lines,
        paste("  ", y, ":", year_tab[y], "effect sizes"))
    }
    summary_lines <- c(summary_lines, "")
  }

  # Moderator distributions
  mod_vars <- list(
    "Human Oversight"    = "human_oversight_f",
    "Agent Architecture" = "agent_architecture_f",
    "Agency Level"       = "agency_level_f",
    "Learning Context"   = "learning_context_f",
    "Outcome Type"       = "outcome_type_f",
    "Agent Role"         = "agent_role_f",
    "AI Technology"      = "ai_technology_f",
    "Bloom's Level"      = "blooms_level_f",
    "Study Design"       = "design_f"
  )

  for (mod_name in names(mod_vars)) {
    col_name <- mod_vars[[mod_name]]
    if (col_name %in% names(dat_analysis)) {
      tab <- table(dat_analysis[[col_name]], useNA = "ifany")
      if (length(tab) > 0) {
        summary_lines <- c(summary_lines, paste("---", mod_name, "---"))
        for (lvl in names(tab)) {
          summary_lines <- c(summary_lines,
            paste("  ", lvl, ":", tab[lvl]))
        }
        summary_lines <- c(summary_lines, "")
      }
    }
  }
}

# Print summary
cat(paste(summary_lines, collapse = "\n"))

# Save summary to file
summary_path <- file.path(PATHS$output, "data_summary.txt")
writeLines(summary_lines, summary_path)
message("\nSummary saved to: ", summary_path)


# ============================================================================
# 10. EXPORT CLEAN DATA
# ============================================================================

# Save as CSV
csv_out <- file.path(PATHS$data_final, "ma_data_clean.csv")
readr::write_csv(dat_analysis, csv_out)
message("Clean data saved to: ", csv_out)

# Save as RDS (preserves factor levels and attributes)
rds_out <- file.path(PATHS$data_final, "ma_data_clean.rds")
saveRDS(dat_analysis, rds_out)
message("Clean data saved to: ", rds_out)

# Also save the full dataset (including excluded rows) for auditing
rds_full <- file.path(PATHS$data_final, "ma_data_full.rds")
saveRDS(dat, rds_full)
message("Full dataset saved to: ", rds_full)

message("\n========== 01: Data Preparation Complete ==========\n")
