# Burnout Predictor — Deployment Guide (Render.com)

Deploy the Burnout Predictor Flask application to **Render.com** (free tier, no credit card required).

---

## Prerequisites

- A [GitHub](https://github.com) account with this repository pushed/forked
- A free [Render.com](https://render.com) account

---

## Step-by-Step Deployment

### 1. Push the repository to GitHub

Ensure all files (including `render.yaml`, `requirements.txt`) are committed and pushed:

```bash
git add .
git commit -m "Add Render.com deployment config"
git push origin main
```

### 2. Sign up / Log in to Render.com

Go to [https://render.com](https://render.com) and create a free account (sign in with GitHub for convenience).

### 3. Create a New Web Service

1. Click **"New +"** in the top navigation bar
2. Select **"Web Service"**
3. Connect your GitHub account if prompted
4. Find and select **this repository** (`Burnout`)
5. Click **"Connect"**

### 4. Configure the Service

Fill in the following settings (most are auto-detected from `render.yaml`):

| Setting | Value |
|---------|-------|
| **Name** | `burnout-predictor` (or any name you prefer) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | `Free` |

### 5. Add Environment Variable

In the **Environment** section, add:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Click **"Generate"** to auto-generate a secure key |

### 6. Deploy

Click **"Create Web Service"**. Render will:
1. Clone your repository
2. Install dependencies from `requirements.txt`
3. Start the app with Gunicorn

Your app will be live at:
```
https://burnout-predictor.onrender.com
```
(or whatever name you chose)

---

## What's Included

| Feature | Status |
|---------|--------|
| User registration & login | ✅ |
| Burnout prediction dashboard | ✅ |
| ML model (Random Forest) | ✅ |
| Historical data tracking | ✅ |
| SQLite database (auto-created) | ✅ |

---

## Notes

- **SQLite database**: Render's free tier uses an ephemeral filesystem. The `users.db` database is created fresh on each deployment. For persistent data, consider upgrading to a paid plan or switching to [Render PostgreSQL](https://render.com/docs/databases).
- **ML model**: The `burnout_rf_model.joblib` file is committed to the repository and will be available on Render automatically.
- **Cold starts**: Free tier services spin down after inactivity. The first request after a period of inactivity may take ~30 seconds.
- **SECRET_KEY**: A randomly generated secret key is set via environment variable. Never hardcode secrets in production.

---

## Local Development

To run the app locally:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).
