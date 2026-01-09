EXTRA_CURRICULAR_KEYWORDS = [
    "volunteer","leadership","captain","award","club","hackathon","competition",
    "community","medal","athletic","sports","relay","tournament","achievement"
]

def extract_extra_curricular(text):
    lines = text.split("\n")
    extras = []
    for line in lines:
        if any(k.lower() in line.lower() for k in EXTRA_CURRICULAR_KEYWORDS):
            extras.append(line.strip())
    return extras
