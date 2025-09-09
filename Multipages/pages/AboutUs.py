import dash
from dash import html

dash.register_page(__name__, path="/about", name="About Us")

layout = html.Div(
    [
        html.H1("About Us"),
        html.P(
            "This is the About Us page for our site. "
            "We are dedicated to making your financial journey as easy as possible. "
            "Our group consists of four diverse members, each with their own skills and capabilities. "
            "We look forward to working with you!"
        ),
        html.Img(
            src="/assets/Team_photo.jpg",  
            style={"width": "400px", "border-radius": "12px", "margin-top": "20px"}
        ),
    ],
    style={
        "textAlign": "center",   # center all text
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",  # center the image
        "justifyContent": "center",
        "padding": "20px"
    }
)
