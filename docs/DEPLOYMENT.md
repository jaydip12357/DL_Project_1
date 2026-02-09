# Railway Deployment Guide

This guide covers deploying the pneumonia detection web application to Railway.

## Prerequisites

- GitHub repository with the application code
- Railway account (https://railway.app)
- Model API endpoint URL (from the model team)

## Deployment Steps

### 1. Connect Repository

1. Log in to Railway
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the Python project

### 2. Configure Environment Variables

In Railway dashboard, go to your service → Variables tab and add:

**Required:**
```
MODEL_API_URL=https://your-model-api.railway.app/predict
SECRET_KEY=<generate-a-random-32-char-string>
```

**Optional:**
```
MODEL_API_HEALTH_URL=https://your-model-api.railway.app/health
MODEL_API_KEY=<if-authentication-required>
API_TIMEOUT_SECONDS=10
MAX_FILE_SIZE_MB=10
DEBUG=False
```

To generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

### 3. Deploy

1. Railway automatically deploys when you push to main branch
2. Or manually trigger deploy from the dashboard
3. Wait for build to complete (usually 1-2 minutes)

### 4. Verify Deployment

1. Click the generated URL in Railway dashboard
2. Check the health endpoint: `https://your-app.railway.app/health`
3. Expected response:
   ```json
   {"status": "healthy", "model_api": "connected"}
   ```

### 5. Test the Application

1. Open the app URL in browser
2. Upload a test X-ray image
3. Verify you receive a prediction result
4. Check error handling with invalid files

## Configuration Files

Railway uses these files:

- **Procfile**: `web: gunicorn app.main:app`
- **runtime.txt**: `python-3.10.12`
- **requirements.txt**: Python dependencies

## Monitoring

### View Logs

1. Go to Railway dashboard → your service
2. Click "Logs" tab
3. Filter by deployment or view live logs

### Health Checks

Railway automatically monitors your app. The `/health` endpoint provides:
- Overall application status
- Model API connectivity status

## Updating the Application

1. Push changes to main branch
2. Railway automatically redeploys
3. Zero-downtime deployment

## Rollback

If a deployment has issues:

1. Go to Railway dashboard → Deployments
2. Find the previous working deployment
3. Click "Rollback" to restore

## Custom Domain (Optional)

1. Go to Settings → Domains
2. Add your custom domain
3. Configure DNS CNAME record as instructed

## Troubleshooting

### App won't start

- Check Procfile syntax
- Verify requirements.txt is complete
- Check logs for import errors

### Model API connection fails

- Verify MODEL_API_URL is correct
- Check if model API is deployed and running
- Try the health check endpoint directly

### Slow response times

- Model inference can take a few seconds
- First request after idle may be slower (cold start)
- Consider keeping the API warm

### Memory issues

- Railway free tier has limits
- Optimize image handling to reduce memory
- Consider upgrading plan for production use

## Environment Comparison

| Setting | Development | Production |
|---------|-------------|------------|
| DEBUG | True | False |
| SECRET_KEY | dev-key | Random secure key |
| MODEL_API_URL | localhost or test | Production API URL |
