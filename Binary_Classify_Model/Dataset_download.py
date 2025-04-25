from duckduckgo_search import DDGS
import requests
import os

output_dir = r"D:\Project\Tumor\Non_Skin_Dataset"
os.makedirs(output_dir, exist_ok=True)

keywords = [
    "car", "dog", "cat", "tree", "flower", "sky", "beach", "laptop", "keyboard", "phone", "table", "chair",
    "book", "coffee", "mountain", "ocean", "river", "mirror", "bottle", "shoe", "pen", "notebook", "painting", "bus",
    "train", "airplane", "sunglasses", "handbag", "road", "clock", "lamp", "plant", "jacket", "bicycle", "basketball",
    "football", "tennis", "piano", "guitar", "saxophone", "cup", "knife", "spoon", "fork", "tv", "bed", "door",
    "window", "rug", "pillow", "blanket", "watch", "earphones", "camera", "calculator", "fan", "refrigerator",
    "microwave", "toaster", "stove", "blender", "toilet", "sink", "bathtub", "shower", "helmet", "drone", "lego",
    "robot", "calendar", "wallet", "keys", "remote", "ball", "hat", "scarf", "gloves", "boots", "sneakers", "sandals",
    "ring", "necklace", "bracelet", "backpack", "suitcase", "umbrella", "newspaper", "magazine", "ticket", "billboard",
    "advertisement", "tower", "bridge", "building", "skyscraper", "city", "village", "forest", "desert", "island",
    "volcano", "castle", "monument", "statue", "fountain", "museum", "stadium", "park", "garden", "playground",
    "school", "university", "office", "factory", "zoo", "barn", "lighthouse", "garage", "fence", "pool", "tent", "cave",
    "mine", "ladder", "elevator", "escalator", "stairs", "balcony", "roof", "ceiling", "floor", "wall", "tile", "brick",
    "cement", "concrete", "wood", "glass", "metal", "plastic", "fabric", "leather", "cotton", "wool", "paper", "soap",
    "shampoo", "toothbrush", "toothpaste", "comb", "razor", "deodorant", "lotion", "perfume", "nail polish", "makeup",
    "mirror", "sink", "towel", "brush", "spatula", "pan", "pot", "grater", "whisk", "measuring cup", "colander",
    "cutting board", "rolling pin", "mug", "plate", "bowl", "tray", "dish", "napkin", "placemat", "coaster", "thermos",
    "thermometer", "scale", "compass", "binoculars", "flashlight", "lighter", "match", "candle", "lantern", "fire",
    "smoke", "ash", "fog", "cloud", "rain", "snow", "ice", "hail", "storm", "lightning", "sunset", "sunrise", "moon",
    "star", "planet","healthy skin"
]
limit = 50

with DDGS() as ddgs:
    for keyword in keywords:
        print(f" Searching: {keyword}")
        results = ddgs.images(keyword, max_results=limit)

        keyword_dir = os.path.join(output_dir, keyword.replace(" ", "_"))
        os.makedirs(keyword_dir, exist_ok=True)

        for i, result in enumerate(results):
            try:
                image_url = result["image"]
                image_data = requests.get(image_url, timeout=10).content
                with open(os.path.join(keyword_dir, f"{i}.jpg"), "wb") as f:
                    f.write(image_data)
            except Exception as e:
                print(f"Failed to download image {i} for '{keyword}': {e}")
