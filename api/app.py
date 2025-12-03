from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import os
import sys
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models.inference import Inference

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS using the CORS_ORIGINS env var if present; default to allow all
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
CORS(app, resources={
    r"/api/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False,
    }
}, expose_headers='Content-Type')

# Configure logging to include request details
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def log_request_info():
    app.logger.info(
        "Incoming request: method=%s path=%s origin=%s remote_addr=%s",
        request.method,
        request.path,
        request.headers.get('Origin'),
        request.remote_addr,
    )

# Load model and vectorizer paths from environment or use defaults
MODEL_DIR = Path(os.environ.get('MODELS_DIR', str(Path(__file__).parent.parent / 'models'))).resolve()
MODEL_PATH = MODEL_DIR / 'spam_classifier.pkl'
VECT_PATH = MODEL_DIR / 'vectorizer.pkl'

# Fallback to root /models if not found
if not MODEL_PATH.exists():
    MODEL_PATH = Path('/models/spam_classifier.pkl')
if not VECT_PATH.exists():
    VECT_PATH = Path('/models/vectorizer.pkl')

logger.info(f"Using model path: {MODEL_PATH}")
logger.info(f"Using vectorizer path: {VECT_PATH}")

# Initialize inference engine
inference = None
try:
    inference = Inference(model_path=str(MODEL_PATH), vectorizer_path=str(VECT_PATH))
    logger.info("Model and vectorizer loaded successfully")
except Exception as e:
    inference = None
    logger.error(f"Error loading model/vectorizer: {e}")

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if inference is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.get_json(force=True)
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        result = inference.predict(message)
        return jsonify({
            'label': result['label'],
            'prediction': result['prediction'],
            'confidence': round(result['confidence'] * 100, 2),
            'probabilities': {
                'ham': round(result['probabilities']['ham'] * 100, 2),
                'spam': round(result['probabilities']['spam'] * 100, 2),
            },
            'input': message
        })
    except Exception as e:
        logger.error(f"Error during prediction: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


# Minimal health endpoints for Railway
@app.route('/health', methods=['GET'])
def health():
    models_loaded = inference is not None
    return jsonify({
        'status': 'healthy' if models_loaded else 'degraded',
        'service': 'spamshieldai-api',
        'models_loaded': models_loaded
    }), 200

@app.route('/api/health', methods=['GET'])
def api_health():
    models_loaded = inference is not None
    return jsonify({
        'status': 'healthy' if models_loaded else 'degraded',
        'service': 'spamshieldai-api',
        'models_loaded': models_loaded
    }), 200


@app.route('/api/ping', methods=['GET'])
def api_ping():
    """A simple ping endpoint that returns minimal server info for debugging"""
    return jsonify({
        'status': 'ok',
        'server': 'spamshield-api',
        'models_loaded': inference is not None
    }), 200


@app.route('/', methods=['GET'])
def root():
    """Root endpoint: provides basic API metadata and indicates if models are loaded"""
    version = os.environ.get('APP_VERSION', '1.0.0')
    models_loaded = inference is not None
    return jsonify({
        'message': 'SpamShieldAI API',
        'status': 'running',
        'models_loaded': models_loaded,
        'version': version,
        'endpoints': {
            'health': '/health or /api/health (GET)',
            'analyze': '/api/analyze (POST)'
        }
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
