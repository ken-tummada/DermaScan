# DermaScan: A Cloud-Powered Deep Learning iOS App for Multi-Class Skin Tumor Classification

### Objective

Bringing hospital-only skin screening tools to mobile devices to monitor conditions anytime, anywhere.

&nbsp;

### Approach

**Step 1 · Model Development**  
Trained MobileNetV2 on a dermoscopic dataset using TensorFlow and Keras frameworks for image classification.

**Step 2 · UI Design in Figma**  
Designed image upload, result, disease info, and records pages in Figma to guide frontend.

**Step 3 · iOS Frontend Implementation**  
Built in SwiftUI, supporting image input and real-time result rendering.

**Step 4 · Backend API Construction**  
FastAPI receives images and returns predictions using exported TensorFlow models.

**Step 5 · Deployment & Integration**  
Backend deployed via AWS Lambda and CDK; app connects via RESTful API.

![image](https://github.com/user-attachments/assets/2fad0d1a-9b9e-4112-8a06-7673e350265a)

&nbsp;

### Methodology

**Model & Training**  
MobileNetV2, pre-trained on ImageNet, was used as the backbone. A two-phase training process was applied: initial training with frozen base layers and a custom classification head, followed by full-network fine-tuning with a cosine learning rate decay schedule for stable convergence. The head included global average pooling, a 512 → 256 unit dense layer with ReLU, and Softmax output. A total of 30 epochs were used, and early stopping was applied with model checkpointing to retain the best model.

**Imbalance & Augmentation**  
To handle class imbalance, class weights were computed using the balanced mode of scikit-learn’s compute_class_weight. To improve generalization, we used real-time data augmentation with random rotation, width/height shifting, zooming, shearing, horizontal flipping, and brightness variation via Keras’ ImageDataGenerator.

**Regularization & Optimization**  
30%-40% Dropout and batch normalization were applied between dense layers to reduce overfitting. The model was trained using categorical cross-entropy loss and the Adam optimizer, with cosine decay in the fine-tuning phase. Validation performance-guided checkpointing.

&nbsp;

### Results & Conclusion

Our MobileNetV2 model achieved strong performance, with a mean AUC of 0.946 and overall accuracy of 91.4%. VASC showed perfect AUC (1.00), and NV had the highest true positives (1,741). Despite class imbalance, class-weighting and augmentation helped maintain a mean specificity of 0.948 and sensitivity of 67.8%.

We developed a lightweight deep learning model for skin lesion classification and successfully deployed it in a fully integrated mobile app. Users can capture skin images, receive classification results in real-time, and access detailed medical context for each prediction.

The entire pipeline is now operational and scalable, offering a foundation for mobile-based skin screening in remote or underserved areas.

&nbsp;

<p align="center">
  <img src="https://github.com/user-attachments/assets/e8f0feea-cb03-4345-92a6-a555cafcbe4d" width="40%" />
  <img src="https://github.com/user-attachments/assets/4e371eef-6ced-4c23-947b-2ba85b0082a7" width="40%" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/05c234ce-e07a-4bc1-ab27-559f68914c2a" width="90%" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/1d6928a2-ee81-4434-8558-195cfa3d3bee" width="70%" />
</p>

&nbsp;

### Supported Conditions & Dataset Information

This app supports multi-class classification of the following eight types of skin tumors:

- **AK**: Actinic Keratoses
- **BCC**: Basal Cell Carcinoma
- **BKL**: Benign Keratosis-like Lesions
- **DF**: Dermatofibroma
- **MEL**: Melanoma
- **NV**: Melanocytic Nevi
- **SCC**: Squamous Cell Carcinoma
- **VASC**: Vascular Lesions

The training data for our model comes from the **International Skin Imaging Collaboration (ISIC)** archive, including both the 2018 and 2019 official datasets. These datasets were carefully curated to include a broad distribution of dermoscopic images and are essential benchmarks in dermatology AI research.

#### Dataset Access

- [ISIC 2018 Data](https://challenge.isic-archive.com/data/#2018)
- [ISIC 2019 Data](https://challenge.isic-archive.com/data/#2019)

&nbsp;

### Citation

We gratefully acknowledge the generous release of the ISIC datasets under the CC-BY-NC license, and cite the datasets and corresponding publications as follows:

**HAM10000 Dataset**: (c) by ViDIR Group, Department of Dermatology, Medical University of Vienna; https://doi.org/10.1038/sdata.2018.161

**MSK Dataset**: (c) Anonymous; https://arxiv.org/abs/1710.05006; https://arxiv.org/abs/1902.03368

**BCN_20000 Dataset**: (c) Department of Dermatology, Hospital Clínic de Barcelona

The corresponding publications are:

1. Tschandl P., Rosendahl C. & Kittler H. The HAM10000 dataset, a large collection of multi-source dermatoscopic images of common pigmented skin lesions. _Sci. Data_ 5, 180161 (2018). https://doi.org/10.1038/sdata.2018.161

2. Noel C. F. Codella et al. "Skin Lesion Analysis Toward Melanoma Detection: A Challenge at the 2017 International Symposium on Biomedical Imaging (ISBI), Hosted by the International Skin Imaging Collaboration (ISIC)", arXiv:1710.05006, arXiv:1902.03368.

3. Hernández-Pérez C. et al. "BCN20000: Dermoscopic lesions in the wild." _Scientific Data_. 2024 Jun 17;11(1):641.
