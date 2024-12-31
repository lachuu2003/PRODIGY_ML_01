import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm: React.FC = () => {
  const [inputData, setInputData] = useState({
    area: '',
    bedrooms: '',
    bathrooms: '',
    stories: ''
  });
  const [predictedPrice, setPredictedPrice] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInputData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
  
    const numericInputData = {
      area: parseFloat(inputData.area),
      bedrooms: parseFloat(inputData.bedrooms),
      bathrooms: parseFloat(inputData.bathrooms),
      stories: parseFloat(inputData.stories),
    };
  
    // Check if any required field is empty or not a valid number
    if (Object.values(numericInputData).some(value => isNaN(value) || value === 0)) {
      setError("All fields are required and must be valid numbers.");
      return;
    }
  
    try {
      console.log('Sending request with data:', numericInputData); // Log the data being sent
      const response = await axios.post(
        'http://127.0.0.1:5000/predict',
        numericInputData,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      console.log('Prediction response:', response); // Log the full response here
      if (response.data && response.data.price) {
        setPredictedPrice(response.data.price);
        setError(null); // Clear any previous errors
      } else {
        setError('Invalid response from server');
      }
    } catch (error: any) {
      console.error('Error in prediction:', error);
      if (error.response) {
        console.error('Response error data:', error.response.data);
      }
      setError(error.response?.data?.error || 'Network error. Please try again later.');
      setPredictedPrice(null); // Clear any previous predictions
    }
  };

  return (
    <div>
      <h1>Predict Housing Price</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="area"
          placeholder="Area"
          value={inputData.area}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="bedrooms"
          placeholder="Bedrooms"
          value={inputData.bedrooms}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="bathrooms"
          placeholder="Bathrooms"
          value={inputData.bathrooms}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="stories"
          placeholder="Stories"
          value={inputData.stories}
          onChange={handleInputChange}
        />
        <button type="submit">Predict Price</button>
      </form>

      {predictedPrice !== null && <h2>Predicted Price: ₹{predictedPrice.toFixed(2)}</h2>}
      {error && <h2 style={{ color: 'red' }}>{error}</h2>}
    </div>
  );
};

export default PredictionForm;
