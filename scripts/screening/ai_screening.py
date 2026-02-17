#!/usr/bin/env python3
"""
AI-assisted screening for agentic AI learning outcomes meta-analysis.
Screens title/abstract records against PICOS inclusion criteria using LLM.
"""

import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# Inclusion criteria
# --------------------------------------------------------------------------
INCLUSION_CRITERIA = {
    "population": (
        "Learners (K-12, higher education, adult/professional) in educational settings."
    ),
    "intervention": (
        "An agentic AI system that exhibits at least one of: autonomy in decision-making, "
        "proactive interaction initiation, adaptive personalization, or multi-step goal pursuit. "
        "This includes intelligent tutoring systems, conversational AI tutors, autonomous "
        "coaching agents, LLM-based tutors, and multi-agent learning systems."
    ),
    "comparator": (
        "Any comparator: no-AI control, human instruction only, non-agentic AI (simple "
        "quiz apps, static e-learning), or pre-intervention baseline (for pre-post designs)."
    ),
    "outcome": (
        "A quantitative measure of learning outcomes: knowledge acquisition, skill "
        "development, academic achievement, test/quiz scores, or competency gains. "
        "Studies reporting only satisfaction, attitude, or engagement WITHOUT a learning "
        "outcome measure are EXCLUDED."
    ),
    "study_design": (
        "Experimental or quasi-experimental designs: RCTs, quasi-experiments with control "
        "groups, or pre-post designs with a single group. Purely qualitative studies, "
        "surveys, or reviews are EXCLUDED."
    ),
    "effect_size_reporting": (
        "Study must report sufficient statistics to compute or estimate an effect size "
        "(means and SDs, t/F statistics, or a pre-computed d/g value)."
    ),
    "language": "Full text available in English."
}

EXCLUSION_CRITERIA = [
    "Study focuses on AI system development/design without an empirical learning outcome evaluation",
    "No comparison condition and no pre-test (cannot compute an effect size)",
    "N < 10 participants total",
    "Outcome is satisfaction or attitude only (no learning measure)",
    "Non-educational context (e.g., workplace safety training with no learning assessment)",
    "Conference abstract without full-text data",
    "Duplicate of an already-included study"
]

SCREENING_PROMPT = """You are a systematic review expert screening studies for a meta-analysis on "Effects of Agentic AI on Learning Outcomes."

INCLUSION CRITERIA:
1. Population: Learners (K-12, higher ed, adult) in educational settings.
2. Intervention: An agentic AI system (ITS, conversational AI tutor, LLM tutor, autonomous coaching agent, multi-agent learning system) that exhibits autonomy, proactivity, adaptivity, or multi-step goal pursuit.
3. Outcome: Quantitative learning outcome (test scores, knowledge gain, skill acquisition). Satisfaction/attitude alone is INSUFFICIENT.
4. Design: Experimental (RCT), quasi-experimental (with control group), or pre-post (single group). Qualitative/survey only is EXCLUDED.
5. Statistics: Must report M, SD, n; or t/F statistics; or pre-computed d/g. No effect size data = EXCLUDED.
6. Language: English full text.

EXCLUSION CRITERIA:
- AI system paper without empirical evaluation
- N < 10 total
- No learning outcome (satisfaction only)
- No comparison or baseline (cannot compute effect size)
- Duplicate study

Respond with ONLY this JSON object:
{
  "decision": "<INCLUDE | EXCLUDE | UNCERTAIN>",
  "confidence": "<high | moderate | low>",
  "rationale": "<2-3 sentences explaining decision>",
  "population_met": <true | false>,
  "intervention_met": <true | false>,
  "outcome_met": <true | false>,
  "design_met": <true | false>,
  "statistics_met": <true | false>,
  "primary_exclusion_reason": "<if EXCLUDE, state the main reason; else null>"
}"""


class AIScreener:
    """Screens title/abstract records for meta-analysis inclusion using an LLM."""

    def __init__(self, model: str = "claude-sonnet-4-5-20250929",
                 cost_tracker=None):
        self.model = model
        self.cost_tracker = cost_tracker
        self._init_client()

    def _init_client(self):
        """Initialize the LLM client."""
        try:
            from anthropic import Anthropic
            api_key = os.environ.get('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = Anthropic(api_key=api_key)
            logger.info(f"Initialized Claude client: {self.model}")
        except ImportError:
            raise ImportError("anthropic package required: pip install anthropic")

    def screen_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Screen a single title/abstract record.

        Args:
            record: Dictionary with keys: title, abstract, authors, year, source

        Returns:
            Screening decision dictionary
        """
        title = record.get('title', 'No title')
        abstract = record.get('abstract', 'No abstract')
        year = record.get('year', '')
        authors = record.get('authors', '')

        user_msg = f"""TITLE: {title}

AUTHORS: {authors}
YEAR: {year}

ABSTRACT:
{abstract}

Based on the above, apply the inclusion/exclusion criteria and return your decision as JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.0,
                system=SCREENING_PROMPT,
                messages=[{"role": "user", "content": user_msg}]
            )

            content = response.content[0].text if response.content else ""
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            if self.cost_tracker:
                self.cost_tracker.track(self.model, input_tokens, output_tokens)

            # Parse JSON
            try:
                decision = json.loads(content)
            except json.JSONDecodeError:
                if '```json' in content:
                    start = content.find('```json') + 7
                    end = content.find('```', start)
                    decision = json.loads(content[start:end])
                else:
                    decision = {
                        'decision': 'UNCERTAIN',
                        'confidence': 'low',
                        'rationale': 'Parse error in AI response',
                        'parse_error': True
                    }

            decision['study_id'] = record.get('id', '')
            decision['title'] = title
            decision['screened_at'] = datetime.now().isoformat()
            decision['model'] = self.model
            decision['tokens'] = input_tokens + output_tokens

            return decision

        except Exception as e:
            logger.error(f"Screening failed for record {record.get('id', '')}: {e}")
            return {
                'study_id': record.get('id', ''),
                'title': title,
                'decision': 'UNCERTAIN',
                'confidence': 'low',
                'rationale': f'Screening error: {str(e)}',
                'error': True
            }

    def screen_batch(self, records: List[Dict[str, Any]],
                     output_path: Path,
                     delay_seconds: float = 0.5) -> Dict[str, Any]:
        """
        Screen a batch of records and save results incrementally.

        Args:
            records: List of title/abstract record dictionaries
            output_path: Path to save JSONL results
            delay_seconds: Delay between API calls (rate limiting)

        Returns:
            Summary statistics
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        results = []
        include_count = 0
        exclude_count = 0
        uncertain_count = 0

        logger.info(f"Screening {len(records)} records...")

        for i, record in enumerate(records):
            logger.info(f"Screening record {i+1}/{len(records)}: {record.get('id', '')}")

            result = self.screen_record(record)
            results.append(result)

            # Save incrementally
            with open(output_path, 'a') as f:
                f.write(json.dumps(result) + '\n')

            decision = result.get('decision', 'UNCERTAIN')
            if decision == 'INCLUDE':
                include_count += 1
            elif decision == 'EXCLUDE':
                exclude_count += 1
            else:
                uncertain_count += 1

            if delay_seconds > 0 and i < len(records) - 1:
                time.sleep(delay_seconds)

        summary = {
            'total_screened': len(records),
            'include': include_count,
            'exclude': exclude_count,
            'uncertain': uncertain_count,
            'inclusion_rate': round(include_count / len(records), 3) if records else 0
        }

        logger.info(f"Screening complete: {summary}")
        return summary

    def export_decisions_csv(self, jsonl_path: Path, output_csv: Path):
        """
        Export screening decisions to CSV for review.

        Args:
            jsonl_path: Path to JSONL decisions file
            output_csv: Output CSV path
        """
        records = []
        with open(jsonl_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))

        df = pd.DataFrame(records)
        cols = [
            'study_id', 'title', 'decision', 'confidence', 'rationale',
            'population_met', 'intervention_met', 'outcome_met', 'design_met',
            'statistics_met', 'primary_exclusion_reason', 'screened_at'
        ]
        available_cols = [c for c in cols if c in df.columns]
        df[available_cols].to_csv(output_csv, index=False)
        logger.info(f"Decisions exported to {output_csv}")


def screen_from_csv(input_csv: str, output_dir: str = "data/00_raw/screening",
                   id_col: str = "id", title_col: str = "title",
                   abstract_col: str = "abstract"):
    """
    Screen records from a CSV file.

    Args:
        input_csv: Path to input CSV with title/abstract data
        output_dir: Directory to save screening results
        id_col: Column name for study ID
        title_col: Column name for title
        abstract_col: Column name for abstract
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    df = pd.read_csv(input_csv)
    logger.info(f"Loaded {len(df)} records from {input_csv}")

    records = []
    for _, row in df.iterrows():
        records.append({
            'id': str(row.get(id_col, '')),
            'title': str(row.get(title_col, '')),
            'abstract': str(row.get(abstract_col, '')),
            'authors': str(row.get('authors', '')),
            'year': str(row.get('year', ''))
        })

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    screener = AIScreener()
    results_jsonl = output_path / 'screening_decisions.jsonl'
    summary = screener.screen_batch(records, results_jsonl)

    # Export to CSV for human review
    results_csv = output_path / 'screening_decisions.csv'
    screener.export_decisions_csv(results_jsonl, results_csv)

    # Save summary
    summary_path = output_path / 'screening_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nScreening complete!")
    print(f"Include:   {summary['include']}")
    print(f"Exclude:   {summary['exclude']}")
    print(f"Uncertain: {summary['uncertain']}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="AI-assisted title/abstract screening for meta-analysis"
    )
    parser.add_argument('--input', required=True, help='Input CSV with title/abstract data')
    parser.add_argument('--output', default='data/00_raw/screening',
                        help='Output directory for screening results')
    parser.add_argument('--id-col', default='id', help='Column name for study ID')
    parser.add_argument('--title-col', default='title', help='Column name for title')
    parser.add_argument('--abstract-col', default='abstract',
                        help='Column name for abstract')

    args = parser.parse_args()
    screen_from_csv(args.input, args.output, args.id_col, args.title_col, args.abstract_col)
