import tensorflow as tf
from tensorflow.keras import layers, models
import pickle

# ===============================
# DATASET PATH
# ===============================

dataset_path = "../datasets/New folder/PlantVillage"

img_size = 128
batch_size = 32

# ===============================
# TRAIN DATA
# ===============================

train_data = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_size, img_size),
    batch_size=batch_size
)

# ===============================
# VALIDATION DATA
# ===============================

val_data = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_size, img_size),
    batch_size=batch_size
)

# ===============================
# CLASS NAMES
# ===============================

class_names = train_data.class_names

print("Classes:")
print(class_names)

train_data = train_data.prefetch(tf.data.AUTOTUNE)
val_data = val_data.prefetch(tf.data.AUTOTUNE)
# ===============================
# CNN MODEL
# ===============================

model = models.Sequential([

    layers.Input(shape=(img_size, img_size, 3)),

    layers.Rescaling(1./255),

    layers.Conv2D(32, (3,3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3,3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(128, activation="relu"),

    layers.Dropout(0.5),

    layers.Dense(len(class_names), activation="softmax")
])

# ===============================
# COMPILE MODEL
# ===============================

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ===============================
# TRAIN MODEL
# ===============================

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=20
)

# ===============================
# SAVE MODEL
# ===============================

model.save("disease_model.keras")

# ===============================
# SAVE CLASS NAMES
# ===============================

with open("disease_classes.pkl", "wb") as f:
    pickle.dump(class_names, f)

print("=================================")
print("Model Saved Successfully")
print("Classes:", class_names)
print("=================================")