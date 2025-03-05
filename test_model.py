import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the trained model
model = tf.keras.models.load_model("tumor_classifier.h5")
print("Model loaded successfully!")

# Define test directories
test_malignant_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/malignant"
test_benign_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/benign"

IMG_SIZE = (224, 224)

# Function to predict multiple images and calculate metrics
def predict_images_in_folder(folder_path, model, true_label):
    predictions = []
    true_labels = []
    
    print(f"\nTesting images in: {folder_path}")
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    if not image_files:
        print("⚠ No images found in this folder!")
        return predictions, true_labels

    for img_name in image_files:
        img_path = os.path.join(folder_path, img_name)

        # Load and preprocess the image
        img = image.load_img(img_path, target_size=IMG_SIZE)
        img_array = image.img_to_array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_label = 1 if prediction[0][0] > 0.5 else 0  # 1 = Malignant, 0 = Benign

        predictions.append(predicted_label)
        true_labels.append(true_label)

        # Print result
        label_str = "Malignant Tumor" if predicted_label == 1 else "Benign Tumor"
        print(f"{img_name}: Predicted -> {label_str}")

    return predictions, true_labels

# Store all predictions and true labels
all_predictions = []
all_true_labels = []

# Test malignant images (True label = 1)
preds_malignant, labels_malignant = predict_images_in_folder(test_malignant_folder, model, true_label=1)
all_predictions.extend(preds_malignant)
all_true_labels.extend(labels_malignant)

# Test benign images (True label = 0)
preds_benign, labels_benign = predict_images_in_folder(test_benign_folder, model, true_label=0)
all_predictions.extend(preds_benign)
all_true_labels.extend(labels_benign)

# Convert to numpy arrays
all_predictions = np.array(all_predictions)
all_true_labels = np.array(all_true_labels)

# Calculate Metrics
accuracy = accuracy_score(all_true_labels, all_predictions)
precision = precision_score(all_true_labels, all_predictions)
recall = recall_score(all_true_labels, all_predictions)
f1 = f1_score(all_true_labels, all_predictions)

# Print Final Evaluation Metrics
print("\n Model Evaluation Results:")
print(f"Accuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1 Score:  {f1 * 100:.2f}%")