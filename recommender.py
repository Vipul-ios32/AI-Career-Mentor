import joblib
import pandas as pd
model = joblib.load("model/career_model.pkl")
FEATURES = [
    "Python","Java","C++","SQL","Machine_Learning","Deep_Learning",
    "NLP","Computer_Vision","AWS","Azure","Docker","Kubernetes",
    "Git","Linux","Flask","Django","Pandas","NumPy",
    "Scikit_Learn","TensorFlow","PyTorch","PowerBI",
    "Tableau","Excel","MongoDB","MySQL",
    "Internship_Months","Projects","Research_Papers",
    "Open_Source","GitHub_Score","LeetCode_Rating",
    "CGPA","AWS_Cert","Google_Cert",
    "Microsoft_Cert","IBM_Cert","Cisco_Cert",
    "Communication","Leadership","Teamwork",
    "Problem_Solving"
]
def recommend_career(user_data):
    """
    user_data should be a dictionary.
    Example:
    {
        "Python":1,
        "SQL":1,
        "AWS":0,
        ...
    }
    """

    input_data = []

    for feature in FEATURES:
        input_data.append(user_data.get(feature, 0))

    df = pd.DataFrame([input_data], columns=FEATURES)

    prediction = model.predict(df)

    return prediction[0]

