import requests
import os
from PIL import Image
from PIL import ImageOps  
from io import BytesIO

Image.MAX_IMAGE_PIXELS = None
os.makedirs("skin_images", exist_ok=True)

base_url = "https://api.isic-archive.com/api/v2/images/search/"

lesion_classes = ["nevus", "melanoma", "actinic keratosis"]

for lesion_class in lesion_classes:
    print(f"Fetching images for {lesion_class}...")
    
    current_url = base_url
    params = {
        "diagnosis": lesion_class,
        "limit": 100  # Fetch up to 100 images per request (max limit)
    }
    image_counter = 0
    max_images = 30000
    
    while current_url:
        response = requests.get(current_url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            
            for img in results:
                img_url = img['files']['full']['url']  
                img_id = img['isic_id']  
                
                file_path = f"skin_images/actinic keratosis/{lesion_class}_{img_id}.jpg"
                
                if not os.path.exists(file_path):
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        image = Image.open(BytesIO(img_response.content))
                        
                        if image.mode == "I;16":  
                            image = ImageOps.autocontrast(image.convert("L"))  
                        image.save(file_path)
                        print(f"Saved: {file_path}")
                        image_counter += 1
                    else:
                        print(f"Failed to download image {img_id} for {lesion_class}")
                else:
                    print(f"Image already exists: {file_path}")
            
            current_url = data.get('next', None)
            params = None
        else:
            print(f"Failed to fetch data for {lesion_class}, status code: {response.status_code}")
            break
    
    print(f"Total images downloaded for {lesion_class}: {image_counter}")
