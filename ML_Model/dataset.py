import os
import pandas as pd
import shutil
import random

image_dir = r"D:\Project\Tumor\Dataset\ISIC_2019_Training_Input"
label_csv = r"D:\Project\Tumor\Dataset\ISIC_2019_Training_GroundTruth.csv"
output_base = r"D:\Project\Tumor"

df = pd.read_csv(label_csv)

df.rename(columns={"AK": "AKIEC"}, inplace=True)

label_columns = df.columns[1:]  
df['label'] = df[label_columns].idxmax(axis=1)  

df = df.sample(frac=1, random_state=42).reset_index(drop=True)
train_end = int(0.7 * len(df))
valid_end = int(0.85 * len(df))

splits = {
    'train': df[:train_end],
    'val': df[train_end:valid_end],
    'test': df[valid_end:]
}

copied_count = 0
skipped_count = 0

for split, data in splits.items():
    for _, row in data.iterrows():
        filename = f"{row['image']}.jpg"
        label = row['label']
        src = os.path.join(image_dir, filename)
        dst_folder = os.path.join(output_base, split, label)
        dst = os.path.join(dst_folder, filename)

        if not os.path.exists(src):
            print(f"[Missing] {src}")
            continue

        if os.path.exists(dst):
            skipped_count += 1
            continue  

        os.makedirs(dst_folder, exist_ok=True)  
        shutil.copy(src, dst)
        copied_count += 1

print("\n Dataset split completed successfully.")
print(f" Total images copied: {copied_count}")
print(f" Skipped (already existed): {skipped_count}")
