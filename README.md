# SpamShield AI

A machine learning-powered email spam detection system with a modern web interface.

## Features

- 🤖 ML-powered spam detection using scikit-learn
- 🎨 Modern React + TypeScript frontend
- 🚀 Dockerized for easy deployment
- ⚙️ Environment-based configuration

## Quick Start with Docker

1. **Set up environment variables:**
   ```bash
   # On Windows (PowerShell)
   .\setup-env.ps1
   
   # On Linux/Mac
   chmod +x setup-env.sh
   ./setup-env.sh
   
   # Or manually copy the template
   cp env.template .env
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - API: http://localhost:5000

## Configuration

Edit the `.env` file to customize:
- API port and host
- Frontend port
- API URL for frontend
- CORS origins
- Flask environment settings

See `env.template` for all available configuration options.

## Documentation

- [🚀 Quick Deploy Guide](DEPLOY_QUICKSTART.md) - **Deploy to cloud in 5 minutes!** ⭐
- [Deployment Summary](DEPLOYMENT_SUMMARY.md) - Quick reference for all deployment options
- [Cloud Deployment Guide](CLOUD_DEPLOY.md) - Comprehensive cloud deployment options
- [Models Deployment Guide](MODELS_DEPLOY.md) - How to handle ML models in deployment
- [Docker Setup Guide](DOCKER.md) - Detailed Docker deployment instructions
- [Environment Variables](env.template) - Configuration template

## Development

### Local Development (without Docker)

**Backend:**
```bash
cd api
pip install -r requirements-api.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## License

MIT
