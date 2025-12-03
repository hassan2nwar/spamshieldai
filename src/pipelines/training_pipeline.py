"""Training pipeline for SMS spam classification"""
import os
import joblib
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


class TrainingPipeline:
    """
    Training pipeline for SMS spam classification.
    
    Orchestrates data loading, model training, and artifact saving.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize training pipeline with configuration.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        self.config = config
        self.training_config = config.get('training', {})
        self.vectorizer_config = config.get('vectorizer', {})
        self.model_config = config.get('model', {})
        self.paths_config = config.get('paths', {})
        
        # Create model directory if it doesn't exist
        self.model_dir = self.paths_config.get('model_dir', 'models')
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Model paths
        self.model_path = os.path.join(self.model_dir, self.paths_config.get('model_file', 'spam_classifier.pkl'))
        self.vectorizer_path = os.path.join(self.model_dir, self.paths_config.get('vectorizer_file', 'vectorizer.pkl'))
        
        self.vectorizer = None
        self.model = None
    
    def prepare_dataset(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Prepare training and testing datasets.
        
        Args:
            df (pd.DataFrame): Raw dataset with 'text' and 'label_num' columns
            
        Returns:
            Tuple: (X_train, X_test, y_train, y_test)
        """
        X = df["text"].astype(str)
        y = df["label_num"].astype(int)
        
        test_size = self.training_config.get('test_size', 0.2)
        random_state = self.training_config.get('random_state', 42)
        stratify = self.training_config.get('stratify', True)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=y if stratify else None
        )
        
        return X_train, X_test, y_train, y_test
    
    def vectorize_data(self, X_train: pd.Series, X_test: pd.Series) -> Tuple:
        """
        Vectorize text data using CountVectorizer.
        
        Args:
            X_train (pd.Series): Training text data
            X_test (pd.Series): Testing text data
            
        Returns:
            Tuple: (X_train_vec, X_test_vec)
        """
        vect_params = {
            'lowercase': self.vectorizer_config.get('lowercase', True),
            'stop_words': self.vectorizer_config.get('stop_words', 'english'),
            'max_df': self.vectorizer_config.get('max_df', 0.95),
            'min_df': self.vectorizer_config.get('min_df', 2),
        }
        
        self.vectorizer = CountVectorizer(**vect_params)
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        return X_train_vec, X_test_vec
    
    def train_model(self, X_train_vec, y_train) -> None:
        """
        Train logistic regression model.
        
        Args:
            X_train_vec: Vectorized training data
            y_train (pd.Series): Training labels
        """
        model_params = {
            'max_iter': self.model_config.get('max_iter', 1000),
        }
        
        self.model = LogisticRegression(**model_params)
        self.model.fit(X_train_vec, y_train)
    
    def evaluate_model(self, X_test_vec, y_test: pd.Series) -> Dict[str, Any]:
        """
        Evaluate model on test data.
        
        Args:
            X_test_vec: Vectorized test data
            y_test (pd.Series): Test labels
            
        Returns:
            Dict: Evaluation metrics including accuracy
        """
        preds = self.model.predict(X_test_vec)
        accuracy = accuracy_score(y_test, preds)
        report = classification_report(y_test, preds, output_dict=True, digits=4)
        
        print(f"Accuracy: {accuracy:.4f}")
        print("Classification report:\n", classification_report(y_test, preds, digits=4))
        
        return {
            'accuracy': accuracy,
            'report': report,
            'predictions': preds
        }
    
    def save_artifacts(self) -> None:
        """Save trained model and vectorizer to disk"""
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.vectorizer, self.vectorizer_path)
        
        print(f"Saved model to {self.model_path}")
        print(f"Saved vectorizer to {self.vectorizer_path}")
    
    def run(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Execute the full training pipeline.
        
        Args:
            df (pd.DataFrame): Raw dataset with preprocessing already applied
            
        Returns:
            Dict: Training results including metrics and paths to saved artifacts
        """
        print("Starting training pipeline...")
        
        # Prepare data
        print("Preparing dataset...")
        X_train, X_test, y_train, y_test = self.prepare_dataset(df)
        
        # Vectorize
        print("Vectorizing text data...")
        X_train_vec, X_test_vec = self.vectorize_data(X_train, X_test)
        
        # Train
        print("Training model...")
        self.train_model(X_train_vec, y_train)
        
        # Evaluate
        print("Evaluating model...")
        metrics = self.evaluate_model(X_test_vec, y_test)
        
        # Save artifacts
        print("Saving artifacts...")
        self.save_artifacts()
        
        return {
            'metrics': metrics,
            'model_path': self.model_path,
            'vectorizer_path': self.vectorizer_path,
        }
