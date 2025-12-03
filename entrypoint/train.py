#!/usr/bin/env python3
"""
Training entrypoint script.

Usage:
    python entrypoint/train.py --config config/default_config.yaml
"""
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config_loader import ConfigLoader
from utils.data_loader import DataLoader
from pipelines.training_pipeline import TrainingPipeline


def main():
    """Main training entrypoint"""
    parser = argparse.ArgumentParser(description="Train SMS Spam Classifier model")
    parser.add_argument(
        "--config",
        default="config/default_config.yaml",
        help="Path to configuration YAML file"
    )
    args = parser.parse_args()
    
    try:
        print(f"Loading configuration from {args.config}...")
        config = ConfigLoader.load_config(args.config)
        
        print("Initializing data loader...")
        data_loader = DataLoader(config)
        
        print("Downloading and extracting dataset...")
        data_loader.download_and_extract()
        
        print("Loading data...")
        df = data_loader.load_data()
        
        print("Preprocessing labels...")
        df = DataLoader.preprocess_labels(df)
        
        print("Initializing training pipeline...")
        pipeline = TrainingPipeline(config)
        
        print("Running training pipeline...")
        results = pipeline.run(df)
        
        print(f"\nTraining completed successfully!")
        print(f"  Accuracy: {results['metrics']['accuracy']:.4f}")
        print(f"  Model saved to: {results['model_path']}")
        print(f"  Vectorizer saved to: {results['vectorizer_path']}")
        
        return 0
        
    except Exception as e:
        print(f"Error during training: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
