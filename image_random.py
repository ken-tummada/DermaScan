import os
import shutil
import random

# Define paths for original melanoma and nevus datasets
Keratosis_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/Benign Keratosis-like Lesions (BKL)"
BCC_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/Basal Cell Carcinoma (BCC)"
Eczema_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/Eczema"
Seborrheic_folder = "D:/学习/UCSB/DS/Tumor Project/skin_images/Seborrheic Keratoses and other Benign Tumors"
# Define destination folders for train and test
train_benign_ActinicKeratosis = "D:/学习/UCSB/DS/Tumor Project/skin_images/train/benign/Actinic Keratosis"
train_benign_Eczema = "D:/学习/UCSB/DS/Tumor Project/skin_images/train/benign/Eczema"
train_benign_SeborrheicKeratosis = "D:/学习/UCSB/DS/Tumor Project/skin_images/train/benign/Seborrheic Keratosis"
test_benign_ActinicKeratosis = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/benign/Actinic Keratosis"
test_benign_Eczema = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/benign/Eczema"
test_benign_SeborrheicKeratosis = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/benign/Seborrheic Keratosis"
train_malignant_BasalCellCarcinoma = "D:/学习/UCSB/DS/Tumor Project/skin_images/train/malignant/Basal Cell Carcinoma"
test_malignant_BasalCellCarcinoma = "D:/学习/UCSB/DS/Tumor Project/skin_images/test/malignant/Basal Cell Carcinoma"

# Ensure destination directories exist
for folder in [train_benign_ActinicKeratosis, train_benign_Eczema, train_benign_SeborrheicKeratosis, test_benign_ActinicKeratosis, 
               test_benign_Eczema, test_benign_SeborrheicKeratosis, train_malignant_BasalCellCarcinoma, test_malignant_BasalCellCarcinoma]:
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
split_data(Keratosis_folder, train_benign_ActinicKeratosis, test_benign_ActinicKeratosis)
split_data(Eczema_folder, train_benign_Eczema, test_benign_Eczema)
split_data(BCC_folder, train_malignant_BasalCellCarcinoma, test_malignant_BasalCellCarcinoma)
split_data(Seborrheic_folder, train_benign_SeborrheicKeratosis, test_benign_SeborrheicKeratosis)


print("Dataset successfully split into training and testing sets!")
