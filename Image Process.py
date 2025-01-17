import os
import pydicom
import matplotlib.pyplot as plt

root_folder = "D:/学习/UCSB/DS/Tumor Project/Tumor Dataset/manifest-1600709154662/LIDC-IDRI"
output_folder = "D:/学习/UCSB/DS/Tumor Project/Tumor Dataset/Processed Images"

os.makedirs(output_folder, exist_ok=True)

def process_dicom_files(root_folder, output_folder):
    file_counter = 1  
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".dcm"):
                dicom_file_path = os.path.join(subdir, file)
                try:
                    dicom_data = pydicom.dcmread(dicom_file_path)
                    
                    output_file = os.path.join(output_folder, f"image_{file_counter}.png")
                    file_counter += 1  

                    plt.imsave(output_file, dicom_data.pixel_array, cmap="gray")
                    print(f"Saved: {output_file}")
                except Exception as e:
                    print(f"Error processing file {dicom_file_path}: {e}")

process_dicom_files(root_folder, output_folder)
