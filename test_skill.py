from skill_extractor import extract_skills

resume = """

I know Python.

I know SQL.

I use Git.

I built Machine Learning projects.

"""

skills = extract_skills(resume)

print(skills)