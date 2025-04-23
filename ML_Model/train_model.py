import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import tensorflow as tf

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

    # === Data Generators ===
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.15,
        height_shift_range=0.15,
        zoom_range=0.25,
        shear_range=0.15,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
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

    # === Compute class weights ===
    labels = train_generator.classes
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(labels),
        y=labels
    )
    class_weights = dict(enumerate(class_weights))

    # === Load Base Model ===
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')

    for layer in base_model.layers[:80]:
        layer.trainable = False
    for layer in base_model.layers[80:]:
        layer.trainable = True

    # === Build New Model Head ===
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(train_generator.num_classes, activation='softmax')
    ])

    # === Compile (initial training) ===
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks = [
        EarlyStopping(patience=4, restore_best_weights=True),
        ModelCheckpoint(model_path, save_best_only=True)
    ]

    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=initial_epochs,
        callbacks=callbacks,
        class_weight=class_weights
    )

    # === Fine-Tuning Entire Model (with learning rate schedule) ===
    cosine_decay = tf.keras.optimizers.schedules.CosineDecay(
        initial_learning_rate=1e-4,
        decay_steps=fine_tune_epochs * len(train_generator),
        alpha=1e-6
    )
    model.compile(
        optimizer=optimizers.Adam(learning_rate=cosine_decay),
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

    # === Save Final Model ===
    model.save(model_path)
    print(f"\nModel saved to: {model_path}")

    # === Plot Accuracy ===
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