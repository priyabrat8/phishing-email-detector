import pandas as pd
import re
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from scipy.sparse import hstack


# -------------------------
# NORMALIZE TEXT
# -------------------------

def normalize_text(text):
    replacements = {
        "0": "o", "1": "i", "3": "e",
        "5": "s", "$": "s", "@": "a"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


# -------------------------
# CLEAN TEXT + FEATURES
# -------------------------

def clean_text(text):
    text = str(text).lower()
    text = normalize_text(text)

    # Count BEFORE replacing
    url_count = len(re.findall(r"http\S+", text))
    email_count = len(re.findall(r"\S+@\S+", text))

    # Replace with tokens
    text = re.sub(r"http\S+", " URL_TOKEN ", text)
    text = re.sub(r"\S+@\S+", " EMAIL_TOKEN ", text)

    # Keep ! and ?
    text = re.sub(r"[^a-zA-Z0-9!? ]", " ", text)

    # Normalize repeated chars
    text = re.sub(r"(.)\1+", r"\1", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text, url_count, email_count


# -------------------------
# LOAD ENRON
# -------------------------

print("Loading datasets...")

enron = pd.read_csv("enron_spam_data.csv")

enron = enron[["Message", "Spam/Ham"]]

enron["Spam/Ham"] = enron["Spam/Ham"].map({
    "ham": 0,
    "spam": 1
})

enron.columns = ["text", "label"]


# -------------------------
# LOAD CEAS (ROBUST HANDLING)
# -------------------------

ceas = pd.read_csv("CEAS_08.csv")

print("CEAS columns:", ceas.columns)

# Try to detect correct text column
text_col = None
for col in ceas.columns:
    if col.lower() in ["body", "text", "email", "content"]:
        text_col = col
        break

if text_col is None:
    text_col = ceas.columns[0]  # fallback

label_col = None
for col in ceas.columns:
    if "label" in col.lower():
        label_col = col
        break

if label_col is None:
    label_col = ceas.columns[1]  # fallback

ceas = ceas[[text_col, label_col]]
ceas.columns = ["text", "label"]

# Ensure numeric labels
ceas["label"] = pd.to_numeric(ceas["label"], errors="coerce")

ceas = ceas.dropna(subset=["label"])


# -------------------------
# MERGE DATA
# -------------------------

data = pd.concat([enron, ceas], ignore_index=True)

data = data.dropna(subset=["text"])
data = data.drop_duplicates(subset="text")

print("Total samples:", len(data))


# -------------------------
# CLEAN + FEATURE EXTRACTION
# -------------------------

cleaned = data["text"].apply(clean_text)

data["clean_text"] = cleaned.apply(lambda x: x[0])
data["url_count"] = cleaned.apply(lambda x: x[1])
data["email_count"] = cleaned.apply(lambda x: x[2])

texts = data["clean_text"]
labels = data["label"]


# -------------------------
# TF-IDF
# -------------------------

print("Vectorizing...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),
    min_df=5,
    max_df=0.9
)

X_text = vectorizer.fit_transform(texts)

meta = data[["url_count", "email_count"]]

X = hstack([X_text, meta])


# -------------------------
# TRAIN / TEST SPLIT
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42
)


# -------------------------
# TRAIN MODEL
# -------------------------

print("Training model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# -------------------------
# EVALUATION
# -------------------------

probs = model.predict_proba(X_test)[:, 1]

threshold = 0.6
preds = (probs > threshold).astype(int)

print("\nAccuracy:", accuracy_score(y_test, preds))
print("\nClassification Report:\n")
print(classification_report(y_test, preds))


# -------------------------
# SAVE MODEL
# -------------------------

joblib.dump(model, "email_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nTraining completed successfully!")