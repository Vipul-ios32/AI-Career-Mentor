from skill_gap import analyze_gap

skills = [
    "python",
    "git",
    "numpy"
]

required, missing = analyze_gap(
    skills,
    "AI Engineer"
)

print(required)

print(missing)