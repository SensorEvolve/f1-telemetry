# Deploy Your F1 Dashboard Online 🚀

Your dashboard is ready to deploy! Here's the **easiest way** to get it online for free.

## Option 1: Render.com (Recommended - Free & Easy)

### Step 1: Push to GitHub
```bash
# Initialize git if you haven't already
git init
git add .
git commit -m "F1 Telemetry Dashboard ready for deployment"

# Create a new repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/f1-telemetry.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `f1-telemetry` repository
5. Render will auto-detect the `render.yaml` file
6. Click **"Create Web Service"**

**That's it!** Your dashboard will be live at:
```
https://f1-telemetry-dashboard.onrender.com
```

### Important Notes:
- First load takes 30-60 seconds (free tier spins down when idle)
- Subsequent loads are faster
- Free tier includes HTTPS automatically
- Auto-deploys when you push to GitHub

---

## Option 2: Railway.app (Also Easy)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repo
5. Railway auto-detects Python and deploys

**Live at:** `https://YOUR-APP.up.railway.app`

---

## Option 3: PythonAnywhere (Manual but Reliable)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com) (free tier)
2. Upload your files via their web interface
3. Set up a web app pointing to `f1_dashboard.py`
4. Install requirements in their console

**Live at:** `https://YOUR_USERNAME.pythonanywhere.com`

---

## Files Created for Deployment

I've created these files to make deployment work:

1. **`requirements.txt`** - Lists all Python dependencies
2. **`render.yaml`** - Configuration for Render.com
3. **`f1_dashboard.py`** - Updated with `server = app.server` for WSGI

---

## Troubleshooting

### "Module not found" error
Make sure `requirements.txt` includes all dependencies:
```
dash==2.14.2
plotly==5.18.0
fastf1==3.3.9
pandas==2.1.4
gunicorn==21.2.0
```

### "Application timeout"
Free tiers may timeout on first load (FastF1 downloads data). Just wait 60s and refresh.

### Data not loading
Some 2025 races may not have data until they complete. Try 2024 Abu Dhabi GP for testing.

---

## Cost Comparison

| Platform | Free Tier | Build Time | Ease |
|----------|-----------|------------|------|
| **Render.com** | ✅ Yes (750hrs/mo) | 2-3 min | ⭐⭐⭐⭐⭐ |
| **Railway.app** | ✅ $5 credit/mo | 1-2 min | ⭐⭐⭐⭐⭐ |
| **PythonAnywhere** | ✅ Yes (limited) | 5-10 min | ⭐⭐⭐ |
| **Fly.io** | ✅ Yes (generous) | 2-3 min | ⭐⭐⭐ |
| **Heroku** | ❌ No (paid only) | 3-5 min | ⭐⭐⭐⭐ |

**My recommendation: Start with Render.com**

---

## Next Steps

1. Push your code to GitHub
2. Sign up for Render.com
3. Deploy (literally 2 clicks)
4. Share your live URL!

Your dashboard will be accessible from anywhere in the world at:
`https://YOUR-APP-NAME.onrender.com`

Enjoy! 🏁
