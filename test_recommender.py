from recommender import recommend_career

candidate = {
    "Python":1,
    "SQL":1,
    "Machine_Learning":1,
    "Deep_Learning":1,
    "Git":1,
    "Pandas":1,
    "NumPy":1,
    "TensorFlow":1,
    "PyTorch":1,
    "AWS":1,
    "Internship_Months":6,
    "Projects":5,
    "Research_Papers":1,
    "GitHub_Score":90,
    "LeetCode_Rating":1800,
    "CGPA":8.9,
    "Communication":9,
    "Leadership":8,
    "Teamwork":9,
    "Problem_Solving":9
}

career = recommend_career(candidate)

print(career)