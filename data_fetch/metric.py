from fetch import create_connection  

import pandas as pd
import numpy as np
import datetime

def fetch_stock_data(symbol):
    """
    Read all data for the given symbol from the stock_data table.
    Expected columns: symbol, date, open_price, high_price, low_price, close_price, volume.
    Data is ordered by date.
    """
    conn = create_connection()
    query = """
        SELECT symbol, date, open_price, high_price, low_price, close_price, volume
        FROM stock_data
        WHERE symbol = %s
        ORDER BY date
    """
    df = pd.read_sql(query, conn, params=(symbol,))
    conn.close()
    return df

def handle_missing_values(df):
    """
    Handle missing values:
      - Sort the data by date,
      - Use forward fill, then backward fill,
      - Finally, fill remaining gaps using linear interpolation.
    """
    df = df.sort_values(by='date').reset_index(drop=True)
    df.fillna(method='ffill', inplace=True)
    return df

def transform_data(df):
    """
    Convert the 'date' column to datetime type and set it as index for time series calculations.
    """
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

def compute_daily_metrics(df):
    """
    Compute daily metrics:
      - daily_return: daily percentage change of closing price.
      - cumulative_return: cumulative return (starting with 1).
      - SMA_10: 10-day simple moving average of closing price.
      - volatility_20: 20-day standard deviation of daily returns.
    """
    # Calculate daily return
    df['daily_return'] = df['close_price'].pct_change()
    # Calculate cumulative return (starting at 1)
    df['cumulative_return'] = (1 + df['daily_return']).cumprod()
    # Calculate 10-day simple moving average
    df['SMA_10'] = df['close_price'].rolling(window=10).mean()
    # Calculate 20-day volatility (standard deviation of daily returns)
    df['volatility_20'] = df['daily_return'].rolling(window=20).std()
    return df

def store_daily_metrics(df, symbol):
    """
    Store the calculated daily metrics into the daily_metrics table using an UPSERT (ON DUPLICATE KEY UPDATE) query.
    Any NaN values in the DataFrame are converted to None.
    """
    conn = create_connection()
    cursor = conn.cursor()
    insert_sql = """
       INSERT INTO daily_metrics
       (symbol, date, daily_return, cumulative_return, SMA_10, volatility_20)
       VALUES (%s, %s, %s, %s, %s, %s)
       ON DUPLICATE KEY UPDATE
          daily_return = VALUES(daily_return),
          cumulative_return = VALUES(cumulative_return),
          SMA_10 = VALUES(SMA_10),
          volatility_20 = VALUES(volatility_20)
    """
    count = 0
    for date, row in df.iterrows():
        data_tuple = (
            symbol,
            date.date(),  # Only store the date part
            row.get('daily_return'),
            row.get('cumulative_return'),
            row.get('SMA_10'),
            row.get('volatility_20')
        )
        # Convert NaN values to None so that MySQL gets NULL values
        data_tuple = tuple(None if pd.isna(x) else x for x in data_tuple)
        try:
            cursor.execute(insert_sql, data_tuple)
            count += 1
        except Exception as e:
            print(f"Error inserting data for {symbol} on {date.date()}: {e}")
    conn.commit()
    print(f"Successfully stored {count} daily metric rows for {symbol}.")
    cursor.close()
    conn.close()

def main():
    symbol = input("Enter the stock symbol for daily metrics calculation (e.g., AAPL): ").strip().upper()
    print(f"Fetching historical data for {symbol} from the database...")
    df = fetch_stock_data(symbol)
    if df.empty:
        print(f"No historical data available for {symbol}. Please ensure data has been collected.")
        return
    print("Preview of raw data:")
    print(df.head())
    
    # Process missing values and transform the date column
    df = handle_missing_values(df)
    df = transform_data(df)
    
    # Compute daily metrics
    df = compute_daily_metrics(df)
    
    print("\nPreview of computed daily metrics:")
    print(df[['daily_return', 'cumulative_return', 'SMA_10', 'volatility_20']].head(15))
    
    # Store results into the daily_metrics table
    store_daily_metrics(df, symbol)

if __name__ == "__main__":
    main()
