import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import (roc_auc_score, average_precision_score,
                             precision_score, recall_score, f1_score,
                             confusion_matrix, accuracy_score)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from sklearn.preprocessing import label_binarize

base_dir = r"D:\Project\Tumor"
val_dir = os.path.join(base_dir, "val")
model_path = os.path.join(base_dir, "ML_Model", "tumor_classifier.h5")

model = load_model(model_path)

img_size = (224, 224)
val_gen = ImageDataGenerator(rescale=1./255).flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=1,
    class_mode='categorical',
    shuffle=False
)

class_names = list(val_gen.class_indices.keys())

y_true = val_gen.classes
y_probs = model.predict(val_gen, verbose=1)
y_pred = np.argmax(y_probs, axis=1)
y_true_bin = label_binarize(y_true, classes=list(range(len(class_names))))

metrics = {
    "AUC": [],
    "Average Precision": [],
    "Accuracy": [],
    "Sensitivity": [],
    "Specificity": [],
    "Dice Coefficient": [],
    "PPV": [],
    "NPV": []
}

for i, class_name in enumerate(class_names):
    y_true_i = y_true_bin[:, i]
    y_pred_i = y_pred == i

    tn, fp, fn, tp = confusion_matrix(y_true_i, y_pred_i).ravel()

    metrics["AUC"].append(roc_auc_score(y_true_i, y_probs[:, i]))
    metrics["Average Precision"].append(average_precision_score(y_true_i, y_probs[:, i]))
    metrics["Accuracy"].append((tp + tn) / (tp + tn + fp + fn))
    metrics["Sensitivity"].append(tp / (tp + fn) if (tp + fn) else 0)
    metrics["Specificity"].append(tn / (tn + fp) if (tn + fp) else 0)
    metrics["Dice Coefficient"].append(f1_score(y_true_i, y_pred_i))
    metrics["PPV"].append(tp / (tp + fp) if (tp + fp) else 0)
    metrics["NPV"].append(tn / (tn + fn) if (tn + fn) else 0)

df = pd.DataFrame(metrics, index=class_names).astype(float)
df.loc["Mean Value"] = df.mean()
df = df.T 

plt.figure(figsize=(13, 5))
ax = sns.heatmap(df, annot=True, fmt=".3f", cmap="YlGnBu",
            annot_kws={"fontsize": 15}, 
            cbar=True, linewidths=0.5)

plt.yticks(fontsize=14)
plt.xticks(fontsize=12)

cbar = ax.collections[0].colorbar
cbar.ax.yaxis.set_tick_params(labelsize=15)

plt.title("Evaluation Metrics Per Class")
plt.tight_layout()
plt.savefig(os.path.join(base_dir, "metrics_table.png"))
plt.show()