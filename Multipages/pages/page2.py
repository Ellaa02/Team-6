# page3

import dash
from dash import dcc, html, callback, Input, Output, State
import plotly.express as px
import yfinance as yf
import pandas as pd

# Register the page in your Dash app
dash.register_page(__name__, path="/page2", name="Page 2")

# --- Define the Page Layout ---
layout = html.Div([
    # Store user-added tickers in the browser's memory
    dcc.Store(id='ticker-store', data=[]),

    html.H1("Stocks vs. Volatility Index (VIX)", style={'textAlign': 'center'}),
    html.P("Comparing normalized performance. Add your own stock tickers below.", style={'textAlign': 'center'}),

    # Div for user inputs
    html.Div([
        dcc.Input(
            id='ticker-input',
            type='text',
            placeholder='Enter a stock ticker (e.g., AAPL)',
            style={'marginRight': '10px'}
        ),
        html.Button('Add Ticker', id='submit-button', n_clicks=0)
    ], style={'textAlign': 'center', 'padding': '20px'}),

    # The graph component that will be updated by the callback
    dcc.Graph(id='asset-performance-chart')
])

# --- Create the Callback ---
# This function connects the inputs/button to the graph and storage
@callback(
    Output('asset-performance-chart', 'figure'),
    Output('ticker-store', 'data'),
    Input('submit-button', 'n_clicks'),
    State('ticker-input', 'value'),
    State('ticker-store', 'data')
)
def update_chart(n_clicks, new_ticker, stored_tickers):
    # This function runs on page load and whenever the button is clicked

    # 1. Update the list of stored tickers when the button is clicked
    # 'dash.ctx.triggered_id' checks if the button was the component that fired the callback
    if dash.ctx.triggered_id == 'submit-button' and new_ticker:
        ticker_to_add = new_ticker.strip().upper()
        # Add the new ticker only if it's not already in the list
        if ticker_to_add and ticker_to_add not in stored_tickers:
            stored_tickers.append(ticker_to_add)

    # 2. Define the complete list of tickers to plot
    base_tickers = ["^GSPC", "^VIX"]
    all_tickers = base_tickers + stored_tickers

    # 3. Fetch data for all tickers
    if not all_tickers: # Return empty fig if no tickers
        return px.line(title="Enter a ticker to begin"), stored_tickers

    data = yf.download(
        all_tickers,
        start="2024-01-01",
        end="2025-01-01",
        auto_adjust=True,
        progress=False # Hides yfinance download status text
    )['Close']

    # If only one ticker is fetched, data is a Series, not a DataFrame. Convert it.
    if isinstance(data, pd.Series):
        data = data.to_frame(name=all_tickers[0])

    # 4. Normalize and create the chart
    # Drop columns that failed to download (all NaN)
    data.dropna(axis=1, how='all', inplace=True)
    if data.empty:
        return px.line(title=f"Could not find data for ticker: {new_ticker}"), stored_tickers

    normalized_prices = (data - data.min()) / (data.max() - data.min())

    fig = px.line(
        normalized_prices,
        title="Asset Performance (Normalized)",
        labels={
            "Date": "Date",
            "value": "Normalized Closing Price (0–1)",
            "variable": "Ticker"
        }
    )

    # 5. Return the updated figure and the new list of tickers for storage
    return fig, stored_tickers
