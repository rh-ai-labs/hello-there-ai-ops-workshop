"""
MLflow tracking utilities for experiment management.
"""

import mlflow
import json
from typing import Dict, Optional, Any
from datetime import datetime


def setup_mlflow(
    experiment_name: str = "incident_enrichment",
    tracking_uri: Optional[str] = None
):
    """
    Setup MLflow experiment tracking.
    
    Args:
        experiment_name: Name of the MLflow experiment
        tracking_uri: Optional MLflow tracking URI (defaults to local)
    """
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
    
    try:
        experiment_id = mlflow.create_experiment(experiment_name)
        print(f"Created new experiment: {experiment_name} (ID: {experiment_id})")
    except Exception:
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        print(f"Using existing experiment: {experiment_name} (ID: {experiment_id})")
    
    mlflow.set_experiment(experiment_name)
    return experiment_id


def log_incident_enrichment_run(
    run_name: str,
    prompt_variant: str,
    model_name: str,
    incident_id: str,
    prompt_text: str,
    generated_text: str,
    evaluation_metrics: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Log a single incident enrichment run to MLflow.
    
    Args:
        run_name: Name for this MLflow run
        prompt_variant: Name of the prompt variant used
        model_name: Name/ID of the LLM model used
        incident_id: ID of the incident being enriched
        prompt_text: The prompt that was sent to the LLM
        generated_text: The LLM-generated enrichment
        evaluation_metrics: Dictionary with evaluation results
        metadata: Optional additional metadata
    """
    with mlflow.start_run(run_name=run_name):
        # Log parameters
        mlflow.log_param("prompt_variant", prompt_variant)
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("incident_id", incident_id)
        
        # Log prompt and generated text as artifacts
        mlflow.log_text(prompt_text, "prompt.txt")
        mlflow.log_text(generated_text, "generated_enrichment.txt")
        
        # Log evaluation metrics
        for metric_name, metric_value in flatten_dict(evaluation_metrics).items():
            if isinstance(metric_value, (int, float)):
                mlflow.log_metric(metric_name, metric_value)
            elif isinstance(metric_value, bool):
                mlflow.log_metric(metric_name, 1.0 if metric_value else 0.0)
        
        # Log metadata
        if metadata:
            for key, value in metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    mlflow.log_param(f"metadata_{key}", value)
                else:
                    mlflow.log_dict({key: value}, f"metadata_{key}.json")
        
        # Log timestamp
        mlflow.log_param("timestamp", datetime.now().isoformat())


def log_comparison_run(
    scenario_name: str,
    scenario_a_results: Dict[str, Any],
    scenario_b_results: Dict[str, Any],
    comparison_metrics: Dict[str, float]
):
    """
    Log a comparison run between Scenario A and Scenario B.
    
    Args:
        scenario_name: Name for this comparison run
        scenario_a_results: Results from Scenario A (general LLM)
        scenario_b_results: Results from Scenario B (tuned LLM)
        comparison_metrics: Calculated comparison metrics
    """
    with mlflow.start_run(run_name=f"comparison_{scenario_name}"):
        # Log scenario A metrics
        for metric_name, metric_value in flatten_dict(scenario_a_results).items():
            if isinstance(metric_value, (int, float)):
                mlflow.log_metric(f"scenario_a_{metric_name}", metric_value)
        
        # Log scenario B metrics
        for metric_name, metric_value in flatten_dict(scenario_b_results).items():
            if isinstance(metric_value, (int, float)):
                mlflow.log_metric(f"scenario_b_{metric_name}", metric_value)
        
        # Log comparison metrics (differences, improvements)
        for metric_name, metric_value in comparison_metrics.items():
            mlflow.log_metric(f"comparison_{metric_name}", metric_value)


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    """
    Flatten a nested dictionary for MLflow logging.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for nested keys
        
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def get_best_run(experiment_name: str, metric: str = "overall_quality_score", ascending: bool = False):
    """
    Retrieve the best run from an experiment based on a metric.
    
    Args:
        experiment_name: Name of the MLflow experiment
        metric: Metric name to sort by
        ascending: Whether to sort ascending (True) or descending (False)
        
    Returns:
        Best run data
    """
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        return None
    
    runs = mlflow.search_runs(experiment.experiment_id, order_by=[f"metrics.{metric} {'ASC' if ascending else 'DESC'}"])
    
    if runs.empty:
        return None
    
    best_run = runs.iloc[0]
    return {
        'run_id': best_run['run_id'],
        'run_name': best_run.get('tags.mlflow.runName', ''),
        'metric_value': best_run[f'metrics.{metric}'],
        'metrics': {col.replace('metrics.', ''): val for col, val in best_run.items() if col.startswith('metrics.')},
        'params': {col.replace('params.', ''): val for col, val in best_run.items() if col.startswith('params.')}
    }

