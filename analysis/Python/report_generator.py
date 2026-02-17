#!/usr/bin/env python3
"""
Analysis report generator for the agentic AI learning outcomes meta-analysis.
Produces a comprehensive HTML and text report from the validated dataset.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Meta-analysis functions (self-contained, no external deps beyond numpy/pandas)
# --------------------------------------------------------------------------

def random_effects_meta(g: np.ndarray, se: np.ndarray) -> Dict[str, Any]:
    """DerSimonian-Laird random-effects meta-analysis."""
    k = len(g)
    if k == 0:
        return {'error': 'No data'}

    var = se ** 2
    w_fixed = 1.0 / var
    g_fixed = np.sum(w_fixed * g) / np.sum(w_fixed)
    Q = float(np.sum(w_fixed * (g - g_fixed) ** 2))
    c = float(np.sum(w_fixed) - np.sum(w_fixed ** 2) / np.sum(w_fixed))
    tau2 = max(0.0, (Q - (k - 1)) / c)

    w_re = 1.0 / (var + tau2)
    g_pooled = float(np.sum(w_re * g) / np.sum(w_re))
    se_pooled = float(np.sqrt(1.0 / np.sum(w_re)))

    I2 = max(0.0, (Q - (k - 1)) / Q * 100) if Q > 0 else 0.0

    try:
        from scipy.stats import chi2, norm
        p_Q = float(chi2.sf(Q, k - 1))
        z = g_pooled / se_pooled
        p_pooled = float(2 * norm.sf(abs(z)))
    except ImportError:
        p_Q = float(np.exp(-0.5 * max(0, Q - (k - 1))))
        p_pooled = None

    return {
        'k': k,
        'g_pooled': round(g_pooled, 4),
        'se_pooled': round(se_pooled, 4),
        'ci_lower': round(g_pooled - 1.96 * se_pooled, 4),
        'ci_upper': round(g_pooled + 1.96 * se_pooled, 4),
        'p_pooled': round(p_pooled, 4) if p_pooled is not None else None,
        'Q': round(Q, 3),
        'df_Q': k - 1,
        'p_Q': round(p_Q, 4),
        'I2': round(I2, 1),
        'tau2': round(tau2, 4),
        'tau': round(float(np.sqrt(tau2)), 4),
        'pi_lower': round(g_pooled - 1.96 * float(np.sqrt(se_pooled**2 + tau2)), 3),
        'pi_upper': round(g_pooled + 1.96 * float(np.sqrt(se_pooled**2 + tau2)), 3)
    }


def subgroup_analysis(df: pd.DataFrame,
                      subgroup_col: str,
                      g_col: str = 'hedges_g',
                      se_col: str = 'se_g') -> Dict[str, Any]:
    """
    Run random-effects meta-analysis within each subgroup.

    Args:
        df: DataFrame with effect size data
        subgroup_col: Column defining subgroups
        g_col: Hedges' g column
        se_col: Standard error column

    Returns:
        Dictionary of subgroup results
    """
    results = {}
    df_clean = df.dropna(subset=[g_col, se_col, subgroup_col])

    for group in sorted(df_clean[subgroup_col].unique()):
        sg = df_clean[df_clean[subgroup_col] == group]
        if len(sg) < 2:
            continue
        meta = random_effects_meta(
            sg[g_col].values.astype(float),
            sg[se_col].values.astype(float)
        )
        results[str(group)] = meta

    return results


# --------------------------------------------------------------------------
# Report sections
# --------------------------------------------------------------------------

class ReportGenerator:
    """Generates a comprehensive meta-analysis report."""

    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)
        self.df = self.df.dropna(subset=['hedges_g', 'se_g'])
        self.g = self.df['hedges_g'].values.astype(float)
        self.se = self.df['se_g'].values.astype(float)
        self.overall = random_effects_meta(self.g, self.se)
        self.timestamp = datetime.now()

    def section_overview(self) -> Dict[str, Any]:
        """Generate dataset overview statistics."""
        df = self.df
        return {
            'n_studies': int(df['study_id'].nunique()),
            'n_effect_sizes': len(df),
            'year_range': [
                int(df['year_published'].min()) if 'year_published' in df.columns
                    and df['year_published'].notna().any() else 'N/A',
                int(df['year_published'].max()) if 'year_published' in df.columns
                    and df['year_published'].notna().any() else 'N/A'
            ],
            'education_level_counts': (
                df.drop_duplicates('study_id')['education_level'].value_counts().to_dict()
                if 'education_level' in df.columns else {}
            ),
            'technology_counts': (
                df.drop_duplicates('study_id')['technology'].value_counts().to_dict()
                if 'technology' in df.columns else {}
            ),
            'oversight_level_counts': (
                df.drop_duplicates('study_id')['oversight_level'].value_counts().to_dict()
                if 'oversight_level' in df.columns else {}
            ),
            'design_type_counts': (
                df.drop_duplicates('study_id')['design_type'].value_counts().to_dict()
                if 'design_type' in df.columns else {}
            )
        }

    def section_subgroups(self) -> Dict[str, Dict[str, Any]]:
        """Run subgroup analyses for all moderator variables."""
        moderators = [
            'oversight_level', 'architecture', 'agency_level',
            'agent_role', 'modality', 'technology', 'adaptivity',
            'education_level', 'learning_domain', 'design_type'
        ]

        results = {}
        for mod in moderators:
            if mod in self.df.columns and self.df[mod].notna().sum() >= 4:
                results[mod] = subgroup_analysis(self.df, mod)

        return results

    def section_effect_size_distribution(self) -> Dict[str, Any]:
        """Describe the distribution of effect sizes."""
        g = self.g
        return {
            'mean_g': round(float(np.mean(g)), 3),
            'median_g': round(float(np.median(g)), 3),
            'sd_g': round(float(np.std(g)), 3),
            'min_g': round(float(np.min(g)), 3),
            'max_g': round(float(np.max(g)), 3),
            'q25': round(float(np.percentile(g, 25)), 3),
            'q75': round(float(np.percentile(g, 75)), 3),
            'n_positive': int(np.sum(g > 0)),
            'n_negative': int(np.sum(g < 0)),
            'n_zero': int(np.sum(g == 0)),
            'pct_positive': round(float(np.sum(g > 0) / len(g) * 100), 1)
        }

    def generate_text_report(self) -> str:
        """Generate a plain-text summary report."""
        ov = self.section_overview()
        dist = self.section_effect_size_distribution()
        meta = self.overall

        lines = [
            "=" * 70,
            "EFFECTS OF AGENTIC AI ON LEARNING OUTCOMES — META-ANALYSIS REPORT",
            f"Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M')}",
            "=" * 70,
            "",
            "1. DATASET OVERVIEW",
            "-" * 40,
            f"   Studies included:     {ov['n_studies']}",
            f"   Effect sizes:         {ov['n_effect_sizes']}",
            f"   Year range:           {ov['year_range'][0]} – {ov['year_range'][1]}",
            "",
            "   Education levels:",
        ]
        for level, n in ov.get('education_level_counts', {}).items():
            lines.append(f"     {level:<35} {n}")

        lines += [
            "",
            "   AI technology types:",
        ]
        for tech, n in ov.get('technology_counts', {}).items():
            lines.append(f"     {tech:<35} {n}")

        lines += [
            "",
            "2. OVERALL META-ANALYTIC RESULT",
            "-" * 40,
            f"   k (effect sizes):     {meta.get('k')}",
            f"   Hedges' g (pooled):   {meta.get('g_pooled')} "
            f"[{meta.get('ci_lower')}, {meta.get('ci_upper')}]",
            f"   SE:                   {meta.get('se_pooled')}",
            f"   p-value:              {meta.get('p_pooled', 'N/A')}",
            f"   95% prediction int.:  [{meta.get('pi_lower')}, {meta.get('pi_upper')}]",
            "",
            "   Heterogeneity:",
            f"     Q({meta.get('df_Q')}) = {meta.get('Q')}, p = {meta.get('p_Q')}",
            f"     I² = {meta.get('I2')}%",
            f"     τ² = {meta.get('tau2')}, τ = {meta.get('tau')}",
            "",
            "3. EFFECT SIZE DISTRIBUTION",
            "-" * 40,
            f"   Mean g:    {dist['mean_g']}",
            f"   Median g:  {dist['median_g']}",
            f"   SD:        {dist['sd_g']}",
            f"   Range:     [{dist['min_g']}, {dist['max_g']}]",
            f"   IQR:       [{dist['q25']}, {dist['q75']}]",
            f"   % Positive effects: {dist['pct_positive']}%",
            "",
            "4. SUBGROUP ANALYSES",
            "-" * 40,
        ]

        subgroups = self.section_subgroups()
        for moderator, groups in subgroups.items():
            lines.append(f"\n   Moderator: {moderator}")
            lines.append(f"   {'Group':<35} {'k':>4} {'g':>7} {'95% CI':>22} {'I²':>8}")
            lines.append(f"   {'-'*35} {'-'*4} {'-'*7} {'-'*22} {'-'*8}")
            for group, result in groups.items():
                ci_str = f"[{result['ci_lower']}, {result['ci_upper']}]"
                lines.append(
                    f"   {group:<35} {result['k']:>4} {result['g_pooled']:>7.3f} "
                    f"{ci_str:>22} {result['I2']:>7.1f}%"
                )

        lines += [
            "",
            "=" * 70,
            "END OF REPORT",
            "=" * 70
        ]

        return '\n'.join(lines)

    def generate_json_report(self) -> Dict[str, Any]:
        """Generate full JSON report with all analyses."""
        return {
            'report_metadata': {
                'title': 'Effects of Agentic AI on Learning Outcomes — Meta-Analysis Report',
                'generated_at': self.timestamp.isoformat(),
                'n_effect_sizes': len(self.df)
            },
            'dataset_overview': self.section_overview(),
            'effect_size_distribution': self.section_effect_size_distribution(),
            'overall_meta_analysis': self.overall,
            'subgroup_analyses': self.section_subgroups()
        }

    def generate_html_report(self) -> str:
        """Generate a minimal HTML report for browser viewing."""
        json_data = self.generate_json_report()
        text = self.generate_text_report()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Agentic AI Learning Outcomes Meta-Analysis Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; color: #2c3e50; }}
    h1 {{ color: #2980b9; }}
    h2 {{ color: #27ae60; border-bottom: 2px solid #27ae60; padding-bottom: 4px; }}
    pre {{ background: #f8f9fa; padding: 16px; border-radius: 6px; overflow-x: auto; font-size: 13px; }}
    .stat {{ background: #eaf4fb; border-left: 4px solid #2980b9; padding: 8px 14px; margin: 6px 0; }}
    .warning {{ background: #fef9e7; border-left: 4px solid #e67e22; padding: 8px 14px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th {{ background: #2980b9; color: white; padding: 8px; }}
    td {{ padding: 7px 10px; border-bottom: 1px solid #ecf0f1; }}
    tr:hover {{ background: #eaf4fb; }}
  </style>
</head>
<body>
  <h1>Agentic AI Learning Outcomes — Meta-Analysis Report</h1>
  <p>Generated: {self.timestamp.strftime('%Y-%m-%d %H:%M')}</p>

  <h2>Overall Meta-Analytic Result</h2>
  <div class="stat">
    <strong>Hedges' g (pooled) = {self.overall.get('g_pooled')}</strong>
    95% CI [{self.overall.get('ci_lower')}, {self.overall.get('ci_upper')}]
    | k = {self.overall.get('k')}
    | I² = {self.overall.get('I2')}%
    | τ² = {self.overall.get('tau2')}
  </div>

  <h2>Full Text Report</h2>
  <pre>{text}</pre>

  <h2>Raw JSON Data</h2>
  <pre>{json.dumps(json_data, indent=2)}</pre>
</body>
</html>"""
        return html


def generate_report(data_path: str,
                    output_dir: str = "reports",
                    formats: List[str] = None):
    """
    Generate analysis report in multiple formats.

    Args:
        data_path: Path to cleaned/validated dataset CSV
        output_dir: Directory to save report files
        formats: List of formats to generate: 'txt', 'json', 'html'
                 Defaults to all three.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if formats is None:
        formats = ['txt', 'json', 'html']

    gen = ReportGenerator(data_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')

    if 'txt' in formats:
        txt_path = output / f'meta_analysis_report_{timestamp_str}.txt'
        txt = gen.generate_text_report()
        with open(txt_path, 'w') as f:
            f.write(txt)
        print(txt)
        logger.info(f"Text report saved: {txt_path}")

    if 'json' in formats:
        json_path = output / f'meta_analysis_report_{timestamp_str}.json'
        json_data = gen.generate_json_report()
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=2, default=str)
        logger.info(f"JSON report saved: {json_path}")

    if 'html' in formats:
        html_path = output / f'meta_analysis_report_{timestamp_str}.html'
        html = gen.generate_html_report()
        with open(html_path, 'w') as f:
            f.write(html)
        logger.info(f"HTML report saved: {html_path}")

    print(f"\nReports saved to: {output}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate meta-analysis report from validated dataset"
    )
    parser.add_argument('--data', required=True,
                        help='Path to cleaned/validated dataset CSV')
    parser.add_argument('--output', default='reports',
                        help='Output directory for reports')
    parser.add_argument('--format', nargs='+', default=['txt', 'json', 'html'],
                        choices=['txt', 'json', 'html'],
                        help='Output format(s): txt json html')

    args = parser.parse_args()
    generate_report(args.data, args.output, args.format)
