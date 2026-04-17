import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

DATA_PATH = "./formatted_data.csv"

COLORS = {
    "bg": "#FFF8F0",
    "card": "#FFE0B2",
    "accent": "#E65100",
    "text": "#3E2723",
}

df = pd.read_csv(DATA_PATH)
df = df.sort_values("date")

dash_app = Dash(__name__)


def build_figure(data):
    fig = px.line(data, x="date", y="sales")
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        plot_bgcolor=COLORS["card"],
        paper_bgcolor=COLORS["bg"],
        font=dict(color=COLORS["text"]),
    )
    fig.update_traces(line_color=COLORS["accent"])
    return fig


dash_app.layout = html.Div([
    html.H1(
        "Pink Morsel Sales Visualiser",
        id="header",
        style={
            "textAlign": "center",
            "color": COLORS["text"],
            "backgroundColor": COLORS["card"],
            "padding": "16px",
            "borderRadius": "12px",
            "marginBottom": "20px",
        }
    ),
    html.Div([
        html.Label("Filter by region:", style={"fontWeight": "bold", "marginRight": "12px"}),
        dcc.RadioItems(
            id="region_picker",
            options=[{"label": r.capitalize(), "value": r}
                     for r in ["north", "south", "east", "west", "all"]],
            value="all",
            inline=True,
            inputStyle={"marginRight": "6px"},
            labelStyle={"marginRight": "18px"},
        ),
    ], style={"textAlign": "center", "marginBottom": "10px"}),
    dcc.Graph(id="visualization", figure=build_figure(df)),
], style={
    "backgroundColor": COLORS["bg"],
    "fontFamily": "Arial, sans-serif",
    "maxWidth": "1100px",
    "margin": "0 auto",
    "padding": "30px",
    "borderRadius": "16px",
})


@dash_app.callback(Output("visualization", "figure"), Input("region_picker", "value"))
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    return build_figure(filtered)


if __name__ == "__main__":
    dash_app.run_server()
