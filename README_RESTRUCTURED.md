# SpamShieldAI

> Intelligent SMS and Email Spam Detection with Machine Learning

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18%2B-blue.svg)](https://reactjs.org/)

## 📋 Project Overview

SpamShieldAI is a full-stack spam detection system that combines machine learning, a Flask REST API, and a modern React frontend. It detects spam and phishing attempts in SMS messages and emails with high accuracy.

**Live Demo:** [SpamShield Frontend](https://spamshield-frontend-production.up.railway.app/)

## 🎯 Key Features

- 🤖 **ML-Powered Detection**: Logistic Regression classifier trained on SMS Spam Collection dataset
- 🚀 **REST API**: Flask-based API with CORS support for easy integration
- 💻 **Modern UI**: React + TypeScript + Tailwind CSS frontend
- 🐳 **Docker Support**: Production-ready Docker and Docker Compose configurations
- 📊 **Model Management**: Versioned ML models and vectorizers with easy retraining
- 🔒 **Production Ready**: Deployed on Railway, Render, and Fly.io

## 📁 Project Structure

```
spamshieldai/
├── src/                          # Python ML source code
│   ├── data/                     # Data processing modules
│   │   ├── __init__.py
│   │   └── preprocessing.py      # Data cleaning and preprocessing utilities
│   ├── models/                   # ML model training and inference
│   │   ├── __init__.py
│   │   ├── train.py             # Model training script
│   │   └── predict.py           # Model prediction script
│   ├── features/                 # Feature engineering modules
│   │   └── __init__.py
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py           # Config and logging helpers
│   └── __init__.py
│
├── deployment/                   # Deployment configurations
│   ├── api/                      # Flask REST API
│   │   ├── app.py               # Main Flask application
│   │   ├── requirements.txt      # Python dependencies
│   │   ├── Dockerfile           # API container configuration
│   │   ├── Procfile             # Process file for platforms
│   │   └── ...
│   ├── frontend/                 # React TypeScript frontend
│   │   ├── src/                 # React components and pages
│   │   ├── package.json         # JavaScript dependencies
│   │   ├── tailwind.config.js   # Tailwind CSS configuration
│   │   └── vite.config.ts       # Vite build configuration
│   └── docker/                   # Docker Compose files
│       ├── docker-compose.yml
│       ├── docker-compose.prod.yml
│       └── .dockerignore
│
├── data/                         # Dataset directory
│   ├── raw/                      # Original unprocessed data
│   ├── processed/                # Cleaned and processed data
│   ├── interim/                  # Intermediate data files
│   └── external/                 # External data sources
│
├── models/                       # Trained ML models
│   ├── spam_classifier.pkl       # Trained classifier model
│   ├── vectorizer.pkl            # TF-IDF/CountVectorizer
│   └── .gitkeep
│
├── notebooks/                    # Jupyter notebooks for exploration
│   └── exploratory/              # Exploratory data analysis
│
├── config/                       # Configuration files
│   ├── config.yaml              # ML and application parameters
│   ├── logging.yaml             # Logging configuration
│   ├── env.template             # Environment template
│   └── env.production.template   # Production environment template
│
├── scripts/                      # Utility shell scripts
│   ├── setup.sh                 # Development environment setup
│   ├── train_model.sh           # Model training script
│   └── run_api.sh               # API server startup
│
├── docs/                         # Documentation
│   ├── DEPLOY_QUICKSTART.md     # Quick deployment guide
│   ├── DEPLOYMENT_SUMMARY.md    # Deployment overview
│   ├── CLOUD_DEPLOY.md          # Cloud deployment guides
│   ├── MODELS_DEPLOY.md         # Model deployment guide
│   └── DOCKER.md                # Docker setup guide
│
├── tests/                        # Unit and integration tests
│   └── __init__.py
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation configuration
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
└── fly.toml / render.yaml        # Platform deployment configs
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker & Docker Compose (optional)

### 1. Development Setup

```bash
# Clone the repository
git clone https://github.com/hassan2nwar/spamshieldai.git
cd spamshieldai

# Run setup script
./scripts/setup.sh

# Activate virtual environment
source venv/bin/activate
```

### 2. Train the Model

```bash
# Download dataset and train model
./scripts/train_model.sh

# Or directly:
python src/models/train.py
```

Model will be saved to:
- `models/spam_classifier.pkl` - Trained classifier
- `models/vectorizer.pkl` - Text vectorizer

### 3. Run the API

```bash
# In a terminal with venv activated
./scripts/run_api.sh

# API will be available at: http://localhost:5000
```

### 4. Run the Frontend

```bash
# In another terminal
cd deployment/frontend
npm install
npm run dev

# Frontend will be available at: http://localhost:5173
```

## 📚 API Documentation

### Predict Endpoint

**POST** `/api/predict`

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations! You have won a free iPhone."}'
```

**Response:**
```json
{
  "text": "Congratulations! You have won a free iPhone.",
  "prediction": "spam",
  "confidence": 0.92,
  "probability": {
    "ham": 0.08,
    "spam": 0.92
  }
}
```

## 🐳 Docker Deployment

### Build and Run with Docker Compose

```bash
cd deployment/docker

# Development
docker-compose -f docker-compose.yml up --build

# Production
docker-compose -f docker-compose.prod.yml up --build
```

Access the application:
- Frontend: http://localhost:3000
- API: http://localhost:5000

## 🌐 Production Deployment

### Railway Deployment

```bash
# Push to Railway
railway up

# View logs
railway logs
```

### Render Deployment

See `render.yaml` for configuration.

### Fly.io Deployment

See `fly.toml` for configuration.

## 📊 Model Performance

- **Dataset**: SMS Spam Collection (5,574 messages)
- **Train/Test Split**: 80/20
- **Algorithm**: Logistic Regression
- **Vectorizer**: CountVectorizer
- **Accuracy**: ~97%

## 🔧 Configuration

### ML Parameters

Edit `config/config.yaml` to customize:

```yaml
training:
  test_split: 0.2
  random_state: 42
  vectorizer_type: "count"
  max_features: 5000
```

### Environment Variables

Copy and configure:

```bash
cp config/env.template .env
```

## 📝 Project Components

### Source Code (`src/`)

- **`data/preprocessing.py`** - Data cleaning and preparation
- **`models/train.py`** - Model training pipeline
- **`models/predict.py`** - Inference and predictions
- **`utils/helpers.py`** - Configuration and logging utilities

### Deployment (`deployment/`)

- **`api/`** - Flask REST API server
- **`frontend/`** - React TypeScript UI
- **`docker/`** - Docker configurations

### Data Pipeline

1. **Raw Data** → `data/raw/`
2. **Preprocessing** → `data/processed/`
3. **Model Training** → `models/`
4. **API Serving** → `deployment/api/`

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/
```

## 📖 Documentation

Detailed documentation for each component:

- **[Quick Deployment Guide](docs/DEPLOY_QUICKSTART.md)**
- **[Deployment Summary](docs/DEPLOYMENT_SUMMARY.md)**
- **[Cloud Deployment](docs/CLOUD_DEPLOY.md)**
- **[Model Deployment](docs/MODELS_DEPLOY.md)**
- **[Docker Guide](docs/DOCKER.md)**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Hassan Anwar**
- GitHub: [@hassan2nwar](https://github.com/hassan2nwar)
- Project: [SpamShieldAI](https://github.com/hassan2nwar/spamshieldai)

## 🙏 Acknowledgments

- **Dataset**: [SMS Spam Collection](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection)
- **Framework**: Flask, React, Tailwind CSS
- **ML Libraries**: scikit-learn, pandas, joblib

## 📞 Support

For issues, questions, or suggestions:
- Open an [GitHub Issue](https://github.com/hassan2nwar/spamshieldai/issues)
- Check [Documentation](docs/)
- Review deployment guides for platform-specific help

---

**Happy Spam Detecting! 🛡️✨**
