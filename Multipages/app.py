from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Team 6 Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # <-- load Bootstrap CSS
)
server = app.server

app.layout = html.Div(
    [
        dbc.NavbarSimple(
            color="primary",          
            dark=True,                
            expand="md",              
            sticky="top",             
            className="mb-4 shadow",  
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/", active="exact", className="px-3")),
                dbc.NavItem(dbc.NavLink("Page 1", href="/page1", active="exact", className="px-3")),
                dbc.NavItem(dbc.NavLink("Page 2", href="/page2", active="exact", className="px-3")),
                dbc.NavItem(dbc.NavLink("About Us", href="/about", active="exact", className="px-3")),

            ],
        ),
        html.Div(page_container, className="container pb-5"),  # readable width + bottom padding
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
