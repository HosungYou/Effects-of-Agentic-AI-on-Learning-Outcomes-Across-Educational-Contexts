#!/usr/bin/env python3
"""
Phase 2: Extract Effect Sizes
Extract M, SD, n for treatment/control or pre/post groups, plus pre-computed d/g values.
Converts all reported statistics to Hedges' g with standard errors.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from phase0_rag_index import RAGIndexBuilder
from utils.llm_clients import ClaudeClient
from utils.pdf_processor import PDFProcessor
from utils.effect_size_calculator import EffectSizeCalculator

logger = logging.getLogger(__name__)


class EffectSizeExtractor:
    """Extracts effect size data from research papers using Claude + RAG."""

    def __init__(self, config: Dict[str, Any], cost_tracker, audit_logger):
        self.config = config
        self.cost_tracker = cost_tracker
        self.audit_logger = audit_logger

        self.rag = RAGIndexBuilder(config)
        self.claude = ClaudeClient(
            model=config['models']['claude']['model'],
            cost_tracker=cost_tracker
        )
        self.pdf_processor = PDFProcessor()
        self.calculator = EffectSizeCalculator()

        prompt_path = Path(config['paths']['prompts']) / 'effect_size_extraction.txt'
        with open(prompt_path, 'r') as f:
            self.extraction_prompt = f.read()

    def query_relevant_chunks(self, study_id: str, n_chunks: int = 8) -> List[str]:
        """
        Query RAG index for effect-size-relevant chunks.

        Args:
            study_id: Study identifier
            n_chunks: Number of chunks to retrieve per query

        Returns:
            List of relevant text chunks
        """
        queries = [
            f"{study_id} mean standard deviation sample size results",
            f"{study_id} treatment control group pre post test scores",
            f"{study_id} effect size Cohen Hedges t-statistic F-statistic",
            f"{study_id} table descriptive statistics performance scores",
            f"{study_id} learning outcome achievement test improvement"
        ]

        all_chunks = []
        for query in queries:
            chunks = self.rag.query(query, n_results=n_chunks)
            all_chunks.extend(chunks)

        unique_chunks = {chunk['id']: chunk for chunk in all_chunks}

        sorted_chunks = sorted(
            unique_chunks.values(),
            key=lambda x: x.get('distance', float('inf'))
        )

        return [chunk['text'] for chunk in sorted_chunks[:n_chunks * 2]]

    def extract_from_study(self, pdf_path: Path, study_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract effect size data from a single study.

        Args:
            pdf_path: Path to study PDF
            study_info: Previously extracted study characteristics

        Returns:
            Extraction result with effect sizes converted to Hedges' g
        """
        study_id = pdf_path.stem
        logger.info(f"Extracting effect sizes from: {study_id}")

        # Get tables directly for numeric precision
        tables = self.pdf_processor.find_effect_size_tables(pdf_path)
        table_text = ""
        if tables:
            table_text = "\n\nEXTRACTED TABLES:\n"
            for tbl in tables[:5]:  # limit to 5 most relevant tables
                table_text += f"\n[Page {tbl['page']}, Table {tbl['table_index']+1}]\n"
                for row in tbl['table_data']:
                    table_text += "\t".join(str(c) if c else "" for c in row) + "\n"

        relevant_chunks = self.query_relevant_chunks(study_id)

        if not relevant_chunks and not tables:
            logger.warning(f"No relevant content found for {study_id}")
            return {
                'study_id': study_id,
                'status': 'no_content',
                'effect_sizes': []
            }

        context = "\n\n---CHUNK BREAK---\n\n".join(relevant_chunks)
        design_type = study_info.get('design_type', 'unknown')

        user_prompt = f"""Study ID: {study_id}
Study Design: {design_type}

RELEVANT EXCERPTS FROM THE PAPER:
{context}
{table_text}

Extract all effect size data following the system instructions. Return valid JSON only."""

        start_time = datetime.now()
        response = self.claude.send_prompt(
            system=self.extraction_prompt,
            user=user_prompt,
            temperature=0.0,
            max_tokens=4096
        )
        extraction_time = (datetime.now() - start_time).total_seconds()

        try:
            extracted_data = json.loads(response['content'])
        except json.JSONDecodeError:
            if '```json' in response['content']:
                json_start = response['content'].find('```json') + 7
                json_end = response['content'].find('```', json_start)
                try:
                    extracted_data = json.loads(response['content'][json_start:json_end])
                except Exception:
                    extracted_data = {'raw_effects': [], 'parse_error': True}
            else:
                extracted_data = {'raw_effects': [], 'parse_error': True}

        # Convert all raw effects to Hedges' g
        raw_effects = extracted_data.get('raw_effects', [])
        converted_effects = []

        for raw in raw_effects:
            conversion = self.calculator.extract_effect_size(raw)
            converted = {
                **raw,
                'hedges_g': conversion.get('g'),
                'se_g': conversion.get('se'),
                'conversion_method': conversion.get('method'),
                'ci_95': conversion.get('ci_95'),
                'conversion_valid': conversion.get('valid', False),
                'conversion_issues': conversion.get('issues', [])
            }
            converted_effects.append(converted)

            # Audit log each effect size
            if conversion.get('g') is not None:
                self.audit_logger.log_effect_size(
                    study_id=study_id,
                    outcome_label=raw.get('outcome_label', 'unknown'),
                    g=conversion['g'],
                    se=conversion.get('se', 0),
                    method=conversion.get('method', 'unknown'),
                    model=self.config['models']['claude']['model'],
                    raw_data=raw
                )

        result = {
            'study_id': study_id,
            'source_file': pdf_path.name,
            'extraction_timestamp': datetime.now().isoformat(),
            'extraction_time_seconds': extraction_time,
            'model': self.config['models']['claude']['model'],
            'n_chunks_used': len(relevant_chunks),
            'n_tables_used': len(tables),
            'tokens_input': response.get('input_tokens', 0),
            'tokens_output': response.get('output_tokens', 0),
            'status': 'success' if not extracted_data.get('parse_error') else 'parse_error',
            'n_effects_extracted': len(converted_effects),
            'effect_sizes': converted_effects,
            'extraction_notes': extracted_data.get('notes', '')
        }

        return result

    def extract_all(self, pdf_dir: Path, study_info_dir: Path,
                   output_dir: Path) -> Dict[str, Any]:
        """
        Extract effect sizes from all PDFs.

        Args:
            pdf_dir: Directory containing PDFs
            study_info_dir: Directory with phase1 study info JSON files
            output_dir: Directory to save extraction results

        Returns:
            Summary statistics
        """
        pdf_files = list(pdf_dir.glob("*.pdf"))
        logger.info(f"Processing {len(pdf_files)} PDFs for effect sizes")

        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        successful = 0
        failed = 0
        total_effects = 0

        for pdf_path in pdf_files:
            # Load study info if available
            info_path = study_info_dir / f"{pdf_path.stem}_study_info.json"
            study_info = {}
            if info_path.exists():
                with open(info_path, 'r') as f:
                    study_info = json.load(f)

            try:
                result = self.extract_from_study(pdf_path, study_info)

                output_path = output_dir / f"{pdf_path.stem}_effects.json"
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)

                results.append(result)

                if result['status'] == 'success':
                    successful += 1
                    total_effects += result.get('n_effects_extracted', 0)
                else:
                    failed += 1

            except Exception as e:
                logger.error(f"Failed to process {pdf_path.name}: {e}", exc_info=True)
                failed += 1
                results.append({
                    'study_id': pdf_path.stem,
                    'status': 'error',
                    'error': str(e)
                })

        summary = {
            'n_studies_processed': len(pdf_files),
            'n_successful': successful,
            'n_failed': failed,
            'total_effects_extracted': total_effects,
            'avg_effects_per_study': round(total_effects / successful, 2) if successful > 0 else 0
        }

        summary_path = output_dir / 'effect_size_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        all_results_path = output_dir / 'all_effect_sizes.json'
        with open(all_results_path, 'w') as f:
            json.dump(results, f, indent=2)

        return summary


def extract_effect_sizes(config: Dict[str, Any], cost_tracker, audit_logger) -> Dict[str, Any]:
    """
    Phase 2 entry point: Extract effect sizes from all studies.

    Args:
        config: Pipeline configuration
        cost_tracker: Cost tracking instance
        audit_logger: Audit logging instance

    Returns:
        Result dictionary with success status and statistics
    """
    logger.info("Starting Phase 2: Effect Size Extraction")

    try:
        extractor = EffectSizeExtractor(config, cost_tracker, audit_logger)

        pdf_dir = Path(config['paths']['pdfs'])
        study_info_dir = Path(config['paths']['extracted']) / 'study_info'
        output_dir = Path(config['paths']['extracted']) / 'effect_sizes'

        summary = extractor.extract_all(pdf_dir, study_info_dir, output_dir)
        logger.info(f"Phase 2 complete: {summary}")

        return {
            'success': True,
            'summary': summary,
            'output_path': str(output_dir)
        }

    except Exception as e:
        logger.error(f"Phase 2 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import yaml
    from utils.cost_tracker import CostTracker
    from utils.audit import AuditLogger

    with open('scripts/ai_coding_pipeline/config.yaml') as f:
        config = yaml.safe_load(f)

    result = extract_effect_sizes(
        config,
        CostTracker(),
        AuditLogger(config['paths']['logs'])
    )

    print(json.dumps(result, indent=2))
