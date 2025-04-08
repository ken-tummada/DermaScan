import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.multiclass import unique_labels
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

# Paths
base_dir = r"D:\Project\Tumor"
val_dir = os.path.join(base_dir, "val")
model_path = os.path.join(base_dir, "tumor_classifier.h5")

# Parameters
img_size = (224, 224)
batch_size = 1  # For accurate prediction per image

# Load model
model = load_model(model_path)

# Prepare validation data
val_datagen = ImageDataGenerator(rescale=1./255)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

# Predict
y_true = val_generator.classes
y_pred_probs = model.predict(val_generator, verbose=1)
y_pred = np.argmax(y_pred_probs, axis=1)

# Class name mapping
class_names = list(val_generator.class_indices.keys())
present_labels = unique_labels(y_true, y_pred)
present_class_names = [class_names[i] for i in present_labels]

# Accuracy
acc = (y_pred == y_true).mean()
print(f"\n Validation Accuracy: {acc:.2f}")

# Classification report
print("\n Classification Report:")
print(classification_report(y_true, y_pred, labels=present_labels, target_names=present_class_names))

# Confusion matrix
print(" Confusion Matrix:")
cm = confusion_matrix(y_true, y_pred, labels=present_labels)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=present_class_names,
            yticklabels=present_class_names)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "confusion_matrix.png"))
plt.show()
