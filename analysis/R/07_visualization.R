# ============================================================================
# 07_visualization.R
# Publication-Quality Visualizations
# ============================================================================
#
# Purpose:
#   Generate all figures for the manuscript and supplementary materials.
#   Figures follow APA 7th edition style guidelines and are produced in
#   both PNG (300 dpi for review) and PDF (vector for publication) formats.
#
# Figures:
#   1. Forest plots by moderator (RQ2, RQ3, RQ4)
#   2. Funnel plots (standard and contour-enhanced)
#   3. Bubble plots for meta-regression
#   4. Bar charts for subgroup comparisons
#   5. HALO Framework mapping visualization
#   6. PRISMA flow diagram
#   7. Summary figure: effect sizes across all moderators
#   8. Risk-of-bias summary figure
#
# Input:
#   data/04_final/ma_data_clean.rds
#   analysis/output/moderator_analysis/moderator_summary.csv
#   analysis/output/model_re.rds
#
# Output:
#   analysis/output/figures/*.png
#   analysis/output/figures/*.pdf
#   figures/output/*.png
#
# Authors: Hosung You
# Date:    2026-02-16
# ============================================================================

source(file.path(dirname(sys.frame(1)$ofile %||% "analysis/R"), "00_setup.R"))

message("\n========== 07: Visualization ==========\n")


# ============================================================================
# 1. LOAD DATA
# ============================================================================

dat <- readRDS(file.path(PATHS$data_final, "ma_data_clean.rds"))

re_path <- file.path(PATHS$output, "model_re.rds")
if (file.exists(re_path)) {
  res_re <- readRDS(re_path)
} else {
  res_re <- rma(yi = hedges_g, vi = var_g, data = dat, method = "REML",
                slab = dat$study_label)
}

# Load moderator results if available
mod_path <- file.path(PATHS$out_mod, "moderator_summary.csv")
if (file.exists(mod_path)) {
  mod_results <- readr::read_csv(mod_path, show_col_types = FALSE)
} else {
  mod_results <- NULL
  message("  Warning: No moderator results found. Some plots will be skipped.")
}

fig_dir <- PATHS$out_figures
if (!dir.exists(fig_dir)) dir.create(fig_dir, recursive = TRUE)

# Define a consistent color palette for the project
PALETTE <- list(
  primary    = "#2C3E50",    # Dark blue-grey
  secondary  = "#3498DB",    # Bright blue
  accent     = "#E74C3C",    # Red
  success    = "#27AE60",    # Green
  warning    = "#F39C12",    # Orange
  oversight  = c("#E74C3C", "#F39C12", "#27AE60"),  # Red, Orange, Green
  context    = c("#3498DB", "#9B59B6", "#1ABC9C", "#E67E22", "#95A5A6"),
  arch       = c("#2C3E50", "#3498DB"),
  sequential = c("#EBF5FB", "#AED6F1", "#5DADE2", "#2E86C1", "#1B4F72")
)


# ============================================================================
# 2. FOREST PLOTS BY MODERATOR
# ============================================================================

message("\n--- 2. Forest Plots by Moderator ---\n")

# --- Helper function: subgroup forest plot ---
plot_subgroup_forest <- function(data, moderator_col, moderator_label,
                                  colors = NULL, filename) {
  if (!moderator_col %in% names(data)) {
    message("  Skipping ", moderator_label, ": column not found")
    return(invisible(NULL))
  }

  d <- data %>% filter(!is.na(!!sym(moderator_col)))
  if (nrow(d) < 3) {
    message("  Skipping ", moderator_label, ": too few observations")
    return(invisible(NULL))
  }

  # Fit subgroup models
  levels_present <- sort(unique(d[[moderator_col]]))
  sub_results <- list()

  for (lvl in levels_present) {
    d_sub <- d[d[[moderator_col]] == lvl, ]
    if (nrow(d_sub) >= 2) {
      tryCatch({
        res_sub <- rma(yi = hedges_g, vi = var_g, data = d_sub, method = "REML")
        sub_results[[as.character(lvl)]] <- tibble(
          group  = as.character(lvl),
          g      = coef(res_sub),
          ci_lo  = res_sub$ci.lb,
          ci_hi  = res_sub$ci.ub,
          k      = res_sub$k,
          I2     = res_sub$I2
        )
      }, error = function(e) NULL)
    }
  }

  if (length(sub_results) == 0) return(invisible(NULL))

  plot_df <- bind_rows(sub_results) %>%
    mutate(
      label = paste0(group, " (k = ", k, ")"),
      label = factor(label, levels = rev(label))
    )

  if (is.null(colors)) {
    colors <- scales::hue_pal()(nrow(plot_df))
  } else {
    colors <- colors[1:nrow(plot_df)]
  }

  p <- ggplot(plot_df, aes(x = g, y = label, color = group)) +
    geom_vline(xintercept = 0, linetype = "dotted", color = "grey50") +
    geom_vline(xintercept = coef(res_re), linetype = "dashed",
               color = "grey40", linewidth = 0.4) +
    geom_errorbarh(aes(xmin = ci_lo, xmax = ci_hi), height = 0.25,
                   linewidth = 0.8) +
    geom_point(size = 4, shape = 18) +
    scale_color_manual(values = colors, guide = "none") +
    labs(
      title    = paste0("Effect Sizes by ", moderator_label),
      subtitle = paste0("Overall g = ", fmt(coef(res_re), 3),
                        " (dashed line)"),
      x        = "Hedges' g [95% CI]",
      y        = NULL
    ) +
    theme_meta(base_size = 13) +
    theme(
      plot.margin  = margin(10, 20, 10, 10),
      axis.text.y  = element_text(size = 11, face = "bold")
    )

  # Add effect size annotations
  p <- p +
    geom_text(
      aes(x = ci_hi + 0.05,
          label = paste0("g = ", fmt(g, 2))),
      hjust = 0, size = 3.5, color = "grey30"
    )

  # Save
  ggsave(file.path(fig_dir, paste0(filename, ".png")), p,
         width = 10, height = max(3, nrow(plot_df) * 0.8 + 2),
         dpi = 300, bg = "white")
  ggsave(file.path(fig_dir, paste0(filename, ".pdf")), p,
         width = 10, height = max(3, nrow(plot_df) * 0.8 + 2))
  message("  Saved: ", filename)

  return(p)
}

# RQ2: Human oversight
p_oversight <- plot_subgroup_forest(
  dat, "human_oversight_f", "Human Oversight Level (RQ2)",
  colors = PALETTE$oversight, filename = "forest_oversight")

# RQ3: Agent architecture
p_arch <- plot_subgroup_forest(
  dat, "agent_architecture_f", "Agent Architecture (RQ3)",
  colors = PALETTE$arch, filename = "forest_architecture")

# RQ4: Learning context
p_context <- plot_subgroup_forest(
  dat, "learning_context_f", "Learning Context (RQ4)",
  colors = PALETTE$context, filename = "forest_context")

# Additional moderators
p_role <- plot_subgroup_forest(
  dat, "agent_role_f", "Agent Role", filename = "forest_role")
p_agency <- plot_subgroup_forest(
  dat, "agency_level_f", "Agency Level (APCP)", filename = "forest_agency")
p_outcome <- plot_subgroup_forest(
  dat, "outcome_type_f", "Outcome Type", filename = "forest_outcome_type")
p_blooms <- plot_subgroup_forest(
  dat, "blooms_level_f", "Bloom's Taxonomy Level", filename = "forest_blooms")
p_tech <- plot_subgroup_forest(
  dat, "ai_technology_f", "AI Technology", filename = "forest_technology")


# ============================================================================
# 3. BUBBLE PLOTS FOR META-REGRESSION
# ============================================================================

message("\n--- 3. Bubble Plots ---\n")

# Publication year regression
if ("year" %in% names(dat)) {
  p_year <- ggplot(dat, aes(x = year, y = hedges_g)) +
    geom_hline(yintercept = 0, linetype = "dotted", color = "grey50") +
    geom_point(aes(size = 1 / var_g), alpha = 0.6, color = PALETTE$secondary) +
    geom_smooth(aes(weight = 1 / var_g), method = "lm", se = TRUE,
                color = PALETTE$primary, fill = PALETTE$secondary,
                alpha = 0.15, linewidth = 1) +
    scale_size_continuous(range = c(2, 10), guide = "none") +
    labs(
      title    = "Effect Size by Publication Year",
      subtitle = "Bubble size proportional to precision (1/variance)",
      x        = "Publication Year",
      y        = "Hedges' g"
    ) +
    theme_meta()

  ggsave(file.path(fig_dir, "bubble_year.png"), p_year,
         width = 8, height = 6, dpi = 300, bg = "white")
  ggsave(file.path(fig_dir, "bubble_year.pdf"), p_year,
         width = 8, height = 6)
  message("  Saved: bubble_year")
}

# Sample size regression
if (all(c("n_treatment_es", "n_control_es") %in% names(dat))) {
  dat$n_total_es <- dat$n_treatment_es + dat$n_control_es

  p_n <- ggplot(dat, aes(x = n_total_es, y = hedges_g)) +
    geom_hline(yintercept = 0, linetype = "dotted", color = "grey50") +
    geom_point(aes(size = 1 / var_g), alpha = 0.6, color = PALETTE$secondary) +
    geom_smooth(aes(weight = 1 / var_g), method = "lm", se = TRUE,
                color = PALETTE$primary, fill = PALETTE$secondary,
                alpha = 0.15, linewidth = 1) +
    scale_x_log10() +
    scale_size_continuous(range = c(2, 10), guide = "none") +
    labs(
      title    = "Effect Size by Sample Size",
      subtitle = "Log-scaled x-axis; bubble size proportional to precision",
      x        = "Total Sample Size (log scale)",
      y        = "Hedges' g"
    ) +
    theme_meta()

  ggsave(file.path(fig_dir, "bubble_sample_size.png"), p_n,
         width = 8, height = 6, dpi = 300, bg = "white")
  message("  Saved: bubble_sample_size")
}


# ============================================================================
# 4. BAR CHARTS FOR SUBGROUP COMPARISONS
# ============================================================================

message("\n--- 4. Subgroup Comparison Charts ---\n")

if (!is.null(mod_results) && nrow(mod_results) > 0) {

  # --- 4.1 Grouped bar chart: Key moderators (RQ2-RQ4) ---
  key_mods <- mod_results %>%
    filter(moderator %in% c("Human Oversight Level (RQ2)",
                            "Agent Architecture (RQ3)",
                            "Learning Context (RQ4)"))

  if (nrow(key_mods) > 0) {
    # Determine the RQ label for coloring
    key_mods <- key_mods %>%
      mutate(rq = case_when(
        grepl("RQ2", moderator) ~ "RQ2: Human Oversight",
        grepl("RQ3", moderator) ~ "RQ3: Architecture",
        grepl("RQ4", moderator) ~ "RQ4: Learning Context"
      ))

    p_bar_key <- ggplot(key_mods,
                        aes(x = reorder(level, g), y = g, fill = rq)) +
      geom_hline(yintercept = 0, color = "grey50", linetype = "dotted") +
      geom_col(alpha = 0.85, width = 0.7) +
      geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper),
                    width = 0.2, linewidth = 0.5) +
      geom_text(aes(label = paste0("g = ", fmt(g, 2), "\nk = ", k)),
                vjust = -0.3, size = 2.8) +
      facet_wrap(~ rq, scales = "free_x", ncol = 3) +
      scale_fill_manual(values = c(
        "RQ2: Human Oversight" = PALETTE$accent,
        "RQ3: Architecture"    = PALETTE$secondary,
        "RQ4: Learning Context" = PALETTE$success
      ), guide = "none") +
      labs(
        title = "Effect Sizes by Key Moderators (RQ2-RQ4)",
        x     = NULL,
        y     = "Hedges' g [95% CI]"
      ) +
      theme_meta() +
      theme(
        axis.text.x = element_text(angle = 30, hjust = 1, size = 9),
        strip.text  = element_text(face = "bold", size = 11)
      )

    ggsave(file.path(fig_dir, "bar_key_moderators.png"), p_bar_key,
           width = 14, height = 6, dpi = 300, bg = "white")
    ggsave(file.path(fig_dir, "bar_key_moderators.pdf"), p_bar_key,
           width = 14, height = 6)
    message("  Saved: bar_key_moderators")
  }

  # --- 4.2 Comprehensive moderator comparison (dot-and-whisker) ---
  p_all_mods <- ggplot(mod_results,
                       aes(x = g, y = reorder(level, g), color = moderator)) +
    geom_vline(xintercept = 0, linetype = "dotted", color = "grey50") +
    geom_vline(xintercept = coef(res_re), linetype = "dashed",
               color = "grey60", linewidth = 0.4) +
    geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper),
                   height = 0.3, linewidth = 0.5) +
    geom_point(size = 3) +
    facet_wrap(~ moderator, scales = "free_y", ncol = 2) +
    labs(
      title    = "Effect Sizes Across All Moderators",
      subtitle = paste0("Overall g = ", fmt(coef(res_re), 3), " (dashed line)"),
      x        = "Hedges' g [95% CI]",
      y        = NULL
    ) +
    scale_color_viridis_d(guide = "none") +
    theme_meta(base_size = 10) +
    theme(
      strip.text = element_text(face = "bold", size = 9),
      axis.text.y = element_text(size = 8)
    )

  n_panels <- length(unique(mod_results$moderator))
  ggsave(file.path(fig_dir, "all_moderators_comparison.png"), p_all_mods,
         width = 14, height = max(8, n_panels * 1.5),
         dpi = 300, bg = "white")
  message("  Saved: all_moderators_comparison")
}


# ============================================================================
# 5. HETEROGENEITY VISUALIZATION
# ============================================================================

message("\n--- 5. Heterogeneity Visualization ---\n")

# Prediction interval vs confidence interval comparison
if (!is.null(mod_results) && nrow(mod_results) > 0 &&
    "pi_lower" %in% names(mod_results)) {

  pi_plot_data <- mod_results %>%
    filter(!is.na(pi_lower), !is.na(pi_upper)) %>%
    filter(moderator %in% c("Human Oversight Level (RQ2)",
                            "Agent Architecture (RQ3)",
                            "Learning Context (RQ4)"))

  if (nrow(pi_plot_data) > 0) {
    p_pi <- ggplot(pi_plot_data, aes(y = reorder(level, g))) +
      geom_vline(xintercept = 0, linetype = "dotted", color = "grey50") +
      # Prediction interval (wider)
      geom_errorbarh(aes(xmin = pi_lower, xmax = pi_upper),
                     height = 0.15, color = "grey70", linewidth = 1.5) +
      # Confidence interval (narrower)
      geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper),
                     height = 0.3, color = PALETTE$secondary, linewidth = 0.8) +
      geom_point(aes(x = g), size = 3, color = PALETTE$primary) +
      facet_wrap(~ moderator, scales = "free_y", ncol = 1) +
      labs(
        title    = "Confidence Intervals vs. Prediction Intervals",
        subtitle = "Blue = 95% CI; Grey = 95% prediction interval",
        x        = "Hedges' g",
        y        = NULL
      ) +
      theme_meta()

    ggsave(file.path(fig_dir, "prediction_intervals.png"), p_pi,
           width = 10, height = 8, dpi = 300, bg = "white")
    message("  Saved: prediction_intervals")
  }
}


# ============================================================================
# 6. RISK-OF-BIAS SUMMARY
# ============================================================================

message("\n--- 6. Risk-of-Bias Summary ---\n")

rob_cols <- c("rob_randomization", "rob_allocation", "rob_blinding_participants",
              "rob_blinding_outcome", "rob_incomplete_data",
              "rob_selective_reporting", "rob_other")
rob_present <- intersect(rob_cols, names(dat))

if (length(rob_present) >= 3) {
  # Reshape for plotting
  rob_long <- dat %>%
    select(study_id, all_of(rob_present)) %>%
    distinct(study_id, .keep_all = TRUE) %>%
    tidyr::pivot_longer(
      cols = all_of(rob_present),
      names_to = "domain",
      values_to = "rating"
    ) %>%
    filter(!is.na(rating)) %>%
    mutate(
      domain = gsub("rob_", "", domain),
      domain = gsub("_", " ", domain),
      domain = stringr::str_to_title(domain),
      rating_label = case_when(
        rating == 0 ~ "High Risk",
        rating == 1 ~ "Some Concerns",
        rating == 2 ~ "Low Risk"
      ),
      rating_label = factor(rating_label,
                            levels = c("Low Risk", "Some Concerns", "High Risk"))
    )

  # Summary proportions
  rob_summary <- rob_long %>%
    group_by(domain, rating_label) %>%
    summarise(n = n(), .groups = "drop") %>%
    group_by(domain) %>%
    mutate(pct = n / sum(n) * 100) %>%
    ungroup()

  p_rob <- ggplot(rob_summary,
                  aes(x = pct, y = reorder(domain, -as.numeric(rating_label)),
                      fill = rating_label)) +
    geom_col(position = "stack", width = 0.7) +
    scale_fill_manual(
      values = c("Low Risk" = "#27AE60", "Some Concerns" = "#F39C12",
                 "High Risk" = "#E74C3C"),
      name = "Judgment"
    ) +
    scale_x_continuous(labels = function(x) paste0(x, "%")) +
    labs(
      title = "Risk of Bias Summary",
      x     = "Proportion of Studies",
      y     = NULL
    ) +
    theme_meta() +
    theme(legend.position = "bottom")

  ggsave(file.path(fig_dir, "risk_of_bias_summary.png"), p_rob,
         width = 10, height = 5, dpi = 300, bg = "white")
  ggsave(file.path(fig_dir, "risk_of_bias_summary.pdf"), p_rob,
         width = 10, height = 5)
  message("  Saved: risk_of_bias_summary")
} else {
  message("  Insufficient RoB data for summary figure")
}


# ============================================================================
# 7. PRISMA FLOW DIAGRAM
# ============================================================================

message("\n--- 7. PRISMA Flow Diagram ---\n")

# This creates a template PRISMA diagram. Actual numbers should be
# updated during the screening phase.

if (requireNamespace("DiagrammeR", quietly = TRUE)) {
  prisma_graph <- DiagrammeR::grViz("
  digraph PRISMA {
    graph [rankdir=TB, fontsize=11, fontname=Helvetica]
    node [shape=box, style=filled, fillcolor='#EBF5FB',
          fontname=Helvetica, fontsize=10, margin='0.3,0.15']

    # Identification
    subgraph cluster_id {
      label='IDENTIFICATION'; style=dashed; color=grey70;
      id1 [label='Records identified through\\ndatabase searching\\n(n = __)']
      id2 [label='Additional records from\\nother sources\\n(n = __)']
    }

    # Screening
    subgraph cluster_screen {
      label='SCREENING'; style=dashed; color=grey70;
      s1 [label='Records after duplicates removed\\n(n = __)']
      s2 [label='Records screened\\n(n = __)']
      s3 [label='Records excluded\\n(n = __)', fillcolor='#FADBD8']
    }

    # Eligibility
    subgraph cluster_elig {
      label='ELIGIBILITY'; style=dashed; color=grey70;
      e1 [label='Full-text articles\\nassessed for eligibility\\n(n = __)']
      e2 [label='Full-text articles excluded\\nwith reasons\\n(n = __)\\n- No comparison group (n = __)\\n- Not agentic AI (n = __)\\n- No learning outcome (n = __)\\n- Insufficient data (n = __)', fillcolor='#FADBD8']
    }

    # Included
    subgraph cluster_inc {
      label='INCLUDED'; style=dashed; color=grey70;
      i1 [label='Studies included in\\nmeta-analysis\\n(n = __)\\n(effect sizes: n = __)', fillcolor='#D5F5E3']
    }

    # Edges
    id1 -> s1
    id2 -> s1
    s1 -> s2
    s2 -> s3 [style=dashed]
    s2 -> e1
    e1 -> e2 [style=dashed]
    e1 -> i1
  }
  ")

  # Export using DiagrammeR (requires webshot or rsvg for PNG)
  tryCatch({
    prisma_html <- file.path(fig_dir, "prisma_flow.html")
    DiagrammeR::export_graph(
      DiagrammeR::from_igraph(DiagrammeR::to_igraph(prisma_graph)),
      file_name = file.path(fig_dir, "prisma_flow.png")
    )
    message("  Saved: prisma_flow")
  }, error = function(e) {
    # Fallback: save as HTML
    htmlwidgets::saveWidget(prisma_graph, prisma_html, selfcontained = TRUE)
    message("  Saved PRISMA as HTML (install webshot2 for PNG export): ", prisma_html)
  })
} else {
  message("  DiagrammeR not available. Skipping PRISMA diagram.")
  message("  Install with: install.packages('DiagrammeR')")
}


# ============================================================================
# 8. COMBINED SUMMARY FIGURE
# ============================================================================

message("\n--- 8. Combined Summary Figure ---\n")

# Create a single figure combining the three key moderator forest plots
if (!is.null(p_oversight) && !is.null(p_arch) && !is.null(p_context)) {
  if (requireNamespace("patchwork", quietly = TRUE)) {
    p_combined <- (p_oversight / p_arch / p_context) +
      patchwork::plot_annotation(
        title    = "Key Moderator Analyses (RQ2-RQ4)",
        subtitle = paste0("Overall Hedges' g = ", fmt(coef(res_re), 3),
                          " | k = ", res_re$k, " effect sizes"),
        theme    = theme(
          plot.title = element_text(face = "bold", size = 16),
          plot.subtitle = element_text(size = 12, color = "grey40")
        )
      )

    ggsave(file.path(fig_dir, "combined_moderators.png"), p_combined,
           width = 12, height = 14, dpi = 300, bg = "white")
    ggsave(file.path(fig_dir, "combined_moderators.pdf"), p_combined,
           width = 12, height = 14)
    message("  Saved: combined_moderators")
  }
}


# ============================================================================
# 9. COPY KEY FIGURES TO MANUSCRIPT DIRECTORY
# ============================================================================

message("\n--- 9. Copying Key Figures ---\n")

key_figures <- c(
  "forest_oversight.png",
  "forest_architecture.png",
  "forest_context.png",
  "bar_key_moderators.png",
  "combined_moderators.png",
  "risk_of_bias_summary.png",
  "all_moderators_comparison.png"
)

for (fig_name in key_figures) {
  src <- file.path(fig_dir, fig_name)
  dst <- file.path(PATHS$figures, fig_name)
  if (file.exists(src)) {
    file.copy(src, dst, overwrite = TRUE)
    message("  Copied: ", fig_name, " -> figures/output/")
  }
}

# List all generated figures
all_figs <- list.files(fig_dir, pattern = "\\.(png|pdf)$")
message("\nTotal figures generated: ", length(all_figs))
for (f in all_figs) {
  message("  ", f)
}

message("\n========== 07: Visualization Complete ==========\n")
