import yfinance as yf
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import os
from .models import StockPrice
import pickle
import pandas as pd
def fetch_stock_data(symbol, period='2y'):
    data = yf.download(symbol, period=period)
    return data

def store_stock_data_in_db(symbol):
    data = fetch_stock_data(symbol)
    if data is None or data.empty:
        print(f"No data found for symbol {symbol}.")
        return

    for index, row in data.iterrows():
        try:
            StockPrice.objects.update_or_create(
                stock_symbol=symbol,
                date=index.date(),
                defaults={
                    # Extract scalar values and handle NaN
                    'open_price': float(row['Open']) if not pd.isna(row['Open']) else None,
                    'close_price': float(row['Close']) if not pd.isna(row['Close']) else None,
                    'high_price': float(row['High']) if not pd.isna(row['High']) else None,
                    'low_price': float(row['Low']) if not pd.isna(row['Low']) else None,
                    'volume': int(row['Volume']) if not pd.isna(row['Volume']) else None,
                }
            )
        except Exception as e:
            print(f"Error saving data for {symbol} on {index.date()}: {e}")
    train_and_save_model(symbol)
    
def train_and_save_model(symbol):
    # Fetch data from the database
    stock_data = StockPrice.objects.filter(stock_symbol=symbol).order_by('date')
    
    if not stock_data:
        raise ValueError(f"No data found in the database for symbol {symbol}")

    # Prepare data for the model
    X = np.array([(data.date - stock_data[0].date).days for data in stock_data]).reshape(-1, 1)
    y = np.array([data.close_price for data in stock_data])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"Model trained. Train score: {train_score:.4f}, Test score: {test_score:.4f}")

    # Save the trained model
    model_dir = os.path.join(os.getcwd(), 'ml_models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, f'{symbol}_linear_regression_model.pkl')

    with open(model_path, 'wb') as model_file:
        pickle.dump(model, model_file)

    print(f"Model saved to {model_path}")

    return model, model_path
