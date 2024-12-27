import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm: React.FC = () => {
  const [inputData, setInputData] = useState({
    Avg_Area_Income: '',
    Avg_Area_House_Age: '',
    Avg_Area_Number_of_Rooms: '',
    Avg_Area_Number_of_Bedrooms: '',
    Area_Population: ''
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
      Avg_Area_Income: parseFloat(inputData.Avg_Area_Income),
      Avg_Area_House_Age: parseFloat(inputData.Avg_Area_House_Age),
      Avg_Area_Number_of_Rooms: parseFloat(inputData.Avg_Area_Number_of_Rooms),
      Avg_Area_Number_of_Bedrooms: parseFloat(inputData.Avg_Area_Number_of_Bedrooms),
      Area_Population: parseFloat(inputData.Area_Population),
    };
  
    // Check if any required field is empty or not a valid number
    if (Object.values(numericInputData).some(value => isNaN(value) || value === 0)) {
      setError("All fields are required and must be valid numbers.");
      return;
    }
  
    try {
      console.log('Sending request with data:', numericInputData); // Log the data being sent
      const response = await axios.post(
        'https://app.onrender.com/predict',
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
          name="Avg_Area_Income"
          placeholder="Avg Area Income"
          value={inputData.Avg_Area_Income}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="Avg_Area_House_Age"
          placeholder="Avg Area House Age"
          value={inputData.Avg_Area_House_Age}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="Avg_Area_Number_of_Rooms"
          placeholder="Avg Area Number of Rooms"
          value={inputData.Avg_Area_Number_of_Rooms}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="Avg_Area_Number_of_Bedrooms"
          placeholder="Avg Area Number of Bedrooms"
          value={inputData.Avg_Area_Number_of_Bedrooms}
          onChange={handleInputChange}
        />
        <input
          type="number"
          name="Area_Population"
          placeholder="Area Population"
          value={inputData.Area_Population}
          onChange={handleInputChange}
        />
        <button type="submit">Predict Price</button>
      </form>

      {predictedPrice !== null && <h2>Predicted Price: ${predictedPrice.toFixed(2)}</h2>}
      {error && <h2 style={{ color: 'red' }}>{error}</h2>}
    </div>
  );
};

export default PredictionForm;
