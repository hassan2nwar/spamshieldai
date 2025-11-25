# SpamShield Deployment & Integration Guide

## Project Structure
- `frontend/` — React/Vite app (copied from https://github.com/hassan2nwar/SpamShield)
- `api/` — Flask backend API (`/api/analyze`)
- `models/` — Trained ML model and vectorizer
- `data/` — Raw data and training artifacts

---

## 1. Running Locally

### Backend (Flask API)
```bash
chmod +x api/deploy-setup.sh
./api/deploy-setup.sh
python api/app.py
```
API will run at `http://localhost:5000/api/analyze`

### Frontend (React/Vite)
```bash
cd frontend
npm install
npm run dev
```
Frontend will run at `http://localhost:5173`

---

## 2. Deploying Backend (Railway/Heroku)
- Push your backend code to a new GitHub repo (e.g. `spamshield-api`)
- Deploy on Railway:
  - Go to https://railway.app
  - Click "New Project" → "Deploy from GitHub" → Select your repo
  - Set the root directory to your backend (if needed)
  - Railway will auto-detect the `Procfile` and deploy
- Your API will be live at `https://your-railway-url.up.railway.app/api/analyze`

---

## 3. Connecting Frontend to Backend
- In your frontend code (e.g. `EmailChecker.tsx`), set:
```typescript
const API_URL = 'https://your-railway-url.up.railway.app/api/analyze';
```
- Deploy your frontend to Netlify (or Vercel, etc.)
- Your live site will now use the ML backend for predictions!

---

## 4. Troubleshooting
- If you see CORS errors, add CORS support to Flask:
  - Install: `pip install flask-cors`
  - Add to `api/app.py`:
    ```python
    from flask_cors import CORS
    CORS(app)
    ```
- If model files are missing, re-run training or copy from `models/`
- For slow API responses, check Railway logs and optimize model loading

---

## 5. Next Steps
- Add authentication or rate limiting to your API for production
- Monitor usage and errors via Railway dashboard
- Update frontend UI for better error handling

---

## 6. Resources
- [SpamShield Frontend Repo](https://github.com/hassan2nwar/SpamShield)
- [Railway Docs](https://docs.railway.app/)
- [Netlify Docs](https://docs.netlify.com/)
- [Flask Docs](https://flask.palletsprojects.com/)

---

**SpamShield is now ready for full-stack deployment! 🚀**
