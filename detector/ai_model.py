import os

import joblib
from phishing_detector import settings
from .preprocessing import preprocess_email

model_path = os.path.join(settings.BASE_DIR, "detector",  "ml_model", "phishing_model.pkl")
vectorizer_path = os.path.join(settings.BASE_DIR,"detector", "ml_model", "vectorizer.pkl")
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)


def predict_email(text):
    text = preprocess_email(text)
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)[0]
    probability = model.predict_proba(vector)[0][1]
    return prediction, probability