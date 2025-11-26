# 🚀 Quick Deploy Guide - Get Live in 5 Minutes

Choose your platform and follow the steps:

## Option 1: Railway (Recommended - Easiest)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign up/login
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will auto-detect Docker

### Step 3: Add Two Services

**Service 1: API**
- Click **"+ New"** → **"GitHub Repo"** (if not already added)
- In service settings:
  - **Root Directory:** `/` (leave empty)
  - **Dockerfile Path:** `api/Dockerfile`
  - **Port:** `5000`

**Service 2: Frontend**
- Click **"+ New"** → **"GitHub Repo"** (same repo)
- In service settings:
  - **Root Directory:** `/frontend`
  - **Dockerfile Path:** `Dockerfile`
  - **Port:** `80`

### Step 4: Set Environment Variables

**For API Service:**
1. Go to API service → **Variables** tab
2. Add:
   ```
   CORS_ORIGINS=https://your-frontend-name.up.railway.app
   FLASK_ENV=production
   ```

**For Frontend Service:**
1. Go to Frontend service → **Variables** tab
2. Add:
   ```
   VITE_API_URL=https://your-api-name.up.railway.app
   ```
   (Replace with your actual API URL from Railway)

### Step 5: Deploy Models

**Option A:** If models are in your repo (< 100MB):
- They'll be included automatically ✅

**Option B:** If models are too large:
1. Go to API service → **Volumes** tab
2. Create a volume and mount to `/app/models`
3. Upload models via Railway CLI or SSH

### Step 6: Get Your URLs

Railway provides URLs like:
- API: `https://spamshield-api-production.up.railway.app`
- Frontend: `https://spamshield-frontend-production.up.railway.app`

**Update frontend's `VITE_API_URL`** with your API URL and redeploy!

---

## Option 2: Render (Free Tier)

### Step 1: Push to GitHub
(Same as Railway)

### Step 2: Deploy Backend

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `spamshield-api`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `api/Dockerfile`
   - **Root Directory:** `/` (leave empty)
   - **Port:** `5000`

### Step 3: Deploy Frontend

1. Click **"New +"** → **"Web Service"**
2. Same repository
3. Configure:
   - **Name:** `spamshield-frontend`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `frontend/Dockerfile`
   - **Root Directory:** `/frontend`
   - **Port:** `80`

### Step 4: Environment Variables

**Backend:**
```
CORS_ORIGINS=https://spamshield-frontend.onrender.com
FLASK_ENV=production
```

**Frontend:**
```
VITE_API_URL=https://spamshield-api.onrender.com
```

### Step 5: Deploy!

Click **"Create Web Service"** for both. Render will build and deploy automatically.

---

## Option 3: Fly.io (Global Edge)

### Step 1: Install Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login
```bash
fly auth login
```

### Step 3: Deploy API

```bash
cd api
fly launch --name spamshield-api
# When prompted:
# - Select Dockerfile: api/Dockerfile
# - Port: 5000
# - Region: Choose closest to you
fly secrets set CORS_ORIGINS=https://spamshield-frontend.fly.dev
fly deploy
```

### Step 4: Deploy Frontend

```bash
cd ../frontend
fly launch --name spamshield-frontend
# When prompted:
# - Select Dockerfile: frontend/Dockerfile
# - Port: 80
fly secrets set VITE_API_URL=https://spamshield-api.fly.dev
fly deploy
```

Done! Your app is live at:
- API: `https://spamshield-api.fly.dev`
- Frontend: `https://spamshield-frontend.fly.dev`

---

## ✅ Post-Deployment Checklist

- [ ] API health check works: `https://your-api-url/api/health`
- [ ] Frontend loads correctly
- [ ] Frontend can connect to API (test the analyze feature)
- [ ] CORS is configured correctly
- [ ] HTTPS is enabled (automatic on most platforms)
- [ ] Environment variables are set correctly

---

## 🐛 Common Issues

**"CORS Error"**
- Make sure `CORS_ORIGINS` in API includes your frontend URL exactly
- Check URLs use `https://` not `http://`

**"Frontend can't connect to API"**
- Verify `VITE_API_URL` is set to your API URL
- Check API is accessible: visit API URL in browser

**"Models not found"**
- Ensure models are in repository or uploaded to persistent storage
- Check file paths in container logs

---

## 🎉 You're Live!

Share your frontend URL with others to use your SpamShield AI application!

For more detailed information, see [CLOUD_DEPLOY.md](CLOUD_DEPLOY.md)

