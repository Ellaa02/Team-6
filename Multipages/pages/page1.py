# pages/page1.py — Single-ticker lookup (company name or ticker)#

import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta

dash.register_page(__name__, path="/page1", name="Page 1")

def resolve_to_symbol(query: str) -> str | None:
    """
    Resolve a free-text query (company name or ticker) to a Yahoo Finance symbol.
    - Prefer US exchanges (NASDAQ=NMS, NYSE=NYQ).
    - Fallback to first quote if nothing on those exchanges.
    - Returns uppercase symbol or None.
    """
    q = (query or "").strip()
    if not q:
        return None
    try:
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={q}"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=6)
        resp.raise_for_status()
        data = resp.json()
        quotes = data.get("quotes", [])
        if not quotes:
            return q.upper()  # last-resort: treat input as a ticker
        # Filter out weird non-plain symbols like BRK.B (“.” can cause trouble)
        quotes = [qq for qq in quotes if "." not in (qq.get("symbol") or "")]
        us_quotes = [qq for qq in quotes if qq.get("exchange") in ("NMS", "NYQ")]
        symbol = (us_quotes[0]["symbol"] if us_quotes else quotes[0]["symbol"]).upper()
        return symbol
    except Exception:
        return q.upper()  # fallback to user entry as-is

layout = html.Div(
    className="page-wrap",
    style={
        "display": "flex",          
        "flexDirection": "column",  
        "alignItems": "center",     
        "justifyContent": "flex-start",  
        "minHeight": "120vh",       
        "fontFamily": "Arial, sans-serif",  
    },
    children=[
    html.H1("Single-Ticker Lookup", className="page-title"),
        html.P(
            "Enter a company name or ticker (e.g., “Apple” or “AAPL”).",
            className="page-subtext",
        ),

        html.Div(
            className="controls",
            children=[
                dcc.Input(
                    id="lookup-input",
                    type="text",
                    placeholder="Enter company name or ticker (e.g., Apple or AAPL)",
                    debounce=True,  # allow Enter to submit without button
                    style={"width": "320px"},
                ),
                html.Button("Show", id="lookup-button", n_clicks=0),
            ],
        ),

        html.Div(id="lookup-meta", className="message"),

        html.Div(
            className="panel panel--chart",
            children=[
                html.Div(
                    className="graph-pad",
                    children=[dcc.Graph(id="lookup-figure", config={"displayModeBar": False})],
                )
            ],
        ),
        # add look-up summary: descriptor of the company
        html.Div(id='lookup-summary', className='summary-box'),
    ],
)

@callback(
    Output("lookup-figure", "figure"),
    Output("lookup-meta", "children"),
    Output('lookup-summary', 'children'),
    Input("lookup-button", "n_clicks"),
    State("lookup-input", "value"),
)
def show_single_ticker(n_clicks, user_query):
    if not user_query:
        fig = px.line(title="Enter a company name or ticker to begin")
        fig.update_layout(title_x=0.5)
        return fig, "", ""

    # 1) Resolve user input to a symbol
    symbol = resolve_to_symbol(user_query)
    if not symbol:
        fig = px.line(title="Please enter a valid company name or ticker.")
        fig.update_layout(title_x=0.5)
        return fig, "Please enter a valid company name or ticker."

    # 2) Fetch 1Y of data
    end = datetime.today()
    start = end - timedelta(days=365)
    try:
        df = yf.download(symbol, start=start, end=end, auto_adjust=True, progress=False)
        if df.empty:
            fig = px.line(title=f"No data found for “{user_query}” ({symbol})")
            fig.update_layout(title_x=0.5)
            return fig, f"Could not fetch data for: {user_query} ({symbol}). Try another query.", "Could not fetch company information."

        # Prefer adjusted close
        price = df["Adj Close"] if "Adj Close" in df.columns else df["Close"]
        # 3) Set up the graph
        fig = px.line(
            price,
            title=f"{symbol}",
            labels={"value": "Closing Price (USD)"},
            width=1000,  # Increase width
            height=600   # Increase height
        )
        fig.update_layout(
            title_x=0.5,
            title_font_size=20,
            title_font_weight="bold",
            margin=dict(l=20, r=20, t=60, b=40),
            legend_title_text="Ticker",
            
        )
        fig.update_yaxes(tickprefix="$")
        
        fig.add_annotation(
            text="Source: Yahoo Finance via yfinance",
            xref="paper",
            yref="paper",
            x=1,
            y=0,
            xanchor="right",
            yanchor="bottom",
            showarrow=False,
            font=dict(size=11, color="#666"),
        )

        # 4) Info line (uses yfinance metadata; best-effort)
        info_bits = []
        try:
            tk = yf.Ticker(symbol)
            long_name = tk.info.get("longName") or tk.info.get("shortName") or symbol
            exchange = tk.info.get("exchange") or tk.info.get("fullExchangeName")
            currency = tk.info.get("currency") or ""
            summary = tk.info.get("longBusinessSummary", "Could not fetch company information.")
            if long_name:
                info_bits.append(f"Name: {long_name}")
            if exchange:
                info_bits.append(f"Exchange: {exchange}")
            if currency:
                info_bits.append(f"Currency: {currency}")
        except Exception:
            info_bits.append(f"Ticker: {symbol}")

        return fig, " | ".join(info_bits), summary

    except Exception as e:
        fig = px.line(title=f"Error fetching {symbol}")
        fig.update_layout(title_x=0.5)
        return fig, f"Error: {e}", "Could not fetch company information."
