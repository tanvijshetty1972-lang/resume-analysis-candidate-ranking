import re
from dateutil import parser
from datetime import datetime

def extract_years_of_experience(text):
    """
    Detects all date ranges like 'Dec 2020 – Aug 2024' and sums total months
    """
    text = text.replace("\n", " ")
    # Match patterns like Dec 2020–Aug 2024, Feb.2024 – Apr.2024
    pattern = r"([A-Za-z]{3,}\.?\s?\d{4})\s?[-–]\s?([A-Za-z]{3,}\.?\s?\d{4}|Present)"
    matches = re.findall(pattern, text)
    total_months = 0

    for start_str, end_str in matches:
        try:
            start = parser.parse(start_str)
            end = datetime.now() if "Present" in end_str else parser.parse(end_str)
            months = (end.year - start.year) * 12 + (end.month - start.month)
            total_months += months
        except:
            continue
    years = round(total_months / 12, 1)
    return years

def extract_required_experience(text):
    """
    Detects phrases like 'X+ years' in JD
    """
    match = re.search(r"(\d+)\+?\s?years", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0
