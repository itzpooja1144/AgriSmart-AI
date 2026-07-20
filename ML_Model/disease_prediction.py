import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Load dataset
data = pd.read_csv("datasets/disease_data.csv")

# Combine symptoms and crop as input
X_text = data["crop_name"] + " " + data["symptoms"]
y = data["disease"]

# Convert text into numbers
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X_text)

# Train model
model = MultinomialNB()
model.fit(X, y)

# Save model and vectorizer
pickle.dump(model, open("ML_Model/disease_model.pkl", "wb"))
pickle.dump(vectorizer, open("ML_Model/disease_vectorizer.pkl", "wb"))

print("Disease model trained successfully!")
