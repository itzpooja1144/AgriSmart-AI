import tensorflow as tf

print("Loading model...")

model = tf.keras.models.load_model("../ML_Model/disease_model.keras")

print("Loaded Successfully!")