import pandas as pd
import re
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


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
# CLEAN TEXT
# -------------------------

def clean_text(text):
    text = str(text).lower()
    text = normalize_text(text)

    text = re.sub(r"http\S+", " URL_TOKEN ", text)
    text = re.sub(r"\S+@\S+", " EMAIL_TOKEN ", text)

    text = re.sub(r"[^a-zA-Z0-9!? ]", " ", text)
    text = re.sub(r"(.)\1+", r"\1", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


# -------------------------
# LOAD DATA
# -------------------------

print("Loading datasets...")

# ENRON
enron = pd.read_csv("enron_spam_data.csv")
enron = enron[["Message", "Spam/Ham"]]
enron["Spam/Ham"] = enron["Spam/Ham"].map({"ham": 0, "spam": 1})
enron.columns = ["text", "label"]

# CEAS
ceas = pd.read_csv("CEAS_08.csv")

# Auto-detect columns
text_col = ceas.columns[0]
label_col = ceas.columns[1]

ceas = ceas[[text_col, label_col]]
ceas.columns = ["text", "label"]

ceas["label"] = pd.to_numeric(ceas["label"], errors="coerce")
ceas = ceas.dropna(subset=["label"])


# -------------------------
# MERGE
# -------------------------

data = pd.concat([enron, ceas], ignore_index=True)

data = data.dropna(subset=["text"])
data = data.drop_duplicates(subset="text")

print("Total samples:", len(data))


# -------------------------
# CLEAN
# -------------------------

data["text"] = data["text"].apply(clean_text)

texts = data["text"]
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

X = vectorizer.fit_transform(texts)


# -------------------------
# SPLIT
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=42
)


# -------------------------
# TRAIN
# -------------------------

print("Training model...")

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train, y_train)


# -------------------------
# EVALUATE
# -------------------------

probs = model.predict_proba(X_test)[:, 1]

threshold = 0.6
preds = (probs > threshold).astype(int)

print("\nAccuracy:", accuracy_score(y_test, preds))
print("\nClassification Report:\n")
print(classification_report(y_test, preds))


# -------------------------
# SAVE
# -------------------------

joblib.dump(model, "email_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\nTraining completed successfully!")