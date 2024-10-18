import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import os

# Create some dummy training data (you can replace this with actual stock data)
X = np.arange(100).reshape(-1, 1)  # Fake data: day numbers
y = 1.5 * X.flatten() + 10  # Fake data: stock prices

# Train a simple linear regression model
model = LinearRegression()
model.fit(X, y)

# Save the trained model as a pickle file
# model_dir = 'stocks/ml_models'
# os.makedirs(model_dir, exist_ok=True)  # Ensure the directory exists


model_path = os.path.join(os.getcwd(), 'ml_models','linear_regression_model.pkl')
with open(model_path, 'wb') as model_file:
    pickle.dump(model, model_file)

print(f"Model saved to {model_path}")