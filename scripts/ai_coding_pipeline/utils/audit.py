#!/usr/bin/env python3
"""
Audit logging for AI coding pipeline.
Tracks all extractions, decisions, and modifications with effect-size context.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class AuditLogger:
    """Comprehensive audit logging for the AI coding pipeline."""

    def __init__(self, log_dir: str):
        """
        Initialize audit logger.

        Args:
            log_dir: Directory to store audit logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = self.log_dir / f"audit_log_{timestamp}.jsonl"

        logger.info(f"Audit logger initialized: {self.log_file}")

    def _write_entry(self, entry: Dict[str, Any]):
        """Write an entry to the audit log."""
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.now().isoformat()

        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def log_extraction(self, study_id: str, phase: str, field: str,
                      value: Any, confidence: str, model: str,
                      tokens: int):
        """
        Log an AI extraction event.

        Args:
            study_id: Study identifier
            phase: Pipeline phase
            field: Field being extracted (e.g., 'hedges_g', 'design_type')
            value: Extracted value
            confidence: Confidence level (high / moderate / low)
            model: Model used
            tokens: Token count
        """
        entry = {
            'type': 'extraction',
            'study_id': study_id,
            'phase': phase,
            'field': field,
            'value': value,
            'confidence': confidence,
            'model': model,
            'tokens': tokens
        }
        self._write_entry(entry)

    def log_effect_size(self, study_id: str, outcome_label: str,
                       g: float, se: float, method: str,
                       model: str, raw_data: Dict[str, Any]):
        """
        Log an effect size extraction with conversion details.

        Args:
            study_id: Study identifier
            outcome_label: Label of the outcome measure
            g: Hedges' g value
            se: Standard error of g
            method: Conversion method used (means_sds, t_statistic, etc.)
            model: Model that performed extraction
            raw_data: Raw input data before conversion
        """
        entry = {
            'type': 'effect_size_extraction',
            'study_id': study_id,
            'outcome_label': outcome_label,
            'hedges_g': g,
            'se': se,
            'conversion_method': method,
            'model': model,
            'raw_data': raw_data
        }
        self._write_entry(entry)

    def log_consensus(self, study_id: str, field: str, ai_value: Any,
                     human_value: Any, resolution: Any, reason: str):
        """
        Log a consensus resolution event.

        Args:
            study_id: Study identifier
            field: Field being resolved
            ai_value: AI-extracted value
            human_value: Human-coded value
            resolution: Final resolved value
            reason: Resolution reason
        """
        entry = {
            'type': 'consensus',
            'study_id': study_id,
            'field': field,
            'ai_value': ai_value,
            'human_value': human_value,
            'resolution': resolution,
            'reason': reason
        }
        self._write_entry(entry)

    def log_event(self, phase: str, event_type: str, details: Dict[str, Any]):
        """
        Log a general pipeline event.

        Args:
            phase: Pipeline phase
            event_type: Type of event
            details: Event details
        """
        entry = {
            'type': 'event',
            'phase': phase,
            'event_type': event_type,
            'details': details
        }
        self._write_entry(entry)

    def log_error(self, phase: str, error_type: str, error_message: str,
                 context: Optional[Dict[str, Any]] = None):
        """
        Log a pipeline error.

        Args:
            phase: Pipeline phase
            error_type: Type of error
            error_message: Error message
            context: Additional context
        """
        entry = {
            'type': 'error',
            'phase': phase,
            'error_type': error_type,
            'error_message': error_message,
            'context': context or {}
        }
        self._write_entry(entry)

    def log_quality_check(self, gate_name: str, passed: bool, details: Dict[str, Any]):
        """
        Log a quality gate check.

        Args:
            gate_name: Name of quality gate
            passed: Whether the check passed
            details: Check details
        """
        entry = {
            'type': 'quality_check',
            'gate_name': gate_name,
            'passed': passed,
            'details': details
        }
        self._write_entry(entry)

    def log_icr_sampling(self, study_id: str, sampled: bool, reason: str):
        """
        Log ICR sampling decision.

        Args:
            study_id: Study identifier
            sampled: Whether the study was sampled for ICR
            reason: Reason for sampling/exclusion
        """
        entry = {
            'type': 'icr_sampling',
            'study_id': study_id,
            'sampled': sampled,
            'reason': reason
        }
        self._write_entry(entry)

    def get_summary(self) -> Dict[str, Any]:
        """
        Generate summary statistics from audit log.

        Returns:
            Summary dictionary
        """
        if not self.log_file.exists():
            return {'error': 'No audit log file found'}

        entries = []
        with open(self.log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))

        type_counts: Dict[str, int] = {}
        for entry in entries:
            entry_type = entry.get('type', 'unknown')
            type_counts[entry_type] = type_counts.get(entry_type, 0) + 1

        phase_counts: Dict[str, int] = {}
        for entry in entries:
            phase = entry.get('phase')
            if phase:
                phase_counts[phase] = phase_counts.get(phase, 0) + 1

        model_usage: Dict[str, int] = {}
        for entry in entries:
            if entry.get('type') in ('extraction', 'effect_size_extraction'):
                model = entry.get('model')
                if model:
                    model_usage[model] = model_usage.get(model, 0) + 1

        errors = [e for e in entries if e.get('type') == 'error']

        summary = {
            'total_entries': len(entries),
            'type_counts': type_counts,
            'phase_counts': phase_counts,
            'model_usage': model_usage,
            'n_errors': len(errors),
            'errors': errors[:10] if len(errors) > 10 else errors
        }

        return summary

    def export_summary(self, output_path: Optional[Path] = None):
        """
        Export audit log summary to JSON.

        Args:
            output_path: Path to save summary (default: log_dir/audit_summary.json)
        """
        summary = self.get_summary()

        if output_path is None:
            output_path = self.log_dir / 'audit_summary.json'

        with open(output_path, 'w') as f:
            json.dump(summary, indent=2, fp=f)

        logger.info(f"Audit summary exported to: {output_path}")

    def query_extractions(self, study_id: Optional[str] = None,
                         phase: Optional[str] = None,
                         field: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query extraction entries from audit log.

        Args:
            study_id: Filter by study ID
            phase: Filter by phase
            field: Filter by field

        Returns:
            List of matching extraction entries
        """
        if not self.log_file.exists():
            return []

        matches = []
        with open(self.log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)

                if entry.get('type') not in ('extraction', 'effect_size_extraction'):
                    continue

                if study_id and entry.get('study_id') != study_id:
                    continue

                if phase and entry.get('phase') != phase:
                    continue

                if field and entry.get('field') != field:
                    continue

                matches.append(entry)

        return matches

    def get_study_timeline(self, study_id: str) -> List[Dict[str, Any]]:
        """
        Get chronological timeline of all events for a study.

        Args:
            study_id: Study identifier

        Returns:
            List of events in chronological order
        """
        if not self.log_file.exists():
            return []

        timeline = []
        with open(self.log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                if entry.get('study_id') == study_id:
                    timeline.append(entry)

        timeline.sort(key=lambda x: x.get('timestamp', ''))
        return timeline
