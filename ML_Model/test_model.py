import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, accuracy_score

base_dir = r"D:\Project\Tumor"
model_path = os.path.join(base_dir, "ML_Model","tumor_classifier.h5")
test_dir = os.path.join(base_dir, "test")
img_size = (224, 224)
batch_size = 32

def evaluate_model_on_test_set(model, test_dir, img_size, batch_size):
    datagen = ImageDataGenerator(rescale=1./255)
    test_generator = datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    predictions = model.predict(test_generator, verbose=1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = test_generator.classes
    class_labels = list(test_generator.class_indices.keys())

    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_labels))
    
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\n Test Accuracy: {accuracy:.4f}")

def main():
    model = load_model(model_path)

    evaluate_model_on_test_set(model, test_dir, img_size, batch_size)

if __name__ == "__main__":
    main()

