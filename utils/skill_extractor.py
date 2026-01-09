import re
from utils.skills import SKILL_SET

def extract_skills(text):
    text = text.lower()
    skills_found = []
    for skill in SKILL_SET:
        if re.search(rf"\b{re.escape(skill)}\b", text):
            skills_found.append(skill)
    return sorted(list(set(skills_found)))
