# 🌿 Plant Disease Detection using Deep Learning  

### 🚀 AI-Powered Leaf Disease Classification with CNNs & Flask Web App  

This project focuses on **automated plant disease detection** using **Convolutional Neural Networks (CNNs)**. By analyzing images of plant leaves, the model classifies **33 different disease categories** across **9 plant species** and provides **prevention recommendations**. The trained model is deployed using a **Flask web application**, allowing users to upload leaf images and receive instant predictions.  

---  

## 📌 Project Overview  

🌱 **Why is this important?**  
Early detection of plant diseases helps farmers **reduce crop losses, improve yield quality, and take preventive action** before widespread infection. Traditional manual inspection is time-consuming and requires expert knowledge—this AI-powered approach makes disease detection **faster, automated, and accessible** to everyone.  

🔥 **Key Highlights**  
✔️ **CNN Model** trained on a dataset with **33 disease classes** across **9 plant species**  
✔️ **Achieved 96% validation accuracy**  
✔️ **Real-time image classification using a Flask Web App**  
✔️ **Provides prevention recommendations for detected diseases**  

---

## 🎯 Objective  

1️⃣ **Train a Deep Learning Model** to classify plant diseases from leaf images  
2️⃣ **Develop a Flask Web App** for real-time predictions  
3️⃣ **Provide prevention recommendations** to help farmers take immediate action  

---

## ⚙️ Model Development  

The model is built using a **Convolutional Neural Network (CNN)** with multiple layers for feature extraction and classification.  

📌 **Model Architecture**  
- **Input Layer**: 256x256 images with 3 color channels (RGB)  
- **Convolutional Layers**: Extract patterns and features from images  
- **Batch Normalization & Dropout**: Prevent overfitting and stabilize learning  
- **Activation Functions**: ReLU (hidden layers) & Softmax (output layer)  
- **Loss Function**: Categorical Cross-Entropy  
- **Optimizer**: Adam (Adaptive Moment Estimation)  
- **Output Layer**: 33 neurons (one for each disease class)  

📊 **Training Results**  
✅ **Training Accuracy**: 93%  
✅ **Validation Accuracy**: 96%  
✅ **Loss reduced significantly over epochs**  

---

## 🌐 Deployment: Flask Web App  

A **user-friendly web application** is developed using **Flask, HTML, CSS, and JavaScript**, allowing users to upload plant leaf images and get instant disease predictions.  

## 🌟 Frontend Features  

🔹 **HTML, CSS, and JavaScript** for a **responsive & interactive UI**  
🔹 **Bootstrap & Custom Styling** for a clean, modern design  
🔹 **Drag-and-Drop File Upload** for easy image submission  
🔹 **Real-time Disease Prediction Display** with prevention recommendations  


## 🛠️ Technologies Used  

| Technology | Purpose |
|------------|---------|
| **Python** | Backend & Model Training |
| **TensorFlow & Keras** | Deep Learning Model |
| **OpenCV** | Image Processing |
| **NumPy & Pandas** | Data Handling |
| **Matplotlib** | Data Visualization |
| **Flask** | Backend Web Framework |
| **HTML, CSS, JavaScript** | Frontend Web Development |
| **Bootstrap** | UI Styling |
