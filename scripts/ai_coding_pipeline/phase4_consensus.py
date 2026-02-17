#!/usr/bin/env python3
"""
Phase 4: Three-Model Consensus
Run Claude, GPT-4o, and Groq independently on extracted data and synthesize consensus.
Adapted for effect size and agent characteristic verification.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import Counter

from utils.llm_clients import ClaudeClient, GPT4oClient, GroqClient

logger = logging.getLogger(__name__)


class ConsensusBuilder:
    """Builds consensus across three LLM models for extracted effect size data."""

    def __init__(self, config: Dict[str, Any], cost_tracker, audit_logger):
        self.config = config
        self.cost_tracker = cost_tracker
        self.audit_logger = audit_logger

        self.claude = ClaudeClient(
            model=config['models']['claude']['model'],
            cost_tracker=cost_tracker
        )
        self.gpt4o = GPT4oClient(
            model=config['models']['gpt4o']['model'],
            cost_tracker=cost_tracker
        )
        self.groq = GroqClient(
            model=config['models']['groq']['model'],
            cost_tracker=cost_tracker
        )

        self.models = {
            'claude': self.claude,
            'gpt4o': self.gpt4o,
            'groq': self.groq
        }

    def verify_with_model(self, model_name: str, study_data: Dict[str, Any],
                          prompt_template: str) -> Dict[str, Any]:
        """
        Verify extracted data using a specific model.

        Args:
            model_name: Name of model to use
            study_data: Merged study data (study info + effect sizes + agent codes)
            prompt_template: System prompt for verification

        Returns:
            Verification result from the model
        """
        model = self.models[model_name]

        user_prompt = f"""Study ID: {study_data['study_id']}

Extracted Study Information:
{json.dumps(study_data.get('study_info', {}), indent=2)}

Extracted Effect Sizes:
{json.dumps(study_data.get('effect_sizes', []), indent=2)}

Extracted Agent Characteristics:
{json.dumps(study_data.get('agent_characteristics', {}), indent=2)}

Please verify and validate this extracted data. Respond with a JSON object containing:
{{
  "verified_effect_sizes": [list of verified effect size objects with hedges_g and se_g],
  "verified_agent_characteristics": {{coded characteristics object}},
  "verified_study_info": {{study info object}},
  "confidence": "high|moderate|low",
  "concerns": [list of concerns or flags],
  "suggested_corrections": [list of suggested corrections]
}}"""

        response = model.send_prompt(
            system=prompt_template,
            user=user_prompt,
            temperature=0.0,
            max_tokens=4096
        )

        try:
            result = json.loads(response['content'])
        except json.JSONDecodeError:
            if '```json' in response['content']:
                json_start = response['content'].find('```json') + 7
                json_end = response['content'].find('```', json_start)
                try:
                    result = json.loads(response['content'][json_start:json_end])
                except Exception:
                    result = {'error': 'Failed to parse', 'raw_response': response['content'][:500]}
            else:
                result = {'error': 'Failed to parse', 'raw_response': response['content'][:500]}

        result['model'] = model_name
        result['tokens_used'] = response.get('input_tokens', 0) + response.get('output_tokens', 0)
        return result

    def build_consensus(self, study_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build consensus across three models for a single study.

        Args:
            study_data: Merged study data dictionary

        Returns:
            Consensus result with agreement statistics
        """
        study_id = study_data['study_id']
        logger.info(f"Building consensus for study: {study_id}")

        # Verification system prompt
        verification_prompt = (
            "You are an expert meta-analyst verifying extracted data from educational research papers. "
            "Check effect sizes for plausibility (|g| < 5.0), verify sample sizes are reasonable "
            "(n >= 10), confirm agent characteristic codes are valid, and flag any inconsistencies. "
            "Respond only with valid JSON."
        )

        model_results = {}
        for model_name in ['claude', 'gpt4o', 'groq']:
            try:
                result = self.verify_with_model(model_name, study_data, verification_prompt)
                model_results[model_name] = result

                self.audit_logger.log_extraction(
                    study_id=study_id,
                    phase='phase4',
                    field='consensus_verification',
                    value=result.get('verified_effect_sizes', []),
                    confidence=result.get('confidence', 'unknown'),
                    model=model_name,
                    tokens=result.get('tokens_used', 0)
                )

            except Exception as e:
                logger.error(f"Model {model_name} failed for {study_id}: {e}")
                model_results[model_name] = {'error': str(e)}

        agreement_analysis = self._analyze_agreement(model_results)
        consensus_effects = self._synthesize_effect_sizes(model_results)
        consensus_agent = self._synthesize_agent_characteristics(model_results)

        return {
            'study_id': study_id,
            'consensus_timestamp': datetime.now().isoformat(),
            'model_results': model_results,
            'agreement_analysis': agreement_analysis,
            'consensus_effect_sizes': consensus_effects,
            'consensus_agent_characteristics': consensus_agent,
            'original_data': study_data
        }

    def _analyze_agreement(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze agreement between the three models.

        Args:
            model_results: Results from all three models

        Returns:
            Agreement analysis dictionary
        """
        successful_models = [
            name for name, r in model_results.items() if 'error' not in r
        ]

        confidences = [
            model_results[m].get('confidence') for m in successful_models
            if model_results[m].get('confidence')
        ]

        concern_counts = sum(
            len(model_results[m].get('concerns', [])) for m in successful_models
        )

        return {
            'n_models_completed': len(successful_models),
            'models_completed': successful_models,
            'confidence_values': confidences,
            'modal_confidence': Counter(confidences).most_common(1)[0][0] if confidences else None,
            'total_concerns_raised': concern_counts,
            'high_confidence': all(c == 'high' for c in confidences) if confidences else False
        }

    def _synthesize_effect_sizes(self, model_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Synthesize consensus effect sizes from model results.
        Uses majority-vote on validity; averages numeric values when 2+ models agree.

        Args:
            model_results: Results from all models

        Returns:
            List of consensus effect size records
        """
        # Collect effect sizes by outcome label
        label_effects: Dict[str, List[Dict]] = {}

        for model_name, result in model_results.items():
            if 'error' in result:
                continue
            for es in result.get('verified_effect_sizes', []):
                label = es.get('outcome_label', 'unknown')
                if label not in label_effects:
                    label_effects[label] = []
                label_effects[label].append({
                    'model': model_name,
                    'hedges_g': es.get('hedges_g'),
                    'se_g': es.get('se_g'),
                    'valid': es.get('conversion_valid', True)
                })

        consensus = []
        for label, values in label_effects.items():
            n_models = len(values)
            valid_values = [v for v in values if v.get('hedges_g') is not None]

            if not valid_values:
                continue

            g_values = [v['hedges_g'] for v in valid_values]
            se_values = [v['se_g'] for v in valid_values if v.get('se_g') is not None]

            g_consensus = sum(g_values) / len(g_values)
            se_consensus = sum(se_values) / len(se_values) if se_values else None

            if n_models == 3:
                quality = '3/3_agree'
                flag = None
            elif n_models == 2:
                quality = '2/3_agree'
                flag = 'majority_consensus'
            else:
                quality = '1/3_only'
                flag = 'human_review_needed'

            consensus.append({
                'outcome_label': label,
                'hedges_g_consensus': round(g_consensus, 4),
                'se_g_consensus': round(se_consensus, 4) if se_consensus else None,
                'g_values_per_model': g_values,
                'n_models_agree': n_models,
                'consensus_quality': quality,
                'flag': flag
            })

        return consensus

    def _synthesize_agent_characteristics(self, model_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize consensus agent characteristics using majority vote.

        Args:
            model_results: Results from all models

        Returns:
            Consensus agent characteristics dictionary
        """
        fields = [
            'oversight_level', 'architecture', 'agency_level',
            'role', 'modality', 'technology', 'adaptivity'
        ]

        consensus = {}
        for field in fields:
            values = []
            for result in model_results.values():
                if 'error' in result:
                    continue
                agent = result.get('verified_agent_characteristics', {})
                val = agent.get(field)
                if val is not None:
                    values.append(val if not isinstance(val, list) else tuple(sorted(val)))

            if not values:
                consensus[field] = None
                continue

            most_common, count = Counter(values).most_common(1)[0]
            consensus[field] = list(most_common) if isinstance(most_common, tuple) else most_common
            consensus[f"{field}_agreement"] = f"{count}/{len(values)}"

        return consensus

    def process_all_studies(self, extracted_dir: Path,
                           output_dir: Path) -> Dict[str, Any]:
        """
        Build consensus for all extracted studies.

        Args:
            extracted_dir: Directory with phase1-3 extraction results
            output_dir: Directory to save consensus results

        Returns:
            Summary statistics
        """
        # Load and merge extracted data per study
        study_info_dir = extracted_dir / 'study_info'
        effect_sizes_dir = extracted_dir / 'effect_sizes'
        agent_codes_dir = extracted_dir / 'agent_codes'

        study_ids = set()
        for d in [study_info_dir, effect_sizes_dir, agent_codes_dir]:
            if d.exists():
                for f in d.glob("*.json"):
                    stem = f.stem.replace('_study_info', '').replace(
                        '_effects', '').replace('_agent_codes', '')
                    study_ids.add(stem)

        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for study_id in study_ids:
            # Load all available data for this study
            study_data = {'study_id': study_id}

            info_path = study_info_dir / f"{study_id}_study_info.json"
            if info_path.exists():
                with open(info_path) as f:
                    study_data['study_info'] = json.load(f)

            es_path = effect_sizes_dir / f"{study_id}_effects.json"
            if es_path.exists():
                with open(es_path) as f:
                    es_data = json.load(f)
                    study_data['effect_sizes'] = es_data.get('effect_sizes', [])

            agent_path = agent_codes_dir / f"{study_id}_agent_codes.json"
            if agent_path.exists():
                with open(agent_path) as f:
                    agent_data = json.load(f)
                    study_data['agent_characteristics'] = agent_data.get(
                        'agent_characteristics', {}
                    )

            try:
                consensus_result = self.build_consensus(study_data)

                output_path = output_dir / f"{study_id}_consensus.json"
                with open(output_path, 'w') as f:
                    json.dump(consensus_result, f, indent=2)

                results.append(consensus_result)

            except Exception as e:
                logger.error(f"Consensus failed for {study_id}: {e}", exc_info=True)

        summary = {
            'n_studies_processed': len(results),
            'n_three_model_complete': sum(
                1 for r in results
                if r.get('agreement_analysis', {}).get('n_models_completed', 0) == 3
            )
        }

        summary_path = output_dir / 'consensus_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        return summary


def run_consensus(config: Dict[str, Any], cost_tracker, audit_logger) -> Dict[str, Any]:
    """
    Phase 4 entry point: Run three-model consensus.

    Args:
        config: Pipeline configuration
        cost_tracker: Cost tracking instance
        audit_logger: Audit logging instance

    Returns:
        Result dictionary with success status and statistics
    """
    logger.info("Starting Phase 4: Three-Model Consensus")

    try:
        builder = ConsensusBuilder(config, cost_tracker, audit_logger)

        extracted_dir = Path(config['paths']['extracted'])
        output_dir = Path(config['paths']['verified'])

        summary = builder.process_all_studies(extracted_dir, output_dir)
        logger.info(f"Phase 4 complete: {summary}")

        return {
            'success': True,
            'summary': summary,
            'output_path': str(output_dir)
        }

    except Exception as e:
        logger.error(f"Phase 4 failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    import yaml
    from utils.cost_tracker import CostTracker
    from utils.audit import AuditLogger

    with open('scripts/ai_coding_pipeline/config.yaml') as f:
        config = yaml.safe_load(f)

    result = run_consensus(
        config,
        CostTracker(),
        AuditLogger(config['paths']['logs'])
    )

    print(json.dumps(result, indent=2))
