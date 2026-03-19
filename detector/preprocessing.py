import re

def normalize_text(text):
    """Converts common l33t speak to standard characters."""
    replacements = {
        "0": "o", "1": "i", "3": "e",
        "5": "s", "$": "s", "@": "a"
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

def clean_and_extract(text):
    """
    Cleans the email text and extracts metadata BEFORE destroying the URLs/Emails.
    Returns: (cleaned_text_string, url_count, email_count)
    """
    # 1. Safety check for empty inputs
    if not isinstance(text, str) or not text.strip():
        return "", 0, 0

    text = text.lower()
    text = normalize_text(text)

    # 2. Extract Meta Data First
    url_count = len(re.findall(r"http[s]?://\S+", text))
    email_count = len(re.findall(r"\S+@\S+", text))

    # 3. Replace with standard AI tokens
    text = re.sub(r"http[s]?://\S+", " URL_TOKEN ", text)
    text = re.sub(r"\S+@\S+", " EMAIL_TOKEN ", text)

    # 4. Strip dangerous/useless punctuation, but keep !, ?, and spaces
    text = re.sub(r"[^a-z0-9!? ]", " ", text)

    # 5. Normalize repeated characters (e.g., "urgeeent" -> "urgent")
    text = re.sub(r"(.)\1+", r"\1", text)
    
    # 6. Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text, url_count, email_count