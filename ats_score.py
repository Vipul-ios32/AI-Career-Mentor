def calculate_ats_score(text, skills):

    score = 0

    suggestions = []

    # -----------------------
    # Resume Length
    # -----------------------

    if len(text) > 1000:
        score += 15
    else:
        suggestions.append("Resume is too short.")

    # -----------------------
    # Contact Details
    # -----------------------

    if "@" in text:
        score += 10
    else:
        suggestions.append("Email not found.")

    if "linkedin" in text.lower():
        score += 10
    else:
        suggestions.append("LinkedIn profile missing.")

    # -----------------------
    # Sections
    # -----------------------

    sections = [
        "education",
        "skills",
        "project",
        "experience",
        "certification"
    ]

    found = 0

    for section in sections:

        if section in text.lower():
            found += 1

    score += found * 5

    # -----------------------
    # Skills
    # -----------------------

    score += min(len(skills) * 3, 30)

    if len(skills) < 6:
        suggestions.append("Add more technical skills.")

    # -----------------------
    # Final Score
    # -----------------------

    if score > 100:
        score = 100

    return score, suggestions