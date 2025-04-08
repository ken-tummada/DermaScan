import os
import json
from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_dir = r"D:\Project\Tumor\train"
img_size = (224, 224)

datagen = ImageDataGenerator(rescale=1./255)
generator = datagen.flow_from_directory(train_dir, target_size=img_size, batch_size=1, class_mode='categorical')
class_indices = generator.class_indices
index_to_label = {v: k for k, v in class_indices.items()}

# Save to JSON
with open("class_labels.json", "w") as f:
    json.dump(index_to_label, f, indent=4)

print("Labels saved to class_labels.json")
