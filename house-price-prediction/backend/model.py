import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
import pickle

# Load the dataset
data = pd.read_csv('Housing.csv')

# Preprocessing: Remove rows with missing values
data = data.dropna()

# Feature Selection: Only select area, bedrooms, bathrooms, and stories
X = data[['area', 'bedrooms', 'bathrooms', 'stories']]
y = data['price']

# Scaling the features using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply Polynomial Features to capture non-linear relationships
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X_scaled)

# Train-test split (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Train the model using Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the prices on the test data
y_pred = model.predict(X_test)

# Calculate the Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)

# Print the MAE value
print(f"Mean Absolute Error (MAE): ₹{mae:.2f}")

# Save the trained model, scaler, and polynomial transformer to a file
with open('model.pkl', 'wb') as file:
    pickle.dump((model, scaler, poly), file)
    print("Model, scaler, and polynomial features saved to 'model.pkl'")
