from django.test import TestCase
from .backtesting import moving_average_strategy
from .models import StockPrice

class BacktestingTests(TestCase):
    def setUp(self):
        # Create mock stock price data
        StockPrice.objects.create(stock_symbol='AAPL', date='2023-01-01', close_price=150)
        StockPrice.objects.create(stock_symbol='AAPL', date='2023-02-01', close_price=160)
        StockPrice.objects.create(stock_symbol='AAPL', date='2023-03-01', close_price=170)
        StockPrice.objects.create(stock_symbol='AAPL', date='2023-04-01', close_price=180)
        StockPrice.objects.create(stock_symbol='AAPL', date='2023-05-01', close_price=190)
        StockPrice.objects.create(stock_symbol='AAPL', date='2023-06-01', close_price=200)

    def test_moving_average_strategy(self):
        # Test with default parameters
        result = moving_average_strategy('AAPL', initial_investment=10000, short_window=50, long_window=200)
        self.assertEqual(result['trades'], 0)  # No trades for such small dataset
        self.assertTrue('total_return' in result)
