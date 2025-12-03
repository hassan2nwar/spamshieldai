# SpamShield AI - API (Backend)

This document explains how to run and deploy the SpamShield AI backend app.

## Quick start (local)

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. (Optional) If your models are hosted remotely, set the environment variable `MODEL_BASE_URL`.

3. Run locally (dev):

```bash
export PORT=5000
python app.py
```

4. Test health and endpoints:

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/api/analyze -H "Content-Type: application/json" -d '{"message":"test"}'
```

## Docker

The contained `Dockerfile` in the `api/` directory builds a production-ready image using `gunicorn`.

To build and run the image locally:

```bash
docker build -f api/Dockerfile -t spamshield-api:local .
docker run -d --name spamshield-api -p 5000:5000 -e PORT=5000 spamshield-api:local
```

## Railway / Cloud Deployment

The repository includes a `railway.json` that configures the backend build to use `api/Dockerfile` and start with `/start.sh`. When deploying:

- Set `CORS_ORIGINS` to your frontend URL (e.g. `https://spamshield-frontend-production.up.railway.app`).
- If using large models, add `MODEL_BASE_URL` to download models at runtime.
- Ensure `MODELS_DIR` is set to `/app/models` if using volumes.

Example env variables for Railway backend service:

```
CORS_ORIGINS=https://spamshield-frontend-production.up.railway.app
MODELS_DIR=/app/models
MODEL_BASE_URL=  # optional
APP_VERSION=1.0.0
```

Health checks:
- Path: `/api/health` or `/health` (both supported)
- Start command: the image uses `/start.sh` which starts `gunicorn` and optionally downloads models

## Troubleshooting
- If you see `Error contacting backend API` in the frontend, confirm `VITE_API_URL` is set and points to the deployed API.
- Check backend logs for request logs and CORS origins.
- Confirm model files are present in `/app/models` or that `MODEL_BASE_URL` is set.
