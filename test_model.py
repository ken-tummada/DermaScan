import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the trained model
model = tf.keras.models.load_model("tumor_classifier.h5")
print("Model loaded successfully!")

# Define the new test directory structure
test_base_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/test"

IMG_SIZE = (224, 224)

# Get all tumor subfolders inside `test/benign` and `test/malignant`
tumor_classes = {}  # Dictionary to store class mappings
class_folders = []

for category in ["benign", "malignant"]:
    category_path = os.path.join(test_base_folder, category)
    
    if os.path.exists(category_path):  # Ensure the path exists
        for subfolder in sorted(os.listdir(category_path)):  # Ensure consistent class order
            tumor_classes[subfolder] = len(tumor_classes)  # Assign a numeric label
            class_folders.append((subfolder, os.path.join(category_path, subfolder)))

print("\n Tumor Class Mapping:", tumor_classes)

# Function to predict multiple images and calculate metrics
def predict_images_in_folder(folder_path, model, true_label):
    predictions = []
    true_labels = []
    
    print(f"\n Testing images in: {folder_path}")
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    if not image_files:
        print("No images found in this folder!")
        return predictions, true_labels

    for img_name in image_files:
        img_path = os.path.join(folder_path, img_name)

        # Load and preprocess the image
        img = image.load_img(img_path, target_size=IMG_SIZE)
        img_array = image.img_to_array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_array)[0]  # Get multi-class probability distribution
        predicted_label = np.argmax(prediction)  # Get the class with the highest probability

        predictions.append(predicted_label)
        true_labels.append(true_label)

        # Print result
        predicted_class_name = list(tumor_classes.keys())[predicted_label]
        print(f"{img_name}: Predicted -> {predicted_class_name} (Confidence: {max(prediction) * 100:.2f}%)")

    return predictions, true_labels

# Store all predictions and true labels
all_predictions = []
all_true_labels = []

# Loop through all tumor type subfolders in test dataset
for tumor_type, tumor_folder in class_folders:
    if os.path.isdir(tumor_folder):  # Ensure it's a valid directory
        preds, labels = predict_images_in_folder(tumor_folder, model, true_label=tumor_classes[tumor_type])
        all_predictions.extend(preds)
        all_true_labels.extend(labels)

# Convert to numpy arrays
if all_predictions and all_true_labels:  # Prevent division by zero
    all_predictions = np.array(all_predictions)
    all_true_labels = np.array(all_true_labels)

    # Calculate Multi-Class Metrics
    accuracy = accuracy_score(all_true_labels, all_predictions)
    precision = precision_score(all_true_labels, all_predictions, average="weighted")
    recall = recall_score(all_true_labels, all_predictions, average="weighted")
    f1 = f1_score(all_true_labels, all_predictions, average="weighted")

    # Print Final Evaluation Metrics
    print("\n Model Evaluation Results:")
    print(f"Accuracy:  {accuracy * 100:.2f}%")
    print(f"Precision: {precision * 100:.2f}%")
    print(f"Recall:    {recall * 100:.2f}%")
    print(f"F1 Score:  {f1 * 100:.2f}%")
else:
    print("No predictions were made. Please check your test dataset structure.")
