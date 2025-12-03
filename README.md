# SpamShieldAI

> Intelligent SMS and Email Spam Detection with Machine Learning

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18%2B-blue.svg)](https://reactjs.org/)

![SpamShield Screenshot](https://github.com/user-attachments/assets/c2bc7c84-90a0-4865-b206-97bddba36758)

## 📋 Overview

SpamShieldAI is a full-stack spam detection system combining machine learning, a Flask REST API, and a modern React frontend. It detects spam and phishing attempts in SMS messages and emails with high accuracy using logistic regression and text analysis.

**Live Demo:** [SpamShield Frontend](https://spamshield-frontend-production.up.railway.app/)

## 🎯 Key Features

- 🤖 **ML-Powered Detection**: Logistic Regression classifier trained on SMS Spam Collection dataset
- 🚀 **REST API**: Flask-based API with CORS support for easy integration
- 💻 **Modern UI**: React + TypeScript + Tailwind CSS frontend
- 🐳 **Docker Support**: Production-ready Docker and Docker Compose configurations
- 📊 **Model Management**: Versioned ML models with easy retraining
- ☁️ **Cloud Ready**: Deployed on Railway, Render, and Fly.io

## 📁 Project Structure

The project follows an industry-standard ML project template:

```
spamshieldai/
├── src/                          # Python ML source code
│   ├── data/                     # Data processing
│   ├── models/                   # Training & prediction
│   ├── features/                 # Feature engineering
│   └── utils/                    # Utilities & helpers
├── deployment/                   # Deployment configurations
│   ├── api/                      # Flask REST API
│   ├── frontend/                 # React TypeScript UI
│   └── docker/                   # Docker configs
├── config/                       # Configuration files
├── data/                         # Dataset pipeline
├── models/                       # Trained ML models
├── scripts/                      # Utility scripts
├── docs/                         # Documentation
└── tests/                        # Unit tests
```

For detailed structure, see [README_RESTRUCTURED.md](README_RESTRUCTURED.md).

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose (optional)

### 1. Setup Development Environment

```bash
./scripts/setup.sh
source venv/bin/activate
```

### 2. Train the Model

```bash
./scripts/train_model.sh
```

Models are saved to: `models/spam_classifier.pkl` and `models/vectorizer.pkl`

### 3. Run the API

```bash
./scripts/run_api.sh
```

API available at: `http://localhost:5000`

### 4. Run the Frontend

```bash
cd deployment/frontend
npm install
npm run dev
```

Frontend available at: `http://localhost:5173`

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

### Development

```bash
cd deployment/docker
docker-compose -f docker-compose.yml up --build
```

### Production

```bash
docker-compose -f docker-compose.prod.yml up --build
```

## 🌐 Cloud Deployment

### Railway

```bash
railway up
railway logs
```

### Render

See `render.yaml` for configuration.

### Fly.io

See `fly.toml` for configuration.

```bash
flyctl deploy
```

## 📖 Documentation

- **[README_RESTRUCTURED.md](README_RESTRUCTURED.md)** - Complete project documentation
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Quick reference guide
- **[docs/DEPLOY_QUICKSTART.md](docs/DEPLOY_QUICKSTART.md)** - Deployment guide
- **[docs/DOCKER.md](docs/DOCKER.md)** - Docker setup guide

## 📊 Model Performance

- **Dataset**: SMS Spam Collection (5,574 messages)
- **Algorithm**: Logistic Regression
- **Vectorizer**: CountVectorizer
- **Accuracy**: ~97%

## 🔧 Configuration

### ML Parameters

Edit `config/config.yaml`:

```yaml
training:
  test_split: 0.2
  random_state: 42
  vectorizer_type: "count"
  max_features: 5000
```

### Environment Variables

```bash
cp config/env.template .env
```

## 🧪 Testing

```bash
pytest tests/
pytest --cov=src tests/
```

## 🛠️ Development

### Project Structure Benefits

- ✨ Industry-standard ML project layout
- 🏗️ Scalable architecture
- 🔄 Clear data pipeline
- 📦 Modular design
- 🧪 Testing infrastructure
- 📖 Comprehensive documentation

### Adding Features

1. Data processing: `src/data/`
2. Model code: `src/models/`
3. Tests: `tests/`
4. Documentation: `docs/`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE for details.

## 👨‍💻 Author

**Hassan Anwar**
- GitHub: [@hassan2nwar](https://github.com/hassan2nwar)
- Project: [SpamShieldAI](https://github.com/hassan2nwar/spamshieldai)

## 🙏 Acknowledgments

- **Dataset**: [SMS Spam Collection](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection)
- **Framework**: Flask, React, Tailwind CSS
- **ML**: scikit-learn, pandas, joblib

## 📞 Support

For issues, questions, or suggestions:
- Open a [GitHub Issue](https://github.com/hassan2nwar/spamshieldai/issues)
- Check [Documentation](docs/)
- Review [Quick Start Guide](QUICK_START_GUIDE.md)

---

**Happy Spam Detecting! 🛡️✨**
