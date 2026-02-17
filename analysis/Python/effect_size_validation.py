#!/usr/bin/env python3
"""
Effect size validation for the agentic AI learning outcomes meta-analysis.
Validates Hedges' g values, checks for consistency, and runs heterogeneity analyses.
Replaces matrix_validation.py from the source MASEM repo.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Core statistical validation
# --------------------------------------------------------------------------

def validate_effect_size_range(g: float, max_g: float = 5.0) -> Tuple[bool, str]:
    """Check that |g| is within a plausible range."""
    if np.isnan(g):
        return False, "Value is NaN"
    if abs(g) > max_g:
        return False, f"|g| = {abs(g):.3f} exceeds maximum {max_g}"
    return True, "OK"


def validate_standard_error(se: float, n1: int, n2: int) -> Tuple[bool, str]:
    """
    Check that the SE is consistent with the sample sizes.
    SE for Hedges' g is approximately sqrt(2/n_total).
    """
    if np.isnan(se) or se <= 0:
        return False, f"SE = {se} is invalid (must be positive)"

    n_total = n1 + n2
    expected_min = np.sqrt(2.0 / (n_total * 2))  # very small se allowed
    expected_max = np.sqrt(8.0 / max(n1, n2))    # generous upper bound

    if se > expected_max * 2:
        return False, (
            f"SE = {se:.4f} seems too large for n1={n1}, n2={n2} "
            f"(expected max ~{expected_max:.4f})"
        )

    return True, "OK"


def validate_sample_sizes(n1: Optional[int], n2: Optional[int],
                           min_n: int = 10) -> Tuple[bool, str]:
    """Check sample sizes meet minimum threshold."""
    issues = []
    if n1 is not None and n1 < min_n:
        issues.append(f"n_treatment = {n1} < {min_n}")
    if n2 is not None and n2 < min_n:
        issues.append(f"n_control = {n2} < {min_n}")
    if issues:
        return False, "; ".join(issues)
    return True, "OK"


def check_sign_consistency(g: float, m_treatment: Optional[float],
                            m_control: Optional[float]) -> Tuple[bool, str]:
    """
    Check that sign of g is consistent with raw means if available.
    g = (m_treatment - m_control) / pooled_sd, so positive g should have m_treatment > m_control.
    """
    if m_treatment is None or m_control is None or np.isnan(g):
        return True, "Cannot check (raw means not available)"

    expected_positive = m_treatment > m_control
    g_positive = g > 0

    if expected_positive != g_positive and abs(g) > 0.01:
        return False, (
            f"Sign inconsistency: g = {g:.3f} but m_treatment ({m_treatment}) "
            f"{'>' if m_treatment > m_control else '<'} m_control ({m_control})"
        )

    return True, "OK"


def check_ci_plausibility(g: float, se: float,
                           p_reported: Optional[float] = None) -> Dict[str, Any]:
    """
    Check that confidence interval is plausible.
    If p-value is reported, check consistency with CI crossing zero.
    """
    ci_lo = g - 1.96 * se
    ci_hi = g + 1.96 * se
    ci_crosses_zero = ci_lo < 0 < ci_hi

    result = {
        'ci_lower': round(ci_lo, 4),
        'ci_upper': round(ci_hi, 4),
        'ci_crosses_zero': ci_crosses_zero,
        'consistent_with_p': True
    }

    if p_reported is not None:
        # If CI crosses zero, p should be >= 0.05
        if ci_crosses_zero and p_reported < 0.05:
            result['consistent_with_p'] = False
            result['p_ci_note'] = (
                f"CI [{ci_lo:.3f}, {ci_hi:.3f}] crosses zero but p = {p_reported:.3f} < 0.05"
            )
        elif not ci_crosses_zero and p_reported >= 0.05:
            result['consistent_with_p'] = False
            result['p_ci_note'] = (
                f"CI [{ci_lo:.3f}, {ci_hi:.3f}] does not cross zero but p = {p_reported:.3f} >= 0.05"
            )

    return result


# --------------------------------------------------------------------------
# Study-level validation
# --------------------------------------------------------------------------

def validate_study(row: pd.Series) -> Dict[str, Any]:
    """
    Run all validation checks for a single study row.

    Args:
        row: DataFrame row with effect size data

    Returns:
        Validation result dictionary
    """
    study_id = row.get('study_id', 'unknown')
    g = row.get('hedges_g')
    se = row.get('se_g')
    n1 = row.get('n_treatment')
    n2 = row.get('n_control')
    m_trt = row.get('m_treatment')
    m_ctrl = row.get('m_control')
    p_val = row.get('p_value')

    checks = {}
    overall_valid = True

    # 1. Effect size range
    if g is not None and not np.isnan(float(g)):
        ok, msg = validate_effect_size_range(float(g))
        checks['effect_size_range'] = {'passed': ok, 'message': msg}
        if not ok:
            overall_valid = False
    else:
        checks['effect_size_range'] = {'passed': False, 'message': 'g is missing'}
        overall_valid = False

    # 2. Standard error
    if se is not None and not np.isnan(float(se)):
        n1_int = int(n1) if n1 is not None and not np.isnan(float(n1)) else 20
        n2_int = int(n2) if n2 is not None and not np.isnan(float(n2)) else 20
        ok, msg = validate_standard_error(float(se), n1_int, n2_int)
        checks['standard_error'] = {'passed': ok, 'message': msg}
        if not ok:
            overall_valid = False
    else:
        checks['standard_error'] = {'passed': False, 'message': 'SE is missing'}
        overall_valid = False

    # 3. Sample sizes
    n1_val = int(n1) if n1 is not None and not np.isnan(float(n1)) else None
    n2_val = int(n2) if n2 is not None and not np.isnan(float(n2)) else None
    ok, msg = validate_sample_sizes(n1_val, n2_val)
    checks['sample_sizes'] = {'passed': ok, 'message': msg}
    if not ok:
        overall_valid = False

    # 4. Sign consistency
    if g is not None and not np.isnan(float(g)):
        ok, msg = check_sign_consistency(
            float(g),
            float(m_trt) if m_trt is not None and not np.isnan(float(m_trt)) else None,
            float(m_ctrl) if m_ctrl is not None and not np.isnan(float(m_ctrl)) else None
        )
        checks['sign_consistency'] = {'passed': ok, 'message': msg}
        if not ok:
            overall_valid = False

    # 5. CI plausibility
    if g is not None and se is not None and not np.isnan(float(g)) and not np.isnan(float(se)):
        ci_result = check_ci_plausibility(
            float(g), float(se),
            float(p_val) if p_val is not None and not np.isnan(float(p_val)) else None
        )
        checks['ci_plausibility'] = {
            'passed': ci_result['consistent_with_p'],
            'message': ci_result.get('p_ci_note', 'OK'),
            **ci_result
        }
        if not ci_result['consistent_with_p']:
            overall_valid = False

    return {
        'study_id': study_id,
        'overall_valid': overall_valid,
        'checks': checks
    }


# --------------------------------------------------------------------------
# Dataset-level heterogeneity analysis
# --------------------------------------------------------------------------

def cochrans_q(g: np.ndarray, se: np.ndarray) -> Dict[str, float]:
    """
    Compute Cochran's Q statistic and I² index.

    Args:
        g: Effect size array
        se: Standard error array

    Returns:
        Dictionary with Q, df, p_value, I2, interpretation
    """
    var = se ** 2
    w = 1.0 / var
    k = len(g)

    g_fixed = np.sum(w * g) / np.sum(w)
    Q = float(np.sum(w * (g - g_fixed) ** 2))
    df = k - 1
    I2 = max(0.0, (Q - df) / Q * 100) if Q > 0 else 0.0

    # Chi-squared p-value approximation
    try:
        from scipy.stats import chi2
        p_Q = float(chi2.sf(Q, df))
    except ImportError:
        # Rough approximation without scipy
        p_Q = float(np.exp(-0.5 * max(0, Q - df)))

    if I2 < 25:
        interpretation = "Low heterogeneity"
    elif I2 < 50:
        interpretation = "Moderate heterogeneity"
    elif I2 < 75:
        interpretation = "Substantial heterogeneity"
    else:
        interpretation = "Considerable heterogeneity"

    return {
        'Q': round(Q, 3),
        'df': df,
        'p_Q': round(p_Q, 4),
        'I2': round(I2, 1),
        'interpretation': interpretation,
        'significant_heterogeneity': p_Q < 0.10
    }


def tau_squared_dl(g: np.ndarray, se: np.ndarray) -> Dict[str, float]:
    """
    Estimate tau² using DerSimonian-Laird method.

    Args:
        g: Effect size array
        se: Standard error array

    Returns:
        Dictionary with tau2, tau, and prediction interval
    """
    var = se ** 2
    w = 1.0 / var
    k = len(g)

    g_fixed = np.sum(w * g) / np.sum(w)
    Q = np.sum(w * (g - g_fixed) ** 2)
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)

    tau2 = max(0.0, (Q - (k - 1)) / c)
    tau = np.sqrt(tau2)

    # Random-effects pooled estimate for prediction interval
    w_re = 1.0 / (var + tau2)
    g_pooled = np.sum(w_re * g) / np.sum(w_re)
    se_pooled = np.sqrt(1.0 / np.sum(w_re))

    # 95% prediction interval (using t distribution approximation)
    pi_lower = g_pooled - 1.96 * np.sqrt(se_pooled ** 2 + tau2)
    pi_upper = g_pooled + 1.96 * np.sqrt(se_pooled ** 2 + tau2)

    return {
        'tau2': round(float(tau2), 4),
        'tau': round(float(tau), 4),
        'g_pooled_re': round(float(g_pooled), 4),
        'se_pooled_re': round(float(se_pooled), 4),
        'prediction_interval_95': [round(float(pi_lower), 3), round(float(pi_upper), 3)]
    }


# --------------------------------------------------------------------------
# Main validation pipeline
# --------------------------------------------------------------------------

def validate_dataset(data_path: str, output_path: str,
                     report_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate effect sizes in the cleaned dataset and generate a validation report.

    Args:
        data_path: Path to cleaned CSV dataset
        output_path: Path to save validation results CSV
        report_path: Optional path for JSON validation report

    Returns:
        Validation report dictionary
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    df = pd.read_csv(data_path)
    logger.info(f"Validating {len(df)} effect sizes")

    # Study-level validation
    validation_results = []
    for _, row in df.iterrows():
        result = validate_study(row)
        validation_results.append(result)

    # Summarize
    n_valid = sum(1 for r in validation_results if r['overall_valid'])
    n_invalid = len(validation_results) - n_valid

    # Dataset-level heterogeneity
    clean = df.dropna(subset=['hedges_g', 'se_g'])
    g_arr = clean['hedges_g'].values.astype(float)
    se_arr = clean['se_g'].values.astype(float)

    heterogeneity = {}
    tau_results = {}
    if len(g_arr) >= 3:
        heterogeneity = cochrans_q(g_arr, se_arr)
        tau_results = tau_squared_dl(g_arr, se_arr)

    report = {
        'validation_timestamp': datetime.now().isoformat(),
        'n_total': len(df),
        'n_valid': n_valid,
        'n_invalid': n_invalid,
        'validation_rate': round(n_valid / len(df), 4) if len(df) > 0 else 0,
        'heterogeneity': heterogeneity,
        'tau_estimate': tau_results,
        'study_results': validation_results
    }

    # Save results CSV
    val_df = pd.DataFrame([
        {
            'study_id': r['study_id'],
            'overall_valid': r['overall_valid'],
            **{f"check_{k}": v.get('passed') for k, v in r.get('checks', {}).items()},
            **{f"msg_{k}": v.get('message') for k, v in r.get('checks', {}).items()}
        }
        for r in validation_results
    ])

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    val_df.to_csv(output, index=False)
    logger.info(f"Validation results saved: {output}")

    if report_path:
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"Validation report saved: {report_path}")

    print(f"\nEffect Size Validation Summary:")
    print(f"  Total effect sizes:  {report['n_total']}")
    print(f"  Valid:               {report['n_valid']}")
    print(f"  Invalid:             {report['n_invalid']}")
    print(f"  Validation rate:     {report['validation_rate']:.1%}")

    if heterogeneity:
        print(f"\nHeterogeneity (overall):")
        print(f"  Q({heterogeneity['df']}) = {heterogeneity['Q']:.2f}, "
              f"p = {heterogeneity['p_Q']:.4f}")
        print(f"  I² = {heterogeneity['I2']:.1f}% ({heterogeneity['interpretation']})")
        print(f"  τ = {tau_results.get('tau', 'N/A'):.3f}, "
              f"τ² = {tau_results.get('tau2', 'N/A'):.4f}")

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate effect sizes in the meta-analysis dataset"
    )
    parser.add_argument('--input', required=True,
                        help='Cleaned dataset CSV')
    parser.add_argument('--output', required=True,
                        help='Validation results CSV')
    parser.add_argument('--report', default=None,
                        help='Optional JSON report path')

    args = parser.parse_args()
    validate_dataset(args.input, args.output, args.report)
