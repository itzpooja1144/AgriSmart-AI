import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

data = pd.read_csv("datasets/crop_data.csv")

X = data[["N", "P", "K", "temperature", "humidity", "rainfall"]]
y = data["crop"]

model = DecisionTreeClassifier(random_state=42)

model.fit(X, y)

os.makedirs("ML_Model", exist_ok=True)

pickle.dump(
    model,
    open("ML_Model/crop_model.pkl", "wb")
)

print("Crop model trained successfully!")