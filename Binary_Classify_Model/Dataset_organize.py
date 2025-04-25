import os, shutil

skin_src =  r"D:\Project\Tumor\binary_skin_dataset\Skin_Dataset"
non_skin_src = r"D:\Project\Tumor\binary_skin_dataset\Non_Skin_Dataset"

valid_dst = r"D:\Project\Tumor\binary_skin_check\valid"
invalid_dst = r"D:\Project\Tumor\binary_skin_check\invalid"
os.makedirs(valid_dst, exist_ok=True)
os.makedirs(invalid_dst, exist_ok=True)

for folder in os.listdir(skin_src):
    folder_path = os.path.join(skin_src, folder)
    for img in os.listdir(folder_path):
        src = os.path.join(folder_path, img)
        dst = os.path.join(valid_dst, f"{folder}_{img}")
        shutil.copy2(src, dst)

for folder in os.listdir(non_skin_src):
    folder_path = os.path.join(non_skin_src, folder)
    for img in os.listdir(folder_path):
        src = os.path.join(folder_path, img)
        dst = os.path.join(invalid_dst, f"{folder}_{img}")
        shutil.copy2(src, dst)

print("Images organized for binary classification")
