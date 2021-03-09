import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# Get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
FILE = DATA_PATH.joinpath('flights.csv')

# Open dataset containing flight information
flight_data = pd.read_csv(FILE)

# Create useful lists for dropdown menus
airlines = sorted(flight_data.airline_name.unique())
airports = flight_data.airport_origin_code.unique()

# Create a list state with unique values (removing blanks from dataset)
states = flight_data.airport_origin_state.unique()
states = [x for x in states if str(x) != 'nan']
states = sorted(states)

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

def display_value(state_choice):

    # Filter flights with origin on selected state
    flights_state = flight_data[flight_data['airport_origin_state'] == state_choice]
    flights_state = flights_state.groupby(['airline_name', 'year_month']).sum('departures')
    flights_state.reset_index(inplace=True)

    # Filter Top 10 airlines with depatures on selected state
    airlines_state = flights_state.groupby('airline_name').sum('departures').nlargest(10, 'departures')
    airlines_state.reset_index(inplace=True)
    airlines_state = airlines_state['airline_name']
    
    # Filter dataset to show only the flights from the Top 10 airlines
    top_10_airlines = flights_state[flights_state['airline_name'].isin(airlines_state)]

    # Create plot with flight information, summarized by year and month
    fig = px.line(
        top_10_airlines,
        x = 'year_month',
        y = 'departures',
        color = 'airline_name',
        hover_name = 'airline_name',
        #log_y = True,
        labels = {
            'departures' : "Departures", 
            'year_month' : 'Month',
            'airline_name' : 'Airline'}
    )

    return fig

