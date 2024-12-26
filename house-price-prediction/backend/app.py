from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import logging

app = Flask(__name__)

# Enable CORS for all routes or specify React server's origin
CORS(app, resources={r"/predict": {"origins": "http://localhost:5173"}})
logging.basicConfig(level=logging.DEBUG)

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def hello():
    return 'Hello, Flask is running!'

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if the required keys are in the input data
        required_keys = [
            'Avg_Area_Income', 'Avg_Area_House_Age',
            'Avg_Area_Number_of_Rooms', 'Avg_Area_Number_of_Bedrooms', 'Area_Population'
        ]
        
        if not all(key in data for key in required_keys):
            return jsonify({'error': 'Missing required keys'}), 400

        # Process the input data and make prediction
        features = np.array([[data['Avg_Area_Income'], data['Avg_Area_House_Age'],
                               data['Avg_Area_Number_of_Rooms'], data['Avg_Area_Number_of_Bedrooms'], data['Area_Population']]])

        prediction = model.predict(features)

        return jsonify({'price': prediction[0]})

    except Exception as e:
        return jsonify({'error': f'Error during prediction: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
