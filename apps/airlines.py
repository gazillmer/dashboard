import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

def get_flight_data():

    # Get relative data folder
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../datasets").resolve()
    FILE_FLIGHTS = DATA_PATH.joinpath('flights.csv')
    FILE_AIRPORTS = DATA_PATH.joinpath('airport_list.csv')

    # Open dataset containing flight information
    flights = pd.read_csv(FILE_FLIGHTS)
    airports = pd.read_csv(FILE_AIRPORTS, encoding = 'UTF-8')

    flights = pd.merge(flights, airports[['airport_icao', 'airport_iata', 'name']], left_on='airport_origin_code', right_on='airport_icao')
    flights = pd.merge(flights, airports[['airport_icao', 'airport_iata', 'name']], left_on='airport_destination_code', right_on='airport_icao')

    flights.rename(columns = {'airport_icao_x' : 'icao_origin', 
                          'airport_icao_y' : 'icao_destination',
                          'airport_iata_x' : 'iata_origin', 
                          'airport_iata_y' : 'iata_destination',
                          'name_x' : 'airport_origin',
                          'name_y' : 'airport_destination'}, inplace=True)

    flights.drop(columns=['airport_origin_code', 'airport_destination_code'], inplace=True)

    '''
    flights = pd.merge(flights, airports[['icao', 'name']], left_on='airport_origin_code', right_on='icao')
    flights = pd.merge(flights, airports[['icao', 'airport_name']], left_on='airport_destination_code', right_on='icao')
    flights.rename(columns = {'icao_x' : 'icao_origin', 
                          'icao_y' : 'icao_destination',
                          'airport_name_x' : 'airport_origin',
                          'airport_name_y' : 'airport_destination'}, inplace=True)
    flights.drop(columns=['airport_origin_code', 'airport_destination_code'], inplace=True)
    '''    
    return flights

flight_data = get_flight_data()

# Create useful lists for dropdown menus
airlines = sorted(flight_data.airline_name.unique())

airports = flight_data.airport_origin.unique()
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
            id='airport-origin', value='Select Origin Airport', clearable=False, 
            options=[{'label': y, 'value': y} for y in airports]
        ), className='six columns', style={"width": "35%"}),
        html.Div(
            dcc.Dropdown(
            id='airport-destination', value='Select Destination Airport', clearable=False, 
            options=[{'label': y, 'value': y} for y in airports]
        ), className='six columns', style={"width": "35%"}),
    ], className='row'),
    dcc.Graph(id='my-bar', figure={}),
])

@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='airport-origin', component_property='value'),
    Input(component_id='airport-destination', component_property='value')]
)

def display_value(airport_origin, airport_destination):

    # Filter flights with origin on selected airport
    flights_airport = flight_data[flight_data['airport_origin'] == airport_origin]
    if(airport_destination in airports):
        flights_airport = flight_data[flight_data['airport_destination'] == airport_destination]
    
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

