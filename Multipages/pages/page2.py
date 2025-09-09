### page 2

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import yfinance as yf
import pandas as pd
import requests # Import requests to fetch ticker data
from datetime import date, timedelta # Import date and timedelta for the date picker

### register the page Dash app
dash.register_page(__name__, path="/page2", name="Comparisons")

### page layout
layout = html.Div([
    html.H1("Stocks vs. Volatility Index (VIX)", style={'textAlign': 'center'}),
    html.P([
        "Comparing normalized performance. S&P 500 included to show general market performance.",
        html.Br(),
        "Add up to two stock tickers below."
    ], style={'textAlign': 'center'}),

### store user-added tickers in memory
    dcc.Store(id='ticker-store', data=[]),  ### Storing an empty list of tickers
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
    
    ### from SimpleDatePickerRange documentation https://dash.plotly.com/dash-core-components/datepickerrange
    html.Div([
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=date(2010, 1, 1), ### only going back to year 2010 for purposes of this app
            max_date_allowed=date.today() - timedelta(days=1), ### Ensure max date is not today since market data might be incomplete or market closed
            initial_visible_month=date(2025, 1, 1),
            start_date=date(2025, 1, 1),
            end_date=date.today() - timedelta(days=1) ### Default to yesterday's date
        )
    ], style={'textAlign': 'center', 'paddingBottom': '10px'}),


    ### div to display feedback messages to the user
    html.Div(id='message-output', style={'textAlign': 'center', 'paddingBottom': '10px', 'color': 'red'}),

    ### div to hold the chart and the matrix side-by-side
    html.Div([
        ### left holds Chart - 66.6% width with a new border
        html.Div(
            dcc.Graph(id='ticker-performance-chart'),
            style={'flex': '2', 'paddingRight': '10px', 'margin': '1px','border': '1px solid black', 'padding': '10px'}
        ),
        ### right holds Correlation Matrix - 33.3% width with a new border
        html.Div(
            id='correlation-matrix',
            style={'flex': '1', 'paddingLeft': '10px', 'margin': '1px', 'border': '1px solid black', 'padding': '10px'}
        )
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'}) # Added alignItems to vertically center
])

### matrix color table
col_table = {
    "str_cor": "#2E8B57",
    "mod_cor": "#3CB371",
    "weak_cor": "#90EE90",
    "no_cor": "#FFFFFF",
    "weak_n_cor": "#FC9A9A",
    "mod_n_cor": "#F95454",
    "str_n_cor": "#FF0000",
}

### create callbacks
@callback(
    Output('ticker-performance-chart', 'figure'), ### updates the chart
    Output('ticker-store', 'data'),  ### updates the stored list of tickers
    Output('message-output', 'children'),  ### updates the message output if there's an error or info
    Output('correlation-matrix', 'children'), ### updates the correlation matrix
    Input('submit-button', 'n_clicks'), 
    Input('clear-button', 'n_clicks'),
    Input('date-picker-range', 'start_date'), # New INPUT for start date
    Input('date-picker-range', 'end_date'),   # New INPUT for end date
    State('ticker-input', 'value'), ### accesses the text input value
    State('ticker-store', 'data') ### accesses the stored list of tickers
)
def update_chart(submit_clicks, clear_clicks, start_date, end_date, new_ticker, stored_tickers): ### submit clicks and clear clicks are not accessed but have to be there or the program breaks,
    triggered_id = dash.ctx.triggered_id
    message = ""
    correlation_component = [] ### Initialize as empty

    ### button clicks
    if triggered_id == 'clear-button':
        stored_tickers = []

    elif triggered_id == 'submit-button' and new_ticker:
        query = new_ticker.strip()
        ticker_to_add = query.upper()  ### default to uppercase version of input

        ### Build and send the API request
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and data.get('quotes'):
                quotes = [q for q in data['quotes'] if '.' not in q.get('symbol', '')]
                us_quotes = [q for q in quotes if q.get('exchange') in ('NMS', 'NYQ')]
            if us_quotes:
                selected_ticker = us_quotes[0].get('symbol')
            elif quotes:
                selected_ticker = quotes[0].get('symbol')
            if selected_ticker:
                ticker_to_add = selected_ticker
        ### end of API request
        if not ticker_to_add: ### error message if no ticker found
            message = "Please enter a valid company name or ticker."
        elif ticker_to_add in stored_tickers:  ### error message if ticker already added
            message = f"{ticker_to_add} is already on the chart."
        elif len(stored_tickers) >= 2: ### error message if 2 tickers already typed in
            message = "You can only add up to two custom tickers."
        else: ### when a ticker is valid, this verifies there is valid data for the ticker
            check_data = yf.download(ticker_to_add, period="5d", progress=False)
            if check_data.empty:
                message = f"Could not find valid data for '{query}'. Please try again."
            else:
                stored_tickers.append(ticker_to_add)

    ### fetch data and process for chart and matrix
    ### this section runs if a button is clicked OR if a date is changed
    base_tickers = ["^GSPC", "^VIX"]
    all_tickers = base_tickers + stored_tickers

    if not start_date or not end_date:
        message = "Please select a valid start and end date."
        ### prevents app from crashing if dates are cleared
        return dash.no_update, dash.no_update, message, dash.no_update

    ### Grab the non-normalized closing prices for correlation
    close_prices = yf.download(
        all_tickers, start=start_date, end=end_date, auto_adjust=True, progress=False
    )['Close']
    close_prices.dropna(axis=1, how='all', inplace=True)

    if isinstance(close_prices, pd.Series):
        close_prices = close_prices.to_frame(name=all_tickers[0])

    if close_prices.empty:
        if not stored_tickers and triggered_id == 'submit-button':
             message = f"Could not find data for ticker: {new_ticker}"
        # Create an empty figure to avoid errors
        fig = px.line(title="No data available for the selected range/tickers.")
        fig.update_layout(title_font_size=20, title_font_weight='bold', title_x=0.5)
        return fig, stored_tickers, message, []

    ### correlation matrix and legend
    ### Helper function to determine cell color based on correlation value using
    def get_cell_style(value):
        textcolor = 'black'
        if value >= 0.7:
            bgcolor = col_table["str_cor"]  # Strong
            textcolor = 'white'
        elif value >= 0.5:
            bgcolor = col_table["mod_cor"]  # Moderate
            textcolor = 'white'
        elif value >= 0.3:
            bgcolor = col_table["weak_cor"]  # Weak
            textcolor = 'black'
        elif value > -0.3:
            bgcolor = col_table["no_cor"]  # Little/No
            textcolor = 'black'
        elif value > -0.5:
            bgcolor = col_table["weak_n_cor"]  # Weak Negative
            textcolor = 'black'
        elif value > -0.7:
            bgcolor = col_table["mod_n_cor"]  # Moderate Negative
            textcolor = 'black'
        else:  # value <= -0.7
            bgcolor = col_table["str_n_cor"]  # Strong Negative
            textcolor = 'white'
        return {'textAlign': 'center', 'backgroundColor': bgcolor, 'color': textcolor, 'padding': '5px'}

    ### create matrix table
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

    ### create legend table for correlation colors using dictionary
    legend_data = {
        "Strong: 0.7 to 1.0": col_table["str_cor"],
        "Moderate: 0.5 to 0.7": col_table["mod_cor"],
        "Weak: 0.3 to 0.5": col_table["weak_cor"],
        "Little to No: -0.3 to 0.3": col_table["no_cor"],
        "Weak Negative: -0.5 to -0.3": col_table["weak_n_cor"],
        "Moderate Negative: -0.7 to -0.5": col_table["mod_n_cor"],
        "Strong Negative: -1.0 to -0.7": col_table["str_n_cor"],
    }

    legend_rows = []
    for text, color in legend_data.items():
        legend_rows.append(html.Tr([
            html.Td(html.Div(style={'width': '20px', 'height': '20px', 'backgroundColor': color, 'border': '1px solid black'})),
            html.Td(text, style={'paddingLeft': '10px'})
        ]))
        
    legend_table = html.Table(legend_rows, style={'marginTop': '20px', 'width': '100%'})

    ### combine matrix and legend into one component
    correlation_component = html.Div([matrix_component, legend_table])

    ### normalize prices and create line chart
    normalized_prices = (close_prices - close_prices.min()) / (close_prices.max() - close_prices.min())
    fig = px.line(
        normalized_prices,
        title="Asset Performance (Normalized)",
        labels={"Date": "Date", "value": "Normalized Closing Price (0–1)", "variable": "Ticker"}
    )
    ### standardize chart title font and center it
    fig.update_layout(title_font_size=20, title_font_weight='bold', title_x=0.5)


    ### return all updated components
    return fig, stored_tickers, message, correlation_component

