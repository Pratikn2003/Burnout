from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3, hashlib, random, re, os
from datetime import date
import joblib
from joke_generator import fetch_joke

app = Flask(__name__, template_folder=".")
app.secret_key = os.environ.get("SECRET_KEY", "burnout_secret_key")

# ---------------- LOAD ML MODEL ----------------
try:
    model = joblib.load("burnout_rf_model.joblib")
except Exception as e:
    model = None
    print("❌ Model load failed:", e)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row

    # Users table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dob TEXT,
        mobile TEXT,
        profession TEXT,
        user_id TEXT UNIQUE,
        password TEXT
    )
    """)

    # Daily data table (MATCHES ML + DASHBOARD)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS daily_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        log_date TEXT,
        work_hours REAL,
        screen_time REAL,
        meetings INTEGER,
        breaks INTEGER,
        after_hours INTEGER,
        sleep REAL,
        task_rate REAL,
        burnout_level TEXT
    )
    """)

    return conn

# ---------------- PASSWORD HASH ----------------
def hash_pwd(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        dob = request.form["dob"]
        mobile = request.form["mobile"]
        profession = request.form["profession"]

        if not re.fullmatch(r"[A-Za-z ]+", name):
            return "❌ Name must contain only letters"

        if not mobile.isdigit() or len(mobile) != 10:
            return "❌ Mobile number must be 10 digits"

        first = name.split()[0].lower()

        conn = get_db()
        cur = conn.cursor()

        while True:
            user_id = f"{first}_{random.randint(1000,9999)}"
            cur.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
            if not cur.fetchone():
                break

        conn.close()

        session["reg_data"] = {
            "name": name.title(),
            "dob": dob,
            "mobile": mobile,
            "profession": profession,
            "user_id": user_id
        }

        return redirect(url_for("details"))

    return render_template("register.html")

# ---------------- DETAILS ----------------
@app.route("/details")
def details():
    if "reg_data" not in session:
        return redirect(url_for("register"))
    return render_template("details.html", **session["reg_data"])

# ---------------- SET PASSWORD ----------------
@app.route("/set-password", methods=["GET", "POST"])
def set_password():
    if "reg_data" not in session:
        return redirect(url_for("register"))

    if request.method == "POST":
        pwd = request.form["password"]
        confirm = request.form["confirm_password"]

        if pwd != confirm:
            return "❌ Passwords do not match"

        data = session["reg_data"]
        conn = get_db()
        conn.execute("""
            INSERT INTO users(name, dob, mobile, profession, user_id, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["dob"],
            data["mobile"],
            data["profession"],
            data["user_id"],
            hash_pwd(pwd)
        ))
        conn.commit()
        conn.close()

        session.pop("reg_data")
        return redirect(url_for("login"))

    return render_template("set_password.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uid = request.form["user_id"]
        pwd = hash_pwd(request.form["password"])

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id=? AND password=?", (uid, pwd))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = uid
            return redirect(url_for("menu"))
        else:
            return render_template("invalid.html")

    return render_template("login.html")

# ---------------- MENU ----------------
@app.route("/menu")
def menu():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("menu.html")

# ---------------- SUGGESTION ----------------
@app.route("/suggestion")
def suggestion():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("suggestion.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ---------------- SUGGESTIONS ----------------
def get_suggestions(level):
    if level == "High":
        return [
            {"icon": "🛑", "text": "Take immediate time off or a mental health day to recover."},
            {"icon": "⏰", "text": "Reduce your daily work hours and set strict boundaries between work and rest."},
            {"icon": "🧠", "text": "Seek support from a mental health professional or counsellor."},
            {"icon": "📵", "text": "Disconnect from work emails and notifications outside working hours."},
            {"icon": "🤝", "text": "Talk to your manager about redistributing your workload."},
            {"icon": "😴", "text": "Prioritise at least 7–8 hours of quality sleep each night."},
        ]
    elif level == "Medium":
        return [
            {"icon": "⚖️", "text": "Establish a healthier work-life balance by scheduling personal time daily."},
            {"icon": "☕", "text": "Take regular short breaks throughout the day (e.g., the Pomodoro technique)."},
            {"icon": "🏃", "text": "Incorporate light exercise or a short walk into your daily routine."},
            {"icon": "📝", "text": "Review your task list and delegate or defer non-urgent items."},
            {"icon": "🧘", "text": "Try mindfulness or relaxation techniques such as deep breathing or meditation."},
            {"icon": "👥", "text": "Stay connected with friends or colleagues for social support."},
        ]
    else:
        return [
            {"icon": "✅", "text": "Keep up your current healthy habits — you're doing great!"},
            {"icon": "🌱", "text": "Continue maintaining a consistent sleep schedule for long-term wellness."},
            {"icon": "📅", "text": "Plan regular activities you enjoy to sustain positive energy levels."},
            {"icon": "💧", "text": "Stay hydrated and maintain a balanced diet to support focus and mood."},
            {"icon": "📊", "text": "Monitor your stress levels periodically so you catch changes early."},
            {"icon": "🎯", "text": "Set realistic goals and celebrate small achievements to stay motivated."},
        ]

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if model is None:
        return "❌ ML model not loaded"

    try:
        features = [[
            float(request.form["work_hours"]),
            float(request.form["screen_time"]),
            int(request.form["meetings"]),
            int(request.form["breaks"]),
            int(request.form["after_hours"]),
            float(request.form["sleep"]),
            float(request.form["task_rate"])
        ]]
    except ValueError:
        return "❌ Invalid input"

    burnout_level = model.predict(features)[0]

    conn = get_db()
    conn.execute("""
        INSERT INTO daily_data
        (user_id, log_date, work_hours, screen_time, meetings, breaks,
         after_hours, sleep, task_rate, burnout_level)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        date.today().isoformat(),
        *features[0],
        burnout_level
    ))
    conn.commit()
    conn.close()

    suggestions = get_suggestions(burnout_level)
    return render_template("result.html", level=burnout_level, suggestions=suggestions)

# ---------------- HISTORY ----------------
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT log_date, work_hours, screen_time, meetings, breaks,
               after_hours, sleep, task_rate, burnout_level
        FROM daily_data
        WHERE user_id=?
        ORDER BY log_date DESC
        LIMIT 30
    """, (session["user_id"],))
    rows = cur.fetchall()
    conn.close()

    return render_template(
        "history.html",
        dates=[r[0] for r in rows][::-1],
        work_hours=[r[1] for r in rows][::-1],
        screen_time=[r[2] for r in rows][::-1],
        meetings=[r[3] for r in rows][::-1],
        breaks=[r[4] for r in rows][::-1],
        after_hours=[r[5] for r in rows][::-1],
        sleep_hours=[r[6] for r in rows][::-1],
        task_rate=[r[7] for r in rows][::-1],
        burnout_level=[r[8] for r in rows][::-1]
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- JOKE ----------------
@app.route("/joke")
def joke():
    result = fetch_joke()
    if "error" in result:
        return jsonify(result), 503
    return jsonify(result)

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
