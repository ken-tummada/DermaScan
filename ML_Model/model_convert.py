import coremltools as ct
import tensorflow as tf

# Load the trained Keras model
keras_model = tf.keras.models.load_model("tumor_classifier.h5")

# Convert to Core ML (explicitly setting source framework)
mlmodel = ct.convert(keras_model, 
                    source="tensorflow",  # Explicitly tell coremltools that this is a TensorFlow model
                     inputs=[ct.ImageType(shape=(1, 224, 224, 3))])

# Save the Core ML model
mlmodel.save("TumorClassifier.mlmodel")

print("Model successfully converted to Core ML format: TumorClassifier.mlmodel")
