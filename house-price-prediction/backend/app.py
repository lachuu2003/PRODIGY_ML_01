from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import numpy as np
import logging
import os

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')

# Enable CORS for all routes or specify React server's origin
CORS(app, resources={r"/predict": {"origins": "http://localhost:5173/"}})

logging.basicConfig(level=logging.DEBUG)

# Load the trained model, scaler, and polynomial transformer
base_dir = os.path.dirname(os.path.abspath(__file__))  # This will give the absolute path to the backend folder
model_path = os.path.join(base_dir, 'model.pkl')

# Open the model file
with open(model_path, 'rb') as file:
    model, scaler, poly = pickle.load(file)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_keys = ['area', 'bedrooms', 'bathrooms', 'stories']
        if not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing required keys'}), 400

        # Prepare the input features as a numpy array
        features = np.array([[data['area'], data['bedrooms'], data['bathrooms'], data['stories']]])

        # Scale the features using the same scaler that was used during training
        features_scaled = scaler.transform(features)

        # Apply PolynomialFeatures (degree=2)
        features_poly = poly.transform(features_scaled)

        # Make prediction using the model
        prediction = model.predict(features_poly)

        return jsonify({'price': prediction[0]})

    except Exception as e:
        logging.error(f"Error during prediction: {str(e)}")
        return jsonify({'error': f'Error during prediction: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
