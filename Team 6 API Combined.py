###Team 6
### Andrew Sexton, Ella Pan, Steven Alvarado, Alexa Mikeska 

#### Question: How does the market respond to percieved risk in the market?
#### Data Examined: S&P 500 - Represents the overall Market
####               Bitcoin - Represents a high risk/high reward asset commonly used as a hedge against inflation
####               Gold - Represents a traditional safe-haven asset
####               VIX - Represents the market's expectation of used to measure market risk and sentiment

### We are trying to show... 3 different investment vehicles alongside the 
### CBOE Volatility Index and see if they move independently, together, or
### perhaps opposite each other

# Import yfinance library for downloading financial data, utilized AI to learn how to import yfinance 
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Define the tickers (symbols) we want to analyze
tickers = ["BTC-USD", "GC=F", "^GSPC", "^VIX"]
# "BTC-USD" = Bitcoin in US dollars
# "GC=F"    = Gold Futures
# "^GSPC"   = S&P 500 Index
# "^VIX"    = CBOE Volatility Index

data = yf.download(
    tickers,
    start="2024-09-01",
    end="2025-09-01")["Close"]

# Normalize the close prices for trendline comparison
# Formula: (value - min) / (max - min) → rescales all values between 0 and 1
normalized = (data - data.min()) / (data.max() - data.min())
print(normalized.head())  # Print first 5 rows of normalized data
print(normalized.isna().sum())
#Clean the data by removing non-trading days including weekends and holidays
#Bitcoin trades 24/7 so it has more data points than the other assets. To align all assets, we drop rows with NaN values.
mormalized=normalized.dropna(inplace=True) 

# Assign specific colors: Bitcoin blue, Gold orange, S&P 500 green, VIX black using colorblind-friendly palette
colors = {
    'BTC-USD': "#377eb8",
    'GC=F': '#ff7f00',    # Now orange instead of gold
    '^GSPC': '#4daf4a',
    '^VIX': 'black'
}
light_grey = '#f2f2f2'

# Creats a 2x2 grid of subplots. While the x is shared, we wanted to show the dates for each subplot.
### GenAI helped with identifying how to create subplots with matplotlib.
fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor=light_grey)
# Title and style function support from matplotlib documentation
fig.suptitle("Market Risk and Asset Behavior: S&P 500, BTC, Gold, VS VIX" , fontsize=16, weight="bold")
fig.text(.5,.01,"Data from Yahoo Finance", ha="center")


# 1. All assets + VIX
axes[0, 0].plot(normalized.index, normalized['BTC-USD'], label='Bitcoin', color=colors['BTC-USD'])
axes[0, 0].plot(normalized.index, normalized['GC=F'], label='Gold', color=colors['GC=F'])
axes[0, 0].plot(normalized.index, normalized['^GSPC'], label='S&P 500', color=colors['^GSPC'])
axes[0, 0].plot(normalized.index, normalized['^VIX'], label='VIX', color=colors['^VIX'], alpha=0.75) 
axes[0, 0].set_title('All Assets + VIX')
axes[0, 0].legend()
axes[0, 0].set_facecolor(light_grey)

# 2. S&P 500 + VIX
axes[0, 1].plot(normalized.index, normalized['^GSPC'], label='S&P 500', color=colors['^GSPC'])
axes[0, 1].plot(normalized.index, normalized['^VIX'], label='VIX', color=colors['^VIX'], alpha=0.75) 
axes[0, 1].set_title('S&P 500 + VIX')
axes[0, 1].legend()
axes[0, 1].set_facecolor(light_grey)

# 3. Gold + VIX
axes[1, 0].plot(normalized.index, normalized['GC=F'], label='Gold', color=colors['GC=F'])
axes[1, 0].plot(normalized.index, normalized['^VIX'], label='VIX',  color=colors['^VIX'], alpha=0.75) 
axes[1, 0].set_title('Gold + VIX')
axes[1, 0].legend()
axes[1, 0].set_facecolor(light_grey)

# 4. Bitcoin + VIX
axes[1, 1].plot(normalized.index, normalized['BTC-USD'], label='Bitcoin', color=colors['BTC-USD'])
axes[1, 1].plot(normalized.index, normalized['^VIX'], label='VIX', color=colors['^VIX'], alpha=0.75)
axes[1, 1].set_title('Bitcoin + VIX')
axes[1, 1].legend()
axes[1, 1].set_facecolor(light_grey)


for ax in axes.flat: # the .flat atribute lets us iterate through each subplot as if in a 1D array to avoid nesting loops
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Price")
    ax.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()

# Calculate correlation matrix
correlation_matrix = normalized.corr()
print("Correlation matrix of normalized closing prices:")
print(correlation_matrix)
#Ticker   BTC-USD     Gold     S&P 500  Volitility Index (VIX)
#BTC-USD  1.000000  0.682213  0.702935 -0.289363
#Gold     0.682213  1.000000  0.300961  0.147123
#S&P500   0.702935  0.300961  1.000000 -0.752331
#VIX     -0.289363  0.147123 -0.752331  1.000000

# Takeaways:
#There is a strong negative correlation between the S&P 500 and the VIX. This is expected as sentiment of fear and uncertainty typically rises when the market falls.
#Bitcoin shows it is strongly correlated with the S&P 500, a moderate correaltion with Gold, and a weak negative correlation with the VIX. This suggests Bitcoin behaves more like a risk asset than a safe-haven asset.
#Gold has a weak positive correlation with the S&P 500 and a very weak positive correlation with the VIX, indicating it does not move strongly with market risk sentiment. 
##However, it has a strong positive correlation with Bitcoin, suggesting some shared market drivers.
# Overall, in 2024-2025, Bitcoin previously seen as a potential safe-haven asset, is showing behavior more aligned with risk assets like stocks rather than traditional safe-havens like Gold.
# Gold is not strongly acting as a safe-haven either, as it is not negatively correlated with the VIX or strongly related to the S&P 500.
# While the VIX is a strong indicator of market risk sentiment, neither Bitcoin nor Gold are moving inversely to it which brings their roles as safe-haven assets into question for this time period.

