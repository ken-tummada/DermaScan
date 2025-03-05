import os
import shutil
import random

# Define paths for original melanoma and nevus datasets
melanoma_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/melanoma_test"
nevus_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/nevus_test"

# Define destination folders for train and test
train_benign = "D:/学习/UCSB/DS/Tumor Project/skin_images/train/benign"
test_benign = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/benign"
train_malignant = "D:/学习/UCSB/DS/Tumor Project/skin_images/train/malignant"
test_malignant = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/malignant"

# Ensure destination directories exist
for folder in [train_benign, test_benign, train_malignant, test_malignant]:
    os.makedirs(folder, exist_ok=True)

# Function to split and move images
def split_data(source_folder, train_folder, test_folder, split_ratio=0.8):
    # Get all image files
    images = [f for f in os.listdir(source_folder) if f.endswith(('.jpg', '.png'))]
    
    # Shuffle images for randomness
    random.shuffle(images)

    # Split into train and test sets
    split_index = int(len(images) * split_ratio)
    train_images = images[:split_index]
    test_images = images[split_index:]

    # Move images
    for img in train_images:
        shutil.move(os.path.join(source_folder, img), os.path.join(train_folder, img))

    for img in test_images:
        shutil.move(os.path.join(source_folder, img), os.path.join(test_folder, img))

# Split melanoma (malignant) and nevus (benign)
split_data(melanoma_folder, train_malignant, test_malignant)
split_data(nevus_folder, train_benign, test_benign)

print("Dataset successfully split into training and testing sets!")
