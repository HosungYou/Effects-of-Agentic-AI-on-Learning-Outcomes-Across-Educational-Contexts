# ============================================================================
# 08_halo_mapping.R
# RQ5: HALO Framework Mapping -- Meta-Analysis to Design Principles
# ============================================================================
#
# Purpose:
#   Extract key findings from the moderator analyses (RQ2-RQ4 and additional)
#   and systematically map them to the three layers of the HALO (Human-AI
#   Learning Orchestration) Framework. Generates design principles with
#   evidence strength ratings, a comprehensive mapping table, and
#   visualization of the evidence-to-framework linkages.
#
# HALO Framework Layers:
#   Layer 1 (Foundation):   Agency level, context-specific rules, outcome rules
#   Layer 2 (Protocol):     Dynamic learner state, multi-agent comm, adaptivity
#   Layer 3 (Orchestration): Human oversight calibration, agent role assignment
#
# Input:
#   data/04_final/ma_data_clean.rds
#   analysis/output/moderator_analysis/moderator_summary.csv
#   analysis/output/model_primary.rds
#
# Output:
#   analysis/output/halo_mapping_report.txt
#   analysis/output/halo_design_principles.csv
#   analysis/output/halo_evidence_table.csv
#   analysis/output/figures/halo_mapping.png
#   analysis/output/figures/halo_evidence_strength.png
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 08: HALO Framework Mapping (RQ5) ==========\n")


# ============================================================================
# 1. LOAD DATA AND RESULTS
# ============================================================================

dat <- readRDS(file.path(PATHS$data_final, "ma_data_clean.rds"))

# Load moderator results
mod_path <- file.path(PATHS$out_mod, "moderator_summary.csv")
if (file.exists(mod_path)) {
  mod_results <- readr::read_csv(mod_path, show_col_types = FALSE)
  message("Loaded moderator results: ", nrow(mod_results), " subgroup estimates")
} else {
  stop("Moderator results not found at: ", mod_path,
       "\nRun 03_moderator_analysis.R first.")
}

# Load overall model
primary_path <- file.path(PATHS$output, "model_primary.rds")
if (file.exists(primary_path)) {
  res_primary <- readRDS(primary_path)
  overall_g <- coef(res_primary)
} else {
  overall_g <- NA
  message("  Warning: Primary model not found. Overall g will be NA.")
}

fig_dir <- PATHS$out_figures
if (!dir.exists(fig_dir)) dir.create(fig_dir, recursive = TRUE)


# ============================================================================
# 2. EXTRACT KEY FINDINGS FROM MODERATOR ANALYSES
# ============================================================================

message("\n--- 2. Extracting Key Findings ---\n")

# Helper function to extract the best-performing subgroup
extract_finding <- function(mod_df, moderator_name) {
  sub <- mod_df %>% filter(moderator == moderator_name)
  if (nrow(sub) == 0) return(NULL)

  best <- sub %>% arrange(desc(g)) %>% slice(1)
  worst <- sub %>% arrange(g) %>% slice(1)

  list(
    moderator     = moderator_name,
    best_level    = best$level,
    best_g        = best$g,
    best_ci       = c(best$ci_lower, best$ci_upper),
    worst_level   = worst$level,
    worst_g       = worst$g,
    worst_ci      = c(worst$ci_lower, worst$ci_upper),
    g_difference  = best$g - worst$g,
    QM_p          = unique(sub$QM_p),
    significant   = unique(sub$QM_p) < ALPHA,
    k_total       = sum(sub$k),
    n_levels      = nrow(sub)
  )
}

# Extract findings for all key moderators
findings <- list(
  oversight   = extract_finding(mod_results, "Human Oversight Level (RQ2)"),
  architecture= extract_finding(mod_results, "Agent Architecture (RQ3)"),
  context     = extract_finding(mod_results, "Learning Context (RQ4)"),
  role        = extract_finding(mod_results, "Agent Role"),
  agency      = extract_finding(mod_results, "Agency Level (APCP)"),
  modality    = extract_finding(mod_results, "Agent Modality"),
  technology  = extract_finding(mod_results, "AI Technology"),
  adaptivity  = extract_finding(mod_results, "Adaptivity Level"),
  domain      = extract_finding(mod_results, "Subject Domain"),
  outcome     = extract_finding(mod_results, "Outcome Type"),
  blooms      = extract_finding(mod_results, "Bloom's Level")
)

# Remove NULL entries
findings <- findings[!sapply(findings, is.null)]

# Print findings summary
for (name in names(findings)) {
  f <- findings[[name]]
  sig_marker <- if (f$significant) " ***" else ""
  message("  ", f$moderator, sig_marker)
  message("    Best: ", f$best_level, " (g = ", fmt(f$best_g, 3), ")")
  message("    Worst: ", f$worst_level, " (g = ", fmt(f$worst_g, 3), ")")
  message("    Difference: ", fmt(f$g_difference, 3),
          " | QM p ", fmt_p(f$QM_p))
}


# ============================================================================
# 3. EVIDENCE STRENGTH RATING
# ============================================================================
# Rate the strength of evidence for each finding based on:
#   - Statistical significance of the moderator test
#   - Number of studies per subgroup
#   - Magnitude of the effect difference
#   - Consistency with theoretical predictions

message("\n--- 3. Evidence Strength Rating ---\n")

rate_evidence_strength <- function(finding) {
  score <- 0

  # Criterion 1: Statistical significance (0-3 points)
  if (!is.na(finding$QM_p)) {
    if (finding$QM_p < 0.001) score <- score + 3
    else if (finding$QM_p < 0.01) score <- score + 2
    else if (finding$QM_p < 0.05) score <- score + 1
  }

  # Criterion 2: Number of studies (0-3 points)
  if (finding$k_total >= 50) score <- score + 3
  else if (finding$k_total >= 20) score <- score + 2
  else if (finding$k_total >= 10) score <- score + 1

  # Criterion 3: Effect size difference magnitude (0-3 points)
  diff <- abs(finding$g_difference)
  if (diff >= 0.50) score <- score + 3
  else if (diff >= 0.30) score <- score + 2
  else if (diff >= 0.15) score <- score + 1

  # Criterion 4: Number of subgroup levels with k >= 3 (0-1 point)
  if (finding$n_levels >= 3) score <- score + 1

  # Convert to rating
  rating <- case_when(
    score >= 8  ~ "Strong",
    score >= 5  ~ "Moderate",
    score >= 3  ~ "Preliminary",
    TRUE        ~ "Insufficient"
  )

  return(list(score = score, rating = rating))
}

# Rate all findings
for (name in names(findings)) {
  evidence <- rate_evidence_strength(findings[[name]])
  findings[[name]]$evidence_score  <- evidence$score
  findings[[name]]$evidence_rating <- evidence$rating
}


# ============================================================================
# 4. MAP FINDINGS TO HALO FRAMEWORK LAYERS
# ============================================================================

message("\n--- 4. Mapping Findings to HALO Framework ---\n")

# --- Layer 1: Foundation ---
# "FOR WHOM and IN WHAT CONTEXT?"
# Maps: agency level, learning context, outcome type, Bloom's level, domain

layer1_findings <- list()

# Agency Level Calibration (from APCP moderator)
if (!is.null(findings$agency)) {
  f <- findings$agency
  layer1_findings[["agency_calibration"]] <- tibble(
    layer           = "Layer 1: Foundation",
    component       = "Agency Level Calibration",
    finding         = paste0(f$best_level, " agency yielded the largest effect (g = ",
                             fmt(f$best_g, 2), ")"),
    design_principle= paste0("Default to ", f$best_level, " agency level; ",
                             "adjust based on learner context and outcome goals"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= paste0("APCP framework calibration: ",
                             f$best_level, " as default starting level")
  )
}

# Context-Specific Rules (from learning context moderator)
if (!is.null(findings$context)) {
  f <- findings$context
  # Get all context effect sizes
  context_data <- mod_results %>%
    filter(moderator == "Learning Context (RQ4)") %>%
    arrange(desc(g))

  context_summary <- paste(
    apply(context_data, 1, function(r) {
      paste0(r["level"], " (g = ", fmt(as.numeric(r["g"]), 2), ")")
    }),
    collapse = "; "
  )

  layer1_findings[["context_rules"]] <- tibble(
    layer           = "Layer 1: Foundation",
    component       = "Context-Specific Rules",
    finding         = paste0("Effect sizes vary by context: ", context_summary),
    design_principle= paste0("Implement context-specific configurations; ",
                             f$best_level, " shows strongest effects"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= "Context-dependent configuration parameters required"
  )
}

# Outcome-Specific Rules (from outcome type and Bloom's level)
if (!is.null(findings$outcome)) {
  f <- findings$outcome
  layer1_findings[["outcome_rules"]] <- tibble(
    layer           = "Layer 1: Foundation",
    component       = "Outcome-Specific Rules",
    finding         = paste0("Effect varies by outcome type; ", f$best_level,
                             " outcomes benefit most (g = ", fmt(f$best_g, 2), ")"),
    design_principle= paste0("Calibrate agent behavior to target outcome type; ",
                             "strongest effects for ", f$best_level, " outcomes"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= "Outcome-aware agent configuration"
  )
}

if (!is.null(findings$blooms)) {
  f <- findings$blooms
  layer1_findings[["blooms_rules"]] <- tibble(
    layer           = "Layer 1: Foundation",
    component       = "Outcome-Specific Rules (Bloom's)",
    finding         = paste0(f$best_level, " tasks show strongest effects (g = ",
                             fmt(f$best_g, 2), ")"),
    design_principle= paste0("Match oversight level and agent behavior to ",
                             "cognitive complexity; ", f$best_level,
                             " tasks benefit most from agentic AI"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= "Bloom's taxonomy-based configuration gradient"
  )
}


# --- Layer 2: Protocol ---
# "WHAT should the system track and communicate?"
# Maps: agent architecture, adaptivity level, AI technology

layer2_findings <- list()

# Multi-Agent Communication (from architecture moderator)
if (!is.null(findings$architecture)) {
  f <- findings$architecture
  layer2_findings[["multiagent_comm"]] <- tibble(
    layer           = "Layer 2: Protocol",
    component       = "Multi-Agent Communication",
    finding         = paste0("Single agent (g = ",
                             fmt(mod_results$g[mod_results$moderator == "Agent Architecture (RQ3)" &
                                                grepl("Single", mod_results$level)][1], 2),
                             ") vs Multi-agent (g = ",
                             fmt(mod_results$g[mod_results$moderator == "Agent Architecture (RQ3)" &
                                                grepl("Multi", mod_results$level)][1], 2), ")"),
    design_principle= ifelse(f$significant,
                             paste0(f$best_level, " systems are significantly more effective; ",
                                    "implement MCP-based coordination"),
                             "No significant difference; architecture choice is context-dependent"),
    evidence_source = f$moderator,
    effect_size     = f$g_difference,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= ifelse(f$significant & grepl("Multi", f$best_level),
                             "MCP protocol justified for multi-agent coordination",
                             "Simpler single-agent may suffice")
  )
}

# Adaptivity Engine (from adaptivity moderator)
if (!is.null(findings$adaptivity)) {
  f <- findings$adaptivity
  layer2_findings[["adaptivity_engine"]] <- tibble(
    layer           = "Layer 2: Protocol",
    component       = "Adaptivity Engine",
    finding         = paste0(f$best_level, " adaptivity most effective (g = ",
                             fmt(f$best_g, 2), ")"),
    design_principle= paste0("Implement ", f$best_level, " state tracking; ",
                             "cost-benefit supports ", f$best_level, " over simpler approaches"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= paste0(f$best_level, " tracking in Layer 2 learner state model")
  )
}

# Dynamic Learner State (from modality and technology)
if (!is.null(findings$technology)) {
  f <- findings$technology
  layer2_findings[["learner_state"]] <- tibble(
    layer           = "Layer 2: Protocol",
    component       = "Dynamic Learner State Tracking",
    finding         = paste0(f$best_level, " technology most effective (g = ",
                             fmt(f$best_g, 2), ")"),
    design_principle= paste0("Leverage ", f$best_level, " capabilities for state tracking; ",
                             "technology choice matters for learner modeling"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= "Technology-informed state tracking design"
  )
}


# --- Layer 3: Orchestration ---
# "HOW should AI agents interact with learners?"
# Maps: human oversight, agent role, modality

layer3_findings <- list()

# Human Oversight Calibration (PRIMARY -- from RQ2)
if (!is.null(findings$oversight)) {
  f <- findings$oversight

  # Get all oversight level effect sizes
  oversight_data <- mod_results %>%
    filter(moderator == "Human Oversight Level (RQ2)") %>%
    arrange(desc(g))

  layer3_findings[["oversight_calibration"]] <- tibble(
    layer           = "Layer 3: Orchestration",
    component       = "Human Oversight Calibration",
    finding         = paste0(f$best_level, " shows strongest effects (g = ",
                             fmt(f$best_g, 2), "); ",
                             f$worst_level, " shows weakest (g = ",
                             fmt(f$worst_g, 2), ")"),
    design_principle= paste0("Default oversight level: ", f$best_level, "; ",
                             "implement Red/Orange/Yellow checkpoint system ",
                             "calibrated to ", f$best_level, " as baseline"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= paste0("Checkpoint system default: ",
                             ifelse(grepl("Checkpoint", f$best_level),
                                    "Moderate frequency (Orange/Yellow dominant)",
                                    ifelse(grepl("Autonomous", f$best_level),
                                           "Low frequency (Yellow dominant)",
                                           "High frequency (Red/Orange dominant)")))
  )
}

# Agent Role Assignment (from role moderator)
if (!is.null(findings$role)) {
  f <- findings$role
  layer3_findings[["role_assignment"]] <- tibble(
    layer           = "Layer 3: Orchestration",
    component       = "Agent Role Assignment",
    finding         = paste0(f$best_level, " role most effective (g = ",
                             fmt(f$best_g, 2), ")"),
    design_principle= paste0("Prioritize ", f$best_level, " role in agent assignment; ",
                             "role-affordance mapping should favor ", f$best_level),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= paste0("Role assignment priority: ", f$best_level)
  )
}

# Modality effects
if (!is.null(findings$modality)) {
  f <- findings$modality
  layer3_findings[["modality"]] <- tibble(
    layer           = "Layer 3: Orchestration",
    component       = "Interaction Modality",
    finding         = paste0(f$best_level, " modality most effective (g = ",
                             fmt(f$best_g, 2), ")"),
    design_principle= paste0("When feasible, implement ", f$best_level,
                             " interaction modality"),
    evidence_source = f$moderator,
    effect_size     = f$best_g,
    significant     = f$significant,
    evidence_rating = f$evidence_rating,
    halo_implication= paste0("Preferred modality: ", f$best_level)
  )
}


# ============================================================================
# 5. COMPILE DESIGN PRINCIPLES TABLE
# ============================================================================

message("\n--- 5. Compiling Design Principles ---\n")

all_principles <- bind_rows(
  bind_rows(layer1_findings),
  bind_rows(layer2_findings),
  bind_rows(layer3_findings)
)

if (nrow(all_principles) > 0) {
  # Add principle IDs
  all_principles <- all_principles %>%
    mutate(
      principle_id = paste0("DP-", sprintf("%02d", row_number())),
      evidence_rating = factor(evidence_rating,
                               levels = c("Strong", "Moderate", "Preliminary", "Insufficient"))
    ) %>%
    select(principle_id, layer, component, finding, design_principle,
           evidence_source, effect_size, significant, evidence_rating,
           halo_implication)

  # Print
  message("\n  HALO Design Principles:")
  for (i in 1:nrow(all_principles)) {
    p <- all_principles[i, ]
    message("  ", p$principle_id, " [", p$layer, " / ", p$component, "]")
    message("    Finding: ", p$finding)
    message("    Principle: ", p$design_principle)
    message("    Evidence: ", p$evidence_rating,
            if (p$significant) " (significant)" else " (not significant)")
    message()
  }

  # Save
  principles_path <- file.path(PATHS$output, "halo_design_principles.csv")
  readr::write_csv(all_principles, principles_path)
  message("Saved: ", principles_path)
} else {
  message("  No design principles could be generated (insufficient moderator data)")
}


# ============================================================================
# 6. EVIDENCE STRENGTH VISUALIZATION
# ============================================================================

message("\n--- 6. Evidence Strength Visualization ---\n")

if (nrow(all_principles) > 0) {

  # --- 6.1 Evidence strength by layer ---
  p_evidence <- ggplot(all_principles,
                       aes(x = effect_size,
                           y = reorder(component, effect_size),
                           fill = evidence_rating)) +
    geom_col(width = 0.7, alpha = 0.85) +
    geom_text(aes(label = paste0("g = ", fmt(effect_size, 2))),
              hjust = -0.1, size = 3.2) +
    facet_wrap(~ layer, scales = "free_y", ncol = 1) +
    scale_fill_manual(
      values = c(
        "Strong"       = "#27AE60",
        "Moderate"     = "#3498DB",
        "Preliminary"  = "#F39C12",
        "Insufficient" = "#BDC3C7"
      ),
      name = "Evidence Strength",
      drop = FALSE
    ) +
    labs(
      title    = "HALO Framework: Evidence Strength by Component",
      subtitle = "Effect sizes from moderator analyses mapped to framework layers",
      x        = "Effect Size (Hedges' g)",
      y        = NULL
    ) +
    theme_meta(base_size = 11) +
    theme(
      strip.text = element_text(face = "bold", size = 12),
      legend.position = "bottom"
    )

  ggsave(file.path(fig_dir, "halo_evidence_strength.png"), p_evidence,
         width = 12, height = max(6, nrow(all_principles) * 0.6 + 3),
         dpi = 300, bg = "white")
  ggsave(file.path(fig_dir, "halo_evidence_strength.pdf"), p_evidence,
         width = 12, height = max(6, nrow(all_principles) * 0.6 + 3))
  message("  Saved: halo_evidence_strength")

  # --- 6.2 HALO mapping diagram (layer structure) ---
  layer_summary <- all_principles %>%
    group_by(layer) %>%
    summarise(
      n_principles  = n(),
      n_significant = sum(significant),
      mean_g        = mean(effect_size, na.rm = TRUE),
      components    = paste(unique(component), collapse = "\n"),
      .groups       = "drop"
    )

  p_halo <- ggplot(layer_summary,
                   aes(x = 1, y = reorder(layer, -row_number()))) +
    geom_tile(aes(fill = mean_g), width = 0.8, height = 0.8,
              color = "white", linewidth = 2) +
    geom_text(aes(label = paste0(
      layer, "\n\n",
      "Principles: ", n_principles, "\n",
      "Significant: ", n_significant, "/", n_principles, "\n",
      "Mean g = ", fmt(mean_g, 2)
    )), size = 3.5, fontface = "bold") +
    scale_fill_gradient(low = "#EBF5FB", high = "#2E86C1",
                        name = "Mean Effect Size") +
    labs(
      title    = "HALO Framework: Evidence Summary by Layer",
      subtitle = "Layers ordered Foundation -> Protocol -> Orchestration"
    ) +
    theme_void() +
    theme(
      plot.title    = element_text(face = "bold", size = 14, hjust = 0.5),
      plot.subtitle = element_text(size = 10, hjust = 0.5, color = "grey40"),
      legend.position = "bottom"
    )

  ggsave(file.path(fig_dir, "halo_mapping.png"), p_halo,
         width = 8, height = 6, dpi = 300, bg = "white")
  message("  Saved: halo_mapping")

  # --- 6.3 Significance matrix ---
  sig_matrix <- all_principles %>%
    mutate(sig_label = ifelse(significant, "Significant", "Not Significant"))

  p_sig <- ggplot(sig_matrix,
                  aes(x = layer, y = reorder(component, as.numeric(evidence_rating)),
                      fill = evidence_rating)) +
    geom_tile(color = "white", linewidth = 1.5) +
    geom_text(aes(label = paste0(
      ifelse(significant, "p < .05", "n.s."), "\n",
      "g = ", fmt(effect_size, 2)
    )), size = 3) +
    scale_fill_manual(
      values = c(
        "Strong"       = "#27AE60",
        "Moderate"     = "#3498DB",
        "Preliminary"  = "#F39C12",
        "Insufficient" = "#BDC3C7"
      ),
      name = "Evidence Strength"
    ) +
    labs(
      title = "HALO Framework: Evidence Matrix",
      x     = NULL,
      y     = NULL
    ) +
    theme_meta() +
    theme(
      axis.text.x = element_text(angle = 15, hjust = 1, size = 9,
                                 face = "bold")
    )

  ggsave(file.path(fig_dir, "halo_evidence_matrix.png"), p_sig,
         width = 12, height = 7, dpi = 300, bg = "white")
  message("  Saved: halo_evidence_matrix")
}


# ============================================================================
# 7. GENERATE EVIDENCE TABLE FOR MANUSCRIPT
# ============================================================================

message("\n--- 7. Evidence Table ---\n")

if (nrow(all_principles) > 0) {
  evidence_table <- all_principles %>%
    select(
      `Principle ID` = principle_id,
      `HALO Layer`   = layer,
      `Component`    = component,
      `Meta-Analytic Finding` = finding,
      `Design Principle`      = design_principle,
      `Effect Size (g)`       = effect_size,
      `Significant`           = significant,
      `Evidence Strength`     = evidence_rating,
      `Implementation Guideline` = halo_implication
    ) %>%
    mutate(
      `Effect Size (g)` = fmt(`Effect Size (g)`, 3),
      `Significant` = ifelse(`Significant`, "Yes", "No")
    )

  # Save as CSV
  evidence_path <- file.path(PATHS$output, "halo_evidence_table.csv")
  readr::write_csv(evidence_table, evidence_path)
  message("Saved: ", evidence_path)

  # Save as Excel if writexl is available
  tryCatch({
    xlsx_path <- file.path(PATHS$output, "halo_evidence_table.xlsx")
    writexl::write_xlsx(evidence_table, xlsx_path)
    message("Saved: ", xlsx_path)
  }, error = function(e) NULL)

  # Print formatted table
  if (requireNamespace("kableExtra", quietly = TRUE)) {
    kbl <- knitr::kable(evidence_table, format = "pipe",
                         caption = "Table: HALO Framework Design Principles Derived from Meta-Analysis")
    cat(kbl, sep = "\n")
  } else {
    print(evidence_table)
  }
}


# ============================================================================
# 8. COMPREHENSIVE REPORT
# ============================================================================

report_path <- file.path(PATHS$output, "halo_mapping_report.txt")
sink(report_path)

cat("=======================================================\n")
cat("RQ5: HALO Framework Mapping Report\n")
cat(paste("Date:", Sys.Date()), "\n")
cat("=======================================================\n\n")

if (!is.na(overall_g)) {
  cat("Overall effect: g = ", fmt(overall_g, 3), "\n\n")
}

cat("-------------------------------------------------------\n")
cat("SUMMARY OF FINDINGS BY HALO LAYER\n")
cat("-------------------------------------------------------\n\n")

for (layer_name in c("Layer 1: Foundation", "Layer 2: Protocol",
                     "Layer 3: Orchestration")) {
  cat("=== ", layer_name, " ===\n\n")

  layer_principles <- all_principles %>% filter(layer == layer_name)
  if (nrow(layer_principles) == 0) {
    cat("  No principles mapped to this layer.\n\n")
    next
  }

  for (i in 1:nrow(layer_principles)) {
    p <- layer_principles[i, ]
    cat(p$principle_id, ": ", p$component, "\n")
    cat("  Finding: ", p$finding, "\n")
    cat("  Principle: ", p$design_principle, "\n")
    cat("  Evidence: ", as.character(p$evidence_rating))
    if (p$significant) cat(" (statistically significant)")
    cat("\n")
    cat("  Effect: g = ", fmt(p$effect_size, 3), "\n")
    cat("  HALO implication: ", p$halo_implication, "\n\n")
  }
}

cat("-------------------------------------------------------\n")
cat("EVIDENCE STRENGTH SUMMARY\n")
cat("-------------------------------------------------------\n\n")

if (nrow(all_principles) > 0) {
  strength_table <- table(all_principles$evidence_rating)
  for (s in names(strength_table)) {
    cat("  ", s, ": ", strength_table[s], " principles\n")
  }
  cat("\n  Total design principles: ", nrow(all_principles), "\n")
  cat("  Significant moderator tests: ",
      sum(all_principles$significant), "/", nrow(all_principles), "\n")
}

cat("\n-------------------------------------------------------\n")
cat("IMPLICATIONS FOR HALO IMPLEMENTATION\n")
cat("-------------------------------------------------------\n\n")

cat("Minimum Viable HALO Implementation (based on strongest evidence):\n\n")

strong_principles <- all_principles %>%
  filter(evidence_rating %in% c("Strong", "Moderate")) %>%
  arrange(layer)

if (nrow(strong_principles) > 0) {
  for (i in 1:nrow(strong_principles)) {
    p <- strong_principles[i, ]
    cat("  ", i, ". [", p$layer, "] ", p$design_principle, "\n")
  }
} else {
  cat("  Insufficient strong evidence for minimum viable recommendations.\n")
  cat("  Consider all principles as preliminary guidelines.\n")
}

cat("\n\nNote: These design principles are derived from the meta-analytic\n")
cat("evidence and represent the empirically-refined version of the HALO\n")
cat("Framework. Principles with 'Strong' or 'Moderate' evidence ratings\n")
cat("have the most robust empirical support.\n")

sink()
message("\nReport saved to: ", report_path)

# Copy key figures to the main figures directory
for (fig_name in c("halo_evidence_strength.png", "halo_mapping.png",
                   "halo_evidence_matrix.png")) {
  src <- file.path(fig_dir, fig_name)
  if (file.exists(src)) {
    file.copy(src, file.path(PATHS$figures, fig_name), overwrite = TRUE)
  }
}

message("\n========== 08: HALO Framework Mapping Complete ==========\n")
