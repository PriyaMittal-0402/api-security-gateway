import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("Loading dataset...")
df = pd.read_csv("dataset/api_urls.csv")

X = df.drop("label", axis=1)
y = df["label"]

print("Training ML model...")
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X, y)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/api_model.pkl")

print("Model trained and saved successfully.")
