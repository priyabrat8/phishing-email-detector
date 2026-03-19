import os
import joblib
from django.conf import settings
from scipy.sparse import hstack, csr_matrix
from .preprocessing import clean_and_extract


# Absolute paths to the model files
MODEL_PATH = os.path.join(settings.BASE_DIR, "detector", "ml_model", "email_model.pkl")
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, "detector", "ml_model", "vectorizer.pkl")

# Load models safely on startup
try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
except FileNotFoundError as e:
    model, vectorizer = None, None

def predict_email(text):
    """
    Takes raw email text, processes it securely, and returns (prediction_int, probability_float).
    """
    if model is None or vectorizer is None:
        return 0, 0.0 # Fail safe if models didn't load

    try:
        # 1. Run the unified preprocessing
        clean_text, url_count, email_count = clean_and_extract(text)
        
        # 2. Vectorize the text
        vector = vectorizer.transform([clean_text])
        
        # 3. Format metadata securely
        meta_matrix = csr_matrix([[url_count, email_count]])
        
        # 4. Stack and convert to expected CSR format
        final_vector = hstack([vector, meta_matrix]).tocsr()
        
        # 5. Get Probability
        probability = model.predict_proba(final_vector)[0][1]
        
        # 6. Enforce strict 60% Threshold (Matches training evaluation)
        prediction = 1 if probability >= 0.60 else 0
        
        return prediction, probability

    except Exception as e:
        # If the ML pipeline crashes, fail open (safe) rather than crashing the website
        return 0, 0.0