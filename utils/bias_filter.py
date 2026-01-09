import re

def remove_bias_terms(text):
    patterns = [
        r"\b(male|female|gender)\b",
        r"\b(age|years old)\b",
        r"\b(married|single)\b",
        r"\b(religion|caste)\b"
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text
