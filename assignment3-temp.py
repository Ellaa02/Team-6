###Team 6
### Andrew Sexton, Ella Pan, Steven Alvarado, Alexa Mikeska 

###We are trying to show... 3 differnet investment vehicles and see if they move independently, together, or perhaps opposite each other

import yfinance as yf

# Define tickers
tickers = ["BTC-USD", "GC=F", "^GSPC", "^VIX"]   # <-- BTC-USD is Bitcoin in US Dollars, GC=F is Gold Futures, ^GSPC is the S&P 500 Index, ^VIX is the CBOE Volatility Index

# Download historical data (last year, daily)
data = yf.download(tickers, start="2024-01-01", end="2025-01-01")

# Show the first few rows
print(data.head())

# Example: closing prices only
close_prices = data["Close"]
print(close_prices.head())

# normalize the close prices
normalized_close_prices = (close_prices - close_prices.min()) / (close_prices.max() - close_prices.min())
print(normalized_close_prices.head())

# Plot the closing prices
import matplotlib.pyplot as plt
import pandas as pd

plt.figure(figsize=(10, 6))
for ticker in ['BTC-USD', 'GC=F', '^GSPC', '^VIX']:
    # Drop rows with NaN values for the current ticker and reset the index
    ticker_data = normalized_close_prices[ticker].dropna()
    plt.plot(ticker_data.index, ticker_data, label=ticker)

plt.title("Normalized Closing Price Over Time")
plt.xlabel("Date")
plt.ylabel("Normalized Price")
plt.legend(["Bitcoin", "Gold", "S&P 500"])
plt.show()

# Calculate correlation matrix
correlation_matrix = normalized_close_prices.corr()
print("Correlation matrix of normalized closing prices:")
print(correlation_matrix)

