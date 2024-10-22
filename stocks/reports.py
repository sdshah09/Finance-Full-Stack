import matplotlib.pyplot as plt
import numpy as np
import os
from weasyprint import HTML
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import StockPrice, StockPrediction
import base64
import matplotlib
from datetime import timedelta

matplotlib.use('Agg')  # Use a non-GUI backend, ideal for server environments


# Function to generate performance metrics and visualizations
def create_pdf_report(data, symbol):
    plot_image = data['plot_image']  # Binary image data
    total_return = data['total_return']
    max_drawdown = data['max_drawdown']

    # Convert the plot image to base64 string
    image_base64 = base64.b64encode(plot_image.getvalue()).decode('utf-8')

    # Prepare HTML content for the PDF
    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    text-align: center;
                }}
                .metrics {{
                    font-size: 16px;
                    margin-bottom: 20px;
                }}
                img {{
                    display: block;
                    margin: 0 auto;
                    width: 100%;  /* Make sure the image fits the width of the page */
                    max-width: 700px;  /* Optional: restrict max width */
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <h1>Stock Report for {symbol}</h1>
            <h2>Performance Metrics:</h2>
            <ul class="metrics">
                <li>Total Return: {total_return:.2f}%</li>
                <li>Max Drawdown: {max_drawdown}</li>
            </ul>
            <h2>Price Comparison:</h2>
            <img src="data:image/png;base64,{image_base64}" alt="Stock Price Plot">
        </body>
    </html>
    """

    # Generate PDF using WeasyPrint
    pdf_file = BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)
    return pdf_file

# Ensure the proper calculation logic in generate_report
def generate_report(symbol):
    # Fetch the last 30 actual stock prices in chronological order
    actual_prices = StockPrice.objects.filter(stock_symbol=symbol).order_by('-date')[:30]
    actual_prices = actual_prices[::-1]  # Reverse to get them in chronological order

    # Fetch the next 30 predicted stock prices
    predicted_prices = StockPrediction.objects.filter(stock_symbol=symbol).order_by('predicted_date')[:30]

    if not predicted_prices:
        print(f"No predictions found for {symbol}")
        return None

    # Extract actual prices and their dates
    actual_dates = [price.date for price in actual_prices]
    actual_values = [float(price.close_price) for price in actual_prices]

    # Start predicted dates after the last actual date
    last_actual_date = actual_dates[-1]
    predicted_dates = [last_actual_date + timedelta(days=i+1) for i in range(len(predicted_prices))]
    predicted_values = [float(prediction.predicted_price) for prediction in predicted_prices]

    # Calculate performance metrics
    total_return = (predicted_values[-1] - actual_values[0]) / actual_values[0] * 100 if actual_values[0] != 0 else 0
    max_drawdown = min(predicted_values)  # Simplified for example

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(actual_dates, actual_values, label="Actual Prices (Last 30 Days)", color="blue")
    plt.plot(predicted_dates, predicted_values, label="Predicted Prices (Next 30 Days)", color="orange", linestyle="--")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Stock Prices: Actual vs Predicted for {symbol} (30 Key Points)")
    plt.legend()
    plt.grid(True)

    # Save the plot to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    # Return the performance metrics and plot image
    return {
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'plot_image': buffer
    }
