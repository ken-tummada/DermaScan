import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.family'] = 'DIN Alternate'

teal_cmap = LinearSegmentedColormap.from_list("custom_teal", ["#F4F8F8", "#0D7377"])

base_dir = r"D:\Project\Tumor"
val_dir = os.path.join(base_dir, "val")
model_path = os.path.join(base_dir, "ML_Model", "tumor_classifier.h5")

model = load_model(model_path)

img_size = (224, 224)
val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=1,
    class_mode='categorical',
    shuffle=False
)

y_true = val_generator.classes
y_pred_prob = model.predict(val_generator, verbose=1)
y_pred = np.argmax(y_pred_prob, axis=1)

class_names = list(val_generator.class_indices.keys())

cm = confusion_matrix(y_true, y_pred)

cm_prob = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

plt.figure(figsize=(6, 5))
ax = sns.heatmap(
    cm_prob, annot=True, fmt=".2f", cmap=teal_cmap, cbar=True,
    xticklabels=class_names, yticklabels=class_names,
    annot_kws={"fontsize": 14},
    square=True, linewidths=0,
)

cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12)

for _, spine in ax.spines.items():
    spine.set_visible(True)
    spine.set_linewidth(1.5)

plt.xlabel('Predicted', fontsize=12)
plt.ylabel('True', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.title('Confusion Matrix', fontsize=14, pad=10)

plt.tight_layout(pad=1.0)
plt.savefig(os.path.join(base_dir, "confusion_matrix_prob.png"), dpi=300)
plt.show()