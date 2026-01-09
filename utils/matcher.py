# utils/matcher.py
from utils.skills import SKILL_SET

def match_resume_to_job(resume_skills, job_text):
    resume_skills = set([s.lower() for s in resume_skills])
    job_skills = set()

    for skill in SKILL_SET:
        if skill.lower() in job_text:
            job_skills.add(skill.lower())

    if not job_skills:
        return 0, [], []

    matched = resume_skills & job_skills
    missing = job_skills - resume_skills

    match_score = round((len(matched) / len(job_skills)) * 100, 2)

    return match_score, sorted(matched), sorted(missing)
