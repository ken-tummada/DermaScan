import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def main():
    base_dir = r"D:\Project\Tumor"
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "val")
    model_path = os.path.join(base_dir, "tumor_classifier.h5")

    img_size = (224, 224)
    batch_size = 32
    initial_epochs = 10
    fine_tune_epochs = 20

    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        raise FileNotFoundError("Train or validation directory not found.")

    # Data Generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.2,
        shear_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=img_size,
        batch_size=1,
        class_mode='categorical',
        shuffle=False
    )

    # Compute class weights
    labels = train_generator.classes
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(labels),
        y=labels
    )
    class_weights = dict(enumerate(class_weights))
    print(" Computed class weights:", class_weights)

    #  Build model
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(train_generator.num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    callbacks = [
        EarlyStopping(patience=3, restore_best_weights=True),
        ModelCheckpoint(model_path, save_best_only=True)
    ]

    # Train head layers
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=initial_epochs,
        callbacks=callbacks,
        class_weight=class_weights
    )

    # Fine-tune entire model
    base_model.trainable = True
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-5),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    fine_tune_history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=fine_tune_epochs,
        callbacks=callbacks,
        class_weight=class_weights
    )

    # Save model
    model.save(model_path)
    print(f"\n Model saved to: {model_path}")

    # Plot training accuracy
    acc = history.history['accuracy'] + fine_tune_history.history['accuracy']
    val_acc = history.history['val_accuracy'] + fine_tune_history.history['val_accuracy']

    plt.figure(figsize=(8, 4))
    plt.plot(acc, label='Train Accuracy')
    plt.plot(val_acc, label='Val Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training + Fine-Tuning Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "fine_tune_plot.png"))
    plt.show()

if __name__ == "__main__":
    main()
