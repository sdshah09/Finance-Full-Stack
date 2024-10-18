from .models import StockPrice
import pandas as pd

def calculate_moving_average(prices, window):
    return prices.rolling(window=window).mean()

def moving_average_strategy(stock_symbol, initial_investment, short_window=50, long_window=200):
    # Fetch historical data from StockPrice model
    stock_prices = StockPrice.objects.filter(stock_symbol=stock_symbol).order_by('date')

    # Convert the stock prices to a DataFrame and convert Decimal to float
    data = pd.DataFrame(list(stock_prices.values('date', 'close_price')))
    data['close_price'] = data['close_price'].apply(float)  # Convert Decimal to float
    data.set_index('date', inplace=True)

    # Calculate the short (50-day) and long (200-day) moving averages
    data['short_ma'] = calculate_moving_average(data['close_price'], short_window)
    data['long_ma'] = calculate_moving_average(data['close_price'], long_window)

    # Initialize backtest variables
    position = 0  # Current position (0: no position, 1: bought stock)
    cash = initial_investment  # Cash available to invest
    stock = 0  # Number of shares owned
    trades = 0  # Number of trades executed
    trade_log = []  # Log of trades

    for i in range(1, len(data)):
        # Buy signal: Short moving average crosses above the long moving average
        if data['short_ma'].iloc[i] > data['long_ma'].iloc[i] and position == 0:
            buy_price = data['close_price'].iloc[i]
            stock = cash / buy_price
            cash = 0
            position = 1
            trades += 1
            trade_log.append((data.index[i], 'BUY', buy_price))

        # Sell signal: Short moving average crosses below the long moving average
        elif data['short_ma'].iloc[i] < data['long_ma'].iloc[i] and position == 1:
            sell_price = data['close_price'].iloc[i]
            cash = stock * sell_price
            stock = 0
            position = 0
            trades += 1
            trade_log.append((data.index[i], 'SELL', sell_price))

    # Calculate final portfolio value
    if position == 1:
        final_value = stock * data['close_price'].iloc[-1]  # Current stock price if still holding
    else:
        final_value = cash

    total_return = (final_value - initial_investment) / initial_investment * 100

    # Calculate max drawdown (optional, advanced metric)
    data['cumulative_return'] = (data['close_price'] / data['close_price'].iloc[0]) * initial_investment
    data['rolling_max'] = data['cumulative_return'].cummax()
    data['drawdown'] = data['rolling_max'] - data['cumulative_return']
    max_drawdown = data['drawdown'].max()

    performance = {
        'initial_investment': initial_investment,
        'final_value': final_value,
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'trades': trades,
        'trade_log': trade_log,
    }

    return performance
