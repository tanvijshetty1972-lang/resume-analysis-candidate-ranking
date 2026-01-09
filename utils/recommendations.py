from utils.skills import SKILL_SET

def generate_recommendations(extracted_skills):
    """
    Generate recommendations for missing skills
    """
    extracted_skills = set([s.lower() for s in extracted_skills])
    all_skills = set([s.lower() for s in SKILL_SET])

    missing_skills = all_skills - extracted_skills

    recommendations = []

    for skill in sorted(missing_skills):
        recommendations.append(
            f"Consider adding a project or certification related to {skill.title()}."
        )

    return recommendations
