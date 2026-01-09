PROJECT_KEYWORDS = ["project", "internship", "developed", "implemented", "designed", "created", "built", "worked on"]

def extract_projects(text):
    lines = text.split("\n")
    projects = []
    current_proj = ""
    for line in lines:
        if any(k.lower() in line.lower() for k in PROJECT_KEYWORDS):
            current_proj += line.strip() + " "
        elif current_proj:
            projects.append(current_proj.strip())
            current_proj = ""
    if current_proj:
        projects.append(current_proj.strip())
    return projects
