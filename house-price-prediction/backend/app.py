from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pickle
import numpy as np
import logging
import os

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app, resources={r"/predict": {"origins": "http://localhost:5173"}})
logging.basicConfig(level=logging.DEBUG)

# Load the trained model
base_dir = os.path.dirname(os.path.abspath(__file__))  # This will give the absolute path to the backend folder
model_path = os.path.join(base_dir, 'model.pkl')

with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_keys = [
            'Avg_Area_Income', 'Avg_Area_House_Age',
            'Avg_Area_Number_of_Rooms', 'Avg_Area_Number_of_Bedrooms', 'Area_Population'
        ]
        if not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing required keys'}), 400

        features = np.array([[data['Avg_Area_Income'], data['Avg_Area_House_Age'],
                               data['Avg_Area_Number_of_Rooms'], data['Avg_Area_Number_of_Bedrooms'], data['Area_Population']]])
        prediction = model.predict(features)
        return jsonify({'price': prediction[0]})

    except Exception as e:
        return jsonify({'error': f'Error during prediction: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
