import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    # Title Section
    html.H1(
        "Stock Market Insights Dashboard",
        style={
            "textAlign": "center",
            "color": "#1f77b4",
            "fontWeight": "bold",
            "marginBottom": "20px"
        }
    ),
    html.Hr(style={"borderWidth": "2px", "borderColor": "#1f77b4", "width": "50%", "margin": "auto"}),

    # About Project Section
    html.Div([
        html.H2("About This Project", style={"color": "#ffffff", "backgroundColor": "#1f77b4",
                                             "padding": "10px", "borderRadius": "5px"}),
        html.P(
            "This dashboard helps investors explore how different stocks respond "
            "to market volatility. By comparing stock performance with the S&P 500 and the CBOE "
            "Volatility Index (VIX) and major market indices, users can gain "
            "insight into risk and correlation patterns.",
            style={"padding": "10px", "lineHeight": "1.6"}
        )
    ], style={"marginBottom": "30px", "boxShadow": "2px 2px 10px #888888", "borderRadius": "5px"}),

    # S&P 500 Explanation Section
    html.Div([
        html.H2("What is the S&P 500 (GSPC)?", style={"color": "#ffffff",
                                                                     "backgroundColor": "#2ca02c",
                                                                     "padding": "10px",
                                                                     "borderRadius": "5px"}),

        html.P(
            "The S&P 500,  is a stock market index that measures the performance"
            "of the largest 500 publicly traded companies in the U.S. It is widely "
            "used as a benchmark for the overall performance of the U.S. stock market. ",
            style={"padding": "10px", "lineHeight": "1.6"}
        )
    ], style={"boxShadow": "2px 2px 10px #888888", "borderRadius": "5px", "marginBottom": "30px"}),
    
    # CBOE Explanation Section
    html.Div([
        html.H2("What is the CBOE Volatility Index (VIX)?", style={"color": "#ffffff",
                                                                     "backgroundColor": "#a02c2c",
                                                                     "padding": "10px",
                                                                     "borderRadius": "5px"}),

        html.P(
            "Often called the 'fear gauge,' the VIX measures the market’s "
            "expectation of volatility based on S&P 500 index options. "
            "A higher VIX indicates more expected market swings, while "
            "a lower VIX signals calmer conditions.",
            style={"padding": "10px", "lineHeight": "1.6"}
        )
    ], style={"boxShadow": "2px 2px 10px #888888", "borderRadius": "5px"})

],
    style={"maxWidth": "900px", "margin": "auto", "fontFamily": "Arial, sans-serif"}
)