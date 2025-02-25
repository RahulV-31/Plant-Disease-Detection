import os
import numpy as np
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Make sure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the model
MODEL_PATH = 'model/plant_disease_model(1).h5'
model = load_model(MODEL_PATH)

# Define class names (removing underscores)
class_names = [name.replace('_', ' ') for name in [
    'Apple Black Rot', 'Apple Healthy', 'Apple Scab', 'Cedar Apple Rust', 
    'Cherry Healthy', 'Cherry Powdery Mildew', 'Corn Cercospora Leaf Spot', 
    'Corn Healthy', 'Corn Northern Leaf Blight', 'Corn common Rust', 
    'Grape Esca (Black Measles)', 'Grape Healthy', 'Grape Leaf Blight', 
    'Grapes Black Rot', 'Peach Bacterial Spot', 'Peach Healthy', 
    'Pepper bell Bacterial spot', 'Pepper bell healthy', 
    'Potato Early blight', 'Potato Late blight', 'Potato healthy', 
    'Strawberry Healthy', 'Strawberry Leaf Scorch', 'Tomato Bacterial spot', 
    'Tomato Early blight', 'Tomato Late blight', 'Tomato Leaf Mold', 
    'Tomato Septoria leaf spot', 'Tomato Spider mites Two spotted spider mite', 
    'Tomato Target Spot', 'Tomato YellowLeaf Curl Virus', 
    'Tomato mosaic virus', 'Tomato healthy']]

# Define recommendations for each disease
disease_recommendations = {
    'Apple Black Rot': 'Remove infected leaves and fruit. Apply fungicides like captan or myclobutanil.',
    'Apple Scab': 'Apply fungicides early in the growing season. Remove and destroy fallen leaves.',
    'Cedar Apple Rust': 'Remove nearby cedar trees if possible. Apply fungicides like mancozeb.',
    'Cherry Powdery Mildew': 'Apply sulfur-based fungicides. Prune plants to improve air circulation.',
    'Corn Cercospora Leaf Spot': 'Rotate crops. Apply fungicides like pyraclostrobin or azoxystrobin.',
    'Corn Northern Leaf Blight': 'Plant resistant varieties. Apply fungicides like propiconazole.',
    'Corn common Rust': 'Apply fungicides like azoxystrobin or pyraclostrobin. Avoid overhead irrigation.',
    'Grape Esca (Black Measles)': 'Prune during dry weather. Apply fungicides preventatively.',
    'Grape Leaf Blight': 'Apply fungicides like mancozeb or copper-based products.',
    'Grapes Black Rot': 'Remove mummified fruits. Apply fungicides like myclobutanil or mancozeb.',
    'Peach Bacterial Spot': 'Apply copper-based bactericides. Prune during dry weather.',
    'Pepper bell Bacterial spot': 'Rotate crops. Apply copper-based bactericides.',
    'Potato Early blight': 'Apply fungicides like chlorothalonil or mancozeb. Practice crop rotation.',
    'Potato Late blight': 'Apply fungicides preventatively. Remove volunteer potatoes.',
    'Strawberry Leaf Scorch': 'Remove infected leaves. Apply fungicides like captan.',
    'Tomato Bacterial spot': 'Apply copper-based bactericides. Practice crop rotation.',
    'Tomato Early blight': 'Remove lower infected leaves. Apply fungicides like chlorothalonil.',
    'Tomato Late blight': 'Apply fungicides preventatively. Remove and destroy infected plants.',
    'Tomato Leaf Mold': 'Improve air circulation. Reduce humidity.',
    'Tomato Septoria leaf spot': 'Remove infected leaves. Apply fungicides like chlorothalonil.',
    'Tomato Spider mites Two spotted spider mite': 'Apply insecticidal soap or neem oil.',
    'Tomato Target Spot': 'Apply fungicides like chlorothalonil or mancozeb.',
    'Tomato YellowLeaf Curl Virus': 'Control whiteflies with insecticides.',
    'Tomato mosaic virus': 'Remove and destroy infected plants. Control aphids.'
}

# Add healthy plant messages
for plant_type in ['Apple', 'Cherry', 'Corn', 'Grape', 'Peach', 'Pepper bell', 'Potato', 'Strawberry', 'Tomato']:
    key = f'{plant_type} Healthy'
    disease_recommendations[key] = f'Your {plant_type} plant appears healthy! Maintain regular care.'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def predict_disease(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions[0])
    confidence = float(predictions[0][predicted_class_index]) * 100
    
    return {
        'class': class_names[predicted_class_index],
        'confidence': confidence,
        'recommendation': disease_recommendations.get(class_names[predicted_class_index], 'No specific recommendations.')
    }

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get prediction
        result = predict_disease(file_path)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': file_path,
            'class': result['class'],
            'confidence': result['confidence'],
            'recommendation': result['recommendation']
        })
    
    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(debug=True)
