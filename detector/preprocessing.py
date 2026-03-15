import re

def normalize_text(text):

    replacements = {
        "0": "o",
        "1": "i",
        "3": "e",
        "5": "s",
        "$": "s",
        "@": "a"
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    return text


def preprocess_email(text):

    text = text.lower()

    text = normalize_text(text)

    # remove urls
    text = re.sub(r"http\S+", "", text)

    # remove email addresses
    text = re.sub(r"\S+@\S+", "", text)

    # normalize repeated characters
    text = re.sub(r"(.)\1+", r"\1", text)

    # remove punctuation
    text = re.sub(r"\W", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()