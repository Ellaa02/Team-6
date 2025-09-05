###Team 6
### Andrew Sexton, Ella Pan, Steven Alvarado, Alexa Mikeska 

#### Question: How does the market respond to perceived risk in the market?
#### Data Examined: S&P 500 - Chosen to represent the overall U.S. Stock Market
####               Bitcoin - Chosen to represent cryptocurrency
####               Gold - Chosen to represent tangible assets
####               VIX - Chosen to represent market volatility and investor sentiment

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
axes[0, 0].set_title('All Assets vs. Volatility Index')
axes[0, 0].legend()
axes[0, 0].set_facecolor(light_grey)

# 2. S&P 500 + VIX
axes[0, 1].plot(normalized.index, normalized['^GSPC'], label='S&P 500', color=colors['^GSPC'])
axes[0, 1].plot(normalized.index, normalized['^VIX'], label='VIX', color=colors['^VIX'], alpha=0.75) 
axes[0, 1].set_title('S&P 500 vs. Volatility Index')
axes[0, 1].legend()
axes[0, 1].set_facecolor(light_grey)

# 3. Gold + VIX
axes[1, 0].plot(normalized.index, normalized['GC=F'], label='Gold', color=colors['GC=F'])
axes[1, 0].plot(normalized.index, normalized['^VIX'], label='VIX',  color=colors['^VIX'], alpha=0.75) 
axes[1, 0].set_title('Gold vs. Volatility Index')
axes[1, 0].legend()
axes[1, 0].set_facecolor(light_grey)

# 4. Bitcoin + VIX
axes[1, 1].plot(normalized.index, normalized['BTC-USD'], label='Bitcoin', color=colors['BTC-USD'])
axes[1, 1].plot(normalized.index, normalized['^VIX'], label='VIX', color=colors['^VIX'], alpha=0.75)
axes[1, 1].set_title('Bitcoin vs. Volatility Index')
axes[1, 1].legend()
axes[1, 1].set_facecolor(light_grey)


for ax in axes.flat: # the .flat atribute lets us iterate through each subplot as if in a 1D array to avoid nesting loops
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Values")
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
#  S&P 500 shows a strong to very strong negative correlation with the CBOE Volatility Index. This is expected as
#  the sentiment of fear and uncertainty typically rises when the market falls.  Each of these symbols should
#  almost always move in opposite directions by definition of what each represents. 

#  Bitcoin shows it is strongly correlated with the S&P 500, a moderate correlation with Gold,
#  and a weak negative correlation with the VIX. This suggests Bitcoin behaves more like a risk asset than a
#  safe-haven asset.

#  Gold has a weak positive correlation with the S&P 500 and a very weak positive correlation
#  with the VIX, indicating it does not move strongly with market risk sentiment. 
#  However, it has a strong positive correlation with Bitcoin, suggesting some shared market drivers.
 
#  Overall, in 2024-2025, Bitcoin, previously seen as a potential safe-haven asset by some but not others, is showing
#  behavior more aligned with traditional investments like stocks, perhaps indicating growing trust among investors
#  in this particular cryptocurrency.

#  Gold, as a safe-haven asset, has shown typical fluctuations, especially during times of higher volatility, but
#  it has continued an overall steady increase in price over the time period shown. This shows that while market
#  volatility rises and falls routinely, there is a general concern about the instability of global markets
#  that is driving investors to tangible assets like gold.
