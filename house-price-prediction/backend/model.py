#model.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

# Load the data
HouseDF = pd.read_csv('Housing.csv')

# Select relevant features for prediction
X = HouseDF[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms', 
             'Avg. Area Number of Bedrooms', 'Area Population']]
y = HouseDF['Price']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

# Create and train the model
lm = LinearRegression()
lm.fit(X_train, y_train)

# Save the model to disk using pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(lm, file)

# Evaluate the model
predictions = lm.predict(X_test)
mae = metrics.mean_absolute_error(y_test, predictions)
mse = metrics.mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)

print(f'MAE: {mae}, MSE: {mse}, RMSE: {rmse}')
