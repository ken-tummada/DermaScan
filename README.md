# DermaScan: A Skin Condition Classifier App for iOS, Powered by Deep Learning

### Objective

Bringing hospital-only skin screening tools to mobile devices to monitor conditions anytime, anywhere.

&nbsp;

### Approach

**1 · Model Development**  
Built a lightweight CNN to filter out non-skin images, followed by fine-tuning MobileNetV2 to classify dermoscopic images by lesion type.

**2 · UI Design & Frontend Development**  
Designed upload, result, and records pages in Figma and implemented them with SwiftUI to support real-time image input and result rendering.

**3 · Backend & Deployment**  
Hosted trained models on AWS Lambda for real-time interaction with the iOS frontend.

&nbsp;

<p align="left">
  <img src="https://github.com/user-attachments/assets/17763ba5-217f-46d0-a110-e858b6109c2f" width="30%" />
</p>

&nbsp;

### Methodology

**Model & Training**  
- Binary Classifier: 2 Conv2D + MaxPooling → GAP → Dense → Dropout → Sigmoid
- Lesion Classifier (MobileNetV2):
  - Custom head training (base frozen)
  - Full model (cosine LR decay)
  - Head: GAP → Dense → Softmax
  - 30 epochs with early stopping

**Augmentation & Imbalance Handling**  
- Augmentation: rotation, shift, zoom, shear, brightness, and flipping
- Class balancing via `compute_class_weight`

**Regularization & Optimization**  
- Dropout (30–40%) + BatchNormalization
- Loss: Categorical cross-entropy
- Optimizer: Adam + cosine LR decay

&nbsp;

### Results & Conclusion

**Outcome**  
- Our MobileNetV2 model achieved 92.8% accuracy and 0.951 mean AUC.
- VASC reached perfect AUC (1.00), and NV had the highest true positives (1,933).
- Class-weighting and augmentation maintained 0.957 specificity and 72.7% sensitivity.

**Area for Improvement**  
- Boost sensitivity with focal loss and SMOTE.
- Enhance generalization using clinical metadata and multi-input models.
- Optimize mobile performance through pruning and quantization.

&nbsp;

<p align="center">
  <img src="https://github.com/user-attachments/assets/8974e25b-e1fb-4d6f-8e3d-b6fb138c9121" width="49%" />
  <img src="https://github.com/user-attachments/assets/a52544fa-d49a-48ed-8d20-6263fde0c1b6" width="31%" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3bf3cbf8-c24a-4480-ad2d-b641622fee0d" width="90%" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3051de8a-fb90-4b16-a068-f2500e79ef61" width="70%" />
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
