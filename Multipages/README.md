# Project overview (problem, audience, value)

## Background
This project was developed as an extension of our previous group project, which was a chart that displayed different ticker symbols that represented:  
- **Cryptocurrency** (Bitcoin in US Dollars)  
- **Tangible assets** (Gold)  
- **Stocks** (S&P 500)  
- **Market volatility** (CBOE Volatility Index)  

We then had a simple correlation matrix that printed in the terminal. The purpose of this was to see if there was any sort of correlation between the movement of each of those individual ticker symbols.  

This project has a primary purpose of allowing people to do some basic research on a stock of their choice and then generate a chart and correlation matrix on the fly. The Volatility Index and S&P 500 are prefilled but the user is able to enter as many as two stocks of their choice.  

---

## Problem
Individual investors often struggle to interpret stock movements. Without context, a single stock chart can be misleading, leading to poor decisions.  

## Audience
Our platform is designed for investors who want a clearer picture of how their chosen stock behaves relative to market volatility.  

## Value
By allowing users to compare their stock of choice against the **VIX** (a volatility index that represents the market’s expectation of volatility based on S&P 500 index options), our platform provides essential context for decision-making. The correlation matrix and the comparison graph empower users to distinguish company performance from market-wide trends, helping them make better investment choices.  

---

# How to run (local + deploy notes)

1. Download zip file and extract all files to your local directory.  
2. Open `app.py`.  
3. Ensure the following are installed (they can be installed using the pip command):  
   - `dash`  
   - `dash_bootstrap_components`  
   - `plotly.express`  
   - `yfinance`  
   - `pandas`  
   - `requests`  
   - `datetime`  
4. Run `app.py`.  
5. Once running the user can access the following pages:  
   - **Home:** Brief description of the application and its intended purpose.  
   - **Research:** Input a stock either by name or ticker symbol (e.g., “Apple” or “AAPL”). The output shows its closing price over the last year and a background summary.  
   - **Comparisons:** Input up to two (2) stocks to compare to the S&P 500 and VIX tickers over a user-selected time period. The result will be a graph and correlation table.  
   - **About us:** Information about the development team.  
   - **Note:** “Stock” is used throughout, but Yahoo Finance ticker symbols are acceptable (e.g. Bitcoin USD Price listed as `BTC-USD`).  

---

# Data sources & data dictionary
### yfinance 0.2.65 unofficial API was used.  
Details can be found at this URL → [https://pypi.org/project/yfinance/](https://pypi.org/project/yfinance/)  
