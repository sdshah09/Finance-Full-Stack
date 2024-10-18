from django.urls import path
from .views import fetch_stock_data_view
from .views import backtest_view
from .views import home
from .views import predict_view
from .views import report_view

from . import views
urlpatterns = [
    path('', home, name='home'),  # This maps the home view to the root URL
    path('fetch/', fetch_stock_data_view, name='fetch_stock_data'),  # Fetch stock data
    path('predict/', predict_view, name='predict_stock_prices'),  # Predict stock prices
    path('backtest/', backtest_view, name='backtest'),
    path('report/', report_view, name='report_view'),  # Report generation

]
