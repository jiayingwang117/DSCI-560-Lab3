# DSCI-560-Lab3

## Fetch.py Instruction
1. After installing all necessary libraries, follow the sql_before_fetch.txt. Type those in the command line and SQL interface to create the database and tables. 
2. Run the fetch.py file. You'll be prompted to create / reuse a portfolio and add / remove stocks from the portfolio.
3. For example, we can create 2 portfolios: Tech Giants and Pharma Picks. They will each have a unique id and a creation date.
4. For each portfolio, we add in corresponding stock symbols. eg. For Tech Giants, we can add `AAPL`, `GOOGL`, `MSFT`. For Pharma Picks, we can add `PFE`, `JNJ`. Use comma to seperate the symbols. Note if the symbol is not valid, you'll see an "invalid stock name" error.
5. Then you'll be prompted to enter start and end date. Use `2020-01-01` syntax.
6. Then data for those symbols within that timeframe will be fetched.

## Metric.py Instruction
1. Type in the context in sql command.txt to create a table for data's metrics.
2. Run the metric.py and type in the symbol of the stock that already in your portfolio to get the metrics of it.
3. For instance, if you already have `AAPL` and `TSLA` in your portfolio, you can type in them to get the metrics.
4. The metrics including daily return, cumulative_return, simple moving average in 10 days, and volatility of the daily return in 20 days.
5. If there is no such stock in your portfolio, then it will return error message.

## Trading.py Instruction

- Implements automated trading strategies where users input their initial capital, stock symbol, date range, and strategy to simulate trades and calculate final portfolio value

### Example Usage

**User Input**
```
Welcome to the Stock Trading Simulator 🚀
Enter your initial investment ($): 10000
Enter the stock symbol to trade (e.g., NVDA): NVDA
Enter start date (YYYY-MM-DD): 2024-12-01
Enter end date (YYYY-MM-DD): 2024-12-31
Choose a trading strategy (1-4): 1
```
**Trading Output**
```
===== Trading Log =====
BUY 71.43 shares at 140.00
SELL all at 155.00, final cash = $11071.43
=======================
Final portfolio value: $11071.43
Return on Investment (ROI): 10.71%
```

