"""
Utility functions for incident enrichment project.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datasets import load_dataset


def load_incident_dataset(sample_size: Optional[int] = None, random_state: int = 42) -> pd.DataFrame:
    """
    Load the synthetic IT call center tickets dataset from Hugging Face.
    
    Args:
        sample_size: If provided, randomly sample this many records
        random_state: Random seed for reproducibility
        
    Returns:
        DataFrame with incident data
    """
    print("Loading dataset from Hugging Face...")
    dataset = load_dataset("KameronB/synthetic-it-callcenter-tickets")
    df = dataset["train"].to_pandas()
    
    if sample_size:
        df = df.sample(sample_size, random_state=random_state)
        print(f"Sampled {sample_size} records from dataset")
    
    print(f"Loaded {len(df)} records")
    return df


def prepare_incident_for_enrichment(df: pd.DataFrame, incident_id: Optional[str] = None) -> Dict:
    """
    Prepare a single incident record for LLM enrichment.
    
    Args:
        df: DataFrame with incident data
        incident_id: Specific incident number to extract, or None for random
        
    Returns:
        Dictionary with incident fields ready for prompt
    """
    if incident_id:
        incident = df[df['number'] == incident_id].iloc[0]
    else:
        incident = df.sample(1).iloc[0]
    
    return {
        'number': incident.get('number', ''),
        'date': incident.get('date', ''),
        'contact_type': incident.get('contact_type', ''),
        'short_description': incident.get('short_description', ''),
        'content': incident.get('content', ''),
        'category': incident.get('category', ''),
        'subcategory': incident.get('subcategory', ''),
        'customer': incident.get('customer', ''),
    }


def save_enriched_results(df: pd.DataFrame, output_path: str):
    """
    Save enriched incident results to CSV.
    
    Args:
        df: DataFrame with enriched data
        output_path: Path to save CSV file
    """
    df.to_csv(output_path, index=False)
    print(f"Saved enriched results to {output_path}")


def calculate_basic_stats(df: pd.DataFrame) -> Dict:
    """
    Calculate basic statistics about the dataset.
    
    Args:
        df: DataFrame with incident data
        
    Returns:
        Dictionary with statistics
    """
    stats = {
        'total_incidents': len(df),
        'incidents': 0,
        'requests': 0,
        'avg_resolution_time': None,
        'categories': {},
    }
    
    # Count incidents vs requests - check both 'type' and 'issue/request' columns
    if 'type' in df.columns:
        stats['incidents'] = df[df['type'].str.contains('Incident', case=False, na=False)].shape[0]
        stats['requests'] = df[df['type'].str.contains('Request', case=False, na=False)].shape[0]
    elif 'issue/request' in df.columns:
        stats['incidents'] = df[df['issue/request'].str.contains('Incident', case=False, na=False)].shape[0]
        stats['requests'] = df[df['issue/request'].str.contains('Request', case=False, na=False)].shape[0]
    
    # Calculate average resolution time
    if 'resolution_time' in df.columns:
        stats['avg_resolution_time'] = df['resolution_time'].mean()
    
    # Get category distribution
    if 'category' in df.columns:
        stats['categories'] = df['category'].value_counts().to_dict()
    
    return stats

