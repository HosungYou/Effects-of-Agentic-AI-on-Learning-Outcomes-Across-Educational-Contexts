#!/usr/bin/env python3
"""
Phase 6: QA Final
Run 6 quality gates on the final dataset before meta-analysis.
Gates adapted for effect size validation (not correlation matrices).
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

VALID_DESIGNS = {
    'randomized_controlled_trial', 'rct',
    'quasi_experimental', 'pre_post', 'pretest_posttest'
}

VALID_OUTCOME_TYPES = {
    'learning_outcome', 'achievement', 'performance', 'test_score',
    'knowledge', 'skill', 'competency', 'grade'
}


class QAFinalChecker:
    """Runs comprehensive quality checks on the final effect size dataset."""

    def __init__(self, config: Dict[str, Any], cost_tracker, audit_logger):
        self.config = config
        self.cost_tracker = cost_tracker
        self.audit_logger = audit_logger
        self.quality_targets = config['quality_targets']

        self.gates = [
            ('Gate 1: Effect Size Range', self.gate1_effect_size_range),
            ('Gate 2: Sample Size Adequacy', self.gate2_sample_size),
            ('Gate 3: Design Validity', self.gate3_design_validity),
            ('Gate 4: Outcome Type Check', self.gate4_outcome_type),
            ('Gate 5: Completeness Check', self.gate5_completeness),
            ('Gate 6: Duplicate Check', self.gate6_no_duplicates)
        ]

    def load_consensus_data(self, consensus_dir: Path) -> pd.DataFrame:
        """
        Load and flatten all consensus JSON files into a DataFrame.

        Args:
            consensus_dir: Directory with consensus JSON files

        Returns:
            DataFrame with one row per effect size
        """
        consensus_files = list(consensus_dir.glob("*_consensus.json"))
        logger.info(f"Loading {len(consensus_files)} consensus files")

        rows = []

        for f in consensus_files:
            with open(f, 'r') as fh:
                data = json.load(fh)

            study_id = data['study_id']
            original = data.get('original_data', {})
            study_info = original.get('study_info', {})
            agent = data.get('consensus_agent_characteristics', {})

            for es in data.get('consensus_effect_sizes', []):
                rows.append({
                    'study_id': study_id,
                    'outcome_label': es.get('outcome_label', ''),
                    'hedges_g': es.get('hedges_g_consensus'),
                    'se_g': es.get('se_g_consensus'),
                    'n_models_agree': es.get('n_models_agree', 0),
                    'consensus_quality': es.get('consensus_quality', ''),
                    'flag': es.get('flag'),
                    # Study-level variables
                    'design_type': study_info.get('design_type', ''),
                    'n_treatment': study_info.get('n_treatment'),
                    'n_control': study_info.get('n_control'),
                    'n_total': study_info.get('sample_size_total'),
                    'outcome_type': study_info.get('outcome_type', ''),
                    'learning_domain': study_info.get('learning_domain', ''),
                    'country': study_info.get('country', ''),
                    'education_level': study_info.get('education_level', ''),
                    # Agent characteristics
                    'oversight_level': agent.get('oversight_level'),
                    'architecture': agent.get('architecture'),
                    'agency_level': agent.get('agency_level'),
                    'agent_role': agent.get('role'),
                    'modality': agent.get('modality'),
                    'technology': agent.get('technology'),
                    'adaptivity': agent.get('adaptivity')
                })

        df = pd.DataFrame(rows)
        logger.info(f"Loaded {len(df)} effect sizes from {df['study_id'].nunique()} studies")
        return df

    def gate1_effect_size_range(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
        """
        Gate 1: All |g| values must be within plausible range (< 5.0).

        Args:
            df: Effect size dataset

        Returns:
            (passed, details)
        """
        logger.info("Running Gate 1: Effect Size Range")

        max_g = self.quality_targets.get('max_effect_size', 5.0)
        out_of_range = df[df['hedges_g'].notna() & (df['hedges_g'].abs() > max_g)]

        passed = len(out_of_range) == 0

        details = {
            'max_allowed': max_g,
            'n_out_of_range': len(out_of_range),
            'n_valid': int(df['hedges_g'].notna().sum()),
            'g_min': float(df['hedges_g'].min()) if not df.empty else None,
            'g_max': float(df['hedges_g'].max()) if not df.empty else None,
            'g_median': float(df['hedges_g'].median()) if not df.empty else None,
            'flagged_entries': out_of_range[['study_id', 'outcome_label', 'hedges_g']].to_dict('records')
        }

        self.audit_logger.log_quality_check(f"Gate 1", passed, details)
        logger.info(f"Gate 1: {'PASSED' if passed else 'FAILED'} ({len(out_of_range)} out of range)")
        return passed, details

    def gate2_sample_size(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
        """
        Gate 2: Sample sizes must be >= 10 per group (or >= 20 total for pre-post).

        Args:
            df: Effect size dataset

        Returns:
            (passed, details)
        """
        logger.info("Running Gate 2: Sample Size Adequacy")

        min_n = self.quality_targets.get('min_sample_size', 10)
        issues = []

        for study_id in df['study_id'].unique():
            study_df = df[df['study_id'] == study_id].iloc[0]

            n_treatment = study_df.get('n_treatment')
            n_control = study_df.get('n_control')
            n_total = study_df.get('n_total')
            design = str(study_df.get('design_type', '')).lower()

            is_prepost = 'pre' in design or 'post' in design

            if is_prepost:
                if n_total is not None and n_total < min_n * 2:
                    issues.append({'study_id': study_id, 'issue': f'n_total={n_total} < {min_n*2}'})
            else:
                if n_treatment is not None and n_treatment < min_n:
                    issues.append({'study_id': study_id, 'issue': f'n_treatment={n_treatment} < {min_n}'})
                if n_control is not None and n_control < min_n:
                    issues.append({'study_id': study_id, 'issue': f'n_control={n_control} < {min_n}'})

        passed = len(issues) == 0

        details = {
            'min_n_per_group': min_n,
            'n_studies_checked': df['study_id'].nunique(),
            'n_issues': len(issues),
            'issues': issues
        }

        self.audit_logger.log_quality_check("Gate 2", passed, details)
        logger.info(f"Gate 2: {'PASSED' if passed else 'FAILED'} ({len(issues)} issues)")
        return passed, details

    def gate3_design_validity(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
        """
        Gate 3: All studies must have valid experimental/quasi-experimental/pre-post designs.

        Args:
            df: Effect size dataset

        Returns:
            (passed, details)
        """
        logger.info("Running Gate 3: Design Validity")

        study_designs = df.drop_duplicates('study_id')[['study_id', 'design_type']]
        invalid = study_designs[
            ~study_designs['design_type'].str.lower().isin(VALID_DESIGNS) &
            study_designs['design_type'].notna() &
            (study_designs['design_type'] != '')
        ]

        missing_design = study_designs[
            study_designs['design_type'].isna() | (study_designs['design_type'] == '')
        ]

        passed = len(invalid) == 0 and len(missing_design) == 0

        details = {
            'valid_designs': list(VALID_DESIGNS),
            'n_invalid_design': len(invalid),
            'n_missing_design': len(missing_design),
            'invalid_studies': invalid.to_dict('records'),
            'missing_design_studies': missing_design['study_id'].tolist()
        }

        self.audit_logger.log_quality_check("Gate 3", passed, details)
        logger.info(f"Gate 3: {'PASSED' if passed else 'FAILED'}")
        return passed, details

    def gate4_outcome_type(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
        """
        Gate 4: Outcome types must be learning-related (not just satisfaction/attitude).

        Args:
            df: Effect size dataset

        Returns:
            (passed, details)
        """
        logger.info("Running Gate 4: Outcome Type Check")

        study_outcomes = df.drop_duplicates('study_id')[['study_id', 'outcome_type']]
        invalid = study_outcomes[
            ~study_outcomes['outcome_type'].str.lower().isin(VALID_OUTCOME_TYPES) &
            study_outcomes['outcome_type'].notna() &
            (study_outcomes['outcome_type'] != '')
        ]

        missing = study_outcomes[
            study_outcomes['outcome_type'].isna() | (study_outcomes['outcome_type'] == '')
        ]

        passed = len(invalid) == 0 and len(missing) == 0

        details = {
            'valid_outcome_types': list(VALID_OUTCOME_TYPES),
            'n_invalid': len(invalid),
            'n_missing': len(missing),
            'invalid_outcomes': invalid.to_dict('records'),
            'missing_outcome_studies': missing['study_id'].tolist()
        }

        self.audit_logger.log_quality_check("Gate 4", passed, details)
        logger.info(f"Gate 4: {'PASSED' if passed else 'FAILED'} ({len(invalid)} invalid)")
        return passed, details

    def gate5_completeness(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
        """
        Gate 5: All required fields must be populated.

        Args:
            df: Effect size dataset

        Returns:
            (passed, details)
        """
        logger.info("Running Gate 5: Completeness Check")

        required_fields = ['hedges_g', 'se_g', 'design_type', 'outcome_type',
                          'oversight_level', 'architecture', 'agency_level']

        incomplete = {}
        for field in required_fields:
            missing_mask = df[field].isna() if field in df.columns else pd.Series([True] * len(df))
            n_missing = int(missing_mask.sum())
            if n_missing > 0:
                incomplete[field] = {
                    'n_missing': n_missing,
                    'study_ids': df[missing_mask]['study_id'].unique().tolist()[:10]
                }

        passed = len(incomplete) == 0

        details = {
            'required_fields': required_fields,
            'n_incomplete_fields': len(incomplete),
            'incomplete_fields': incomplete,
            'total_rows': len(df)
        }

        self.audit_logger.log_quality_check("Gate 5", passed, details)
        logger.info(f"Gate 5: {'PASSED' if passed else 'FAILED'} ({len(incomplete)} incomplete fields)")
        return passed, details

    def gate6_no_duplicates(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
        """
        Gate 6: No duplicate effect sizes within studies.

        Args:
            df: Effect size dataset

        Returns:
            (passed, details)
        """
        logger.info("Running Gate 6: Duplicate Check")

        duplicates = df[df.duplicated(subset=['study_id', 'outcome_label'], keep=False)]
        passed = len(duplicates) == 0

        dup_list = (
            duplicates.groupby(['study_id', 'outcome_label']).size()
            .reset_index(name='count').to_dict('records')
            if len(duplicates) > 0 else []
        )

        details = {
            'n_duplicate_rows': len(duplicates),
            'n_duplicate_groups': len(dup_list),
            'duplicates': dup_list
        }

        self.audit_logger.log_quality_check("Gate 6", passed, details)
        logger.info(f"Gate 6: {'PASSED' if passed else 'FAILED'} ({len(duplicates)} duplicates)")
        return passed, details

    def run_all_gates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Run all 6 quality gates.

        Args:
            df: Effect size dataset

        Returns:
            QA report with all gate results
        """
        logger.info("Running all quality gates...")

        gate_results = []
        all_passed = True

        for gate_name, gate_func in self.gates:
            passed, details = gate_func(df)
            gate_results.append({
                'gate': gate_name,
                'passed': passed,
                'details': details
            })
            if not passed:
                all_passed = False

        qa_report = {
            'qa_timestamp': datetime.now().isoformat(),
            'all_gates_passed': all_passed,
            'gate_results': gate_results,
            'dataset_summary': {
                'n_studies': int(df['study_id'].nunique()),
                'n_effect_sizes': len(df),
                'n_valid_g': int(df['hedges_g'].notna().sum()),
                'g_mean': round(float(df['hedges_g'].mean()), 3) if not df.empty else None,
                'g_sd': round(float(df['hedges_g'].std()), 3) if not df.empty else None,
                'g_range': [
                    round(float(df['hedges_g'].min()), 3),
                    round(float(df['hedges_g'].max()), 3)
                ] if not df.empty else None
            }
        }

        return qa_report

    def export_final_dataset(self, df: pd.DataFrame, output_path: Path):
        """
        Export final validated dataset to CSV and Excel.

        Args:
            df: Effect size dataset
            output_path: CSV output path
        """
        df_export = df.copy()
        df_export = df_export.sort_values(['study_id', 'outcome_label'])
        df_export.to_csv(output_path, index=False)
        logger.info(f"Final dataset exported to: {output_path}")

        excel_path = output_path.with_suffix('.xlsx')
        df_export.to_excel(excel_path, index=False, sheet_name='Agentic_AI_Effects')
        logger.info(f"Final dataset also saved as Excel: {excel_path}")


def run_qa_final(config: Dict[str, Any], cost_tracker, audit_logger) -> Dict[str, Any]:
    """
    Phase 6 entry point: Run QA final quality gates.

    Args:
        config: Pipeline configuration
        cost_tracker: Cost tracking instance
        audit_logger: Audit logging instance

    Returns:
        Result dictionary with success status and QA report
    """
    logger.info("Starting Phase 6: QA Final")

    try:
        qa_checker = QAFinalChecker(config, cost_tracker, audit_logger)

        consensus_dir = Path(config['paths']['verified'])
        df = qa_checker.load_consensus_data(consensus_dir)

        if df.empty:
            return {'success': False, 'error': 'No consensus data found'}

        qa_report = qa_checker.run_all_gates(df)

        output_dir = Path(config['paths']['final'])
        output_dir.mkdir(parents=True, exist_ok=True)

        report_path = output_dir / 'qa_report.json'
        with open(report_path, 'w') as f:
            json.dump(qa_report, f, indent=2)

        dataset_path = output_dir / 'Agentic_AI_Learning_Outcomes_Final_Dataset.csv'
        qa_checker.export_final_dataset(df, dataset_path)

        audit_logger.log_event(
            phase='phase6',
            event_type='qa_final',
            details={
                'all_gates_passed': qa_report['all_gates_passed'],
                'n_studies': qa_report['dataset_summary']['n_studies'],
                'n_effect_sizes': qa_report['dataset_summary']['n_effect_sizes']
            }
        )

        summary = {
            'all_gates_passed': qa_report['all_gates_passed'],
            'n_studies': qa_report['dataset_summary']['n_studies'],
            'n_effect_sizes': qa_report['dataset_summary']['n_effect_sizes'],
            'failed_gates': [g['gate'] for g in qa_report['gate_results'] if not g['passed']]
        }

        logger.info(f"Phase 6 complete: {summary}")

        return {
            'success': qa_report['all_gates_passed'],
            'summary': summary,
            'output_path': str(output_dir),
            'dataset_path': str(dataset_path),
            'qa_report': qa_report
        }

    except Exception as e:
        logger.error(f"Phase 6 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import yaml
    from utils.cost_tracker import CostTracker
    from utils.audit import AuditLogger

    with open('scripts/ai_coding_pipeline/config.yaml') as f:
        config = yaml.safe_load(f)

    result = run_qa_final(
        config,
        CostTracker(),
        AuditLogger(config['paths']['logs'])
    )

    print(json.dumps(result, indent=2))
