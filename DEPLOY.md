# Deployment Guide

## Option 1: Quick Deploy (Fastest - 10 minutes)

### Prerequisites
- Google Cloud account (free tier available)
- gcloud CLI installed

### Steps

1. **Install gcloud CLI** (if not already installed)
   ```bash
   # macOS
   brew install google-cloud-sdk

   # Ubuntu/Debian
   sudo apt-get install google-cloud-sdk

   # Or download: https://cloud.google.com/sdk/docs/install
   ```

2. **Login and setup**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Run quick deploy**
   ```bash
   cd AeroElite
   ./quick-deploy.sh
   ```

4. **Get your URLs**
   - Frontend: Displayed after deployment
   - Backend: Displayed after deployment
   - API Docs: `[BACKEND_URL]/docs`

---

## Option 2: Full Deploy with Database (30 minutes)

For production with PostgreSQL database:

```bash
cd AeroElite
./deploy.sh
```

This will:
- ✅ Create Cloud SQL database
- ✅ Create Cloud Storage bucket
- ✅ Deploy backend with database connection
- ✅ Deploy frontend
- ✅ Configure all services

---

## Option 3: Manual Deploy

### Backend

```bash
cd backend

# Deploy to Cloud Run
gcloud run deploy aeroelite-backend \
    --source . \
    --region=us-central1 \
    --allow-unauthenticated \
    --memory=2Gi
```

### Frontend

```bash
cd frontend

# Build
npm run build

# Deploy
gcloud run deploy aeroelite-frontend \
    --source . \
    --region=us-central1 \
    --allow-unauthenticated
```

---

## Environment Variables

After deployment, set these in Cloud Run console:

**Backend:**
- `GCP_PROJECT_ID` - Your GCP project ID
- `GEMINI_API_KEY` - Your Gemini API key
- `VERTEX_AI_LOCATION` - us-central1
- `JWT_SECRET` - Random secret key
- `DATABASE_URL` - (optional) PostgreSQL connection

**Frontend:**
- `REACT_APP_API_URL` - Backend Cloud Run URL
- `REACT_APP_GOOGLE_CLIENT_ID` - (optional) Google OAuth

---

## Get API Keys

### Gemini API Key (Free)
1. Visit: https://makersuite.google.com/app/apikey
2. Create API key
3. Add to Cloud Run environment

### Enable Vertex AI
```bash
gcloud services enable aiplatform.googleapis.com
```

---

## Verify Deployment

1. **Check services**
   ```bash
   gcloud run services list
   ```

2. **View logs**
   ```bash
   gcloud run services logs read aeroelite-backend
   gcloud run services logs read aeroelite-frontend
   ```

3. **Test API**
   ```bash
   curl https://[BACKEND_URL]/health
   ```

---

## Costs Estimate

**Free Tier:**
- Cloud Run: 2 million requests/month free
- Cloud Build: 120 build-minutes/day free
- Cloud Storage: 5 GB free

**Estimated Monthly Cost:**
- Basic usage: $0-5/month (within free tier)
- Moderate usage: $10-20/month
- Heavy usage: $50-100/month

---

## Custom Domain (Optional)

1. **Map domain to Cloud Run**
   ```bash
   gcloud run domain-mappings create \
       --service=aeroelite-frontend \
       --domain=aeroelite.yourdomain.com
   ```

2. **Add DNS records** (shown in console)

---

## Troubleshooting

**Build fails:**
```bash
# Check logs
gcloud builds log --stream
```

**Service not accessible:**
```bash
# Make sure it's public
gcloud run services set-iam-policy aeroelite-backend policy.yaml
```

**Database connection issues:**
```bash
# Check Cloud SQL instance
gcloud sql instances describe aeroelite-db
```

---

## Update/Redeploy

```bash
# Just run the script again
./quick-deploy.sh
```

Or rebuild specific service:
```bash
cd backend
gcloud run deploy aeroelite-backend --source .
```

---

## Monitoring

View in Google Cloud Console:
- Logs: https://console.cloud.google.com/logs
- Metrics: https://console.cloud.google.com/monitoring
- Cloud Run: https://console.cloud.google.com/run

---

## Support

If deployment fails:
1. Check logs: `gcloud run services logs read SERVICE_NAME`
2. Verify APIs enabled: `gcloud services list`
3. Check billing enabled: https://console.cloud.google.com/billing

---

## Next Steps After Deployment

1. ✅ Visit your frontend URL
2. ✅ Test creating a design
3. ✅ Check API documentation at `/docs`
4. ✅ Set up monitoring alerts
5. ✅ Configure custom domain (optional)
