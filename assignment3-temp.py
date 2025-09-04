###Team 6
### Andrew Sexton, Ella Pan, Steven Alvarado, Alexa Mikeska 

###We are trying to show... 3 different investment vehicles and see if they move independently, together, or perhaps opposite each other

import yfinance as yf  # Import yfinance library for downloading financial data, utilized AI to learn how to import yfinance 

# Define the tickers (symbols) we want to analyze
tickers = ["BTC-USD", "GC=F", "^GSPC", "^VIX"]  
# "BTC-USD" = Bitcoin in US dollars
# "GC=F"    = Gold Futures
# "^GSPC"   = S&P 500 Index
# "^VIX"    = CBOE Volatility Index

# Create a mapping from ticker symbols to readable names
ticker_labels = {
    "BTC-USD": "Bitcoin (USD)",
    "GC=F": "Gold Futures",
    "^GSPC": "S&P 500",
    "^VIX": "CBOE Volatility Index"
}

# Fetch historical daily data from Yahoo Finance
data = yf.download(
    tickers,                # list of tickers
    start="2024-01-01",     # start date
    end="2025-01-01",       # end date (non-inclusive)
    auto_adjust=True        # adjust for splits/dividends (for stocks/ETFs)
)

print(data.head())  

# Extract only the "Close" prices from the full dataset (Open, High, Low, Close, Volume)
close_prices = data["Close"]  
print(close_prices.head())   # Print first 5 rows to check format

# Normalize the close prices for comparison
# Formula: (value - min) / (max - min) → rescales all values between 0 and 1
normalized_close_prices = (close_prices - close_prices.min()) / (close_prices.max() - close_prices.min())
print(normalized_close_prices.head())  # Print first 5 rows of normalized data

# Plot the closing prices
import matplotlib.pyplot as plt
import pandas as pd

plt.figure(figsize=(10, 6))
for ticker in ['BTC-USD', 'GC=F', '^GSPC', '^VIX']:
    # Drop rows with NaN values for the current ticker and reset the index
    ticker_data = normalized_close_prices[ticker].dropna()
    plt.plot(ticker_data.index, ticker_data, label=ticker_labels[ticker]) # use mapped name

plt.title("Bitcoin, Gold, and S&P 500 Performance in 2024-2025 (Normalized)")
plt.xlabel("Date")
plt.legend(["Bitcoin", "Gold", "S&P 500", "CBOE Volatility Index"])
plt.ylabel("Normalized Closing Price (0–1)")
plt.show()

# Calculate correlation matrix
correlation_matrix = normalized_close_prices.corr()
print("Correlation matrix of normalized closing prices:")
print(correlation_matrix)
#Correlation matrix of normalized closing prices:
#Ticker    BTC-USD      GC=F     ^GSPC      ^VIX
#Ticker
#BTC-USD  1.000000  0.651543  0.759932  0.051796
#GC=F     0.651543  1.000000  0.911113  0.450530
#^GSPC    0.759932  0.911113  1.000000  0.249464
#^VIX     0.051796  0.450530  0.249464  1.000000 
# There is strong correlation between Gold and the S&P 500 for the year shown. Some correlation between Bitcoin and the S&P. This would stand to reason that ma
