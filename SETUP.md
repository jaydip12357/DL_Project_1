# MediAlert Setup Guide

## Overview

MediAlert is a two-tier system:
1. **Hospital Portal** - For uploading X-rays and getting AI analysis
2. **Surveillance Dashboard** - For real-time pandemic tracking

This guide will help you set up the complete system.

---

## Step 1: Find Your Friend's Model API URL

Your MediAlert system integrates with your friend's pneumonia detection model via an API. You need to find the endpoint URL.

### Option A: Model API is Already Deployed on Railway

Ask your friend for the Railway deployment URL. It should look like:
```
https://your-model-api.railway.app/predict
```

Then set:
```
MODEL_API_URL=https://your-model-api.railway.app/predict
MODEL_API_HEALTH_URL=https://your-model-api.railway.app/health
```

### Option B: Model API is Local/Not Yet Deployed

If your friend's model is a Python Flask/FastAPI app, you'll deploy it separately:

1. **Get the model code from your friend**
2. **Ensure it has these endpoints:**
   ```
   POST /predict
   - Input: multipart/form-data with 'image' file
   - Output: JSON with {prediction, confidence, probabilities, model_version, processing_time_ms}

   GET /health
   - Output: JSON with {status: 'healthy'}
   ```

3. **Deploy it to Railway** (alongside MediAlert)

### Option C: Local Development

If you want to test locally first:
```
MODEL_API_URL=http://localhost:8000/predict
MODEL_API_HEALTH_URL=http://localhost:8000/health
```

---

## Step 2: Set Up Supabase (Database)

### 2.1 Create Supabase Account
1. Go to https://supabase.com
2. Sign up with GitHub or email
3. Create a new project

### 2.2 Get Your Credentials
After creating a project, go to **Settings > API** and copy:
- `SUPABASE_URL` (looks like `https://xxxxx.supabase.co`)
- `SUPABASE_KEY` (looks like `eyJhb...`)

### 2.3 Set Up Database Schema
1. Go to **SQL Editor** in your Supabase dashboard
2. Click **New Query**
3. Copy all the SQL from `database_schema.sql` and paste it
4. Click **Run**

This creates all the tables and inserts sample hospital data.

---

## Step 3: Set Up Environment Variables

### Create `.env` file in project root:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# Model API (from Step 1)
MODEL_API_URL=https://your-model-api.railway.app/predict
MODEL_API_HEALTH_URL=https://your-model-api.railway.app/health
MODEL_API_KEY=

# Mapbox (for interactive maps)
MAPBOX_ACCESS_TOKEN=your_mapbox_token

# Flask Configuration
SECRET_KEY=your-random-secret-key-min-32-chars
DEBUG=False

# File Configuration
MAX_FILE_SIZE_MB=10
API_TIMEOUT_SECONDS=10
```

### Optional: Mapbox for Interactive Maps
To use interactive geographic maps:
1. Go to https://www.mapbox.com
2. Sign up for free
3. Go to **Account > Tokens**
4. Copy your Default public token
5. Add to `.env` as `MAPBOX_ACCESS_TOKEN`

---

## Step 4: Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 5: Test Locally

```bash
# Run the Flask app
python -m flask --app app.main run --debug

# Visit http://localhost:5000
```

You should see:
- ✅ Landing page with two portals
- ✅ Health check at `/health` showing model API status

---

## Step 6: Deploy to Railway

### 6.1 Prerequisites
- Railway account at https://railway.app
- GitHub repository connected

### 6.2 Deploy

1. **Push code to GitHub:**
   ```bash
   git push origin claude/review-repo-changes-404Rt
   ```

2. **Create Railway project:**
   - Go to railway.app
   - Click **New Project**
   - Select **Deploy from GitHub**
   - Select your repository
   - Select branch `claude/review-repo-changes-404Rt`

3. **Add Environment Variables:**
   - Go to **Variables** in Railway dashboard
   - Add all variables from `.env`:
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `MODEL_API_URL`
     - `MODEL_API_HEALTH_URL`
     - `SECRET_KEY`
     - `MAPBOX_ACCESS_TOKEN`
     - `DEBUG=False`

4. **Configure Port:**
   - Railway should auto-detect Flask app
   - If not, set `PORT=5000` in variables

5. **Deploy:**
   - Railway will automatically deploy when you push to the branch

---

## Step 7: Hospital Portal Login

### Default Test Credentials

The database comes pre-populated with 5 hospitals. Use any of these:

```
Hospital ID: (UUID from database)
API Key: (UUID from database)
```

**To get Hospital ID and API Key:**

1. Go to your Supabase project
2. Click **Table Editor**
3. Open **hospitals** table
4. Copy `id` and `api_key` from any hospital row

Or in Railway:

```bash
# Run SQL query
SELECT id, name, api_key FROM hospitals LIMIT 1;
```

### Access Hospital Portal

1. Go to `https://your-railway-url/hospital/login`
2. Enter Hospital ID and API Key
3. You'll see the hospital dashboard

---

## Step 8: Surveillance Dashboard

The surveillance dashboard is public (no login required):

1. Go to `https://your-railway-url/surveillance`
2. You'll see:
   - ✅ Global case statistics
   - ✅ Country-level heat map
   - ✅ Case trends
   - ✅ Active alerts
   - ✅ Hospital network status

The dashboard is pre-populated with 30 days of dummy data showing exponential case growth.

---

## System Architecture

```
┌─────────────────────────────────────────┐
│  MediAlert Frontend                     │
│  (Hospital Portal + Surveillance)       │
└────────────┬────────────────────────────┘
             │
        ┌────▼────────────────────┐
        │   Flask Backend         │
        │   (Railway)             │
        └────┬────────┬───────┬───┘
             │        │       │
    ┌────────▼──┐ ┌───▼─────┐ └──────┐
    │ Supabase  │ │ Model   │        │
    │(Database) │ │ API     │ Health │
    │           │ │ (external)       │
    └───────────┘ └────────────────┘
```

---

## Data Flow

### Hospital Upload Flow
```
Doctor → Hospital Portal → Flask App → Model API → Analysis Result
                                    → Supabase (save analysis)
                                    → Surveillance Dashboard updates
```

### Surveillance Data Flow
```
Supabase Data → Flask (aggregation) → Dashboard (visualization)
```

---

## Troubleshooting

### Issue: "MODEL_API_URL not configured"
**Solution:** Make sure you've set `MODEL_API_URL` in `.env` or Railway variables

### Issue: "Cannot connect to Supabase"
**Solution:**
- Check `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Ensure database tables are created (run `database_schema.sql`)
- Check network connectivity

### Issue: "Hospital login fails"
**Solution:**
- Verify Hospital ID and API Key exist in `hospitals` table
- Check that hospital record is in Supabase

### Issue: "Map not showing"
**Solution:** Mapbox token is optional. Without it, surveillance dashboard works but without the interactive map.

---

## Testing Checklist

- [ ] Landing page loads with two portals
- [ ] Hospital login page loads
- [ ] Hospital dashboard loads (after login)
- [ ] Upload X-ray image (you'll need a test image)
- [ ] Get analysis result
- [ ] Surveillance dashboard loads
- [ ] Global statistics show
- [ ] No errors in Flask logs

---

## Next Steps

1. **Test locally** with your friend's model API
2. **Deploy to Railway**
3. **Load real hospital data** (replace dummy data with actual hospitals)
4. **Customize branding** (colors, logos, hospital names)
5. **Set up real alerts** (email, SMS integrations)
6. **Add user authentication** (currently using simple API keys)

---

## Support

For issues with:
- **Model API**: Ask your friend for documentation
- **Supabase**: Check https://supabase.com/docs
- **Railway**: Check https://railway.app/docs
- **MediAlert**: Review the PRD and architecture docs

---

**Created:** February 2026
**Version:** 1.0-beta
