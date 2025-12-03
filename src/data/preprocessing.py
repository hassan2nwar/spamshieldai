"""
data/preprocessing.py - Data preprocessing utilities for SpamShieldAI
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_raw_data(file_path: str) -> pd.DataFrame:
    """
    Load raw SMS data from file.
    
    Args:
        file_path: Path to the raw data file
        
    Returns:
        DataFrame with columns 'label' and 'text'
    """
    df = pd.read_csv(file_path, sep="\t", header=None, names=["label", "text"])
    return df


def clean_text(text: str) -> str:
    """
    Clean and normalize text data.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.lower()


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess entire dataframe.
    
    Args:
        df: Input dataframe
        
    Returns:
        Preprocessed dataframe
    """
    df = df.copy()
    
    # Clean text column
    df['text'] = df['text'].apply(clean_text)
    
    # Convert labels to numeric
    df['label_num'] = df['label'].map({'ham': 0, 'spam': 1})
    
    return df


def save_processed_data(df: pd.DataFrame, output_path: str) -> None:
    """
    Save processed data to file.
    
    Args:
        df: Dataframe to save
        output_path: Path where to save the processed data
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
