"""Data loading and preprocessing utilities"""
import os
import zipfile
import urllib.request
import pandas as pd
from typing import Tuple
from pathlib import Path


class DataLoader:
    """Handles dataset downloading, loading, and preprocessing"""
    
    def __init__(self, config: dict):
        """
        Initialize DataLoader with configuration.
        
        Args:
            config (dict): Configuration dictionary containing paths and dataset info
        """
        self.config = config
        self.data_config = config.get('paths', {})
        self.dataset_config = config.get('dataset', {})
        
        self.data_dir = self.data_config.get('data_dir', 'data/raw')
        self.raw_file = os.path.join(self.data_dir, self.data_config.get('raw_file', 'SMSSpamCollection'))
        self.zip_path = os.path.join(self.data_dir, self.data_config.get('zip_file', 'smsspamcollection.zip'))
        self.dataset_url = self.dataset_config.get('url', '')
        
        os.makedirs(self.data_dir, exist_ok=True)
    
    def download_and_extract(self) -> None:
        """Download and extract dataset if not already present"""
        if os.path.exists(self.raw_file):
            print(f"Dataset already present: {self.raw_file}")
            return
        
        print("Downloading dataset...")
        urllib.request.urlretrieve(self.dataset_url, self.zip_path)
        print(f"Downloaded to {self.zip_path}")
        
        with zipfile.ZipFile(self.zip_path, "r") as z:
            z.extractall(self.data_dir)
        print(f"Extracted to {self.data_dir}")
    
    def load_data(self) -> pd.DataFrame:
        """
        Load the SMS spam collection dataset.
        
        Returns:
            pd.DataFrame: Dataset with 'label' and 'text' columns
        """
        if not os.path.exists(self.raw_file):
            raise FileNotFoundError(f"Expected dataset file not found: {self.raw_file}")
        
        df = pd.read_csv(self.raw_file, sep="\t", header=None, names=["label", "text"])
        return df
    
    @staticmethod
    def preprocess_labels(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert text labels to numeric labels.
        
        Args:
            df (pd.DataFrame): DataFrame with 'label' column
            
        Returns:
            pd.DataFrame: DataFrame with added 'label_num' column
        """
        df = df.copy()
        df["label_num"] = df["label"].map({"ham": 0, "spam": 1})
        return df
