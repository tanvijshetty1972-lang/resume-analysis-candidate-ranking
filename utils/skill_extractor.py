from utils.skills import SKILL_SET

def extract_skills(text: str):
    """
    Extract skills from resume text based on predefined SKILL_SET
    """
    text = text.lower()
    found_skills = []

    for skill in SKILL_SET:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))
