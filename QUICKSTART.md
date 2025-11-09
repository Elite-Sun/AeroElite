# 🚀 Aero Elite - Deployment Instructions

## Choose Your Deployment Method

### 🌐 **OPTION 1: Deploy to Google Cloud (Recommended)**

Get live URLs like:
- Frontend: `https://aeroelite-frontend-xxxxx.run.app`
- Backend: `https://aeroelite-backend-xxxxx.run.app`

**Requirements:**
- Google Cloud account (free tier available - no credit card needed for trial)
- 10-15 minutes

**Steps:**

1. **Create GCP Account** (if you don't have one)
   - Go to: https://cloud.google.com/
   - Click "Get started for free"
   - You get $300 free credit

2. **Install gcloud CLI**
   ```bash
   # macOS
   brew install google-cloud-sdk

   # Ubuntu/Debian
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL

   # Windows
   # Download from: https://cloud.google.com/sdk/docs/install
   ```

3. **Deploy** (run ONE command)
   ```bash
   cd AeroElite
   ./quick-deploy.sh
   ```

4. **Done!** 🎉
   - The script will output your live URLs
   - Visit the frontend URL to use Aero Elite

**Cost:** FREE for first year with $300 credit, then ~$5-10/month

---

### 💻 **OPTION 2: Run Locally** (5 minutes)

Run on your computer for testing:

**Requirements:**
- Docker Desktop installed

**Steps:**

1. **Install Docker**
   - macOS: https://docs.docker.com/desktop/install/mac-install/
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Linux: https://docs.docker.com/desktop/install/linux-install/

2. **Start Application**
   ```bash
   cd AeroElite
   ./start-local.sh
   ```

3. **Access**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

**Cost:** FREE (runs on your machine)

---

### 🎯 **OPTION 3: Deploy to Free Hosting**

Deploy frontend to Vercel/Netlify (free):

**Vercel (Frontend Only):**
```bash
cd frontend
npm install -g vercel
vercel
```

**Netlify (Frontend Only):**
```bash
cd frontend
npm install -g netlify-cli
netlify deploy --prod
```

**Note:** This deploys frontend only. Backend features won't work without cloud deployment.

---

## 🔧 Configuration

### Minimal Setup (No AI features)

Works immediately, limited functionality:
- ✅ UI works
- ✅ 3D viewer works
- ❌ AI prompt-to-CAD disabled
- ❌ Dataset search disabled

### Full Setup (All features)

Add to `.env`:
```env
GCP_PROJECT_ID=your-project-id
GEMINI_API_KEY=your-api-key
```

Get Gemini API key (FREE):
1. Visit: https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env`

---

## 📊 Quick Comparison

| Method | Time | Cost | Features | Public URL |
|--------|------|------|----------|------------|
| **Google Cloud** | 15 min | $0-10/mo* | Full | ✅ Yes |
| **Local Docker** | 5 min | Free | Full** | ❌ No |
| **Vercel/Netlify** | 5 min | Free | Limited | ✅ Yes |

*Free for first year with $300 credit
**Requires API keys for AI features

---

## 🎬 Quick Start (Recommended)

**Fastest way to get a working demo:**

1. **Local Demo (2 minutes):**
   ```bash
   cd AeroElite
   docker-compose up -d
   # Visit http://localhost:3000
   ```

2. **Cloud Deploy (10 minutes):**
   ```bash
   cd AeroElite
   gcloud auth login  # One-time setup
   ./quick-deploy.sh
   # Get live URL
   ```

---

## 💡 What I Recommend

**For Testing/Development:**
→ Use **Local Docker** (Option 2)

**For Sharing/Demonstration:**
→ Use **Google Cloud** (Option 1)

**For Quick Frontend Preview:**
→ Use **Vercel** (Option 3)

---

## ❓ Need Help?

**Common Issues:**

1. **"gcloud not found"**
   - Install gcloud CLI (see Option 1, step 2)

2. **"Docker not running"**
   - Start Docker Desktop application

3. **"Permission denied"**
   ```bash
   chmod +x *.sh
   ```

4. **"Port already in use"**
   ```bash
   docker-compose down
   ```

---

## 📞 Next Steps

Choose your preferred option above and run the commands. Each script is designed to be run with a single command and will guide you through the process.

**Which would you like to try first?**
1. Cloud deployment (live URL)
2. Local deployment (your computer)
3. Free hosting (frontend only)
