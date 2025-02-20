import os
import cv2
import torch
import torchvision
import numpy as np
from torchvision.models.detection import maskrcnn_resnet50_fpn
from PIL import Image

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = maskrcnn_resnet50_fpn(pretrained=True)
model.eval()
model.to(device)

CONFIDENCE_THRESHOLD = 0.7

input_dir = r'D:/学习/UCSB/DS/Tumor Project/preprocessed_images/nevus'  
output_dir = r'D:/学习/UCSB/DS/Tumor Project/auto_annotations/nevus_maskrcnn'  
os.makedirs(output_dir, exist_ok=True)

def process_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)

    transform = torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
    image_tensor = transform(image).to(device)

    with torch.no_grad():
        predictions = model([image_tensor])

    for idx, score in enumerate(predictions[0]['scores']):
        if score > CONFIDENCE_THRESHOLD:
            mask = predictions[0]['masks'][idx, 0].mul(255).byte().cpu().numpy()
            bbox = predictions[0]['boxes'][idx].detach().cpu().numpy().astype(int)

            cv2.rectangle(image_np, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

            colored_mask = np.zeros_like(image_np)
            colored_mask[:, :, 1] = mask  
            image_np = cv2.addWeighted(image_np, 1, colored_mask, 0.5, 0)

    return image_np

for img_name in os.listdir(input_dir):
    if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(input_dir, img_name)
        output_path = os.path.join(output_dir, img_name)

        try:
            result_image = process_image(img_path)

            result_pil = Image.fromarray(result_image)
            result_pil.save(output_path)

            print(f"Processed and saved: {output_path}")
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

print("Mask R-CNN annotation complete.")
