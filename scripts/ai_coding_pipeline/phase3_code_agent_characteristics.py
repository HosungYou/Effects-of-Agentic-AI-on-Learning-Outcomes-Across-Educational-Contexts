#!/usr/bin/env python3
"""
Phase 3: Code AI Agent Characteristics
Code oversight level, architecture, agency (APCP), role, modality, technology, adaptivity.
Uses Claude Sonnet with RAG for extraction.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from phase0_rag_index import RAGIndexBuilder
from utils.llm_clients import ClaudeClient

logger = logging.getLogger(__name__)

# Valid codes per characteristic (must match config.yaml)
VALID_CODES = {
    'oversight_level': ['fully_autonomous', 'ai_led_with_checkpoints', 'human_led_with_ai_support'],
    'architecture': ['single_agent', 'multi_agent'],
    'agency_level': ['adaptive', 'proactive', 'co_learner', 'peer'],
    'role': ['tutor', 'coach', 'assessor', 'collaborator', 'facilitator'],
    'modality': ['text_only', 'voice', 'embodied', 'mixed'],
    'technology': ['rule_based', 'ml', 'nlp', 'llm', 'rl'],
    'adaptivity': ['static', 'adaptive_performance', 'adaptive_behavior_affect']
}


class AgentCharacteristicsCoder:
    """Codes AI agent characteristics from research papers."""

    def __init__(self, config: Dict[str, Any], cost_tracker, audit_logger):
        self.config = config
        self.cost_tracker = cost_tracker
        self.audit_logger = audit_logger

        self.rag = RAGIndexBuilder(config)
        self.claude = ClaudeClient(
            model=config['models']['claude']['model'],
            cost_tracker=cost_tracker
        )

        prompt_path = Path(config['paths']['prompts']) / 'agent_classification.txt'
        with open(prompt_path, 'r') as f:
            self.coding_prompt = f.read()

    def query_relevant_chunks(self, study_id: str, n_chunks: int = 8) -> List[str]:
        """
        Query RAG index for agent-characteristic-relevant chunks.

        Args:
            study_id: Study identifier
            n_chunks: Number of chunks to retrieve per query

        Returns:
            Deduplicated list of relevant text chunks
        """
        queries = [
            f"{study_id} AI agent system autonomous intelligent",
            f"{study_id} human oversight control interaction feedback",
            f"{study_id} agent architecture multi single pipeline",
            f"{study_id} tutor coach assessor collaborator role",
            f"{study_id} adaptive personalized voice embodied text",
            f"{study_id} large language model GPT reinforcement learning NLP"
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

    def validate_codes(self, coded: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted codes against allowed values.

        Args:
            coded: Raw coded characteristics

        Returns:
            Validated characteristics with flags for invalid codes
        """
        validated = {}
        issues = []

        for field, allowed in VALID_CODES.items():
            value = coded.get(field)

            if value is None:
                validated[field] = None
                issues.append(f"Missing field: {field}")
            elif isinstance(value, list):
                # Multi-select fields
                invalid = [v for v in value if v not in allowed]
                if invalid:
                    issues.append(f"Invalid {field} codes: {invalid}")
                validated[field] = value
            else:
                if value not in allowed:
                    issues.append(f"Invalid {field} code: {value} (allowed: {allowed})")
                    validated[field] = None
                else:
                    validated[field] = value

        validated['validation_issues'] = issues
        validated['validation_passed'] = len(issues) == 0
        return validated

    def code_study(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Code AI agent characteristics for a single study.

        Args:
            pdf_path: Path to study PDF

        Returns:
            Coding result with validated agent characteristics
        """
        study_id = pdf_path.stem
        logger.info(f"Coding agent characteristics for: {study_id}")

        relevant_chunks = self.query_relevant_chunks(study_id)

        if not relevant_chunks:
            logger.warning(f"No relevant chunks found for {study_id}")
            return {
                'study_id': study_id,
                'status': 'no_chunks',
                'agent_characteristics': {}
            }

        context = "\n\n---CHUNK BREAK---\n\n".join(relevant_chunks)

        user_prompt = f"""Study ID: {study_id}

RELEVANT EXCERPTS FROM THE PAPER:
{context}

Code the AI agent characteristics following the system instructions. Respond with valid JSON only."""

        start_time = datetime.now()
        response = self.claude.send_prompt(
            system=self.coding_prompt,
            user=user_prompt,
            temperature=0.0,
            max_tokens=2048
        )
        coding_time = (datetime.now() - start_time).total_seconds()

        try:
            coded_data = json.loads(response['content'])
        except json.JSONDecodeError:
            if '```json' in response['content']:
                json_start = response['content'].find('```json') + 7
                json_end = response['content'].find('```', json_start)
                try:
                    coded_data = json.loads(response['content'][json_start:json_end])
                except Exception:
                    coded_data = {'parse_error': True}
            else:
                coded_data = {'parse_error': True}

        # Validate codes
        validated = self.validate_codes(coded_data)

        result = {
            'study_id': study_id,
            'source_file': pdf_path.name,
            'coding_timestamp': datetime.now().isoformat(),
            'coding_time_seconds': coding_time,
            'model': self.config['models']['claude']['model'],
            'n_chunks_used': len(relevant_chunks),
            'tokens_input': response.get('input_tokens', 0),
            'tokens_output': response.get('output_tokens', 0),
            'status': 'success' if not coded_data.get('parse_error') else 'parse_error',
            'agent_characteristics': validated,
            'raw_response': coded_data,
            'coding_rationale': coded_data.get('rationale', '')
        }

        self.audit_logger.log_extraction(
            study_id=study_id,
            phase='phase3',
            field='agent_characteristics',
            value=validated,
            confidence=coded_data.get('confidence', 'unknown'),
            model=self.config['models']['claude']['model'],
            tokens=response.get('input_tokens', 0) + response.get('output_tokens', 0)
        )

        return result

    def code_all(self, pdf_dir: Path, output_dir: Path) -> Dict[str, Any]:
        """
        Code agent characteristics for all PDFs.

        Args:
            pdf_dir: Directory containing PDF files
            output_dir: Directory to save coding results

        Returns:
            Summary statistics
        """
        pdf_files = list(pdf_dir.glob("*.pdf"))
        logger.info(f"Coding {len(pdf_files)} studies for agent characteristics")

        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        successful = 0
        failed = 0
        validation_failures = 0

        for pdf_path in pdf_files:
            try:
                result = self.code_study(pdf_path)

                output_path = output_dir / f"{pdf_path.stem}_agent_codes.json"
                with open(output_path, 'w') as f:
                    json.dump(result, f, indent=2)

                results.append(result)

                if result['status'] == 'success':
                    successful += 1
                    if not result['agent_characteristics'].get('validation_passed', True):
                        validation_failures += 1
                else:
                    failed += 1

            except Exception as e:
                logger.error(f"Failed to code {pdf_path.name}: {e}", exc_info=True)
                failed += 1
                results.append({'study_id': pdf_path.stem, 'status': 'error', 'error': str(e)})

        summary = {
            'n_studies_processed': len(pdf_files),
            'n_successful': successful,
            'n_failed': failed,
            'n_validation_failures': validation_failures
        }

        summary_path = output_dir / 'agent_coding_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        all_results_path = output_dir / 'all_agent_codes.json'
        with open(all_results_path, 'w') as f:
            json.dump(results, f, indent=2)

        return summary


def code_agent_characteristics(config: Dict[str, Any], cost_tracker,
                                audit_logger) -> Dict[str, Any]:
    """
    Phase 3 entry point: Code AI agent characteristics.

    Args:
        config: Pipeline configuration
        cost_tracker: Cost tracking instance
        audit_logger: Audit logging instance

    Returns:
        Result dictionary with success status and statistics
    """
    logger.info("Starting Phase 3: AI Agent Characteristic Coding")

    try:
        coder = AgentCharacteristicsCoder(config, cost_tracker, audit_logger)

        pdf_dir = Path(config['paths']['pdfs'])
        output_dir = Path(config['paths']['extracted']) / 'agent_codes'

        summary = coder.code_all(pdf_dir, output_dir)
        logger.info(f"Phase 3 complete: {summary}")

        return {
            'success': True,
            'summary': summary,
            'output_path': str(output_dir)
        }

    except Exception as e:
        logger.error(f"Phase 3 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import yaml
    from utils.cost_tracker import CostTracker
    from utils.audit import AuditLogger

    with open('scripts/ai_coding_pipeline/config.yaml') as f:
        config = yaml.safe_load(f)

    result = code_agent_characteristics(
        config,
        CostTracker(),
        AuditLogger(config['paths']['logs'])
    )

    print(json.dumps(result, indent=2))
