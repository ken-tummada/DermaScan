import os
import pandas as pd
import shutil
import random

# Set your paths
image_dir = r"D:\Project\Tumor\Dataset\ISIC_2019_Training_Input"
label_csv = r"D:\Project\Tumor\Dataset\ISIC_2019_Training_GroundTruth.csv"
output_base = r"D:\Project\Tumor"

# Load the label CSV
df = pd.read_csv(label_csv)

# Rename AK to AKIEC to match folder names
df.rename(columns={"AK": "AKIEC"}, inplace=True)

# Find the label column (one-hot encoding)
label_columns = df.columns[1:]  # assuming first column is image name
df['label'] = df[label_columns].idxmax(axis=1)  # assign a label column

# Shuffle and split
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
train_end = int(0.7 * len(df))
valid_end = int(0.85 * len(df))

splits = {
    'train': df[:train_end],
    'val': df[train_end:valid_end],
    'test': df[valid_end:]
}

# Track how many were copied
copied_count = 0
skipped_count = 0

# Copy images to pre-created folders
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
            continue  # skip if already copied

        os.makedirs(dst_folder, exist_ok=True)  # optional safety
        shutil.copy(src, dst)
        copied_count += 1

# Summary
print("\n Dataset split completed successfully.")
print(f" Total images copied: {copied_count}")
print(f" Skipped (already existed): {skipped_count}")
