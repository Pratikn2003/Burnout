# Burnout Predictor - Random Forest Training (CORRECT VERSION)

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("work_from_home_burnout_dataset.csv")

# Feature columns (FROM YOUR CSV)
features = [
    "work_hours",
    "screen_time_hours",
    "meetings_count",
    "breaks_taken",
    "after_hours_work",
    "sleep_hours",
    "task_completion_rate"
]

X = data[features]
y = data["burnout_risk"]  # Low / Medium / High

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
accuracy = accuracy_score(y_test, preds)

print("Model Accuracy:", round(accuracy * 100, 2), "%")

# Save model
joblib.dump(model, "burnout_rf_model.joblib")
print("✅ Model saved as burnout_rf_model.joblib")
