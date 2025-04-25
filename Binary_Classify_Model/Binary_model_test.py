import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model_path =  r"D:\Project\Tumor\binary_skin_checker.h5"
test_dir =  r"D:\Project\Tumor\binary_test_dataset"
threshold = 0.5
img_size = (224, 224)

model = load_model(model_path)

def predict_image(img_path):
    try:
        img = image.load_img(img_path, target_size=img_size)
        img_arr = image.img_to_array(img) / 255.0
        img_arr = np.expand_dims(img_arr, axis=0)

        prob = model.predict(img_arr)[0][0]
        result = "VALID lesion image" if prob >= threshold else "NOT a lesion image"
        return prob, result
    except Exception as e:
        return None, f"Error reading {img_path}: {e}"

print(f"\n Running test on: {test_dir}")
for fname in os.listdir(test_dir):
    if fname.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(test_dir, fname)
        prob, result = predict_image(path)
        if prob is not None:
            print(f"{fname:20} → Score: {prob:.4f} | {result}")
        else:
            print(result)
