# 🚂 Railway Simple Deployment - Backend API Only

## ✅ This Will Work Now!

I've simplified the deployment to **backend-only** which is much more reliable.

---

## 🚀 Deploy in 3 Steps (5 minutes)

### Step 1: Go to Railway

Visit: **https://railway.app/new**

### Step 2: Deploy from GitHub

1. Click **"Deploy from GitHub repo"**
2. Login with GitHub if needed
3. Select: **`Elite-Sun/AeroElite`**
4. Branch: **`claude/aero-elite-ai-cad-system-011CUwRmFT5mB5raBa8UiQiC`**
5. Click **"Deploy"**

### Step 3: Wait for Build

Railway will:
- ✅ Detect the `railway.toml` configuration
- ✅ Use `Dockerfile.railway` to build
- ✅ Install Python dependencies
- ✅ Start the FastAPI backend
- ✅ Give you a live URL!

---

## 🎉 What You Get

After ~5 minutes:

```
✅ Backend API: https://aeroelite-production-xxxx.up.railway.app
✅ API Docs: https://aeroelite-production-xxxx.up.railway.app/docs
✅ Health Check: https://aeroelite-production-xxxx.up.railway.app/health
```

---

## 📚 Try the API

Once deployed:

1. **Visit API Docs:** `https://your-url.railway.app/docs`
2. **Interactive Testing:** Try all endpoints directly in browser
3. **Create Design:** Use `/api/v1/design/create` endpoint
4. **View Response:** See AI-generated parameters

### Example API Request:

```bash
curl -X POST "https://your-url.railway.app/api/v1/design/create" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 25m wing with NACA2412 airfoil",
    "component_type": "wing",
    "is_public": true
  }'
```

---

## 🎨 Add Frontend Later (Optional)

If you want the UI too:

### Option A: Deploy Frontend on Vercel (Free)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel

# Point frontend to your Railway backend URL
# Add environment variable: REACT_APP_API_URL=https://your-railway-url.railway.app
```

### Option B: Deploy Frontend on Netlify

1. Go to https://netlify.com
2. Drag & drop the `frontend` folder
3. Add environment variable: `REACT_APP_API_URL`

---

## 🔧 Environment Variables (Optional)

For full AI features, add these in Railway dashboard:

1. Click on your deployment
2. Go to "Variables" tab
3. Add:
   - `GEMINI_API_KEY` = your-api-key (get free from https://makersuite.google.com)
   - `GCP_PROJECT_ID` = demo-project
   - `JWT_SECRET` = random-secret-key

**Without these:** API still works but AI features are limited.

---

## 📊 What's Working

**✅ Fully Functional:**
- REST API
- Database models
- CAD generation (without AI)
- Physics validation
- Assembly system
- Export functionality

**⚠️ Requires API Key:**
- AI prompt parsing (needs Gemini API key)
- Dataset search (optional)

**❌ Not Included:**
- Frontend UI (deploy separately if needed)

---

## 🐛 Troubleshooting

### Build Still Failing?

1. Check Railway logs for error
2. Make sure you're on the correct branch
3. Try "Redeploy" in Railway dashboard

### "Module not found" Error?

Railway needs time to install dependencies. Wait for build to complete (~5 min).

### Database Error?

Add PostgreSQL in Railway:
1. In your project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway auto-connects it

---

## 💰 Cost

- **Free Plan:** $5 credit/month (plenty for testing)
- **Hobby Plan:** $5/month for more resources
- Delete anytime to stop charges

---

## 📞 Quick Links

- **Railway Dashboard:** https://railway.app/dashboard
- **Railway Docs:** https://docs.railway.app
- **Gemini API Key:** https://makersuite.google.com/app/apikey

---

## ✨ Success Checklist

After deployment:

- [ ] Backend URL is live
- [ ] `/health` endpoint returns OK
- [ ] `/docs` shows API documentation
- [ ] Can test endpoints in browser
- [ ] (Optional) Added Gemini API key
- [ ] (Optional) Deployed frontend separately

---

## 🎯 Summary

**What you have now:**
- ✅ Working backend API
- ✅ Interactive API documentation
- ✅ All core features functional
- ✅ Public URL to share

**Next steps if you want full UI:**
- Deploy frontend on Vercel or Netlify
- Connect it to your Railway backend URL

---

**Try deploying now! It should work this time.** 🚀

Visit: https://railway.app/new
