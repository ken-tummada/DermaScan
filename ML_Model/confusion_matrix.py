import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
from matplotlib.colors import LinearSegmentedColormap

teal_cmap = LinearSegmentedColormap.from_list("custom_teal", ["#ffffff", "#0D7377"])

# Paths
base_dir = r"D:\Project\Tumor"
val_dir = os.path.join(base_dir, "val")
model_path = os.path.join(base_dir, "tumor_classifier.h5")

# Load model
model = load_model(model_path)

# Load validation data
img_size = (224, 224)
val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=1,
    class_mode='categorical',
    shuffle=False
)

# Predict
y_true = val_generator.classes
y_pred_prob = model.predict(val_generator, verbose=1)
y_pred = np.argmax(y_pred_prob, axis=1)

# Class labels
class_names = list(val_generator.class_indices.keys())

# Confusion matrix
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(6, 5))
ax = sns.heatmap(
    cm, annot=True, fmt="d", cmap=teal_cmap, cbar=True,
    xticklabels=class_names, yticklabels=class_names,
    annot_kws={"fontsize": 10, "weight": "bold"},  # Big numbers
    square=True, linewidths=0,  # No internal lines
)

# Add outer box manually
for _, spine in ax.spines.items():
    spine.set_visible(True)
    spine.set_linewidth(1.5)  # Thickness of outer box

# Axis labels and title
plt.xlabel('Predicted', fontsize=8)
plt.ylabel('True', fontsize=8)
plt.xticks(fontsize=6, rotation=45, ha='right')
plt.yticks(fontsize=6, rotation=0)
plt.title('Confusion Matrix', fontsize=10, pad=10)

plt.tight_layout(pad=1.0)
plt.savefig(os.path.join(base_dir, "confusion_matrix.png"), dpi=300)
plt.show()
