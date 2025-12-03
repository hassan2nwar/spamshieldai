# Cloud Deployment Guide for SpamShield AI

This guide covers deploying SpamShield AI to various cloud platforms so others can use it.

## 🚀 Quick Deploy Options (Recommended)

### Option 1: Railway (Easiest - Recommended for Beginners)
**Best for:** Quick deployment, automatic HTTPS, easy setup
- ✅ Free tier available
- ✅ Automatic HTTPS/SSL
- ✅ Simple GitHub integration
- ✅ Built-in environment variables

[See Railway Deployment Guide](#railway-deployment)

### Option 2: Render
**Best for:** Free hosting, good for small projects
- ✅ Free tier available
- ✅ Automatic SSL
- ✅ Easy setup
- ⚠️ Free tier spins down after inactivity

[See Render Deployment Guide](#render-deployment)

### Option 3: Fly.io
**Best for:** Global edge deployment, Docker-native
- ✅ Free tier available
- ✅ Global edge network
- ✅ Docker-native
- ✅ Great performance

[See Fly.io Deployment Guide](#flyio-deployment)

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

1. ✅ Git repository (GitHub, GitLab, or Bitbucket)
2. ✅ All code committed and pushed
3. ✅ Models directory with `spam_classifier.pkl` and `vectorizer.pkl`
4. ✅ `.env` file configured (or use platform's environment variables)

---

## 🚂 Railway Deployment

### Step 1: Prepare Your Repository

1. Push your code to GitHub/GitLab/Bitbucket
2. Ensure `docker-compose.yml` and Dockerfiles are in the repo

### Step 2: Deploy on Railway

1. **Sign up/Login:** Go to [railway.app](https://railway.app)
2. **New Project:** Click "New Project" → "Deploy from GitHub repo"
3. **Select Repository:** Choose your SpamShield AI repository
4. **Add Services:**
   - Add first service: **API** (backend)
     - Root Directory: `/` (root)
     - Dockerfile Path: `api/Dockerfile`
     - Port: `5000`
   - Add second service: **Frontend**
     - Root Directory: `/frontend`
     - Dockerfile Path: `Dockerfile`
     - Port: `80`

### Step 3: Configure Environment Variables

In Railway dashboard, for **API service**, add:
```
API_PORT=5000
API_HOST=0.0.0.0
FLASK_ENV=production
FLASK_DEBUG=false
CORS_ORIGINS=https://your-frontend-url.up.railway.app
```

For **Frontend service**, add:
```
VITE_API_URL=https://your-api-url.up.railway.app
```

### Step 4: Deploy Models

**Option A: Include in Git (if < 100MB)**
- Commit models to repository

**Option B: Use Railway Volumes**
- In API service settings → Volumes
- Mount `/app/models` to persistent volume
- Upload models via Railway CLI or dashboard

**Option C: Use External Storage (Recommended for production)**
- Upload to S3/Cloud Storage
- Download on container startup

### Step 5: Get Your URLs

Railway provides:
- API URL: `https://your-api-name.up.railway.app`
- Frontend URL: `https://your-frontend-name.up.railway.app`

Update frontend's `VITE_API_URL` to your API URL and redeploy.

---

## 🎨 Render Deployment

### Step 1: Prepare Repository

Same as Railway - push code to Git.

### Step 2: Deploy Backend (API)

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your repository
4. Configure:
   - **Name:** `spamshield-api`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `api/Dockerfile`
   - **Root Directory:** `/`
   - **Port:** `5000`

### Step 3: Deploy Frontend

1. Click "New +" → "Web Service"
2. Configure:
   - **Name:** `spamshield-frontend`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `frontend/Dockerfile`
   - **Root Directory:** `/frontend`
   - **Port:** `80`

### Step 4: Environment Variables

**Backend Service:**
```
API_PORT=5000
API_HOST=0.0.0.0
FLASK_ENV=production
CORS_ORIGINS=https://spamshield-frontend.onrender.com
```

**Frontend Service:**
```
VITE_API_URL=https://spamshield-api.onrender.com
```

### Step 5: Models

Upload models to a persistent disk or use external storage.

---

## ✈️ Fly.io Deployment

### Step 1: Install Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Initialize

```bash
fly auth login
fly launch
```

### Step 3: Deploy API

```bash
cd api
fly launch --name spamshield-api
# Follow prompts, select Dockerfile
fly deploy
```

### Step 4: Deploy Frontend

```bash
cd ../frontend
fly launch --name spamshield-frontend
# Set VITE_API_URL environment variable
fly secrets set VITE_API_URL=https://spamshield-api.fly.dev
fly deploy
```

### Step 5: Configure CORS

```bash
fly secrets set CORS_ORIGINS=https://spamshield-frontend.fly.dev -a spamshield-api
```

---

## ☁️ AWS Deployment (Advanced)

### Option A: AWS App Runner (Easiest AWS Option)

1. **Create App Runner Service:**
   - Go to AWS Console → App Runner
   - Create service from container image or source code
   - Connect to GitHub repository

2. **Configure:**
   - Source: GitHub
   - Build: Docker
   - Port: 5000 (API) / 80 (Frontend)

3. **Environment Variables:** Set in App Runner console

### Option B: AWS ECS with Fargate

1. **Build and Push Images:**
   ```bash
   # Build images
   docker build -t spamshield-api -f api/Dockerfile .
   docker build -t spamshield-frontend -f frontend/Dockerfile ./frontend
   
   # Tag and push to ECR
   aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
   docker tag spamshield-api:latest <account>.dkr.ecr.<region>.amazonaws.com/spamshield-api:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/spamshield-api:latest
   ```

2. **Create ECS Task Definitions** for API and Frontend
3. **Create ECS Services** with Application Load Balancer
4. **Configure Environment Variables** in task definitions

### Option C: AWS EC2 (Traditional)

1. **Launch EC2 Instance** (Ubuntu recommended)
2. **Install Docker:**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   ```

3. **Clone Repository:**
   ```bash
   git clone <your-repo-url>
   cd spamshieldai-main
   ```

4. **Create .env file** with production settings
5. **Deploy:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

6. **Configure Security Group:** Open ports 80, 443, 5000
7. **Set up Nginx Reverse Proxy** (recommended)
8. **Configure SSL** with Let's Encrypt

---

## 🔒 Production Considerations

### Security

1. **Environment Variables:**
   - Never commit `.env` files
   - Use platform's secret management
   - Rotate secrets regularly

2. **CORS:**
   - Only allow your frontend domain
   - Remove localhost origins in production

3. **Rate Limiting:**
   - Add rate limiting to API (Flask-Limiter)
   - Prevent abuse

4. **HTTPS:**
   - Always use HTTPS in production
   - Most platforms provide automatic SSL

### Performance

1. **Model Loading:**
   - Models load on startup (already implemented)
   - Consider caching predictions for common inputs

2. **Scaling:**
   - Use platform's auto-scaling features
   - Consider CDN for frontend static assets

3. **Monitoring:**
   - Set up health checks (already configured)
   - Monitor API response times
   - Track error rates

### Cost Optimization

1. **Free Tier Limits:**
   - Railway: $5/month free credit
   - Render: Free tier with limitations
   - Fly.io: 3 shared VMs free

2. **Resource Usage:**
   - Monitor container resource usage
   - Optimize Docker images (multi-stage builds already used)
   - Use appropriate instance sizes

---

## 📝 Environment Variables for Cloud

Create these in your platform's environment variable settings:

```env
# API Service
API_PORT=5000
API_HOST=0.0.0.0
FLASK_ENV=production
FLASK_DEBUG=false
CORS_ORIGINS=https://your-frontend-domain.com

# Frontend Service
VITE_API_URL=https://your-api-domain.com
FRONTEND_PORT=80
```

---

## 🐛 Troubleshooting

### CORS Errors
- Ensure `CORS_ORIGINS` includes your frontend URL
- Check that URLs match exactly (including https/http)

### Models Not Found
- Verify models are in the repository or uploaded to persistent storage
- Check file paths in container logs

### Frontend Can't Connect to API
- Verify `VITE_API_URL` is set correctly
- Check API is accessible (test with curl)
- Ensure API health endpoint responds

### Port Issues
- Most platforms assign ports automatically
- Use `PORT` environment variable if platform requires it
- Check platform documentation for port configuration

---

## 🔗 Quick Links

- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Fly.io Docs](https://fly.io/docs/)
- [AWS App Runner Docs](https://docs.aws.amazon.com/apprunner/)

---

## 💡 Recommended Setup for Production

1. **Use Railway or Render** for quick deployment
2. **Separate API and Frontend** into different services
3. **Use platform's environment variables** instead of .env files
4. **Enable automatic HTTPS/SSL**
5. **Set up monitoring and alerts**
6. **Configure custom domain** (optional but recommended)

---

**Need help?** Check platform-specific documentation or open an issue in the repository.

