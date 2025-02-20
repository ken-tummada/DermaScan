import os
import numpy as np
from PIL import Image


input_base_path = os.path.normpath(r"D:/学习/UCSB/DS/Tumor Project/skin_images")
output_base_path = os.path.normpath(r"D:/学习/UCSB/DS/Tumor Project/preprocessed_images")

lesion_classes = ["nevus", "melanoma", "actinic keratosis"]

target_size = (224, 224)

for lesion_class in lesion_classes:
    output_dir = os.path.join(output_base_path, lesion_class)
    os.makedirs(output_dir, exist_ok=True)

for lesion_class in lesion_classes:
    input_dir = os.path.join(input_base_path, lesion_class)
    output_dir = os.path.join(output_base_path, lesion_class)
    
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Processing {len(image_files)} images in '{lesion_class}'...")

    for idx, img_file in enumerate(image_files):
        input_img_path = os.path.join(input_dir, img_file)
        output_img_path = os.path.join(output_dir, img_file)

        try:
            img = Image.open(input_img_path)
            img = img.resize(target_size)
            
            img = img.convert("RGB")  
            img_data = (np.array(img) / 255.0).astype('float32')
            
            normalized_img = Image.fromarray((img_data * 255).astype('uint8'))
            normalized_img.save(output_img_path)

            if idx % 1000 == 0 and idx != 0:
                print(f"Processed {idx} images in '{lesion_class}'...")

        except Exception as e:
            print(f"Error processing {input_img_path}: {e}")

print("\n Image resizing and normalization complete.")
