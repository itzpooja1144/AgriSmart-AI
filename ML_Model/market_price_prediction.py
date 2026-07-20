import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("datasets/market_price.csv")

# Label Encoders
crop_encoder = LabelEncoder()
market_encoder = LabelEncoder()
region_encoder = LabelEncoder()

df["crop_name"] = crop_encoder.fit_transform(df["crop_name"])
df["market_name"] = market_encoder.fit_transform(df["market_name"])
df["region"] = region_encoder.fit_transform(df["region"])

# Features
X = df[["crop_name", "market_name", "region"]]

# Target
y = df["price_per_kg"]

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
pickle.dump(model, open("ML_Model/market_price_model.pkl", "wb"))

# Save encoders
pickle.dump(crop_encoder, open("ML_Model/crop_encoder.pkl", "wb"))
pickle.dump(market_encoder, open("ML_Model/market_encoder.pkl", "wb"))
pickle.dump(region_encoder, open("ML_Model/region_encoder.pkl", "wb"))

print("Market Price Model Saved Successfully!")