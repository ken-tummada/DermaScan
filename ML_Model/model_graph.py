import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

dataset_dir = r"D:\Project\Tumor\ML_Model\Graph_data"
model_path = r"D:\Project\Tumor\ML_Model\tumor_classifier.h5"
output_path = r"D:\Project\Tumor\ML_Model\Graphs\real_features_gridspec.png"

class_folders = ['AK', 'BCC', 'BKL', 'DF', 'MEL', 'NV', 'SCC', 'VASC']
selected_images = [os.path.join(dataset_dir, class_name + '.jpg') for class_name in class_folders]
selected_labels = class_folders

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
real_features = features.flatten()

fig = plt.figure(figsize=(15, 5), constrained_layout=True)
gs = gridspec.GridSpec(3, 1, figure=fig, height_ratios=[1, 1, 1])

ax_top = fig.add_subplot(gs[0])
ax_top.axis('off')

rect_top = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor='gray', linestyle='--', linewidth=3, transform=ax_top.transAxes)
ax_top.add_patch(rect_top)

ax_top.set_title('Skin Tumor Images', fontsize=22, weight='bold', pad=20)

for idx, img_path in enumerate(selected_images):
    img = mpimg.imread(img_path)
    left = 0.2 + (((idx/2)+0.05) / len(selected_images))
    ax_img = fig.add_axes([left, 0.68, 0.15, 0.15])  
    ax_img.imshow(img, cmap='gray')
    ax_img.axis('off')
    ax_img.set_title(selected_labels[idx], fontsize=10)

ax_middle = fig.add_subplot(gs[1])
ax_middle.set_title('Deep Feature Extractor (MobileNetV2 + GAP)', fontsize=22, weight='bold', pad=20)

rect_middle = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor='gray', linestyle='--', linewidth=3, transform=ax_middle.transAxes)
ax_middle.add_patch(rect_middle)

ax_middle.plot(real_features, color='black', lw=1)
ax_middle.scatter(range(len(real_features)), real_features, c=np.random.rand(len(real_features)), cmap='rainbow', s=8)
ax_middle.text(len(real_features)-12, np.max(real_features)*0.9, '← GAP layer', fontsize=12, ha='right')
ax_middle.axis('off')

ax_bottom = fig.add_subplot(gs[2])
ax_bottom.set_title('Deep Features (1280 features)', fontsize=22, weight='bold', pad=20)

rect_bottom = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor='gray', linestyle='--', linewidth=3, transform=ax_bottom.transAxes)
ax_bottom.add_patch(rect_bottom)

feature_map_real = real_features.reshape(40, 32) 
ax_bottom.imshow(feature_map_real, cmap='gray', aspect='auto')
ax_bottom.axis('off')

plt.savefig(output_path, dpi=300)
plt.show()

print(f"\nFinal figure saved to: {output_path}")
