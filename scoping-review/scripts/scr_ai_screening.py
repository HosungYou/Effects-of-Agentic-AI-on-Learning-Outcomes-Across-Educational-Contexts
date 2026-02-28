#!/usr/bin/env python3
"""
AI-assisted screening for Trust Calibration Scoping Review.

Screens title/abstract records against PCC inclusion criteria using LLM.
Adapted from parent project's ai_screening.py with scoping-review-specific
PCC criteria (replacing PICOS).

Usage:
    python scr_ai_screening.py --input ../data/01_deduplicated/merged_deduplicated.csv \
                                --output ../data/02_screened
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

import pandas as pd

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------
# PCC Inclusion criteria for scoping review
# --------------------------------------------------------------------------
PCC_CRITERIA = {
    "population": (
        "Learners or educators in formal/informal educational settings "
        "(K-12, higher education, adult education, professional development)."
    ),
    "concept": (
        "Explicitly discusses trust in AI or related constructs: trust, reliance, "
        "resistance, overtrust, distrust, calibration, over-reliance, under-reliance, "
        "appropriate reliance, trustworthiness (in AI context), credibility of AI."
    ),
    "context": (
        "AI-based educational tools: intelligent tutoring systems (ITS), AI chatbots, "
        "generative AI (ChatGPT, Copilot, etc.), AI agents, conversational agents, "
        "AI writing assistants, AI-powered learning platforms."
    ),
    "study_type": (
        "Empirical studies (quantitative, qualitative, mixed methods), conceptual papers "
        "with explicit framework, systematic/scoping reviews, meta-analyses. "
        "Exclude opinion/editorial pieces, conference abstracts without full text."
    ),
    "language": "English",
    "date_range": "2015-2026"
}

SCREENING_PROMPT = """You are a systematic review expert screening studies for a scoping review on "Trust in AI in Educational Contexts."

This is a SCOPING REVIEW using PCC (Population, Concept, Context) criteria, NOT a meta-analysis.

PCC INCLUSION CRITERIA:
1. Population: Learners or educators in formal/informal educational settings (K-12, higher ed, adult education, professional development).
2. Concept: Explicitly discusses trust in AI or related constructs: trust, reliance, resistance, overtrust, distrust, calibration, over-reliance, under-reliance, appropriate reliance, trustworthiness, credibility (in AI context).
3. Context: AI-based educational tools (ITS, chatbot, generative AI, AI agents, conversational agents, AI writing assistants, AI-powered learning platforms).
4. Study type: Empirical studies, conceptual papers with explicit framework, systematic/scoping reviews. NOT opinion pieces or abstracts-only.
5. Language: English
6. Date: 2015-2026

EXCLUSION CRITERIA:
- Non-educational populations (patients, consumers, general public in non-education contexts)
- Trust in human teachers only (no AI involvement)
- AI studies without trust/reliance/resistance discussion
- Opinion/editorial pieces, conference abstracts without full text
- Non-English, pre-2015

PRIORITY CANDIDATES (flag as INCLUDE even if borderline):
- Studies citing Wang et al. (2025) on trust in generative AI in education
- Studies citing Lee & See (2004) on trust in automation
- Studies citing de Visser et al. (2020) on trust calibration
- Studies explicitly discussing "trust calibration" or "appropriate trust"

Respond with ONLY this JSON object:
{
  "decision": "<INCLUDE | EXCLUDE | UNCERTAIN>",
  "confidence": "<high | moderate | low>",
  "rationale": "<2-3 sentences explaining decision>",
  "population_met": <true | false | null>,
  "concept_met": <true | false | null>,
  "context_met": <true | false | null>,
  "study_type_met": <true | false | null>,
  "primary_exclusion_reason": "<if EXCLUDE: E1-no trust concept | E2-non-educational | E3-no AI | E4-not substantive | E5-non-English | E6-pre-2015 | E7-duplicate; else null>",
  "priority_candidate": <true | false>,
  "calibration_mentioned": <true | false>
}"""


class SCRScreener:
    """Screens title/abstract records for scoping review inclusion using LLM."""

    def __init__(self, model: str = "claude-sonnet-4-5-20250929"):
        self.model = model
        self._init_client()

    def _init_client(self):
        try:
            from anthropic import Anthropic
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")
            self.client = Anthropic(api_key=api_key)
            logger.info(f"Initialized Claude client: {self.model}")
        except ImportError:
            raise ImportError("anthropic package required: pip install anthropic")

    def screen_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        title = record.get("title", "No title")
        abstract = record.get("abstract", "No abstract")
        year = record.get("year", "")
        authors = record.get("authors", "")

        user_msg = f"""TITLE: {title}

AUTHORS: {authors}
YEAR: {year}

ABSTRACT:
{abstract}

Based on the above, apply the PCC inclusion/exclusion criteria and return your decision as JSON."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.0,
                system=SCREENING_PROMPT,
                messages=[{"role": "user", "content": user_msg}]
            )

            content = response.content[0].text if response.content else ""

            try:
                decision = json.loads(content)
            except json.JSONDecodeError:
                if "```json" in content:
                    start = content.find("```json") + 7
                    end = content.find("```", start)
                    decision = json.loads(content[start:end])
                else:
                    decision = {
                        "decision": "UNCERTAIN",
                        "confidence": "low",
                        "rationale": "Parse error in AI response",
                        "parse_error": True
                    }

            decision["study_id"] = record.get("study_id", "")
            decision["title"] = title
            decision["screened_at"] = datetime.now().isoformat()
            decision["model"] = self.model

            return decision

        except Exception as e:
            logger.error(f"Screening failed for {record.get('study_id', '')}: {e}")
            return {
                "study_id": record.get("study_id", ""),
                "title": title,
                "decision": "UNCERTAIN",
                "confidence": "low",
                "rationale": f"Screening error: {str(e)}",
                "error": True
            }

    def screen_batch(self, records: List[Dict[str, Any]],
                     output_path: Path,
                     delay_seconds: float = 0.5) -> Dict[str, Any]:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        include_count = 0
        exclude_count = 0
        uncertain_count = 0
        priority_count = 0
        calibration_count = 0

        logger.info(f"Screening {len(records)} records with PCC criteria...")

        for i, record in enumerate(records):
            logger.info(f"Screening {i+1}/{len(records)}: {record.get('study_id', '')}")

            result = self.screen_record(record)

            with open(output_path, "a") as f:
                f.write(json.dumps(result) + "\n")

            decision = result.get("decision", "UNCERTAIN")
            if decision == "INCLUDE":
                include_count += 1
            elif decision == "EXCLUDE":
                exclude_count += 1
            else:
                uncertain_count += 1

            if result.get("priority_candidate"):
                priority_count += 1
            if result.get("calibration_mentioned"):
                calibration_count += 1

            if delay_seconds > 0 and i < len(records) - 1:
                time.sleep(delay_seconds)

        summary = {
            "total_screened": len(records),
            "include": include_count,
            "exclude": exclude_count,
            "uncertain": uncertain_count,
            "priority_candidates": priority_count,
            "calibration_mentioned": calibration_count,
            "inclusion_rate": round(include_count / len(records), 3) if records else 0
        }

        logger.info(f"Screening complete: {summary}")
        return summary

    def export_decisions_csv(self, jsonl_path: Path, output_csv: Path):
        records = []
        with open(jsonl_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))

        df = pd.DataFrame(records)
        cols = [
            "study_id", "title", "decision", "confidence", "rationale",
            "population_met", "concept_met", "context_met", "study_type_met",
            "primary_exclusion_reason", "priority_candidate",
            "calibration_mentioned", "screened_at"
        ]
        available_cols = [c for c in cols if c in df.columns]
        df[available_cols].to_csv(output_csv, index=False)
        logger.info(f"Decisions exported to {output_csv}")


def main():
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser(
        description="AI-assisted PCC screening for scoping review"
    )
    parser.add_argument("--input", required=True,
                        help="Input CSV with deduplicated records")
    parser.add_argument("--output", default="../data/02_screened",
                        help="Output directory")
    parser.add_argument("--id-col", default="study_id",
                        help="Column name for study ID")
    parser.add_argument("--title-col", default="title",
                        help="Column name for title")
    parser.add_argument("--abstract-col", default="abstract",
                        help="Column name for abstract")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250929",
                        help="LLM model for screening")

    args = parser.parse_args()

    df = pd.read_csv(args.input)
    logger.info(f"Loaded {len(df)} records from {args.input}")

    records = []
    for _, row in df.iterrows():
        records.append({
            "study_id": str(row.get(args.id_col, "")),
            "title": str(row.get(args.title_col, "")),
            "abstract": str(row.get(args.abstract_col, "")),
            "authors": str(row.get("authors", "")),
            "year": str(row.get("year", ""))
        })

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path(__file__).resolve().parent.parent / args.output

    output_path.mkdir(parents=True, exist_ok=True)

    screener = SCRScreener(model=args.model)
    results_jsonl = output_path / "screening_decisions.jsonl"
    summary = screener.screen_batch(records, results_jsonl)

    results_csv = output_path / "screening_decisions.csv"
    screener.export_decisions_csv(results_jsonl, results_csv)

    summary_path = output_path / "screening_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nScoping Review Screening Complete!")
    print(f"Include:   {summary['include']}")
    print(f"Exclude:   {summary['exclude']}")
    print(f"Uncertain: {summary['uncertain']}")
    print(f"Priority candidates: {summary['priority_candidates']}")
    print(f"Calibration mentioned: {summary['calibration_mentioned']}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
