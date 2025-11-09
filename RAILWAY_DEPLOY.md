# 🚂 Railway Deployment Guide for Aero Elite

## Quick Deploy (2 Methods)

### Method 1: Deploy Backend Only (Fastest)

1. **Go to Railway:** https://railway.app/new
2. **Login with GitHub**
3. **Click "Deploy from GitHub repo"**
4. **Select:** `Elite-Sun/AeroElite`
5. **Branch:** `claude/aero-elite-ai-cad-system-011CUwRmFT5mB5raBa8UiQiC`
6. **Root Directory:** Set to `backend`
7. **Click Deploy**

Railway will auto-detect Python and deploy the backend.

**You'll get:** `https://aeroelite-production.up.railway.app`

### Method 2: Deploy as Two Services

#### Deploy Backend:
1. Create new project on Railway
2. Add service from GitHub repo
3. Root directory: `backend`
4. Add environment variables:
   - `PORT=8000`
   - `DATABASE_URL=` (Railway will provide PostgreSQL)
   - `GCP_PROJECT_ID=demo-project`
   - `JWT_SECRET=your-secret-here`

#### Deploy Frontend:
1. Add another service
2. Root directory: `frontend`
3. Environment variable:
   - `REACT_APP_API_URL=` (your backend URL from step 1)

---

## Environment Variables to Add

Once deployed, add these in Railway dashboard:

**Backend Service:**
```
PORT=8000
GCP_PROJECT_ID=demo-project
GEMINI_API_KEY=your-api-key (optional, for AI features)
VERTEX_AI_LOCATION=us-central1
JWT_SECRET=random-secret-key-here
DATABASE_URL=${{Postgres.DATABASE_URL}} (if you add PostgreSQL)
CORS_ORIGINS=https://your-frontend-url.railway.app
```

**Frontend Service:**
```
REACT_APP_API_URL=https://your-backend-url.railway.app
```

---

## Add PostgreSQL Database (Optional)

1. In Railway project, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway auto-creates `DATABASE_URL`
4. It's automatically available to your backend

---

## Troubleshooting

### "Build failed"
- Check logs in Railway dashboard
- Make sure root directory is set correctly

### "App crashed"
- Add `PORT` environment variable
- Check startup command is correct

### "Cannot connect to backend"
- Update `REACT_APP_API_URL` in frontend
- Update `CORS_ORIGINS` in backend
- Redeploy frontend after changing env vars

---

## Alternative: Simplified Backend-Only Deploy

Just deploy the backend and use the API:

1. Deploy backend only (Method 1 above)
2. Access API docs at: `https://your-url.railway.app/docs`
3. Use the interactive API documentation

---

## Cost

- **Free Tier:** $5 credit/month (enough for testing)
- **Hobby Plan:** $5/month for more resources
- **Can pause/delete anytime**

---

## Step-by-Step with Screenshots

1. **Create Account:** https://railway.app
2. **New Project:** Click "+ New Project"
3. **Deploy from GitHub:** Select your repo
4. **Configure:**
   - Service 1: Backend (root: `backend`)
   - Service 2: Frontend (root: `frontend`)
5. **Add PostgreSQL:** Optional database
6. **Set Environment Variables:** As listed above
7. **Deploy!**

---

## Quick Test

After deployment:

1. Visit your frontend URL
2. Try creating a design
3. Check API docs at `/docs`

---

## Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check Railway logs for errors

---

## What Gets Deployed

✅ Backend API (FastAPI)
✅ Frontend UI (React)
✅ Database (PostgreSQL - optional)
✅ All features except AI*

*AI features require Gemini API key (free from Google)

---

## Summary

**Easiest way:**
1. Go to https://railway.app/new
2. Deploy from GitHub: `Elite-Sun/AeroElite`
3. Root directory: `backend`
4. Done! You get a live API

**Full deployment:**
- Deploy backend (root: `backend`)
- Deploy frontend (root: `frontend`)
- Connect them via environment variables
- Add PostgreSQL if needed

Both work, choose based on your needs!
