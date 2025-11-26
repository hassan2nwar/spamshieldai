# Models Deployment Guide

The SpamShield AI application requires two model files:
- `models/spam_classifier.pkl` - The trained spam classifier
- `models/vectorizer.pkl` - The text vectorizer

## Option 1: Include in Git Repository (Recommended for Small Models)

If your model files are **under 100MB total**, you can commit them to Git:

```bash
git add models/spam_classifier.pkl models/vectorizer.pkl
git commit -m "Add ML models"
git push
```

**Pros:**
- ✅ Simplest approach
- ✅ Models are versioned with code
- ✅ No additional setup needed

**Cons:**
- ❌ Increases repository size
- ❌ May hit Git LFS limits for very large models

## Option 2: Git LFS (For Larger Models)

If models are **over 100MB**, use Git LFS:

```bash
# Install Git LFS
git lfs install

# Track model files
git lfs track "*.pkl"
git add .gitattributes
git add models/*.pkl
git commit -m "Add models via Git LFS"
git push
```

## Option 3: Platform-Specific Storage

### Railway

**Using Volumes:**
1. Go to your API service → **Volumes** tab
2. Create a new volume
3. Mount it to `/app/models`
4. Upload models via Railway CLI:

```bash
railway run bash
# Then inside the container:
# Upload your models to the mounted volume
```

**Using External Storage:**
Upload models to S3/Cloud Storage and download on startup:

```python
# Add to api/app.py startup
import boto3
import os

if os.environ.get('MODELS_S3_BUCKET'):
    s3 = boto3.client('s3')
    s3.download_file('your-bucket', 'spam_classifier.pkl', '/app/models/spam_classifier.pkl')
    s3.download_file('your-bucket', 'vectorizer.pkl', '/app/models/vectorizer.pkl')
```

### Render

**Using Persistent Disks:**
1. Go to service settings → **Persistent Disks**
2. Create disk and mount to `/app/models`
3. Upload models via Render Shell or CLI

### Fly.io

**Using Volumes:**
```bash
# Create volume
fly volumes create models --size 1 --region iad

# Attach to app
fly volumes attach models -a spamshield-api

# Upload models (SSH into machine)
fly ssh console -a spamshield-api
# Then use scp or other method to upload
```

## Option 4: Build Models into Docker Image

Modify `api/Dockerfile` to copy models during build:

```dockerfile
# Copy models directory
COPY models /app/models
```

This bakes models into the image. **Pros:** Simple, no runtime downloads. **Cons:** Larger images, slower builds.

## Option 5: Download on Container Startup

Create a startup script that downloads models:

```python
# models_downloader.py
import os
import urllib.request
from pathlib import Path

MODELS_URL = os.environ.get('MODELS_URL', '')
MODELS_DIR = Path('/app/models')

if MODELS_URL:
    MODELS_DIR.mkdir(exist_ok=True)
    urllib.request.urlretrieve(f'{MODELS_URL}/spam_classifier.pkl', 
                               MODELS_DIR / 'spam_classifier.pkl')
    urllib.request.urlretrieve(f'{MODELS_URL}/vectorizer.pkl', 
                               MODELS_DIR / 'vectorizer.pkl')
```

Then call this in your Dockerfile before starting the app.

## Recommended Approach

**For Quick Deployment:**
- Use **Option 1** (include in Git) if models are small
- Use **Option 4** (bake into image) for simplicity

**For Production:**
- Use **Option 3** (platform storage) for flexibility
- Use **Option 5** (download on startup) for version control

## Checking Model Sizes

```bash
# Check model file sizes
ls -lh models/*.pkl

# On Windows
dir models\*.pkl
```

If total size is < 100MB, Option 1 is recommended.

## Troubleshooting

**"Models not found" error:**
1. Check models exist in container: `docker exec <container> ls -la /app/models`
2. Verify file paths in `api/app.py`
3. Check volume mounts (if using volumes)
4. Review container logs for model loading errors

**Large repository size:**
- Use Git LFS (Option 2)
- Or use external storage (Option 3 or 5)

