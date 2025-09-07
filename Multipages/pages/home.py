import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = layout = html.Div([
    html.H1("Stock Market Insights Dashboard"),
    html.Hr(),
    html.P("This dashboard helps investors explore how different stocks respond "
           "to market volatility. By comparing stock performance with the CBOE "
           "Volatility Index (VIX) and major market indices, users can gain "
           "insight into risk and correlation patterns."),
    html.H3("What is the CBOE Volatility Index (VIX)?"),
    html.P("Often called the 'fear gauge,' the VIX measures the market’s "
           "expectation of volatility based on S&P 500 index options. "
           "A higher VIX indicates more expected market swings, while "
           "a lower VIX signals calmer conditions.")
])