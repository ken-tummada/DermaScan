import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


def compute_log_weights(labels):
    class_counts = np.bincount(labels)
    total = np.sum(class_counts)
    weights = np.log1p(total / (class_counts + 1e-6))
    return dict(enumerate(weights))


def save_snapshot(model, epoch, snapshot_dir):
    path = os.path.join(snapshot_dir, f"snapshot_epoch_{epoch}.h5")
    model.save(path)
    print(f"\n Snapshot saved: {path}")


def main():
    base_dir = r"D:\Project\Tumor"
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "val")
    model_path = os.path.join(base_dir, "tumor_classifier_efficientnet.h5")
    snapshot_dir = os.path.join(base_dir, "ML_Model", "snapshots")
    os.makedirs(snapshot_dir, exist_ok=True)

    img_size = (224, 224)
    batch_size = 16
    initial_epochs = 15  
    fine_tune_epochs = 10

    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        raise FileNotFoundError("Train or validation directory not found.")

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.2,
        shear_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir, target_size=img_size, batch_size=batch_size,
        class_mode='categorical', shuffle=True)

    val_generator = val_datagen.flow_from_directory(
        val_dir, target_size=img_size, batch_size=1,
        class_mode='categorical', shuffle=False)

    labels = train_generator.classes
    class_weights = compute_log_weights(labels)
    print("\nClass weights (log1p balanced):", class_weights)

    base_model = EfficientNetB0(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu', kernel_regularizer='l2'),
        layers.Dropout(0.4),
        layers.Dense(train_generator.num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    callbacks = [EarlyStopping(patience=5, restore_best_weights=True)]

    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=initial_epochs,
        callbacks=callbacks,
        class_weight=class_weights
    )

    for e in [5, 10, 15]:
        save_snapshot(model, e, snapshot_dir)

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

    model.save(model_path)
    print(f"\nModel saved to: {model_path}")

    acc = history.history['accuracy'] + fine_tune_history.history['accuracy']
    val_acc = history.history['val_accuracy'] + fine_tune_history.history['val_accuracy']

    plt.figure(figsize=(8, 4))
    plt.plot(acc, label='Train Accuracy')
    plt.plot(val_acc, label='Val Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('EfficientNetB0 Training + Fine-Tuning Accuracy')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, "efficientnet_fine_tune_plot.png"))
    plt.show()


if __name__ == "__main__":
    main()
