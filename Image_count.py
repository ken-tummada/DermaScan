import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None 

base_path = os.path.normpath(r"D:/学习/UCSB/DS/Tumor Project/skin_images")  

lesion_classes = ["nevus", "melanoma", "actinic keratosis"]

image_counts = {}
corrupted_images = []

# Check images in each folder
for lesion_class in lesion_classes:
    class_path = os.path.join(base_path, lesion_class)
    if not os.path.exists(class_path):
        print(f" Warning: Folder '{class_path}' does not exist.")
        continue

    image_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_counts[lesion_class] = len(image_files)

    for img_file in image_files:
        img_path = os.path.join(class_path, img_file)
        try:
            img = Image.open(img_path)
            img.verify()  
        except (IOError, SyntaxError) as e:
            corrupted_images.append((img_path, str(e)))

print("\n Image Counts per Category:")
for lesion, count in image_counts.items():
    print(f"- {lesion}: {count} images")

if corrupted_images:
    print(f"\n Found {len(corrupted_images)} corrupted or problematic images:")
    for img, error in corrupted_images[:10]:  
        print(f"- {img} | Error: {error}")
else:
    print("\n No corrupted images found.")
