from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model = load_model('trained_model.keras')
print(f"Model input shape: {model.input_shape}")  # Debug statement

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_path):
    try:
        # Open the image and convert it to RGB (3 channels)
        img = Image.open(image_path).convert('RGB')
        # Resize the image to (256, 256) to match the model's input shape
        img = img.resize((256, 256))
        # Convert the image to a numpy array and normalize pixel values
        img = np.array(img) / 255.0
        # Add a batch dimension
        img = np.expand_dims(img, axis=0)
        print(f"Processed image shape: {img.shape}")  # Debug statement
        return img
    except Exception as e:
        print(f"Error preprocessing image: {e}")  # Debug statement
        return None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file temporarily
        file_path = os.path.join('static', 'images', file.filename)
        file.save(file_path)
        print(f"Uploaded file saved to: {file_path}")  # Debug statement

        # Preprocess the image
        img = preprocess_image(file_path)
        if img is None:
            return jsonify({'error': 'Invalid image file'}), 400

        # Make a prediction
        try:
            prediction = model.predict(img)
            print(f"Model prediction: {prediction}")  # Debug statement
            classes = ['Corona Virus Disease',
                       'Normal', 'Pneumonia', 'Tuberculosis']
            result = classes[np.argmax(prediction)]

            # Return the result as JSON
            return jsonify({'result': result, 'image_url': file_path})
        except Exception as e:
            print(f"Error during prediction: {e}")  # Debug statement
            return jsonify({'error': 'An error occurred during prediction'}), 500

    return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    # Ensure the static/images folder exists
    os.makedirs(os.path.join('static', 'images'), exist_ok=True)
    app.run(debug=True)
