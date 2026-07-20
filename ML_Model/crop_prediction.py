import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load dataset

data = pd.read_csv("datasets/crop_data.csv")
# Input and output
X = data[["N", "P", "K", "temperature", "humidity", "rainfall"]]
y = data["crop"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
pickle.dump(model, open("crop_model.pkl", "wb"))

print("Crop model trained successfully!")