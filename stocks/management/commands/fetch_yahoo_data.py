from django.core.management.base import BaseCommand
from stocks.services import store_stock_data_in_db


class Command(BaseCommand):
    help = 'Fetch stock data from Yahoo Finance for the last 2 years and store it in the database'

    def add_arguments(self, parser):
        parser.add_argument('symbol', type=str, help='Stock symbol to fetch data for (e.g., AAPL)')

    def handle(self, *args, **kwargs):
        symbol = kwargs['symbol']
        
        self.stdout.write(f"Fetching data for {symbol} for the last 2 years...")
        store_stock_data_in_db(symbol)
        self.stdout.write(self.style.SUCCESS(f"Data for {symbol} fetched and stored successfully for the last 2 years."))
