from mentor import career_mentor

career = "AI Engineer"

skills = [
    "Python",
    "SQL",
    "Machine Learning"
]

missing = [
    "AWS",
    "Deep Learning",
    "TensorFlow"
]

result = career_mentor(
    career,
    skills,
    missing
)

print(result)