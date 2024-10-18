import pickle
import os
from datetime import timedelta
import numpy as np
from django.conf import settings
import django
import sys
from .models import StockPrice, StockPrediction

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_backend.settings')
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'AAPL_linear_regression_model.pkl')
print(MODEL_PATH)

def load_model():
    # Try to load the pickle model
    try:
        with open(MODEL_PATH, 'rb') as model_file:
            model = pickle.load(model_file)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

def predict_stock_prices(stock_symbol, days=30):
    # Load pre-trained model
    model = load_model()

    # Fetch the historical stock prices
    historical_prices = StockPrice.objects.filter(stock_symbol=stock_symbol).order_by('date')
    
    if len(historical_prices) == 0:
        raise ValueError("No historical data available for the given stock symbol.")

    # Prepare the input for the model (closing prices as features)
    close_prices = np.array([float(price.close_price) for price in historical_prices]).reshape(-1, 1)

    # Predict the stock prices for the next `days` days
    future_dates = [historical_prices.last().date + timedelta(days=i) for i in range(1, days + 1)]
    predictions = model.predict(np.arange(len(close_prices), len(close_prices) + days).reshape(-1, 1))

    # Store the predictions in the StockPrediction model
    for i, date in enumerate(future_dates):
        StockPrediction.objects.update_or_create(
            stock_symbol=stock_symbol,
            predicted_date=date,
            defaults={'predicted_price': predictions[i]}
        )

    return future_dates, predictions
