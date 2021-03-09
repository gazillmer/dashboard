import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from numpy.core.numeric import NaN
import plotly.express as px
import pandas as pd
import pathlib
from app import app

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
FILE = DATA_PATH.joinpath('flights.csv')

# Open dataset containing flight information
flight_data = pd.read_csv(FILE)

# Create useful lists for dropdown menus
airlines = sorted(flight_data.airline_name.unique())
airports = flight_data.airport_origin_code.unique()

states = flight_data.airport_origin_state.unique()
states = [x for x in states if str(x) != 'nan']
states = sorted(states)

layout = html.Div([
    html.H1('Aircraft and Passenger movement by state', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='states-dropdown', value='SP', clearable=False,
            options=[{'label': x, 'value': x} for x in states]
        ), className='six columns'),
    ], className='row'),
    dcc.Graph(id='my-rank', figure={}),
])

@app.callback(
    Output(component_id='my-rank', component_property='figure'),
    [Input(component_id='states-dropdown', component_property='value')]
)

def display_value(state_choice):

    # Filter flights with origin on selected state
    flights_state = flight_data[flight_data['airport_origin_state'] == state_choice]
    flights_state = flights_state.groupby(['airline_name', 'year_month']).sum('departures')
    flights_state.reset_index(inplace=True)

    # Tráfego interno no período analisado
    internal_traffic = flight_data[flight_data['airport_origin_state'] == state_choice]
    internal_traffic = internal_traffic[internal_traffic.loc[:]['airport_destination_country'] == 'BRASIL']
    internal_traffic['total_passengers'] = internal_traffic['passengers_paid'] + internal_traffic['passengers_free']

    internal_traffic_month = internal_traffic.groupby('year_month').sum('departures')
    internal_traffic_month.reset_index(inplace=True)
    internal_traffic_month['load_factor'] = internal_traffic_month['total_passengers'] / internal_traffic_month['seats']

    # Create plot with information about passenger number and departures, summarized by month
    fig = make_subplots(specs = [[{'secondary_y' : True}]])

    #Add traces
    fig.add_trace(
        go.Line(
            x = internal_traffic_month['year_month'],
            y = internal_traffic_month['total_passengers'],
            name = 'Passengers'),
        secondary_y = False
        )

    fig.add_trace(
        go.Line(
            x = internal_traffic_month['year_month'],
            y = internal_traffic_month['departures'],
            name = 'Departures'),
        secondary_y = True
        )
    """
    fig.update_layout(
        title={
            'text': "Aircraft and Passenger Movement on internal flights",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
    )
    """
    fig.update_xaxes(
        title_text="Month",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="Total <b>Passengers</b>", secondary_y=False)
    fig.update_yaxes(title_text="Total <b>Departures</b>", secondary_y=True)

    return fig

