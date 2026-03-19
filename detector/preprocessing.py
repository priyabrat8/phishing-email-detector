import re

def normalize_text(text):
    replacements = {
        "0": "o", "1": "i", "3": "e",
        "5": "s", "$": "s", "@": "a"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def preprocess_email(text):
    text = str(text).lower()
    text = normalize_text(text)

    text = re.sub(r"http\S+", " URL_TOKEN ", text)
    text = re.sub(r"\S+@\S+", " EMAIL_TOKEN ", text)

    text = re.sub(r"[^a-zA-Z0-9!? ]", " ", text)
    text = re.sub(r"(.)\1+", r"\1", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text