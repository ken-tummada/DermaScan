import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# ---------------- STEP 1: LOAD DATA ----------------
train_dir = "D:/学习/UCSB/DS/Tumor Project/skin_images/train"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Data augmentation for multi-class classification
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2  
)

# Multi-class classification: Use 'categorical' mode
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',  # Multi-class classification
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',  # Multi-class classification
    subset='validation'
)

# Get number of tumor types (classes)
NUM_CLASSES = len(train_generator.class_indices)
print("Detected Tumor Classes:", train_generator.class_indices)

# ---------------- STEP 2: BUILD & TRAIN MODEL ----------------
# Load MobileNetV2 as the base model
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base layers for feature extraction

# Add classification layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
output = Dense(NUM_CLASSES, activation="softmax")(x)  # Multi-class classification

# Create the model
model = Model(inputs=base_model.input, outputs=output)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Train the model
history = model.fit(train_generator, validation_data=val_generator, epochs=10)

# ---------------- STEP 3: SAVE MODEL ----------------
model.save("tumor_classifier.h5")
print("Model successfully saved as 'tumor_classifier.h5'")

# Save class index mapping
class_mapping = train_generator.class_indices
with open("class_indices.json", "w") as f:
    import json
    json.dump(class_mapping, f)
print("Class index mapping saved as 'class_indices.json'")
