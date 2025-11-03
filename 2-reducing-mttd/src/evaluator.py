"""
Evaluation functions for LLM-generated incident enrichments.
"""

import json
import re
import os
from typing import Dict, List, Optional, Tuple
import numpy as np
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class IncidentEnrichmentEvaluator:
    """
    Evaluator for assessing quality of LLM-generated incident enrichments.
    """
    
    def __init__(self, embedding_model: Optional[str] = None):
        """
        Initialize the evaluator with required models.
        
        Args:
            embedding_model: Name of the sentence transformer model to use.
                           Defaults to 'BAAI/bge-small-en-v1.5' (recommended)
                           or can be set via EMBEDDING_MODEL environment variable.
        """
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        
        # Model selection: Use BGE-small-en-v1.5 for best accuracy/speed balance
        default_model = 'BAAI/bge-small-en-v1.5'
        model_name = embedding_model or os.getenv('EMBEDDING_MODEL', default_model)
        
        try:
            self.sentence_model = SentenceTransformer(model_name)
            print(f"Loaded embedding model: {model_name}")
        except Exception as e:
            print(f"Warning: Could not load sentence transformer model: {e}")
            print(f"Falling back to default: {default_model}")
            try:
                self.sentence_model = SentenceTransformer(default_model)
            except Exception as e2:
                print(f"Error loading default model: {e2}")
                self.sentence_model = None
    
    def evaluate_with_ground_truth(
        self, 
        generated: str, 
        ground_truth: str
    ) -> Dict[str, float]:
        """
        Evaluate generated text against ground truth using multiple metrics.
        
        Args:
            generated: LLM-generated enrichment text
            ground_truth: Reference ground truth text (e.g., close_notes)
            
        Returns:
            Dictionary with evaluation metrics
        """
        metrics = {}
        
        # ROUGE scores
        rouge_scores = self.rouge_scorer.score(ground_truth, generated)
        metrics['rouge1'] = rouge_scores['rouge1'].fmeasure
        metrics['rouge2'] = rouge_scores['rouge2'].fmeasure
        metrics['rougeL'] = rouge_scores['rougeL'].fmeasure
        
        # Semantic similarity (if model available)
        if self.sentence_model:
            try:
                gen_embedding = self.sentence_model.encode([generated])
                gt_embedding = self.sentence_model.encode([ground_truth])
                similarity = cosine_similarity(gen_embedding, gt_embedding)[0][0]
                metrics['semantic_similarity'] = float(similarity)
            except Exception as e:
                print(f"Warning: Could not compute semantic similarity: {e}")
                metrics['semantic_similarity'] = None
        
        return metrics
    
    def evaluate_json_structure(self, generated_text: str) -> Dict[str, any]:
        """
        Evaluate if generated text is valid JSON and contains required fields.
        
        Args:
            generated_text: LLM-generated text (should be JSON)
            
        Returns:
            Dictionary with structure evaluation metrics
        """
        result = {
            'is_valid_json': False,
            'has_required_fields': False,
            'missing_fields': [],
            'parsed_json': None
        }
        
        required_fields = [
            'detailed_description',
            'root_cause',
            'resolution_steps',
            'priority',
            'recommended_assignment_group'
        ]
        
        # Try to extract JSON from text (might have extra text)
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', generated_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = generated_text
        
        try:
            parsed = json.loads(json_str)
            result['is_valid_json'] = True
            result['parsed_json'] = parsed
            
            # Check for required fields
            missing = [field for field in required_fields if field not in parsed]
            result['missing_fields'] = missing
            result['has_required_fields'] = len(missing) == 0
            
        except json.JSONDecodeError:
            result['is_valid_json'] = False
        
        return result
    
    def evaluate_specificity(self, generated_text: str) -> Dict[str, any]:
        """
        Evaluate specificity of generated text (avoid vague statements).
        
        Args:
            generated_text: LLM-generated enrichment text
            
        Returns:
            Dictionary with specificity metrics
        """
        vague_phrases = [
            'might be', 'could be', 'possibly', 'maybe', 'unclear',
            'unknown', 'not sure', 'needs investigation', 'various',
            'some issues', 'certain problems'
        ]
        
        text_lower = generated_text.lower()
        vague_count = sum(1 for phrase in vague_phrases if phrase in text_lower)
        
        # Check for specific technical terms (indicator of specificity)
        technical_indicators = [
            'error code', 'exception', 'timeout', 'configuration',
            'cache', 'database', 'network', 'protocol', 'version',
            'log', 'trace', 'debug'
        ]
        technical_count = sum(1 for term in technical_indicators if term in text_lower)
        
        # Check word count (more words might indicate more detail)
        word_count = len(generated_text.split())
        
        return {
            'vague_phrases_count': vague_count,
            'technical_indicators_count': technical_count,
            'word_count': word_count,
            'specificity_score': max(0, min(1, (technical_count * 0.1 - vague_count * 0.2 + word_count / 200)))
        }
    
    def evaluate_actionability(self, generated_text: str) -> Dict[str, any]:
        """
        Evaluate how actionable the generated resolution steps are.
        
        Args:
            generated_text: LLM-generated enrichment text
            
        Returns:
            Dictionary with actionability metrics
        """
        action_verbs = [
            'restart', 'check', 'verify', 'update', 'install', 'configure',
            'clear', 'delete', 'restore', 'reset', 'reinstall', 'upgrade',
            'review', 'analyze', 'test', 'run', 'execute'
        ]
        
        text_lower = generated_text.lower()
        action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        
        # Check for numbered steps or bullet points
        has_numbered_steps = bool(re.search(r'\d+\.\s', generated_text))
        has_bullet_points = bool(re.search(r'[-•*]\s', generated_text))
        
        # Check for step indicators
        step_indicators = ['step', 'action', 'procedure', 'process']
        has_step_indicators = any(indicator in text_lower for indicator in step_indicators)
        
        return {
            'action_verbs_count': action_verb_count,
            'has_numbered_steps': has_numbered_steps,
            'has_bullet_points': has_bullet_points,
            'has_step_indicators': has_step_indicators,
            'actionability_score': min(1.0, (action_verb_count * 0.2 + 
                                              (1 if has_numbered_steps else 0) * 0.3 +
                                              (1 if has_step_indicators else 0) * 0.5))
        }
    
    def comprehensive_evaluation(
        self, 
        generated: str, 
        ground_truth: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Perform comprehensive evaluation of generated enrichment.
        
        Args:
            generated: LLM-generated enrichment text
            ground_truth: Optional ground truth for comparison
            
        Returns:
            Dictionary with all evaluation metrics
        """
        results = {}
        
        # Structure evaluation
        results['structure'] = self.evaluate_json_structure(generated)
        
        # Specificity evaluation
        results['specificity'] = self.evaluate_specificity(generated)
        
        # Actionability evaluation
        results['actionability'] = self.evaluate_actionability(generated)
        
        # Ground truth comparison (if available)
        if ground_truth:
            results['ground_truth_comparison'] = self.evaluate_with_ground_truth(
                generated, ground_truth
            )
        
        # Overall quality score (weighted combination)
        structure_score = 1.0 if results['structure']['is_valid_json'] and results['structure']['has_required_fields'] else 0.5
        specificity_score = results['specificity']['specificity_score']
        actionability_score = results['actionability']['actionability_score']
        
        results['overall_quality_score'] = (
            structure_score * 0.3 +
            specificity_score * 0.4 +
            actionability_score * 0.3
        )
        
        return results

