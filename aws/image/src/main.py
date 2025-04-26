import json
import base64
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import math

def preprocess_image(image_bin):
    from PIL import Image
    import io
    
    img = Image.open(io.BytesIO(image_bin))
    img = img.convert('RGB')
    img = img.resize((224, 224), Image.NEAREST)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def load_skin_detection_resources():
    model_path = "./skin_classifier.h5"
    model = load_model(model_path)
    threshold = 0.5
    
    return (model, threshold)

def is_skin_image(img_arr) -> tuple[bool, float]: 
    (model, threshold) = load_skin_detection_resources()
    prob = model.predict(img_arr)[0][0]
    confidence = math.sqrt(2) * (abs(prob - threshold) ** 0.5)
    
    return (prob >= threshold, confidence)
    

def load_skin_condtion_classifier_resources():
    model_path = "./tumor_classifier.h5"
    model = load_model(model_path)
    
    labels = None
    labels_map = None
    
    with open("labels.json") as f:
        labels = json.load(f)
    
    with open("disease-map.json") as f:
        labels_map = json.load(f)
    
    return (model, labels, labels_map)

def predict_single_image(img_arr):    
    (model, labels, labels_map) = load_skin_condtion_classifier_resources()
    
    prediction = model.predict(img_arr, verbose=0)
    predicted_index = np.argmax(prediction)
    predicted_label = str(labels[str(int(predicted_index))])
    confidence = float(prediction[0][predicted_index])
    
    disease_info = labels_map[predicted_label]
    
    return (disease_info, confidence)

def handler(event, context):
    try:
        image_raw: str = event["body"]
    
        # convert it into jpeg binary
        image_bin = base64.b64decode(image_raw)
    
        img_arr = preprocess_image(image_bin)
        
        is_valid_image, is_valid_confidence = is_skin_image(img_arr)
        
        if is_valid_image:
            (disease_info, confidence) = predict_single_image(img_arr)
        
            body = {
                "type": disease_info["name"],
                "severity": disease_info["severity"],
                "status": "Completed",
                "confidence": float(confidence),
            }
            
        else:
            body = {
               "type": "n/a",
                "severity": "n/a",
                "status": "error",
                "confidence": float(is_valid_confidence),
            }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "text/plain",
            },
            "body": str(e)
        }
    
    return body