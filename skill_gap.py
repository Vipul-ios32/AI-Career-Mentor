career_skills = {

    "AI Engineer":[
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "git",
        "github",
        "aws"
    ],

    "Data Scientist":[
        "python",
        "sql",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "matplotlib",
        "scikit-learn"
    ],

    "Cloud Engineer":[
        "aws",
        "azure",
        "docker",
        "kubernetes",
        "linux",
        "git"
    ],

    "Python Developer":[
        "python",
        "sql",
        "git",
        "flask",
        "django"
    ]

}
def analyze_gap(user_skills, career):

    required = career_skills.get(career, [])

    missing = []

    for skill in required:

        if skill not in user_skills:

            missing.append(skill)

    return required, missing