# page2

import dash
from dash import dcc, html, callback, Input, Output, State
import plotly.express as px
import yfinance as yf
import pandas as pd
import requests # Import the requests library for API calls
from datetime import date, timedelta # Import date and timedelta for the date picker

# Register the page in your Dash app
dash.register_page(__name__, path="/page2", name="Page 2")

# --- Define the Page Layout ---
layout = html.Div([
    # Store user-added tickers in the browser's memory
    dcc.Store(id='ticker-store', data=[]),

    html.H1("Stocks vs. Volatility Index (VIX)", style={'textAlign': 'center'}),
    html.P([
        "Comparing normalized performance. S&P 500 included to show general market performance.",
        html.Br(),
        "Add up to two stock tickers below."
    ], style={'textAlign': 'center'}),

    # Div for user inputs
    html.Div([
        dcc.Input(
            id='ticker-input',
            type='text',
            placeholder='Enter company name or ticker (e.g., Apple)',
            style={'marginRight': '10px'}
        ),
        html.Button('Add Ticker', id='submit-button', n_clicks=0, style={'marginRight': '10px'}),
        html.Button('Clear', id='clear-button', n_clicks=0)
    ], style={'textAlign': 'center', 'padding': '10px'}),
    
    # NEW Div for the Date Picker
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=date(2015, 1, 1),
            max_date_allowed=date.today(),
            initial_visible_month=date(2024, 1, 1),
            start_date=date(2024, 1, 1),
            end_date=date.today() - timedelta(days=1)
        )
    ], style={'textAlign': 'center', 'paddingBottom': '10px'}),


    # Div to display feedback messages to the user
    html.Div(id='message-output', style={'textAlign': 'center', 'paddingBottom': '10px', 'color': 'red'}),

    # New parent Div to hold the chart and the matrix side-by-side
    html.Div([
        # Left side: Chart (75% width) with a new border
        html.Div(
            dcc.Graph(id='asset-performance-chart'),
            style={'flex': '3', 'paddingRight': '10px', 'border': '1px solid black', 'padding': '10px'}
        ),
        # Right side: Correlation Matrix (25% width) with a new border
        html.Div(
            id='correlation-matrix',
            style={'flex': '1', 'paddingLeft': '10px', 'border': '1px solid black', 'padding': '10px'}
        )
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'}) # Added alignItems to vertically center
])

# --- Create the Callback ---
@callback(
    Output('asset-performance-chart', 'figure'),
    Output('ticker-store', 'data'),
    Output('message-output', 'children'),
    Output('correlation-matrix', 'children'), # New output for the matrix
    Input('submit-button', 'n_clicks'),
    Input('clear-button', 'n_clicks'),
    Input('date-picker-range', 'start_date'), # New INPUT for start date
    Input('date-picker-range', 'end_date'),   # New INPUT for end date
    State('ticker-input', 'value'),
    State('ticker-store', 'data')
)
def update_chart(submit_clicks, clear_clicks, start_date, end_date, new_ticker, stored_tickers): # Added dates to function signature
    triggered_id = dash.ctx.triggered_id
    message = ""
    correlation_component = [] # Initialize as empty

    # --- 1. Handle Button Clicks ---
    if triggered_id == 'clear-button':
        stored_tickers = []

    elif triggered_id == 'submit-button' and new_ticker:
        query = new_ticker.strip()
        ticker_to_add = None

        try:
            url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data.get('quotes'):
                quotes = [q for q in data['quotes'] if '.' not in q.get('symbol', '')]
                us_quotes = [q for q in quotes if q.get('exchange') in ('NMS', 'NYQ')]
                ticker_to_add = us_quotes[0]['symbol'] if us_quotes else quotes[0]['symbol'] if quotes else None
        except Exception:
            ticker_to_add = query.upper()

        if not ticker_to_add:
            message = "Please enter a valid company name or ticker."
        elif ticker_to_add in stored_tickers:
            message = f"{ticker_to_add} is already on the chart."
        elif len(stored_tickers) >= 2:
            message = "You can only add up to two custom tickers."
        else:
            check_data = yf.download(ticker_to_add, period="5d", progress=False)
            if check_data.empty:
                message = f"Could not find valid data for '{query}'. Please try again."
            else:
                stored_tickers.append(ticker_to_add)

    # --- 2. Data Fetching and Processing ---
    # This section now runs if a button is clicked OR if a date is changed.
    base_tickers = ["^GSPC", "^VIX"]
    all_tickers = base_tickers + stored_tickers

    if not start_date or not end_date:
        message = "Please select a valid start and end date."
        # Prevents app from crashing if dates are cleared
        return dash.no_update, dash.no_update, message, dash.no_update
        
    # Use the non-normalized closing prices for correlation
    close_prices = yf.download(
        all_tickers, start=start_date, end=end_date, auto_adjust=True, progress=False
    )['Close']

    if isinstance(close_prices, pd.Series):
        close_prices = close_prices.to_frame(name=all_tickers[0])

    close_prices.dropna(axis=1, how='all', inplace=True)
    if close_prices.empty:
        if not stored_tickers and triggered_id == 'submit-button':
             message = f"Could not find data for ticker: {new_ticker}"
        # Create an empty figure to avoid errors
        fig = px.line(title="No data available for the selected range/tickers.")
        fig.update_layout(title_font_size=20, title_font_weight='bold', title_x=0.5)
        return fig, stored_tickers, message, []

    # --- 3. Create Correlation Matrix and Legend ---
    if close_prices.shape[1] > 1: # Can only correlate if there's more than one ticker
        
        # Helper function to determine cell color based on correlation value
        def get_cell_style(value):
            textcolor = 'black'
            if value >= 0.7:
                bgcolor = "#2E8B57"  # Strong
                textcolor = 'white'
            elif value >= 0.5:
                bgcolor = "#3CB371"  # Moderate
                textcolor = 'white'
            elif value >= 0.3:
                bgcolor = "#90EE90"  # Weak
            elif value > -0.3:
                bgcolor = "#FFFFFF"  # Little/No
            elif value > -0.5:
                bgcolor = "#FC9A9A"  # Weak Negative
            elif value > -0.7:
                bgcolor = "#F95454"  # Moderate Negative
            else:  # value <= -0.7
                bgcolor = "#FF0000"  # Strong Negative
                textcolor = 'white'
            return {'textAlign': 'center', 'backgroundColor': bgcolor, 'color': textcolor, 'padding': '5px'}

        # Create Matrix
        corr_matrix = close_prices.corr().round(2)
        header = [html.Th('')] + [html.Th(col, style={'padding': '5px'}) for col in corr_matrix.columns]
        rows = [
            html.Tr([html.Th(index, style={'padding': '5px'})] + 
                    [html.Td(corr_matrix.loc[index, col], style=get_cell_style(corr_matrix.loc[index, col])) 
                     for col in corr_matrix.columns])
            for index in corr_matrix.index
        ]
        matrix_component = html.Div([
            html.H3("Correlation Matrix", style={'textAlign': 'center', 'fontSize': 20, 'fontWeight': 'bold'}),
            html.Table(
                [html.Thead(html.Tr(header)), html.Tbody(rows)],
                style={'width': '100%', 'borderCollapse': 'collapse'}
            )
        ])
        
        # Create Legend Table with negative values
        legend_data = {
            "Strong: 0.7 to 1.0": "#2E8B57",
            "Moderate: 0.5 to 0.7": "#3CB371",
            "Weak: 0.3 to 0.5": "#90EE90",
            "Little to No: -0.3 to 0.3": "#FFFFFF",
            "Weak Negative: -0.5 to -0.3": "#FC9A9A",
            "Moderate Negative: -0.7 to -0.5": "#F95454",
            "Strong Negative: -1.0 to -0.7": "#FF0000",
        }


        legend_rows = []
        for text, color in legend_data.items():
            legend_rows.append(html.Tr([
                html.Td(html.Div(style={'width': '20px', 'height': '20px', 'backgroundColor': color, 'border': '1px solid black'})),
                html.Td(text, style={'paddingLeft': '10px'})
            ]))
        
        legend_table = html.Table(legend_rows, style={'marginTop': '20px', 'width': '100%'})

        # Combine matrix and legend into a single component
        correlation_component = html.Div([matrix_component, legend_table])


    # --- 4. Normalize Prices and Create Chart ---
    normalized_prices = (close_prices - close_prices.min()) / (close_prices.max() - close_prices.min())
    fig = px.line(
        normalized_prices,
        title="Asset Performance (Normalized)",
        labels={"Date": "Date", "value": "Normalized Closing Price (0–1)", "variable": "Ticker"}
    )
    # Standardize chart title font and center it
    fig.update_layout(title_font_size=20, title_font_weight='bold', title_x=0.5)


    # --- 5. Return all updated components ---
    return fig, stored_tickers, message, correlation_component

