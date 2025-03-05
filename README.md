# Tumor Classification Using Machine Learning and Core ML

## Project Overview
This project aims to develop an **AI-powered tumor classification system** that can detect **malignant (cancerous) and benign (non-cancerous) skin tumors** from medical images. The machine learning model is trained using **deep learning (CNNs)** and deployed directly into an iOS application via **Apple’s Core ML framework**.

Our goal is to provide a **fast, reliable, and offline tumor classification tool** that can assist medical professionals and users in identifying potential skin abnormalities.

---

## Key Features
- **Deep Learning Model**: Trained using **Convolutional Neural Networks (CNNs)** to classify skin tumors.
- **iOS Integration**: Deployed on an iPhone using **Core ML**, allowing users to analyze images directly on their devices.
- **Image Processing**: Automatically resizes and normalizes input images for accurate predictions.
- **Confidence-Based Results**: Filters predictions to only include categories with **>60% confidence**, displaying up to **3 top results**.
- **JSON Output Format**: Provides structured **JSON results** for integration into mobile applications.

---

## Project Structure
### **Machine Learning Model (Python)**
- **Trains a CNN model** on a dataset of skin tumors.
- **Converts the trained model** (`tumor_classifier.h5`) into **Core ML format** (`TumorClassifier.mlmodel`).
- **Optimizes the model** for efficient mobile deployment.

### **iOS Integration (Swift)**
- **Uses Core ML** to run predictions inside the iOS app.
- **Processes user-uploaded images** from the camera or gallery.
- **Filters predictions** based on confidence scores and outputs structured results.

### **JSON-Based Output**
- The app generates a **structured JSON response** with the classification type, status, and confidence score.
- Only **categories with >60% confidence** are shown (max 3).
