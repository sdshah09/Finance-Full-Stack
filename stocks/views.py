from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from.services import store_stock_data_in_db
from.backtesting import moving_average_strategy
import logging
from .ml_services import predict_stock_prices
from .reports import generate_report, create_pdf_report
from io import BytesIO
from weasyprint import HTML  # To generate PDF if needed

def home(request):
    return render(request, 'stocks/home.html')

def fetch_stock_data_view(request):
    symbol = request.GET.get('symbol')  # Get stock symbol from the URL parameters
    if not symbol:
        return JsonResponse({'status': 'error', 'message': 'Stock symbol is required'}, status=400)

    try:
        store_stock_data_in_db(symbol)
        return JsonResponse({'status': 'success', 'message': f'Data for {symbol} fetched and stored successfully.'})
    except Exception as e:
        logging.error(f"Error fetching stock data for {symbol}: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

def backtest_view(request):
    # Get parameters from the request
    stock_symbol = request.GET.get('symbol', 'AAPL')
    initial_investment = float(request.GET.get('initial_investment', 10000))
    short_window = int(request.GET.get('short_window', 50))
    long_window = int(request.GET.get('long_window', 200))

    # Basic validation
    if short_window <= 0 or long_window <= 0:
        return JsonResponse({'status': 'error', 'message': 'Window sizes must be positive integers.'})
    if short_window >= long_window:
        return JsonResponse({'status': 'error', 'message': 'Short window must be less than long window.'})
    if initial_investment <= 0:
        return JsonResponse({'status': 'error', 'message': 'Initial investment must be a positive number.'})

    # Run the backtesting strategy
    try:
        result = moving_average_strategy(
            stock_symbol=stock_symbol,
            initial_investment=initial_investment,
            short_window=short_window,
            long_window=long_window,
        )
        return JsonResponse(result)
    except Exception as e:
        logging.error(f"Error running backtest for {stock_symbol}: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def predict_view(request):
    symbol = request.GET.get('symbol')  # Get stock symbol from the URL parameters
    if not symbol:
        return JsonResponse({'status': 'error', 'message': 'Stock symbol is required'}, status=400)

    try:
        future_dates, predictions = predict_stock_prices(symbol)
        
        # Prepare the response data
        response_data = {
            'stock_symbol': symbol,
            'predictions': [
                {'date': str(future_dates[i]), 'predicted_price': float(predictions[i])}
                for i in range(len(future_dates))
            ]
        }
        
        return JsonResponse(response_data, safe=False)
    
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        logging.error(f"Error predicting stock prices for {symbol}: {e}")
        return JsonResponse({'error': 'An error occurred during prediction'}, status=500)
    
def report_view(request):
    symbol = request.GET.get('symbol')  # Get stock symbol from query parameters
    report_format = request.GET.get('format', 'json')  # Get report format (default is JSON)
    
    if not symbol:
        return JsonResponse({'error': 'Stock symbol is required'}, status=400)

    try:
        # Generate report data (including plot)
        report_data = generate_report(symbol)

        # Check if the user requested a PDF
        if report_format == 'pdf':
            # Generate PDF report
            pdf = create_pdf_report(report_data, symbol)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{symbol}_report.pdf"'
            return response
        else:
            # Return JSON response with the report data
            json_data = {
                'total_return': report_data['total_return'],
                'max_drawdown': report_data['max_drawdown'],
                'actual_prices': list(zip(report_data['actual_dates'], report_data['actual_values'])),
                'predicted_prices': list(zip(report_data['predicted_dates'], report_data['predicted_values'])),
            }
            return JsonResponse(json_data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
