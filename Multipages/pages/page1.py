# Page 1
 
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

dash.register_page(__name__, path="/page1", name="Page 1")

layout = html.Div([
    html.H2("Stock Lookup"),
    html.Div([
        dcc.Input(
            id='lookup-input',
            type='text',
            placeholder='Enter a ticker (e.g., AAPL)',
            debounce=True,  # allows pressing Enter to trigger without a button
            style={'width': '240px', 'marginRight': '8px'}
        ),
        html.Button('Show', id='lookup-button', n_clicks=0)
    ], style={'marginBottom': '12px'}),

    html.Div(id='lookup-meta', style={'margin': '8px 0', 'fontSize': '14px'}),
    dcc.Graph(id='lookup-figure')
])

@callback(
    Output('lookup-figure', 'figure'),
    Output('lookup-meta', 'children'),
    Input('lookup-button', 'n_clicks'),
    State('lookup-input', 'value')
)
def show_single_ticker(n_clicks, ticker):
    if not ticker:
        return px.line(title="Enter a ticker to begin"), ""

    t = ticker.strip().upper()
    end = datetime.today()
    start = end - timedelta(days=365)

    try:
        df = yf.download(t, start=start, end=end, auto_adjust=True, progress=False)
        if df.empty:
            return px.line(title=f"No data found for {t}"), f"Could not fetch data for: {t}"

        # Use Adj Close if possible
        price = df['Adj Close'] if 'Adj Close' in df.columns else df['Close']

        # Normalize to 100 at start
        norm = (price / price.dropna().iloc[0]) * 100
        fig = px.line(norm, title=f"{t} — Normalized to 100 (Past 1Y)",
                      labels={"value": "Index (Start=100)", "index": "Date"})
        fig.update_layout(margin=dict(l=30, r=10, t=60, b=40))

        # Small info block
        info = []
        try:
            tk = yf.Ticker(t)
            long_name = tk.info.get("longName") or tk.info.get("shortName") or t
            currency = tk.info.get("currency") or ""
            sector = tk.info.get("sector")
            exchange = tk.info.get("exchange") or tk.info.get("fullExchangeName")
            info.append(f"Name: {long_name}")
            if sector: info.append(f"Sector: {sector}")
            if exchange: info.append(f"Exchange: {exchange}")
            info.append(f"Currency: {currency}")
        except Exception:
            info.append(f"Ticker: {t}")

        return fig, " | ".join(info)

    except Exception as e:
        return px.line(title=f"Error fetching {t}"), f"Error: {e}"