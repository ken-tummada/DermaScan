import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

dataset_dir = r"D:\Project\Tumor\ML_Model\Graph_data"
model_path = r"D:\Project\Tumor\ML_Model\tumor_classifier.h5"
output_path = r"D:\Project\Tumor\ML_Model\Graphs\fixed_real_features.png"

class_folders = ['AK', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'SCC', 'VASC']
selected_images = [os.path.join(dataset_dir, class_name + '.jpg') for class_name in class_folders]
selected_labels = class_folders

print("Selected images:")
for img_path in selected_images:
    print(img_path)

full_model = tf.keras.models.load_model(model_path)

inputs = tf.keras.Input(shape=(224, 224, 3))
x = full_model.layers[0](inputs)    
gap_output = full_model.layers[1](x)  
feature_extractor = tf.keras.Model(inputs=inputs, outputs=gap_output)

feature_img_path = selected_images[0]
img = image.load_img(feature_img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.0

features = feature_extractor.predict(img_array)

fig = plt.figure(figsize=(8,20))
ax = fig.add_subplot(1, 1, 1)
ax.axis('off')

top_y = 0.80
middle_y = 0.58
bottom_y = 0.34
box_height = 0.18

top_box = patches.FancyBboxPatch((0.04, top_y), 0.92, box_height,
    boxstyle="round,pad=0.01", linewidth=2, edgecolor='gray', facecolor='none', linestyle='--')
fig.add_artist(top_box)

fig.text(0.5, top_y + box_height - 0.02, 'Skin Tumor Images', ha='center', fontsize=20, weight='bold')

start = (1 - (8*0.1 + 7*0.01)) / 2
for idx, img_path in enumerate(selected_images):
    img = mpimg.imread(img_path)
    ax_img = fig.add_axes([0.065 + idx*0.085, top_y + 0.01, 0.1, 0.1])  # Closer and slightly smaller
    ax_img.imshow(img, cmap='gray')
    ax_img.axis('off')
    ax_img.set_title(selected_labels[idx], fontsize=12)

middle_box = patches.FancyBboxPatch((0.04, middle_y), 0.92, box_height,
    boxstyle="round,pad=0.01", linewidth=2, edgecolor='gray', facecolor='none', linestyle='--')
fig.add_artist(middle_box)

fig.text(0.5, middle_y + box_height - 0.03, 'Deep Feature Extractor (MobileNetV2 + GAP)', ha='center', fontsize=20, weight='bold')

ax_middle = fig.add_axes([0.06, middle_y + 0.03, 0.88, 0.08])

real_features = features.flatten()
ax_middle.plot(real_features, color='black', lw=1)
ax_middle.scatter(range(len(real_features)), real_features, c=np.random.rand(len(real_features)), cmap='rainbow', s=8)
ax_middle.text(len(real_features)-10, np.max(real_features)*0.9, '← GAP layer', fontsize=12, ha='right')
ax_middle.axis('off')

bottom_box = patches.FancyBboxPatch((0.04, bottom_y), 0.92, box_height,
    boxstyle="round,pad=0.01", linewidth=2, edgecolor='gray', facecolor='none', linestyle='--')
fig.add_artist(bottom_box)

fig.text(0.5, bottom_y + box_height - 0.03, 'Deep Features (1280 features)', ha='center', fontsize=20, weight='bold')

ax_bottom = fig.add_axes([0.06, bottom_y + 0.03, 0.88, 0.08])
feature_map1 = np.random.rand(50, 640)
feature_map2 = np.random.rand(50, 640)
final_feature_map = np.hstack((feature_map1, feature_map2))

ax_bottom.imshow(final_feature_map, cmap='gray', aspect='auto')
ax_bottom.axis('off')

plt.savefig(output_path, dpi=300)
plt.show()

print(f"\n Final figure saved to: {output_path}")
