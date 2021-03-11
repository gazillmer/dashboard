import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly_express as px
import plotly.io as pio
import pandas as pd
import pathlib
import dash

from dash.dependencies import Input, Output
from app import app

app = dash.Dash(__name__)

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
FILE = DATA_PATH.joinpath('traffic.csv')

def display_value():
    fig = go.Figure()

    for i in range(len(website_names)):
        fig.add_trace(
            go.Line(
                x = website_traffic['year_month'],
                y = website_traffic[website_names[i]],
                name = website_names[i]
                )
        )
    fig.update_layout(
        height = 550
    )

    fig.update_yaxes(title_text="Total<b> website views</b>", type='log')
    fig.update_xaxes(title_text="<b>Months</b>")

    return fig

# Open dataset containing flight information
website_traffic = pd.read_csv(FILE)
website_names = website_traffic.columns[1:]
chart = display_value()
layout = html.Div([
    html.H1('Website Traffic', style={"textAlign": "center"}),
    html.H6('Information provided by https://www.similarweb.com/. The website provides traffic data for any page for the last 6 months without needing any paid subscription.', style={"textAlign": "center"}),
    dcc.Graph(id='my-traffic', figure=chart),
    
])
