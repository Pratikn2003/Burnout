# Burnout Prediction Web Application

A Flask-based web application that predicts burnout levels using machine learning. Users can register, log in, input daily work metrics, and get burnout predictions along with historical data visualization.

## Features

- 🔐 User authentication (registration and login)
- 📊 Burnout prediction using Random Forest model
- 📈 Dashboard with historical data visualization
- 💾 SQLite database for user data and daily logs
- 🎯 Personalized burnout level tracking

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Pratikn2003/Burnout.git
cd Burnout
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Deployment Options

### Option 1: Deploy to Render (Recommended)

1. Create a free account at [Render.com](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: burnout-app (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add environment variable (optional):
   - **Key**: `SECRET_KEY`
   - **Value**: Your random secret key
6. Click "Create Web Service"

Your app will be live at: `https://your-app-name.onrender.com`

### Option 2: Deploy to Railway

1. Create account at [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and deploy
5. Add environment variables in Settings if needed:
   - `SECRET_KEY`: Your random secret key

### Option 3: Deploy to Heroku

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Deploy:
```bash
git push heroku main
```

5. Open your app:
```bash
heroku open
```

### Option 4: Deploy to PythonAnywhere

1. Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload your files via Files tab
3. Create a new web app with Flask
4. Configure WSGI file to point to your app
5. Reload the web app

## Environment Variables

- `SECRET_KEY`: Flask secret key for session management (optional, has default)
- `FLASK_DEBUG`: Set to "true" for debug mode, "false" for production (default: false)
- `PORT`: Port number for the application (default: 5000)

## Project Structure

```
Burnout/
├── app.py                          # Main Flask application
├── train_rf_model.py              # ML model training script
├── burnout_rf_model.joblib        # Trained ML model
├── work_from_home_burnout_dataset.csv  # Training dataset
├── templates/                      # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
├── static/                         # CSS and images
│   └── style.css
├── requirements.txt                # Python dependencies
├── Procfile                        # Deployment configuration
└── README.md                       # This file
```

## Security Note

⚠️ **Important**: For production deployment, always set a strong `SECRET_KEY` environment variable. The default key is for development only.

Generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **ML**: scikit-learn, Random Forest Classifier
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn WSGI server

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please open an issue on GitHub.