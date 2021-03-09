import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib
import numpy as np
from app import app
from apps import config

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve() # Datasets folder
FILE = DATA_PATH.joinpath('flights.csv')

# Open dataset containing flight information
flight_data = pd.read_csv(FILE)

# Create useful lists for dropdown menus
airlines = sorted(flight_data.airline_name.unique())
airports = flight_data.airport_origin_code.unique()
states = flight_data.airport_origin_state.unique()

layout = html.Div([
    html.H1('Top 10 Airlines', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='states-dropdown', value='SP', clearable=False,
            options=[{'label': x, 'value': x} for x in states]
        ), className='six columns'),
    ], className='row'),
    dcc.Graph(id='my-bar', figure={}),
])

@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='states-dropdown', component_property='value')]
)

def display_value():

    movements = flight_data.groupby('airport_origin_code').sum('departures')
    movements.reset_index(inplace=True)
        
    #DATA_PATH = PATH.joinpath("../datasets").resolve()
    FILE = DATA_PATH.joinpath('airport_list.csv')
    airports = pd.read_csv(FILE)

    airports = pd.merge(airports, movements[['airport_origin_code', 'departures']], left_on = 'airport_icao', right_on = 'airport_origin_code')


    mapbox_access_token = config.MAPBOX_API_TOKEN

    fig = go.Figure(go.Scattermapbox(
            lat=airports['lat'],
            lon=airports['lon'],
            mode='markers',
            text = airports['name'],
            marker=go.scattermapbox.Marker(
                size=airports['departures'] / 500,
            ),
            hovertemplate=
            "<b>%{text}</b><br><br>" +
            "<b>Departures:</b> %{marker.size}<br>" +
            "<extra></extra>",
            
        ))

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
    return fig
