import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model

base_dir = r"D:\Project\Tumor"
val_dir = os.path.join(base_dir, "val") 
model_path = os.path.join(base_dir, "tumor_classifier.h5")

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

class_names = list(val_generator.class_indices.keys())

y_true = val_generator.classes
y_prob = model.predict(val_generator, verbose=1)
y_true_onehot = label_binarize(y_true, classes=list(range(len(class_names))))

plt.figure(figsize=(10, 8))

for i in range(len(class_names)):
    fpr, tpr, _ = roc_curve(y_true_onehot[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{class_names[i]} (AUC = {roc_auc:.2f})")

plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('ROC Curve – Multi-Class')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "roc_curve.png"))
plt.show()