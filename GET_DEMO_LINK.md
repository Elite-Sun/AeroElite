# 🌐 Get Your Aero Elite Demo Link

## ⚡ Fastest Way - ONE Command Deploy (10 minutes)

### Step 1: Install gcloud CLI

**macOS:**
```bash
brew install google-cloud-sdk
```

**Windows:**
Download installer: https://cloud.google.com/sdk/docs/install

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Step 2: Login to Google Cloud

```bash
gcloud auth login
```

This opens your browser - login with your Google account.

### Step 3: Create/Select Project

```bash
# List existing projects
gcloud projects list

# Or create new one
gcloud projects create aeroelite-demo-$(date +%s) --name="Aero Elite Demo"

# Set as active
gcloud config set project YOUR_PROJECT_ID
```

### Step 4: Deploy (ONE Command!)

```bash
cd AeroElite
./quick-deploy.sh
```

**That's it!** The script will:
- ✅ Enable required APIs
- ✅ Deploy backend to Cloud Run
- ✅ Deploy frontend to Cloud Run
- ✅ Give you live URLs

### Your Demo Links

After deployment completes (10 minutes), you'll see:

```
============================================
🎉 Deployment Complete!
============================================

🌐 Application URL: https://aeroelite-frontend-xxxxx-uc.a.run.app
🔌 API URL: https://aeroelite-backend-xxxxx-uc.a.run.app
📚 API Docs: https://aeroelite-backend-xxxxx-uc.a.run.app/docs
```

**Copy the Application URL - that's your demo link!**

---

## 🎯 Alternative: Local Demo (5 minutes)

If you want to test locally first:

### Requirements
- Docker Desktop installed

### Run

```bash
cd AeroElite
./start-local.sh
```

**Access at:** http://localhost:3000

---

## 💰 Cost

**Google Cloud:**
- FREE for first year ($300 credit)
- After free tier: ~$5-10/month
- Can delete anytime to stop charges

**Local:**
- FREE (runs on your computer)

---

## 🔑 Optional: Enable AI Features

For full functionality, add Gemini API key:

1. Get free API key: https://makersuite.google.com/app/apikey
2. After deployment, go to: https://console.cloud.google.com/run
3. Click on "aeroelite-backend"
4. Click "Edit & Deploy New Revision"
5. Add environment variable:
   - Name: `GEMINI_API_KEY`
   - Value: `your-api-key-here`
6. Deploy

---

## 📱 Share Your Demo

Once deployed, you can share your demo link with anyone:

```
Check out Aero Elite - AI Aircraft Design System:
https://aeroelite-frontend-xxxxx-uc.a.run.app

Try creating a wing with this prompt:
"Create a 25m wingspan with NACA2412 airfoil,
4° dihedral, 2.5m root chord"
```

---

## 🆘 Troubleshooting

**"gcloud: command not found"**
→ Install gcloud CLI (see Step 1)

**"You do not have permission"**
→ Enable billing: https://console.cloud.google.com/billing

**"Build failed"**
→ Check logs: `gcloud builds log --stream`

**Want to delete everything?**
```bash
gcloud run services delete aeroelite-backend --region=us-central1
gcloud run services delete aeroelite-frontend --region=us-central1
```

---

## 📞 Need Help?

1. Check [DEPLOY.md](DEPLOY.md) for detailed instructions
2. Check [QUICKSTART.md](QUICKSTART.md) for all deployment options
3. View logs: `gcloud run services logs read aeroelite-backend`

---

## 🎉 What's Next?

After getting your demo link:

1. ✅ Visit your demo URL
2. ✅ Create a design with a prompt
3. ✅ View in 3D
4. ✅ Run physics validation
5. ✅ Export CAD model
6. ✅ Share your demo link!

---

## 📊 Quick Reference

| What | Command |
|------|---------|
| **Deploy to cloud** | `./quick-deploy.sh` |
| **Run locally** | `./start-local.sh` |
| **View services** | `gcloud run services list` |
| **View logs** | `gcloud run services logs read aeroelite-backend` |
| **Delete deployment** | `gcloud run services delete aeroelite-backend` |

---

**Ready to deploy? Run this:**

```bash
cd AeroElite
./quick-deploy.sh
```

Your demo link will appear in 10 minutes! 🚀
