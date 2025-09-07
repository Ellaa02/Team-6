#app.py

from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Multi-Page",
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # <-- load Bootstrap CSS
)
server = app.server

app.layout = html.Div(
    [
        dbc.NavbarSimple(
            brand="Multi-Page App",
            brand_href="/",
            color="primary",          # navbar background color
            dark=True,                # light text on dark background
            expand="md",              # collapses on small screens, expands >= md
            sticky="top",             # sticks to the top on scroll
            className="mb-4 shadow",  # spacing + subtle shadow
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/", active="exact", className="px-3")),
                dbc.NavItem(dbc.NavLink("Page 1", href="/page1", active="exact", className="px-3")),
                dbc.NavItem(dbc.NavLink("Page 2", href="/page2", active="exact", className="px-3")),
                dbc.NavItem(dbc.NavLink("Page 3", href="/page3", active="exact", className="px-3")),
            ],
        ),
        html.Div(page_container, className="container pb-5"),  # readable width + bottom padding
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
