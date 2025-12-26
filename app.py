from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

model = joblib.load("model/api_model.pkl")

def extract_features(url):
    return [
        len(url),
        1 if url.startswith("https") else 0,
        url.count("?") + url.count("&"),
        1 if any(x in url.lower() for x in ["token", "key", "auth"]) else 0,
        1 if "v1" in url or "v2" in url else 0
    ]

@app.route("/", methods=["GET", "POST"])
def index():
    url = ""
    result = None
    explanation = []
    prevention = []

    if request.method == "POST":
        url = request.form.get("url", "")
        if url.strip():
            features = extract_features(url)
            prediction = model.predict([features])[0]

            if prediction == 1:
                result = "Potentially Unsafe API Endpoint"
                explanation = [
                    "API endpoint shows risky structural patterns",
                    "Possible exposure of authentication data",
                    "Lack of secure design indicators"
                ]
                prevention = [
                    "Use HTTPS with TLS",
                    "Avoid exposing tokens in URLs",
                    "Apply authentication headers",
                    "Implement rate limiting"
                ]
            else:
                result = "API Endpoint Appears Secure"
                explanation = [
                    "No major security red flags detected",
                    "Follows common secure API practices"
                ]
                prevention = [
                    "Continue monitoring API traffic",
                    "Apply logging and alerts",
                    "Rotate credentials periodically"
                ]

    return render_template(
        "index.html",
        url=url,
        result=result,
        explanation=explanation,
        prevention=prevention
    )

if __name__ == "__main__":
    app.run(debug=True)
