import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

import joblib

# Load dataset
data = pd.read_csv("dataset/career_dataset.csv")

# Features
X = data.drop("Career", axis=1)

# Target
y = data["Career"]
print(data["Career"].value_counts())
print(data.shape)
# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Accuracy
from sklearn.metrics import accuracy_score

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Accuracy:", accuracy)

print("Accuracy:", accuracy)

# Save model
joblib.dump(model, "model/career_model.pkl")

print("Model Saved Successfully")