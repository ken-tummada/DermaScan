import json
import base64
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

def load_resources():
    model_path = "./tumor_classifier.h5"
    model = load_model(model_path)
    
    labels = None
    labels_map = None
    
    with open("labels.json") as f:
        labels = json.load(f)
    
    with open("disease-map.json") as f:
        labels_map = json.load(f)
    
    return (model, labels, labels_map)

def predict_single_image(image_bin):    
    (model, labels, labels_map) = load_resources()
    
    from PIL import Image
    import io

    img = Image.open(io.BytesIO(image_bin))
    img = img.convert('RGB')
    img = img.resize((224, 224), Image.NEAREST)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array, verbose=0)
    predicted_index = np.argmax(prediction)
    predicted_label = str(labels[str(int(predicted_index))])
    confidence = float(prediction[0][predicted_index])
    
    disease_info = labels_map[predicted_label]
    
    return (disease_info, confidence)

def handler(event, context):
    
    image_raw: str = event["body"]
    
    # convert it into jpeg binary
    image_bin = base64.b64decode(image_raw)
    
    try:
        (disease_info, confidence) = predict_single_image(image_bin)
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain",
            },
            "body": str(e)
        }
    
    return {
        "type": disease_info["name"],
        "severity": disease_info["severity"],
        "status": "Completed",
        "confidence": float(confidence),
    }