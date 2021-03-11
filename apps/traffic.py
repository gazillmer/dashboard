import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly_express as px
import plotly.io as pio
import pandas as pd
import pathlib

from dash.dependencies import Input, Output
#from app import app

pio.templates.default = "plotly_white"

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
FILE = DATA_PATH.joinpath('traffic.csv')

# Open dataset containing flight information
website_traffic = pd.read_csv(FILE)
website_names = website_traffic.columns[1:]
'''
layout = html.Div([
    html.H1('Website Traffic', style={"textAlign": "center"}),
    dcc.Graph(id='traffic', figure={}),
])

@app.callback(
    Output(component_id='traffic', component_property='figure'),
    [Input(component_id='states-dropdown', component_property='value')]
)

def display_value():
'''
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
    title={
        'text': "Total views of travel websites per month",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
)

fig.update_yaxes(title_text="Total<b> website views</b>", type='log')
fig.update_xaxes(title_text="<b>Months</b>")
fig.show()

#return fig
