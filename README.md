# DSCI-560-Lab3

Fetch.py Instruction
1. After installing all necessary libraries, follow the sql_before_fetch.txt. Type those in the command line and SQL interface to create the database and tables. 
2. Run the fetch.py file. You'll be prompted to create / reuse a portfolio and add stocks to the portfolio.
3. For example, we can create 2 portfolios: Tech Giants and Pharma Picks. They will each have a unique id.
4. For each portfolio, we add in corresponding stock symbols. eg. For Tech Giants, we can add `AAPL`, `GOOGL`, `MSFT`. For Pharma Picks, we can add `PFE`, `JNJ`. Use comma to seperate the symbols. Note if the symbol is not valid, you'll see an "invalid stock name" error.
5. Then you'll be prompted to enter start and end date. Use `2020-01-01` syntax.
6. Then data for those symbols within that timeframe will be fetched.

metric.py Instruction
1. Type in the context in sql command.txt to create a table for data's metrics.
2. Run the metric.py and type in the symbol of the stock that already in your portfolio to get the metrics of it.
3. For instance, if you already have `AAPL` and `TSLA` in your portfolio, you can type in them to get the metrics.
4. The metrics including daily return, cumulative_return, simple moving average in 10 days, and volatility of the daily return in 20 days.
5. If there is no such stock in your portfolio, then it will return error message.
