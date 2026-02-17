#!/usr/bin/env python3
"""
Forest plot generation for meta-analysis of agentic AI effects on learning outcomes.
Generates overall and subgroup forest plots using Hedges' g.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.lines import Line2D
except ImportError:
    raise ImportError("matplotlib required: pip install matplotlib")


# --------------------------------------------------------------------------
# Meta-analysis utilities
# --------------------------------------------------------------------------

def random_effects_meta(g_values: np.ndarray, se_values: np.ndarray,
                        method: str = 'DL') -> Dict[str, float]:
    """
    Random-effects meta-analysis using DerSimonian-Laird (DL) method.

    Args:
        g_values: Array of Hedges' g values
        se_values: Array of standard errors
        method: Method for tau^2 estimation ('DL' only for now)

    Returns:
        Dictionary with pooled_g, se_pooled, ci_lower, ci_upper, Q, I2, tau2
    """
    k = len(g_values)
    if k == 0:
        return {}

    var_values = se_values ** 2
    w_fixed = 1.0 / var_values

    # Fixed-effects estimate
    g_fixed = np.sum(w_fixed * g_values) / np.sum(w_fixed)

    # Q statistic
    Q = np.sum(w_fixed * (g_values - g_fixed) ** 2)

    # DerSimonian-Laird tau^2
    c = np.sum(w_fixed) - np.sum(w_fixed ** 2) / np.sum(w_fixed)
    tau2 = max(0.0, (Q - (k - 1)) / c)

    # Random-effects weights
    w_random = 1.0 / (var_values + tau2)
    g_pooled = np.sum(w_random * g_values) / np.sum(w_random)
    se_pooled = np.sqrt(1.0 / np.sum(w_random))

    ci_lower = g_pooled - 1.96 * se_pooled
    ci_upper = g_pooled + 1.96 * se_pooled

    # I² heterogeneity
    I2 = max(0.0, (Q - (k - 1)) / Q * 100) if Q > 0 else 0.0

    return {
        'pooled_g': g_pooled,
        'se_pooled': se_pooled,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'Q': Q,
        'df': k - 1,
        'p_Q': 1 - float(np.exp(-0.5 * max(0, Q - (k - 1)))),  # approximate
        'I2': I2,
        'tau2': tau2,
        'tau': np.sqrt(tau2),
        'k': k
    }


# --------------------------------------------------------------------------
# Forest plot
# --------------------------------------------------------------------------

class ForestPlotter:
    """Creates publication-quality forest plots for meta-analysis results."""

    COLOURS = {
        'study_dot':     '#2980B9',
        'pooled_diamond':'#E74C3C',
        'ci_line':       '#2C3E50',
        'zero_line':     '#7F8C8D',
        'subgroup_header':'#1A252F',
        'grid':          '#ECF0F1',
        'text':          '#2C3E50'
    }

    def __init__(self, figsize: Tuple[float, float] = (12, None)):
        self.figsize_width = figsize[0]

    def plot_overall(self, df: pd.DataFrame,
                     output_path: str,
                     study_col: str = 'study_id',
                     g_col: str = 'hedges_g',
                     se_col: str = 'se_g',
                     label_col: Optional[str] = None,
                     title: str = "Forest Plot — Overall Effect"):
        """
        Generate an overall forest plot.

        Args:
            df: DataFrame with one row per effect size
            output_path: Output file path
            study_col: Column name for study identifier
            g_col: Column name for Hedges' g
            se_col: Column name for standard error
            label_col: Optional column for custom row labels
            title: Plot title
        """
        df = df.dropna(subset=[g_col, se_col]).copy()
        df = df.sort_values(g_col, ascending=True).reset_index(drop=True)

        g = df[g_col].values
        se = df[se_col].values
        labels = df[label_col].values if label_col else df[study_col].values

        pooled = random_effects_meta(g, se)

        n_rows = len(df) + 4  # extra rows for header, spacer, pooled, footer
        fig_height = max(6, n_rows * 0.35)
        fig, ax = plt.subplots(figsize=(self.figsize_width, fig_height))

        self._draw_forest(ax, labels, g, se, pooled, title)

        plt.tight_layout()
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        logger.info(f"Forest plot saved: {output}")

    def plot_subgroup(self, df: pd.DataFrame,
                      subgroup_col: str,
                      output_path: str,
                      study_col: str = 'study_id',
                      g_col: str = 'hedges_g',
                      se_col: str = 'se_g',
                      title: str = "Forest Plot — Subgroup Analysis"):
        """
        Generate a subgroup forest plot.

        Args:
            df: DataFrame with effect sizes
            subgroup_col: Column name defining subgroups
            output_path: Output file path
            study_col: Study identifier column
            g_col: Hedges' g column
            se_col: Standard error column
            title: Plot title
        """
        df = df.dropna(subset=[g_col, se_col]).copy()

        subgroups = sorted(df[subgroup_col].dropna().unique())
        n_rows = len(df) + len(subgroups) * 3 + 4
        fig_height = max(8, n_rows * 0.32)

        fig, ax = plt.subplots(figsize=(self.figsize_width, fig_height))
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')

        row = 0
        all_g = df[g_col].values
        x_min = min(all_g) - 1.0
        x_max = max(all_g) + 1.0

        ax.axvline(x=0, color=self.COLOURS['zero_line'], linestyle='--',
                   linewidth=1.0, zorder=1)

        y_labels = []
        y_positions = []

        for sg in subgroups:
            sg_df = df[df[subgroup_col] == sg].sort_values(g_col).reset_index(drop=True)
            sg_g = sg_df[g_col].values
            sg_se = sg_df[se_col].values

            # Subgroup header
            ax.text(x_min - 0.05, row, f"▶ {sg}",
                    ha='right', va='center', fontsize=9.5, fontweight='bold',
                    color=self.COLOURS['subgroup_header'])
            row += 1

            # Individual studies
            for _, study_row in sg_df.iterrows():
                g_val = study_row[g_col]
                se_val = study_row[se_col]
                ci_lo = g_val - 1.96 * se_val
                ci_hi = g_val + 1.96 * se_val
                weight = 1 / (se_val ** 2)

                ax.plot([ci_lo, ci_hi], [row, row], '-',
                        color=self.COLOURS['ci_line'], lw=1.2, zorder=2)
                ax.scatter([g_val], [row],
                           s=max(20, min(120, weight * 0.5)),
                           color=self.COLOURS['study_dot'], zorder=3)

                y_labels.append(study_row[study_col])
                y_positions.append(row)

                ax.text(x_max + 0.05, row,
                        f"{g_val:.2f} [{ci_lo:.2f}, {ci_hi:.2f}]",
                        ha='left', va='center', fontsize=7.5,
                        color=self.COLOURS['text'])
                row += 1

            # Subgroup pooled
            if len(sg_g) >= 2:
                sg_pooled = random_effects_meta(sg_g, sg_se)
                d = sg_pooled['pooled_g']
                ci_lo_p = sg_pooled['ci_lower']
                ci_hi_p = sg_pooled['ci_upper']
                self._draw_diamond(ax, d, row, ci_lo_p, ci_hi_p, 0.25,
                                   color=self.COLOURS['pooled_diamond'])
                ax.text(x_max + 0.05, row,
                        f"Pooled: {d:.2f} [{ci_lo_p:.2f}, {ci_hi_p:.2f}] "
                        f"(I²={sg_pooled['I2']:.0f}%)",
                        ha='left', va='center', fontsize=8,
                        fontweight='bold', color=self.COLOURS['pooled_diamond'])
            row += 2

        # Overall pooled
        overall = random_effects_meta(all_g, df[se_col].values)
        if overall:
            ax.axhline(y=row - 0.5, color='#BDC3C7', lw=0.8, linestyle='-')
            d = overall['pooled_g']
            self._draw_diamond(ax, d, row, overall['ci_lower'], overall['ci_upper'], 0.35)
            ax.text(x_max + 0.05, row,
                    f"Overall: {d:.2f} [{overall['ci_lower']:.2f}, "
                    f"{overall['ci_upper']:.2f}] (I²={overall['I2']:.0f}%)",
                    ha='left', va='center', fontsize=9, fontweight='bold',
                    color=self.COLOURS['pooled_diamond'])

        ax.set_yticks(y_positions)
        ax.set_yticklabels(y_labels, fontsize=7.5)
        ax.set_ylim(-1, row + 1)
        ax.set_xlim(x_min - 0.5, x_max + 2.5)
        ax.set_xlabel("Hedges' g", fontsize=10)
        ax.set_title(title, fontsize=11, fontweight='bold', pad=12)
        ax.grid(axis='x', color=self.COLOURS['grid'], linewidth=0.6)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        logger.info(f"Subgroup forest plot saved: {output}")

    def _draw_forest(self, ax, labels, g, se, pooled, title):
        """Draw the main forest plot content on an axis."""
        n = len(g)
        x_min = min(g - 1.96 * se) - 0.5
        x_max = max(g + 1.96 * se) + 0.5

        ax.set_facecolor('white')
        ax.axvline(x=0, color=self.COLOURS['zero_line'], linestyle='--',
                   linewidth=1.0, zorder=1)

        for i in range(n):
            ci_lo = g[i] - 1.96 * se[i]
            ci_hi = g[i] + 1.96 * se[i]
            weight = 1 / (se[i] ** 2)

            ax.plot([ci_lo, ci_hi], [i, i], '-',
                    color=self.COLOURS['ci_line'], lw=1.2, zorder=2)
            ax.scatter([g[i]], [i],
                       s=max(20, min(150, weight * 0.6)),
                       color=self.COLOURS['study_dot'], zorder=3)
            ax.text(x_max + 0.05, i,
                    f"{g[i]:.2f} [{ci_lo:.2f}, {ci_hi:.2f}]",
                    ha='left', va='center', fontsize=7.5,
                    color=self.COLOURS['text'])

        # Pooled diamond
        if pooled:
            pool_y = -1.5
            self._draw_diamond(ax, pooled['pooled_g'], pool_y,
                               pooled['ci_lower'], pooled['ci_upper'], 0.35)
            ax.text(x_max + 0.05, pool_y,
                    f"Pooled: {pooled['pooled_g']:.2f} "
                    f"[{pooled['ci_lower']:.2f}, {pooled['ci_upper']:.2f}]\n"
                    f"k={pooled['k']}, I²={pooled['I2']:.0f}%, "
                    f"τ²={pooled['tau2']:.3f}",
                    ha='left', va='center', fontsize=8.5,
                    fontweight='bold', color=self.COLOURS['pooled_diamond'])

        ax.set_yticks(range(n))
        ax.set_yticklabels(labels, fontsize=7.5)
        ax.set_ylim(-2.5, n)
        ax.set_xlim(x_min, x_max + 2.5)
        ax.set_xlabel("Hedges' g", fontsize=10)
        ax.set_title(title, fontsize=11, fontweight='bold', pad=12)
        ax.grid(axis='x', color=self.COLOURS['grid'], linewidth=0.6)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    def _draw_diamond(self, ax, x_center: float, y: float,
                      ci_lo: float, ci_hi: float, height: float = 0.3,
                      color: str = None):
        """Draw a pooled-effect diamond on the axes."""
        if color is None:
            color = self.COLOURS['pooled_diamond']
        diamond_x = [ci_lo, x_center, ci_hi, x_center, ci_lo]
        diamond_y = [y, y + height, y, y - height, y]
        ax.fill(diamond_x, diamond_y, color=color, zorder=3, alpha=0.85)
        ax.plot(diamond_x, diamond_y, '-', color=color, lw=1.2, zorder=4)


def generate_forest_plots(data_path: str,
                          output_dir: str = "figures/forest_plots",
                          g_col: str = "hedges_g",
                          se_col: str = "se_g",
                          study_col: str = "study_id"):
    """
    Generate all forest plots from the final dataset.

    Args:
        data_path: Path to final CSV dataset
        output_dir: Directory to save forest plot figures
        g_col: Column name for Hedges' g
        se_col: Column name for standard error
        study_col: Column name for study identifier
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    df = pd.read_csv(data_path)
    df = df.dropna(subset=[g_col, se_col])

    logger.info(f"Loaded {len(df)} effect sizes from {data_path}")

    plotter = ForestPlotter(figsize=(13, None))
    output = Path(output_dir)

    # Overall forest plot
    plotter.plot_overall(
        df, str(output / 'forest_overall.png'),
        study_col=study_col, g_col=g_col, se_col=se_col,
        title="Forest Plot — Overall Effect of Agentic AI on Learning Outcomes"
    )

    # Subgroup plots
    subgroup_vars = ['oversight_level', 'architecture', 'agency_level',
                     'agent_role', 'modality', 'technology', 'adaptivity',
                     'education_level', 'learning_domain']

    for var in subgroup_vars:
        if var in df.columns and df[var].notna().sum() > 3:
            plotter.plot_subgroup(
                df, subgroup_col=var,
                output_path=str(output / f'forest_subgroup_{var}.png'),
                study_col=study_col, g_col=g_col, se_col=se_col,
                title=f"Forest Plot — Subgroup: {var.replace('_', ' ').title()}"
            )

    print(f"\nForest plots saved to: {output}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate forest plots for meta-analysis"
    )
    parser.add_argument('--data', required=True,
                        help='Path to final CSV dataset')
    parser.add_argument('--output', default='figures/forest_plots',
                        help='Output directory')

    args = parser.parse_args()
    generate_forest_plots(args.data, args.output)
