import os
import mysql.connector
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',     
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': 'stock_analysis'
}

def create_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_stock_data(symbol, start_date, end_date):
    """Fetch stock data for a given stock symbol between specific dates."""
    conn = create_connection()
    query = f"""
        SELECT date, open_price, high_price, low_price, close_price, volume 
        FROM stock_data 
        WHERE symbol = '{symbol}' AND date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY date ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    
    if df.empty:
        print("No data found for the given stock and date range.")
        exit()

    return df


def moving_average_strategy(df, short_window=10, long_window=50, initial_cash=10000):
    """
    Moving Average Crossover Strategy: 
    Buy when short MA crosses above long MA, sell when short MA crosses below long MA.
    """
    df['SMA_Short'] = df['close_price'].rolling(window=short_window).mean()
    df['SMA_Long'] = df['close_price'].rolling(window=long_window).mean()

    df['Signal'] = 0  # 0 = Hold, 1 = Buy, -1 = Sell
    df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] = 1
    df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1

    return execute_trades(df, initial_cash)


def rsi_strategy(df, period=14, overbought=70, oversold=30, initial_cash=10000):
    """
    RSI (Relative Strength Index) Strategy:
    Buy when RSI < oversold (30), Sell when RSI > overbought (70).
    """
    delta = df['close_price'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['Signal'] = 0
    df.loc[df['RSI'] < oversold, 'Signal'] = 1  # Buy
    df.loc[df['RSI'] > overbought, 'Signal'] = -1  # Sell

    return execute_trades(df, initial_cash)


def buy_low_sell_high(df, initial_cash=10000):
    """
    Buy Low, Sell High Strategy:
    Buy at lowest price, sell at highest price in the date range.
    """
    min_price_idx = df['close_price'].idxmin()
    max_price_idx = df['close_price'].idxmax()

    cash = initial_cash
    position = cash / df.loc[min_price_idx, 'close_price']
    cash = position * df.loc[max_price_idx, 'close_price']

    return [f"BUY {position:.2f} shares at {df.loc[min_price_idx, 'close_price']}",
            f"SELL all at {df.loc[max_price_idx, 'close_price']}, final cash = ${cash:.2f}"], cash


def momentum_strategy(df, lookback=3, threshold=1.02, initial_cash=10000):
    """
    Momentum Strategy:
    Buy when price increases for X consecutive days (momentum), sell when it falls.
    """
    df['Momentum'] = df['close_price'] / df['close_price'].shift(lookback)
    df['Signal'] = 0
    df.loc[df['Momentum'] > threshold, 'Signal'] = 1  # Buy
    df.loc[df['Momentum'] < (2 - threshold), 'Signal'] = -1  # Sell

    return execute_trades(df, initial_cash)


### **Execute Trades Based on Strategy**
def execute_trades(df, initial_cash):
    cash = initial_cash
    position = 0
    trade_log = []

    for i in range(1, len(df)):
        if df.iloc[i-1]['Signal'] == 1 and cash > 0:  # Buy condition
            position = cash / df.iloc[i]['close_price']
            cash = 0
            trade_log.append(f"BUY {position:.2f} shares at {df.iloc[i]['close_price']}")

        elif df.iloc[i-1]['Signal'] == -1 and position > 0:  # Sell condition
            cash = position * df.iloc[i]['close_price']
            position = 0
            trade_log.append(f"SELL all at {df.iloc[i]['close_price']}, final cash = ${cash:.2f}")

    final_value = cash + (position * df.iloc[-1]['close_price'])
    return trade_log, final_value


### **Performance Calculation**
def calculate_performance(initial_cash, final_cash):
    roi = ((final_cash - initial_cash) / initial_cash) * 100
    return roi


### **User Input for Trading System**
def main():
    print("Welcome to the Stock Trading Simulator 🚀\n")

    # User inputs
    initial_cash = float(input("Enter your initial investment ($): "))
    stock_symbol = input("Enter the stock symbol to trade (e.g., NVDA): ").upper()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    print("\nAvailable Trading Strategies:")
    print("1) Moving Average Crossover")
    print("2) RSI Strategy")
    print("3) Buy Low, Sell High")
    print("4) Momentum Strategy")

    strategy_choice = input("\nChoose a trading strategy (1-4): ")

    # Fetch stock data
    df = get_stock_data(stock_symbol, start_date, end_date)

    # Apply selected strategy
    if strategy_choice == "1":
        trade_log, final_cash = moving_average_strategy(df, initial_cash=initial_cash)
    elif strategy_choice == "2":
        trade_log, final_cash = rsi_strategy(df, initial_cash=initial_cash)
    elif strategy_choice == "3":
        trade_log, final_cash = buy_low_sell_high(df, initial_cash=initial_cash)
    elif strategy_choice == "4":
        trade_log, final_cash = momentum_strategy(df, initial_cash=initial_cash)
    else:
        print("Invalid choice! Exiting program.")
        return

    # Print trading results
    print("\n===== Trading Log =====")
    print("\n".join(trade_log))
    print("=======================")
    print(f"Final portfolio value: ${final_cash:.2f}")
    roi = calculate_performance(initial_cash, final_cash)
    print(f"Return on Investment (ROI): {roi:.2f}%")
    print("\nThank you for using the Stock Trading Simulator! 📈")


if __name__ == '__main__':
    main()