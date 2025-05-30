import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.multiclass import unique_labels
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

base_dir = r"D:\Project\Tumor"
val_dir = os.path.join(base_dir, "val")
model_path = os.path.join(base_dir,"ML_Model", "tumor_classifier.h5")

img_size = (224, 224)
batch_size = 1  

model = load_model(model_path)

val_datagen = ImageDataGenerator(rescale=1./255)

val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

y_true = val_generator.classes
y_pred_probs = model.predict(val_generator, verbose=1)
y_pred = np.argmax(y_pred_probs, axis=1)

class_names = list(val_generator.class_indices.keys())
present_labels = unique_labels(y_true, y_pred)
present_class_names = [class_names[i] for i in present_labels]

acc = (y_pred == y_true).mean()
print(f"\n Validation Accuracy: {acc:.2f}")

print("\n Classification Report:")
print(classification_report(y_true, y_pred, labels=present_labels, target_names=present_class_names))