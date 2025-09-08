# page3

import dash
from dash import dcc, html
import plotly.express as px
import yfinance as yf

# Register the page in your Dash app
dash.register_page(__name__, path="/page3", name="Page 3")

# --- 1. Data Fetching and Processing (from your original script) ---
# Define the tickers we want to analyze
tickers = ["BTC-USD", "GC=F", "^GSPC", "^VIX"]

# Fetch historical daily data from Yahoo Finance
data = yf.download(
    tickers,
    start="2024-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# Extract only the "Close" prices
close_prices = data["Close"]

# Normalize the close prices to a 0-1 scale for comparison
normalized_close_prices = (close_prices - close_prices.min()) / (close_prices.max() - close_prices.min())

# Create a mapping from ticker symbols to readable names for the chart legend
ticker_labels = {
    "BTC-USD": "Bitcoin (USD)",
    "GC=F": "Gold Futures",
    "^GSPC": "S&P 500",
    "^VIX": "CBOE Volatility Index"
}
# Rename the columns in the DataFrame for a cleaner legend
normalized_close_prices = normalized_close_prices.rename(columns=ticker_labels)


# --- 2. Create an Interactive Plotly Chart ---
# Instead of matplotlib, we use plotly.express to create a figure object
fig = px.line(
    normalized_close_prices,
    title="Bitcoin, Gold, and S&P 500 Performance in 2024-2025 (Normalized)",
    labels={
        "Date": "Date",
        "value": "Normalized Closing Price (0–1)",
        "variable": "Asset"  # This label is for the legend title
    }
)

# --- 3. Define the Page Layout ---
# The layout now includes a dcc.Graph component that displays our figure
layout = html.Div([
    html.H1("Financial Asset Correlation", style={'textAlign': 'center'}),
    html.P("Comparing the normalized performance of four major assets.", style={'textAlign': 'center'}),

    dcc.Graph(
        id='asset-performance-chart',
        figure=fig  # The Plotly figure is passed to the 'figure' property
    )
])
