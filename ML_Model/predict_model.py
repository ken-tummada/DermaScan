import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

base_dir = r"D:\Project\Tumor"
model_path = os.path.join(base_dir, "tumor_classifier.h5")
train_dir = os.path.join(base_dir, "train")  
img_size = (224, 224)

def load_class_labels(train_dir, img_size):
    datagen = ImageDataGenerator(rescale=1./255)
    generator = datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=1,
        class_mode='categorical'
    )
    return list(generator.class_indices.keys())

def predict_single_image(model, img_path, class_labels):
    if not os.path.exists(img_path):
        print(f" Image not found: {img_path}")
        return

    try:
        img = image.load_img(img_path, target_size=img_size)
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array, verbose=0)
        predicted_index = np.argmax(prediction)
        predicted_label = class_labels[predicted_index]
        confidence = prediction[0][predicted_index]

        print(f"\n Image: {os.path.basename(img_path)}")
        print(f" Predicted class: {predicted_label}")
        print(f" Confidence: {confidence:.2f}")

    except Exception as e:
        print(f" Error processing {img_path}: {e}")

def predict_folder(model, folder_path, class_labels):
    print(f"\n Scanning folder: {folder_path}")
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(folder_path, filename)
            predict_single_image(model, img_path, class_labels)

def main():
    model = load_model(model_path)

    class_labels = load_class_labels(train_dir, img_size)

    # Predict a single image
    test_image = r"D:\Project\Tumor\test\MEL\ISIC_0000174.jpg"  
    predict_single_image(model, test_image, class_labels)

    # predict_folder(model, test_folder, class_labels)

if __name__ == "__main__":
    main()
