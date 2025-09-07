import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H2("Welcome to my HomePage"),
    html.P("This is a simple multipage Dash project")
    
])



##################

import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Stock Market Insights Dashboard", className="display-4 text-center mb-4"),
            html.Hr()
        ])
    ]),

    # Project purpose
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("About This Project", className="card-title"),
                    html.P(
                        "This dashboard helps investors explore how different stocks respond "
                        "to market volatility. By comparing stock performance with the CBOE "
                        "Volatility Index (VIX) and major market indices, users can gain "
                        "insight into risk and correlation patterns."
                    )
                ])
            ], className="mb-4 shadow-sm")
        ])
    ]),

    # CBOE explanation
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("What is the CBOE Volatility Index (VIX)?", className="card-title"),
                    html.P(
                        "Often called the 'fear gauge,' the VIX measures the market’s "
                        "expectation of volatility based on S&P 500 index options. "
                        "A higher VIX indicates more expected market swings, while "
                        "a lower VIX signals calmer conditions."
                    )
                ])
            ], className="mb-4 shadow-sm")
        ])
    ])
], fluid=True)
