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
airports = [x for x in airports if str(x) != 'nan']
airports = sorted(airports)

# Create a list state with unique values (removing blanks from dataset)
states = flight_data.airport_origin_state.unique()
states = [x for x in states if str(x) != 'nan']
states = sorted(states)

layout = html.Div([
    html.H1('Top 10 Airlines', style={"textAlign": "center"}),

    html.Div([
        html.P('Select airport: '),
        html.Div(
            dcc.Dropdown(
            id='airports-dropdown', value='SBPA', clearable=False, 
            options=[{'label': y, 'value': y} for y in airports]
        ), className='six columns', style={"width": "7%"}),
    ], className='row'),
    dcc.Graph(id='my-bar', figure={}),
])

@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    Input(component_id='airports-dropdown', component_property='value')
)

def display_value(airport_choice):

    # Filter flights with origin on selected airport
    flights_airport = flight_data[flight_data['airport_origin_code'] == airport_choice]
    flights_airport = flights_airport.groupby(['airline_name', 'year_month']).sum('departures')
    flights_airport.reset_index(inplace=True)

    # Filter Top 10 airlines with depatures on selected airport
    airlines_airport = flights_airport.groupby('airline_name').sum('departures').nlargest(10, 'departures')
    airlines_airport.reset_index(inplace=True)
    airlines_airport = airlines_airport['airline_name']
    
    # Filter dataset to show only the flights from the Top 10 airlines
    top_10_airlines = flights_airport[flights_airport['airline_name'].isin(airlines_airport)]

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
    fig.update_layout(
        height = 600
    )

    return fig

