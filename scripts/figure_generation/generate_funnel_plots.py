#!/usr/bin/env python3
"""
Funnel plot generation for publication bias assessment.
Includes Egger's test and trim-and-fill method.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("matplotlib required: pip install matplotlib")


# --------------------------------------------------------------------------
# Statistical functions
# --------------------------------------------------------------------------

def random_effects_meta(g: np.ndarray, se: np.ndarray) -> Dict[str, float]:
    """DerSimonian-Laird random-effects meta-analysis."""
    k = len(g)
    if k == 0:
        return {}

    var = se ** 2
    w_fixed = 1.0 / var
    g_fixed = np.sum(w_fixed * g) / np.sum(w_fixed)
    Q = np.sum(w_fixed * (g - g_fixed) ** 2)
    c = np.sum(w_fixed) - np.sum(w_fixed ** 2) / np.sum(w_fixed)
    tau2 = max(0.0, (Q - (k - 1)) / c)

    w_re = 1.0 / (var + tau2)
    g_pooled = np.sum(w_re * g) / np.sum(w_re)
    se_pooled = np.sqrt(1.0 / np.sum(w_re))

    I2 = max(0.0, (Q - (k - 1)) / Q * 100) if Q > 0 else 0.0

    return {
        'pooled_g': g_pooled,
        'se_pooled': se_pooled,
        'ci_lower': g_pooled - 1.96 * se_pooled,
        'ci_upper': g_pooled + 1.96 * se_pooled,
        'Q': Q, 'df': k - 1, 'I2': I2, 'tau2': tau2, 'k': k
    }


def eggers_test(g: np.ndarray, se: np.ndarray) -> Dict[str, float]:
    """
    Egger's test for funnel plot asymmetry.
    Regresses standardised effect (g/se) on precision (1/se).

    Returns:
        Dictionary with intercept, se_intercept, t, p_value, interpretation
    """
    if len(g) < 5:
        return {'error': 'Need at least 5 studies for Egger test'}

    precision = 1.0 / se
    std_effect = g / se

    # WLS regression with weights = precision
    # y = a + b * x  ->  std_effect = intercept + slope * precision
    X = np.column_stack([np.ones_like(precision), precision])
    W = np.diag(precision)

    try:
        XtW = X.T @ W
        beta = np.linalg.solve(XtW @ X, XtW @ std_effect)
        intercept, slope = beta

        residuals = std_effect - (intercept + slope * precision)
        df = len(g) - 2
        mse = np.sum(precision * residuals ** 2) / df
        var_beta = mse * np.linalg.inv(XtW @ X)
        se_intercept = np.sqrt(var_beta[0, 0])

        t_stat = intercept / se_intercept

        # Two-tailed p-value approximation
        from scipy import stats as scipy_stats
        p_value = 2 * scipy_stats.t.sf(abs(t_stat), df=df)

    except Exception:
        # Fallback without scipy
        t_stat = intercept / (se_intercept if 'se_intercept' in dir() else 1)
        p_value = None

    interpretation = (
        "Significant asymmetry detected (possible publication bias)"
        if p_value is not None and p_value < 0.05
        else "No significant asymmetry detected"
    )

    return {
        'intercept': float(intercept),
        'se_intercept': float(se_intercept) if 'se_intercept' in dir() else None,
        't_statistic': float(t_stat),
        'p_value': float(p_value) if p_value is not None else None,
        'df': int(df),
        'interpretation': interpretation
    }


def trim_and_fill(g: np.ndarray, se: np.ndarray,
                  side: str = 'left',
                  max_iter: int = 20) -> Dict[str, Any]:
    """
    Duval & Tweedie trim-and-fill method for publication bias correction.

    Args:
        g: Effect size array
        se: Standard error array
        side: Which side to trim ('left' for negative bias, 'right' for positive)
        max_iter: Maximum iterations

    Returns:
        Dictionary with adjusted pooled estimate and number of imputed studies
    """
    g = np.array(g, dtype=float)
    se = np.array(se, dtype=float)
    k = len(g)

    # Iteratively estimate and remove asymmetric studies
    k0_prev = -1
    k0 = 0

    for iteration in range(max_iter):
        if k0 == k0_prev:
            break
        k0_prev = k0

        # Pool current estimate
        pooled = random_effects_meta(g, se)
        center = pooled.get('pooled_g', np.mean(g))

        # Rank deviations from center
        deviations = g - center
        if side == 'left':
            # Looking for missing studies on the left (small negative studies)
            ranks = np.argsort(deviations)  # ascending
        else:
            ranks = np.argsort(-deviations)  # descending

        # Estimator L0 (number of missing studies)
        n = len(g)
        T_n = 0
        for i in range(n):
            rank = np.where(ranks == i)[0][0]
            sign = np.sign(deviations[i])
            if (side == 'left' and sign < 0) or (side == 'right' and sign > 0):
                T_n += (rank + 1)

        k0 = max(0, round((4 * T_n - n * (n + 1)) / (2 * n - 1)))

        if k0 >= k:
            k0 = max(0, k - 1)
            break

    # Impute missing studies
    if k0 > 0:
        pooled_all = random_effects_meta(g, se)
        center = pooled_all.get('pooled_g', np.mean(g))

        # Add mirror-image studies
        if side == 'left':
            sorted_g = np.sort(g)[::-1][:k0]
            imputed_g = 2 * center - sorted_g
        else:
            sorted_g = np.sort(g)[:k0]
            imputed_g = 2 * center - sorted_g

        imputed_se = se[np.argsort(np.abs(g - center))][:k0]

        g_adj = np.concatenate([g, imputed_g])
        se_adj = np.concatenate([se, imputed_se])
        adjusted = random_effects_meta(g_adj, se_adj)
    else:
        adjusted = random_effects_meta(g, se)

    return {
        'k0_imputed': int(k0),
        'adjusted_pooled_g': adjusted.get('pooled_g'),
        'adjusted_ci_lower': adjusted.get('ci_lower'),
        'adjusted_ci_upper': adjusted.get('ci_upper'),
        'adjusted_se': adjusted.get('se_pooled'),
        'converged': k0 == k0_prev
    }


# --------------------------------------------------------------------------
# Funnel plot
# --------------------------------------------------------------------------

class FunnelPlotter:
    """Creates publication-quality funnel plots with Egger's test annotation."""

    COLOURS = {
        'study_dot':   '#2980B9',
        'pseudo_ci':   '#BDC3C7',
        'pooled_line': '#E74C3C',
        'imputed':     '#E67E22',
        'background':  '#FDFEFE'
    }

    def plot(self, g: np.ndarray, se: np.ndarray,
             output_path: str,
             title: str = "Funnel Plot",
             run_egger: bool = True,
             run_trim_fill: bool = True):
        """
        Generate a funnel plot with optional Egger's test and trim-and-fill.

        Args:
            g: Array of Hedges' g values
            se: Array of standard errors
            output_path: Output file path
            title: Plot title
            run_egger: Whether to compute and display Egger's test
            run_trim_fill: Whether to run trim-and-fill and show imputed studies
        """
        pooled = random_effects_meta(g, se)
        if not pooled:
            logger.warning("Insufficient data for funnel plot")
            return

        egger = eggers_test(g, se) if run_egger else {}
        trim_fill_result = trim_and_fill(g, se) if run_trim_fill else {}

        fig, ax = plt.subplots(figsize=(8, 7))
        ax.set_facecolor(self.COLOURS['background'])
        fig.patch.set_facecolor('white')

        # Pseudo-confidence region (inverted funnel)
        se_range = np.linspace(0, max(se) * 1.1, 200)
        center = pooled['pooled_g']
        ci_lo = center - 1.96 * se_range
        ci_hi = center + 1.96 * se_range

        ax.fill_betweenx(se_range, ci_lo, ci_hi,
                         alpha=0.12, color=self.COLOURS['pseudo_ci'],
                         label='95% pseudo-CI')
        ax.plot(ci_lo, se_range, '--', color=self.COLOURS['pseudo_ci'], lw=1)
        ax.plot(ci_hi, se_range, '--', color=self.COLOURS['pseudo_ci'], lw=1)

        # Pooled estimate vertical line
        ax.axvline(x=center, color=self.COLOURS['pooled_line'],
                   linewidth=1.5, linestyle='-', label=f"Pooled g = {center:.2f}")

        # Zero line
        ax.axvline(x=0, color='#7F8C8D', linewidth=1.0,
                   linestyle=':', label='g = 0')

        # Plot observed studies
        ax.scatter(g, se, s=50, color=self.COLOURS['study_dot'],
                   alpha=0.75, zorder=3, label=f"Observed (k={len(g)})")

        # Trim-and-fill imputed studies
        if run_trim_fill and trim_fill_result.get('k0_imputed', 0) > 0:
            k0 = trim_fill_result['k0_imputed']
            adj_g = trim_fill_result['adjusted_pooled_g']

            sorted_g = np.sort(g)[::-1][:k0]
            imputed_g_vals = 2 * adj_g - sorted_g
            imputed_se_vals = se[np.argsort(np.abs(g - center))][:k0]

            ax.scatter(imputed_g_vals, imputed_se_vals, s=50,
                       color=self.COLOURS['imputed'], alpha=0.75,
                       marker='D', zorder=3,
                       label=f"Imputed (trim-fill, k={k0})")

            if adj_g is not None:
                ax.axvline(x=adj_g, color=self.COLOURS['imputed'],
                           linewidth=1.2, linestyle='--',
                           label=f"Adjusted g = {adj_g:.2f}")

        ax.set_xlabel("Hedges' g", fontsize=11)
        ax.set_ylabel("Standard Error (SE)", fontsize=11)
        ax.invert_yaxis()
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
        ax.legend(fontsize=8, loc='lower left')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Annotation: Egger's test result
        if egger and 'p_value' in egger and egger['p_value'] is not None:
            egger_text = (
                f"Egger's test: b = {egger['intercept']:.2f}, "
                f"p = {egger['p_value']:.3f}"
            )
            ax.text(0.98, 0.02, egger_text, transform=ax.transAxes,
                    ha='right', va='bottom', fontsize=8.5,
                    color='#E74C3C' if egger['p_value'] < 0.05 else '#2C3E50',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor='#BDC3C7', alpha=0.8))

        # Annotation: I² and tau²
        stats_text = (
            f"I² = {pooled['I2']:.0f}%  τ² = {pooled['tau2']:.3f}  "
            f"Q({pooled['df']}) = {pooled['Q']:.1f}"
        )
        ax.text(0.02, 0.02, stats_text, transform=ax.transAxes,
                ha='left', va='bottom', fontsize=8,
                color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='#BDC3C7', alpha=0.8))

        plt.tight_layout()
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        logger.info(f"Funnel plot saved: {output}")


def generate_funnel_plots(data_path: str,
                          output_dir: str = "figures/funnel_plots",
                          g_col: str = "hedges_g",
                          se_col: str = "se_g"):
    """
    Generate funnel plots from the final dataset.

    Args:
        data_path: Path to final CSV dataset
        output_dir: Directory to save funnel plot figures
        g_col: Column name for Hedges' g
        se_col: Column name for standard error
    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

    df = pd.read_csv(data_path)
    df = df.dropna(subset=[g_col, se_col])

    logger.info(f"Loaded {len(df)} effect sizes")

    plotter = FunnelPlotter()
    output = Path(output_dir)

    # Overall funnel plot
    plotter.plot(
        df[g_col].values, df[se_col].values,
        output_path=str(output / 'funnel_overall.png'),
        title="Funnel Plot — Overall Effect of Agentic AI on Learning Outcomes",
        run_egger=True, run_trim_fill=True
    )

    # Subgroup funnel plots
    subgroup_vars = ['oversight_level', 'education_level', 'technology']
    for var in subgroup_vars:
        if var in df.columns:
            for group in df[var].dropna().unique():
                sg_df = df[df[var] == group]
                if len(sg_df) >= 5:
                    plotter.plot(
                        sg_df[g_col].values, sg_df[se_col].values,
                        output_path=str(output / f'funnel_{var}_{group}.png'),
                        title=f"Funnel Plot — {var}: {group}",
                        run_egger=True, run_trim_fill=False
                    )

    print(f"\nFunnel plots saved to: {output}")

    # Run and print Egger's test results
    egger = eggers_test(df[g_col].values, df[se_col].values)
    tf = trim_and_fill(df[g_col].values, df[se_col].values)

    print("\nPublication Bias Assessment:")
    print(f"  Egger's test: b = {egger.get('intercept', 'N/A'):.3f}, "
          f"p = {egger.get('p_value', 'N/A')}")
    print(f"  {egger.get('interpretation', '')}")
    print(f"  Trim-and-fill: {tf.get('k0_imputed', 0)} studies imputed, "
          f"adjusted g = {tf.get('adjusted_pooled_g', 'N/A'):.3f}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate funnel plots for publication bias assessment"
    )
    parser.add_argument('--data', required=True,
                        help='Path to final CSV dataset')
    parser.add_argument('--output', default='figures/funnel_plots',
                        help='Output directory')

    args = parser.parse_args()
    generate_funnel_plots(args.data, args.output)
