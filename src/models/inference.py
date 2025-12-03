"""Inference utilities for SMS spam classification"""
import joblib
import os
from pathlib import Path
from typing import Dict, Tuple


class Inference:
    """Handles model inference for spam classification"""
    
    def __init__(self, model_path: str = None, vectorizer_path: str = None):
        """
        Initialize inference with model and vectorizer paths.
        
        Args:
            model_path (str): Path to trained model pickle file
            vectorizer_path (str): Path to vectorizer pickle file
        """
        if model_path is None:
            model_path = "models/spam_classifier.pkl"
        if vectorizer_path is None:
            vectorizer_path = "models/vectorizer.pkl"
        
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        
        self.model = None
        self.vectorizer = None
        
        self._load_artifacts()
    
    def _load_artifacts(self) -> None:
        """Load model and vectorizer from disk"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {self.model_path}")
        if not self.vectorizer_path.exists():
            raise FileNotFoundError(f"Vectorizer not found: {self.vectorizer_path}")
        
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)
    
    def predict(self, text: str) -> Dict[str, any]:
        """
        Predict spam/ham for a single message.
        
        Args:
            text (str): SMS message text
            
        Returns:
            Dict: Prediction result with label and probability
        """
        if self.model is None or self.vectorizer is None:
            raise RuntimeError("Model or vectorizer not loaded")
        
        text_vec = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vec)[0]
        probability = self.model.predict_proba(text_vec)[0]
        
        label = "spam" if prediction == 1 else "ham"
        confidence = float(max(probability))
        
        return {
            'label': label,
            'prediction': int(prediction),
            'confidence': confidence,
            'probabilities': {
                'ham': float(probability[0]),
                'spam': float(probability[1])
            }
        }
    
    def predict_batch(self, texts: list) -> list:
        """
        Predict spam/ham for multiple messages.
        
        Args:
            texts (list): List of SMS message texts
            
        Returns:
            list: List of prediction results
        """
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
