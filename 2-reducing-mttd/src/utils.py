"""
Utility functions for incident enrichment project.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datasets import load_dataset
from pathlib import Path
import pickle


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


def load_ground_truth_embeddings(data_dir: str = "data") -> Tuple[np.ndarray, Dict]:
    """
    Load pre-computed embeddings for ground truth close notes.
    
    Args:
        data_dir: Directory containing the embeddings files
        
    Returns:
        Tuple of (embeddings_array, metadata_dict)
    """
    data_path = Path(data_dir)
    embeddings_path = data_path / "gt_close_notes_embeddings.npy"
    metadata_path = data_path / "gt_close_notes_embeddings_metadata.pkl"
    
    if not embeddings_path.exists():
        raise FileNotFoundError(f"Embeddings file not found: {embeddings_path}")
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
    
    embeddings = np.load(embeddings_path)
    
    with open(metadata_path, 'rb') as f:
        metadata = pickle.load(f)
    
    return embeddings, metadata


def compute_semantic_similarity(text1: str, text2: str, model_name: str = 'all-MiniLM-L6-v2') -> float:
    """
    Compute semantic similarity between two texts using sentence embeddings.
    
    Args:
        text1: First text
        text2: Second text
        model_name: Name of the sentence transformer model to use
        
    Returns:
        Cosine similarity score between 0 and 1
    """
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        
        model = SentenceTransformer(model_name)
        embeddings = model.encode([text1, text2])
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        return float(similarity)
    except ImportError:
        raise ImportError("sentence-transformers and scikit-learn are required for semantic similarity")
    except Exception as e:
        raise RuntimeError(f"Error computing semantic similarity: {e}")


def find_most_similar_close_note(
    query_text: str,
    embeddings: np.ndarray,
    metadata: Dict,
    ground_truth_df: Optional[pd.DataFrame] = None,
    top_k: int = 5
) -> List[Dict]:
    """
    Find the most semantically similar close notes to a query text.
    
    Args:
        query_text: Text to find similar notes for
        embeddings: Pre-computed embeddings array
        metadata: Metadata dictionary with incident numbers
        ground_truth_df: Optional DataFrame with ground truth data
        top_k: Number of most similar notes to return
        
    Returns:
        List of dictionaries with similarity scores and incident info
    """
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        
        model = SentenceTransformer(metadata.get('model_name', 'all-MiniLM-L6-v2'))
        query_embedding = model.encode([query_text])
        
        # Compute similarities
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        
        # Get top K indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            result = {
                'index': int(idx),
                'similarity': float(similarities[idx]),
                'incident_number': metadata['indices'][idx] if 'indices' in metadata else None
            }
            
            # Add additional info if ground truth DataFrame is provided
            if ground_truth_df is not None and 'number' in ground_truth_df.columns:
                incident = ground_truth_df[ground_truth_df['number'] == result['incident_number']]
                if not incident.empty:
                    result.update({
                        'category': incident.iloc[0].get('category'),
                        'subcategory': incident.iloc[0].get('subcategory'),
                        'close_notes_ref': incident.iloc[0].get('close_notes_ref')
                    })
            
            results.append(result)
        
        return results
    except ImportError:
        raise ImportError("sentence-transformers and scikit-learn are required")

