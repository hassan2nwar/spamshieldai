#!/usr/bin/env python3
"""
Inference entrypoint script for making predictions on SMS messages.

Usage:
    python entrypoint/predict.py --text "Hello, how are you?" --model models/spam_classifier.pkl --vectorizer models/vectorizer.pkl
"""
import argparse
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.inference import Inference


def main():
    """Main inference entrypoint"""
    parser = argparse.ArgumentParser(description="Predict spam/ham for SMS messages")
    parser.add_argument(
        "--text",
        required=True,
        help="SMS message text to classify"
    )
    parser.add_argument(
        "--model",
        default="models/spam_classifier.pkl",
        help="Path to trained model pickle file"
    )
    parser.add_argument(
        "--vectorizer",
        default="models/vectorizer.pkl",
        help="Path to vectorizer pickle file"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )
    args = parser.parse_args()
    
    try:
        print("Loading model and vectorizer...", file=sys.stderr)
        inference = Inference(
            model_path=args.model,
            vectorizer_path=args.vectorizer
        )
        
        print("Making prediction...", file=sys.stderr)
        result = inference.predict(args.text)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\nPrediction for: '{args.text}'")
            print(f"Label: {result['label'].upper()}")
            print(f"Confidence: {result['confidence']:.4f}")
            print(f"Probabilities:")
            print(f"  Ham: {result['probabilities']['ham']:.4f}")
            print(f"  Spam: {result['probabilities']['spam']:.4f}")
        
        return 0
        
    except Exception as e:
        print(f"Error during prediction: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
