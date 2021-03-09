import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib
import numpy as np
from app import app
#from assets import config

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve() # Datasets folder
FILE = DATA_PATH.joinpath('flights.csv')

# Open dataset containing flight information
flight_data = pd.read_csv(FILE)

layout = html.Div([
    html.H1('Map', style={"textAlign": "center"}),
    dcc.Graph(id='my-map', figure={}),
])

@app.callback(
    Output(component_id='my-map', component_property='figure'),
    [Input(component_id='states-dropdown', component_property='value')]
)

def display_value(self):

    movements = flight_data.groupby('airport_origin_code').sum('departures')
    movements.reset_index(inplace=True)
        
    # Get stored path to /datasets folder
    FILE = DATA_PATH.joinpath('airport_list.csv')
    airports = pd.read_csv(FILE)

    # Get airlines and passenger traffic from movements
    airports = pd.merge(airports, movements[['airport_origin_code', 'departures']], left_on = 'airport_icao', right_on = 'airport_origin_code')

    mapbox_access_token = 'pk.eyJ1IjoiZ2F6aWxsbWVyIiwiYSI6ImNrbHdyNTM1azBsejUyc214aTMxbGxtbXEifQ.zHhMMVkUWYvLsOOC2MsmdA'

    fig = go.Figure(go.Scattermapbox(
            lat=airports['lat'],
            lon=airports['lon'],
            mode='markers',
            text = airports['name'],
            marker=go.scattermapbox.Marker(
                size=airports['departures'] / 5000,
            ),
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "<b>Departures:</b> %{marker.size}<br>" +
            "<extra></extra>",
        )    
    )

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style = 'outdoors',
            bearing=2,
            center=go.layout.mapbox.Center(
                lat=-13,
                lon=-53
            ),
            pitch=0,
            zoom=3
        )
    )

    #fig.show()
    return fig
