#!/usr/bin/env python3
"""
Data cleaning and validation for the agentic AI learning outcomes meta-analysis.
Loads extracted data, applies cleaning rules, and outputs a clean analysis-ready dataset.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Validation constants
# --------------------------------------------------------------------------

VALID_DESIGN_TYPES = {
    'randomized_controlled_trial', 'rct', 'quasi_experimental',
    'pre_post', 'pretest_posttest'
}

VALID_EDUCATION_LEVELS = {
    'k12', 'higher_education', 'adult', 'professional', 'mixed'
}

VALID_OUTCOME_TYPES = {
    'learning_outcome', 'achievement', 'test_score', 'knowledge',
    'skill', 'competency', 'grade', 'performance', 'satisfaction',
    'engagement', 'other'
}

VALID_AGENT_CODES = {
    'oversight_level': {
        'fully_autonomous', 'ai_led_with_checkpoints', 'human_led_with_ai_support'
    },
    'architecture': {'single_agent', 'multi_agent'},
    'agency_level': {'adaptive', 'proactive', 'co_learner', 'peer'},
    'agent_role': {'tutor', 'coach', 'assessor', 'collaborator', 'facilitator'},
    'modality': {'text_only', 'voice', 'embodied', 'mixed'},
    'technology': {'rule_based', 'ml', 'nlp', 'llm', 'rl'},
    'adaptivity': {'static', 'adaptive_performance', 'adaptive_behavior_affect'}
}

MAX_HEDGES_G = 5.0
MIN_N_PER_GROUP = 10


# --------------------------------------------------------------------------
# Cleaning functions
# --------------------------------------------------------------------------

def load_final_dataset(data_path: str) -> pd.DataFrame:
    """
    Load the final pipeline output CSV.

    Args:
        data_path: Path to CSV file

    Returns:
        Loaded DataFrame
    """
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} rows from {data_path}")
    return df


def standardize_design_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize design_type values to canonical forms.

    Args:
        df: DataFrame with 'design_type' column

    Returns:
        DataFrame with standardized design_type
    """
    design_map = {
        'rct': 'randomized_controlled_trial',
        'randomized': 'randomized_controlled_trial',
        'random assignment': 'randomized_controlled_trial',
        'quasi-experimental': 'quasi_experimental',
        'quasi experimental': 'quasi_experimental',
        'non-equivalent control group': 'quasi_experimental',
        'pretest_posttest': 'pre_post',
        'pre-post': 'pre_post',
        'pretest-posttest': 'pre_post',
        'one group pre post': 'pre_post'
    }

    if 'design_type' in df.columns:
        df['design_type'] = (
            df['design_type']
            .str.lower()
            .str.strip()
            .map(lambda x: design_map.get(x, x))
        )

    return df


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric columns to proper types, coercing errors to NaN.

    Args:
        df: DataFrame

    Returns:
        DataFrame with numeric columns properly typed
    """
    numeric_cols = [
        'hedges_g', 'se_g', 'n_treatment', 'n_control', 'n_total',
        'n_treatment_1', 'n_control_1'
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def remove_invalid_effect_sizes(df: pd.DataFrame,
                                 max_g: float = MAX_HEDGES_G,
                                 log_removed: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove effect sizes outside the plausible range.

    Args:
        df: DataFrame with 'hedges_g' column
        max_g: Maximum allowed |g|
        log_removed: Whether to log removed records

    Returns:
        (clean_df, removed_df)
    """
    if 'hedges_g' not in df.columns:
        return df, pd.DataFrame()

    invalid_mask = df['hedges_g'].notna() & (df['hedges_g'].abs() > max_g)
    removed = df[invalid_mask].copy()
    clean = df[~invalid_mask].copy()

    if log_removed and len(removed) > 0:
        logger.warning(
            f"Removed {len(removed)} effect sizes with |g| > {max_g}: "
            f"{removed[['study_id', 'hedges_g']].to_dict('records')}"
        )

    return clean, removed


def remove_small_samples(df: pd.DataFrame,
                          min_n: int = MIN_N_PER_GROUP) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove studies with sample sizes below the minimum threshold.

    Args:
        df: DataFrame
        min_n: Minimum sample size per group

    Returns:
        (clean_df, removed_df)
    """
    if 'n_treatment' not in df.columns and 'n_total' not in df.columns:
        return df, pd.DataFrame()

    small_mask = pd.Series([False] * len(df), index=df.index)

    if 'n_treatment' in df.columns:
        small_mask |= df['n_treatment'].notna() & (df['n_treatment'] < min_n)
    if 'n_control' in df.columns:
        small_mask |= df['n_control'].notna() & (df['n_control'] < min_n)
    if 'n_total' in df.columns:
        small_mask |= df['n_total'].notna() & (df['n_total'] < min_n * 2)

    removed = df[small_mask].copy()
    clean = df[~small_mask].copy()

    if len(removed) > 0:
        logger.warning(f"Removed {len(removed)} studies with n < {min_n} per group")

    return clean, removed


def validate_categorical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate categorical columns against allowed values.
    Set invalid values to NaN and log warnings.

    Args:
        df: DataFrame

    Returns:
        DataFrame with validated categorical columns
    """
    for col, valid_values in VALID_AGENT_CODES.items():
        if col in df.columns:
            invalid_mask = (
                df[col].notna() &
                ~df[col].isin(valid_values)
            )
            if invalid_mask.any():
                invalid_vals = df.loc[invalid_mask, col].unique().tolist()
                logger.warning(
                    f"Column '{col}': {invalid_mask.sum()} invalid values "
                    f"set to NaN: {invalid_vals}"
                )
                df.loc[invalid_mask, col] = np.nan

    return df


def handle_outliers(df: pd.DataFrame,
                    z_threshold: float = 3.5) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Flag and optionally remove statistical outliers using winsorization.
    Uses Z-score method on |g|.

    Args:
        df: DataFrame with 'hedges_g'
        z_threshold: Z-score threshold for outlier detection

    Returns:
        (df_with_flag, outlier_df)
    """
    if 'hedges_g' not in df.columns:
        return df, pd.DataFrame()

    g_values = df['hedges_g'].dropna()
    if len(g_values) < 5:
        return df, pd.DataFrame()

    mean_g = g_values.mean()
    std_g = g_values.std()

    z_scores = (df['hedges_g'] - mean_g).abs() / std_g
    df['outlier_flag'] = (z_scores > z_threshold) & df['hedges_g'].notna()

    outliers = df[df['outlier_flag']].copy()
    if len(outliers) > 0:
        logger.warning(
            f"Flagged {len(outliers)} outlier effect sizes (|z| > {z_threshold}): "
            f"{outliers[['study_id', 'hedges_g']].to_dict('records')}"
        )

    return df, outliers


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived columns useful for analysis.

    Args:
        df: DataFrame

    Returns:
        DataFrame with additional derived columns
    """
    # Variance of g
    if 'se_g' in df.columns:
        df['var_g'] = df['se_g'] ** 2

    # 95% confidence interval
    if 'hedges_g' in df.columns and 'se_g' in df.columns:
        df['ci_lower_95'] = df['hedges_g'] - 1.96 * df['se_g']
        df['ci_upper_95'] = df['hedges_g'] + 1.96 * df['se_g']

    # Precision (inverse variance)
    if 'var_g' in df.columns:
        df['precision'] = 1.0 / df['var_g'].replace(0, np.nan)

    # Study weight (proportional to precision)
    if 'precision' in df.columns:
        total_precision = df['precision'].sum()
        df['weight_pct'] = (df['precision'] / total_precision * 100).round(2)

    # Total sample size
    if 'n_treatment' in df.columns and 'n_control' in df.columns:
        df['n_total_computed'] = df['n_treatment'].fillna(0) + df['n_control'].fillna(0)
        df['n_total_computed'] = df['n_total_computed'].replace(0, np.nan)

    # Sign of effect (positive = favours AI)
    if 'hedges_g' in df.columns:
        df['direction'] = df['hedges_g'].apply(
            lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'zero')
            if pd.notna(x) else np.nan
        )

    return df


def generate_cleaning_report(original_n: int, removed_invalid: int,
                              removed_small_n: int, n_outliers: int,
                              final_n: int, output_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a data cleaning report.

    Args:
        original_n: Original number of records
        removed_invalid: Records removed for invalid effect sizes
        removed_small_n: Records removed for small samples
        n_outliers: Records flagged as outliers (not removed)
        final_n: Final record count
        output_path: Optional path to save JSON report

    Returns:
        Report dictionary
    """
    report = {
        'timestamp': datetime.now().isoformat(),
        'original_n': original_n,
        'removed_invalid_effect_size': removed_invalid,
        'removed_small_sample': removed_small_n,
        'outliers_flagged_not_removed': n_outliers,
        'final_n': final_n,
        'total_removed': original_n - final_n,
        'retention_rate': round(final_n / original_n, 4) if original_n > 0 else 0
    }

    if output_path:
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Cleaning report saved: {output_path}")

    return report


def clean_dataset(input_path: str, output_path: str,
                  report_path: Optional[str] = None) -> pd.DataFrame:
    """
    Full cleaning pipeline.

    Args:
        input_path: Path to raw final dataset CSV
        output_path: Path to save cleaned dataset
        report_path: Optional path to save cleaning report JSON

    Returns:
        Cleaned DataFrame
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Load
    df = load_final_dataset(input_path)
    original_n = len(df)

    # Step 1: Standardize
    df = standardize_design_type(df)
    df = clean_numeric_columns(df)

    # Step 2: Remove invalid effect sizes
    df, removed_invalid = remove_invalid_effect_sizes(df)

    # Step 3: Remove small samples
    df, removed_small = remove_small_samples(df)

    # Step 4: Validate categorical columns
    df = validate_categorical_columns(df)

    # Step 5: Flag outliers
    df, outliers = handle_outliers(df)

    # Step 6: Add derived columns
    df = add_derived_columns(df)

    # Save
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    logger.info(f"Cleaned dataset saved: {output} ({len(df)} rows)")

    # Report
    report = generate_cleaning_report(
        original_n=original_n,
        removed_invalid=len(removed_invalid),
        removed_small_n=len(removed_small),
        n_outliers=int(df.get('outlier_flag', pd.Series([False] * len(df))).sum()),
        final_n=len(df),
        output_path=report_path
    )

    print(f"\nData Cleaning Complete:")
    print(f"  Original records:  {report['original_n']}")
    print(f"  Invalid |g| > 5:   {report['removed_invalid_effect_size']}")
    print(f"  Small samples:     {report['removed_small_sample']}")
    print(f"  Outliers flagged:  {report['outliers_flagged_not_removed']}")
    print(f"  Final records:     {report['final_n']}")
    print(f"  Retention rate:    {report['retention_rate']:.1%}")

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean and validate extracted meta-analysis dataset"
    )
    parser.add_argument('--input', required=True,
                        help='Input CSV (raw final dataset)')
    parser.add_argument('--output', required=True,
                        help='Output CSV (cleaned dataset)')
    parser.add_argument('--report', default=None,
                        help='Optional JSON cleaning report path')

    args = parser.parse_args()
    clean_dataset(args.input, args.output, args.report)
