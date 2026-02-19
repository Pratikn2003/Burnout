# Quick Deployment Guide

This guide provides step-by-step instructions for deploying your Burnout prediction website to various hosting platforms.

## Prerequisites

✅ All deployment files are already included:
- `requirements.txt` - Python dependencies
- `Procfile` - Deployment commands
- `render.yaml` - Render configuration
- `runtime.txt` - Python version
- `.env.example` - Environment variables template

## 🚀 Fastest Option: Render (Free Tier Available)

**Time: ~5 minutes**

1. **Sign up** at [Render.com](https://render.com)

2. Click **"New +"** → **"Web Service"**

3. **Connect your GitHub repository:**
   - Authorize Render to access your GitHub
   - Select repository: `Pratikn2003/Burnout`

4. **Configure the service:**
   - **Name**: `burnout-app` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your preferred branch)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

5. **Add Environment Variable (Recommended):**
   - Click "Advanced"
   - Add: `SECRET_KEY` = `<generate a random secure key>`
   - To generate: Run `python3 -c "import secrets; print(secrets.token_hex(32))"`

6. **Click "Create Web Service"**

7. **Your app will be live at:** `https://burnout-app.onrender.com`
   (or whatever name you chose)

⚠️ **Note**: Free tier may sleep after inactivity. First request might take 30-60 seconds.

---

## 🚂 Alternative: Railway (Simple & Fast)

**Time: ~3 minutes**

1. **Sign up** at [Railway.app](https://railway.app)

2. Click **"New Project"** → **"Deploy from GitHub repo"**

3. **Select repository**: `Pratikn2003/Burnout`

4. **Railway auto-detects Python** and deploys automatically!

5. **(Optional) Add environment variables:**
   - Go to Variables tab
   - Add `SECRET_KEY` with a secure random value

6. **Get your URL:**
   - Go to Settings
   - Click "Generate Domain"
   - Your app is live!

---

## 🔮 Alternative: Heroku (Industry Standard)

**Time: ~10 minutes**

### Via Heroku CLI:

1. **Install Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Navigate to your project:**
   ```bash
   cd /path/to/Burnout
   ```

4. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

5. **Set environment variable:**
   ```bash
   heroku config:set SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
   ```

6. **Deploy:**
   ```bash
   git push heroku main
   ```

7. **Open your app:**
   ```bash
   heroku open
   ```

### Via Heroku Dashboard:

1. Go to [dashboard.heroku.com](https://dashboard.heroku.com)
2. Click "New" → "Create new app"
3. Connect to GitHub and select your repository
4. Enable automatic deploys from main branch
5. Click "Deploy Branch"

---

## 🐍 Alternative: PythonAnywhere

**Time: ~10 minutes**

1. **Sign up** at [PythonAnywhere.com](https://www.pythonanywhere.com) (Free tier available)

2. **Upload files:**
   - Go to "Files" tab
   - Create directory: `/home/yourusername/burnout`
   - Upload all project files

3. **Install dependencies:**
   - Go to "Consoles" tab
   - Start a Bash console
   - Run:
     ```bash
     cd ~/burnout
     pip3 install --user -r requirements.txt
     ```

4. **Create web app:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10 or 3.11

5. **Configure WSGI file:**
   - Click on WSGI configuration file
   - Replace content with:
     ```python
     import sys
     path = '/home/yourusername/burnout'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```

6. **Set environment variables:**
   - In Web tab, scroll to "Environment variables"
   - Add `SECRET_KEY` with a secure value

7. **Reload web app:**
   - Click green "Reload" button

8. **Your app is live at:** `https://yourusername.pythonanywhere.com`

---

## 🔒 Security Checklist

Before deploying, ensure:

- [ ] Generate a strong `SECRET_KEY`:
  ```python
  python3 -c "import secrets; print(secrets.token_hex(32))"
  ```
- [ ] Set `SECRET_KEY` as environment variable (never commit it!)
- [ ] `FLASK_DEBUG` is set to `false` (default in production)
- [ ] Database file (`users.db`) is in `.gitignore`
- [ ] Review and understand all deployed code

---

## 🧪 Testing Your Deployment

After deployment:

1. Visit your app URL
2. Test registration: Create a new account
3. Test login: Log in with your credentials
4. Test prediction: Input work metrics and get burnout prediction
5. Check dashboard: Verify data visualization works
6. Test history: Ensure historical data is stored and displayed

---

## 📊 Monitoring

### Render:
- View logs in Render dashboard
- Monitor uptime and performance

### Railway:
- Check Deployments tab for logs
- View metrics in Observability tab

### Heroku:
```bash
heroku logs --tail
```

### PythonAnywhere:
- View error logs in Web tab
- Check server logs for issues

---

## 🆘 Troubleshooting

### App won't start:
- Check logs for errors
- Verify all dependencies are installed
- Ensure Python version matches `runtime.txt`

### Database errors:
- SQLite database is created automatically on first run
- Check file permissions if using PythonAnywhere

### ML Model errors:
- Ensure `burnout_rf_model.joblib` is uploaded
- Check scikit-learn version matches model training version

### 500 Internal Server Error:
- Check server logs
- Verify environment variables are set
- Test locally first: `gunicorn app:app`

---

## 🎉 Success!

Your website is now publicly accessible! Share your URL:
- **Render**: `https://your-app.onrender.com`
- **Railway**: `https://your-app.up.railway.app`
- **Heroku**: `https://your-app.herokuapp.com`
- **PythonAnywhere**: `https://yourusername.pythonanywhere.com`

---

## 📚 Additional Resources

- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/latest/deploying/)
- [Render Python Quickstart](https://render.com/docs/deploy-flask)
- [Railway Python Guide](https://docs.railway.app/guides/python)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)

---

**Need help?** Open an issue on GitHub: [Pratikn2003/Burnout/issues](https://github.com/Pratikn2003/Burnout/issues)
