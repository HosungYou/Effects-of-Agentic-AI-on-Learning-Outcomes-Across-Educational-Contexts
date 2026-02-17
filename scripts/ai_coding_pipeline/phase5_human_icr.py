#!/usr/bin/env python3
"""
Phase 5: Human ICR Sampling and Reliability Calculation
Samples 20% of studies for human inter-coder reliability assessment.
Calculates Cohen's kappa (categorical) and ICC (numerical) metrics.
"""

import logging
import json
import random
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

import numpy as np

logger = logging.getLogger(__name__)


def cohens_kappa(rater1: List, rater2: List) -> float:
    """
    Calculate Cohen's kappa for two raters on categorical data.

    Args:
        rater1: Ratings from rater 1
        rater2: Ratings from rater 2

    Returns:
        Cohen's kappa coefficient
    """
    assert len(rater1) == len(rater2), "Rater lists must have equal length"

    categories = list(set(rater1) | set(rater2))
    n = len(rater1)

    # Observed agreement
    observed_agree = sum(1 for a, b in zip(rater1, rater2) if a == b) / n

    # Expected agreement
    expected_agree = 0.0
    for cat in categories:
        p1 = rater1.count(cat) / n
        p2 = rater2.count(cat) / n
        expected_agree += p1 * p2

    if expected_agree == 1.0:
        return 1.0

    kappa = (observed_agree - expected_agree) / (1 - expected_agree)
    return kappa


def icc_two_way_mixed(ratings: List[List[float]]) -> float:
    """
    Calculate ICC(2,1) two-way mixed for numerical data.
    Uses the Shrout & Fleiss (1979) formula.

    Args:
        ratings: List of rating vectors, one per rater [[r1_s1, r1_s2, ...], [r2_s1, ...]]

    Returns:
        ICC(2,1) value
    """
    ratings_array = np.array(ratings)  # shape: (n_raters, n_subjects)
    n_raters, n_subjects = ratings_array.shape

    grand_mean = ratings_array.mean()

    # Sum of squares
    ss_total = np.sum((ratings_array - grand_mean) ** 2)

    subject_means = ratings_array.mean(axis=0)
    ss_rows = n_raters * np.sum((subject_means - grand_mean) ** 2)

    rater_means = ratings_array.mean(axis=1)
    ss_cols = n_subjects * np.sum((rater_means - grand_mean) ** 2)

    ss_error = ss_total - ss_rows - ss_cols

    # Mean squares
    ms_rows = ss_rows / (n_subjects - 1)
    ms_cols = ss_cols / (n_raters - 1)
    ms_error = ss_error / ((n_subjects - 1) * (n_raters - 1))

    # ICC(2,1)
    icc = (ms_rows - ms_error) / (ms_rows + (n_raters - 1) * ms_error + (n_raters / n_subjects) * (ms_cols - ms_error))

    return float(icc)


class HumanICRSampler:
    """Manages human ICR sampling and reliability calculation."""

    def __init__(self, config: Dict[str, Any], audit_logger):
        self.config = config
        self.audit_logger = audit_logger
        self.sample_pct = config['quality_targets']['human_sample_pct']
        self.kappa_target = config['quality_targets']['kappa_categorical']
        self.icc_target = config['quality_targets']['icc_numerical']

    def sample_studies(self, consensus_dir: Path,
                      random_seed: int = 42) -> List[str]:
        """
        Randomly sample 20% of studies for human ICR.

        Args:
            consensus_dir: Directory with consensus JSON files
            random_seed: Random seed for reproducibility

        Returns:
            List of sampled study IDs
        """
        consensus_files = list(consensus_dir.glob("*_consensus.json"))
        study_ids = [f.stem.replace('_consensus', '') for f in consensus_files]

        n_sample = max(1, round(len(study_ids) * self.sample_pct))

        random.seed(random_seed)
        sampled = random.sample(study_ids, min(n_sample, len(study_ids)))

        logger.info(
            f"Sampled {len(sampled)}/{len(study_ids)} studies "
            f"({self.sample_pct*100:.0f}%) for human ICR"
        )

        for sid in study_ids:
            sampled_flag = sid in sampled
            self.audit_logger.log_icr_sampling(
                study_id=sid,
                sampled=sampled_flag,
                reason='random_20pct_sample' if sampled_flag else 'not_selected'
            )

        return sampled

    def export_icr_package(self, sampled_ids: List[str],
                           consensus_dir: Path,
                           output_dir: Path) -> Dict[str, Any]:
        """
        Export human-readable coding package for ICR raters.

        Args:
            sampled_ids: List of sampled study IDs
            consensus_dir: Directory with consensus JSON files
            output_dir: Directory to save ICR package

        Returns:
            Export summary
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        icr_records = []

        for study_id in sampled_ids:
            consensus_path = consensus_dir / f"{study_id}_consensus.json"

            if not consensus_path.exists():
                logger.warning(f"Consensus file not found for {study_id}")
                continue

            with open(consensus_path, 'r') as f:
                consensus = json.load(f)

            # Build human-readable coding form
            record = {
                'study_id': study_id,
                'source_file': consensus.get('original_data', {}).get('study_info', {}).get('source_file', ''),
                'instructions': 'Please fill in all fields based on the PDF. Do not change the study_id field.',
                'EFFECT_SIZES': {
                    'note': 'List each outcome measure with its M, SD, n for treatment/control groups, or provide d/g directly.',
                    'effects': []  # Human fills this in
                },
                'AGENT_CHARACTERISTICS': {
                    'oversight_level': '',  # fully_autonomous | ai_led_with_checkpoints | human_led_with_ai_support
                    'architecture': '',     # single_agent | multi_agent
                    'agency_level': '',     # adaptive | proactive | co_learner | peer
                    'role': '',             # tutor | coach | assessor | collaborator | facilitator
                    'modality': '',         # text_only | voice | embodied | mixed
                    'technology': '',       # rule_based | ml | nlp | llm | rl
                    'adaptivity': ''        # static | adaptive_performance | adaptive_behavior_affect
                },
                'STUDY_INFO': {
                    'design_type': '',      # rct | quasi_experimental | pre_post
                    'sample_size_total': None,
                    'learning_domain': '',
                    'country': '',
                    'education_level': ''   # k12 | higher_ed | adult | mixed
                },
                'rater_notes': ''
            }

            icr_records.append(record)

        # Save as JSON template
        icr_package_path = output_dir / 'icr_coding_package.json'
        with open(icr_package_path, 'w') as f:
            json.dump(icr_records, f, indent=2)

        # Also save a summary of AI consensus values for comparison (post-ICR)
        ai_values = []
        for study_id in sampled_ids:
            consensus_path = consensus_dir / f"{study_id}_consensus.json"
            if consensus_path.exists():
                with open(consensus_path, 'r') as f:
                    data = json.load(f)
                ai_values.append({
                    'study_id': study_id,
                    'ai_consensus_effects': data.get('consensus_effect_sizes', []),
                    'ai_consensus_agent': data.get('consensus_agent_characteristics', {})
                })

        ai_values_path = output_dir / 'ai_consensus_values_FOR_COMPARISON.json'
        with open(ai_values_path, 'w') as f:
            json.dump(ai_values, f, indent=2)

        logger.info(f"ICR package saved to {output_dir}")
        logger.info(f"IMPORTANT: Share {icr_package_path} with human raters.")
        logger.info(f"DO NOT share {ai_values_path} until human coding is complete.")

        return {
            'n_studies_sampled': len(icr_records),
            'package_path': str(icr_package_path)
        }

    def calculate_reliability(self, human_coding_path: Path,
                              consensus_dir: Path) -> Dict[str, Any]:
        """
        Calculate ICR metrics from completed human coding.

        Args:
            human_coding_path: Path to completed human coding JSON
            consensus_dir: Directory with AI consensus JSON files

        Returns:
            Reliability metrics dictionary
        """
        with open(human_coding_path, 'r') as f:
            human_codings = json.load(f)

        cat_fields = ['oversight_level', 'architecture', 'agency_level',
                      'role', 'modality', 'technology', 'adaptivity']

        ai_cat: Dict[str, List] = {f: [] for f in cat_fields}
        human_cat: Dict[str, List] = {f: [] for f in cat_fields}

        ai_g_values = []
        human_g_values = []

        for human_record in human_codings:
            study_id = human_record['study_id']
            consensus_path = consensus_dir / f"{study_id}_consensus.json"

            if not consensus_path.exists():
                continue

            with open(consensus_path, 'r') as f:
                ai_data = json.load(f)

            ai_agent = ai_data.get('consensus_agent_characteristics', {})
            human_agent = human_record.get('AGENT_CHARACTERISTICS', {})

            for field in cat_fields:
                ai_val = ai_agent.get(field)
                human_val = human_agent.get(field)
                if ai_val is not None and human_val is not None:
                    ai_cat[field].append(str(ai_val))
                    human_cat[field].append(str(human_val))

            # Numeric: first effect size g value
            ai_effects = ai_data.get('consensus_effect_sizes', [])
            human_effects = human_record.get('EFFECT_SIZES', {}).get('effects', [])

            if ai_effects and human_effects:
                ai_g = ai_effects[0].get('hedges_g_consensus')
                human_g = human_effects[0].get('hedges_g') if human_effects else None
                if ai_g is not None and human_g is not None:
                    ai_g_values.append(float(ai_g))
                    human_g_values.append(float(human_g))

        # Calculate kappa per categorical field
        kappa_results = {}
        for field in cat_fields:
            if len(ai_cat[field]) >= 5:
                k = cohens_kappa(ai_cat[field], human_cat[field])
                kappa_results[field] = {
                    'kappa': round(k, 3),
                    'n_compared': len(ai_cat[field]),
                    'passed': k >= self.kappa_target
                }

        # Overall categorical kappa
        all_ai_cat = []
        all_human_cat = []
        for field in cat_fields:
            all_ai_cat.extend(ai_cat[field])
            all_human_cat.extend(human_cat[field])

        overall_kappa = cohens_kappa(all_ai_cat, all_human_cat) if all_ai_cat else None

        # ICC for effect sizes
        icc_value = None
        if len(ai_g_values) >= 5:
            try:
                icc_value = icc_two_way_mixed([ai_g_values, human_g_values])
            except Exception as e:
                logger.warning(f"ICC calculation failed: {e}")

        mae_g = (
            float(np.mean(np.abs(np.array(ai_g_values) - np.array(human_g_values))))
            if ai_g_values else None
        )

        metrics = {
            'n_studies_compared': len(human_codings),
            'categorical_metrics': {
                'per_field_kappa': kappa_results,
                'overall_kappa': round(overall_kappa, 3) if overall_kappa else None,
                'kappa_target': self.kappa_target,
                'overall_kappa_passed': overall_kappa >= self.kappa_target if overall_kappa else False
            },
            'numerical_metrics': {
                'icc_2_1': round(icc_value, 4) if icc_value is not None else None,
                'mae_hedges_g': round(mae_g, 4) if mae_g is not None else None,
                'n_effect_sizes_compared': len(ai_g_values),
                'icc_target': self.icc_target,
                'icc_passed': icc_value >= self.icc_target if icc_value is not None else False
            },
            'all_targets_met': (
                (overall_kappa >= self.kappa_target if overall_kappa else False) and
                (icc_value >= self.icc_target if icc_value is not None else False)
            )
        }

        return metrics


def sample_for_icr(config: Dict[str, Any], cost_tracker, audit_logger) -> Dict[str, Any]:
    """
    Phase 5 entry point: Sample studies for human ICR.

    Args:
        config: Pipeline configuration
        cost_tracker: Cost tracking instance (unused, no LLM calls)
        audit_logger: Audit logging instance

    Returns:
        Result dictionary with success status and sampling info
    """
    logger.info("Starting Phase 5: Human ICR Sampling")

    try:
        sampler = HumanICRSampler(config, audit_logger)

        consensus_dir = Path(config['paths']['verified'])
        output_dir = Path(config['paths']['verified']) / 'icr_package'

        sampled_ids = sampler.sample_studies(consensus_dir)
        export_summary = sampler.export_icr_package(sampled_ids, consensus_dir, output_dir)

        # Check if human coding already exists (from a previous run)
        human_coding_path = output_dir / 'icr_human_completed.json'
        reliability_metrics = None

        if human_coding_path.exists():
            logger.info("Found completed human coding. Calculating reliability...")
            reliability_metrics = sampler.calculate_reliability(
                human_coding_path, consensus_dir
            )

            metrics_path = output_dir / 'reliability_metrics.json'
            with open(metrics_path, 'w') as f:
                json.dump(reliability_metrics, f, indent=2)

            audit_logger.log_event(
                phase='phase5',
                event_type='reliability_calculated',
                details=reliability_metrics
            )
        else:
            logger.info(
                f"Human coding file not found at {human_coding_path}. "
                "Complete human coding and re-run Phase 5 to calculate reliability."
            )

        summary = {
            **export_summary,
            'reliability_metrics': reliability_metrics,
            'awaiting_human_coding': not human_coding_path.exists()
        }

        return {
            'success': True,
            'summary': summary,
            'output_path': str(output_dir)
        }

    except Exception as e:
        logger.error(f"Phase 5 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import yaml
    from utils.cost_tracker import CostTracker
    from utils.audit import AuditLogger

    with open('scripts/ai_coding_pipeline/config.yaml') as f:
        config = yaml.safe_load(f)

    result = sample_for_icr(
        config,
        CostTracker(),
        AuditLogger(config['paths']['logs'])
    )

    print(json.dumps(result, indent=2))
