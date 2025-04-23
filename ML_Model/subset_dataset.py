import os
import random
import shutil

full_data_dir = r"D:\Project\Tumor\train"
subset_dir = r"D:\Project\Tumor\train_small"
fraction = 0.1  # 1/10th of each class

os.makedirs(subset_dir, exist_ok=True)

for class_name in os.listdir(full_data_dir):
    src_class_dir = os.path.join(full_data_dir, class_name)
    dst_class_dir = os.path.join(subset_dir, class_name)

    if not os.path.isdir(src_class_dir):
        continue  # skip non-folder files

    os.makedirs(dst_class_dir, exist_ok=True)

    all_images = [f for f in os.listdir(src_class_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    if len(all_images) == 0:
        print(f"⚠️ Skipping {class_name}: no images found")
        continue

    sample_size = max(1, int(len(all_images) * fraction))
    selected = random.sample(all_images, sample_size)

    for fname in selected:
        src_path = os.path.join(src_class_dir, fname)
        dst_path = os.path.join(dst_class_dir, fname)
        shutil.copy2(src_path, dst_path)

    print(f"✅ {class_name}: Copied {len(selected)} of {len(all_images)} images")

print(f"\n🎉 Done! Subset created in: {subset_dir}")
