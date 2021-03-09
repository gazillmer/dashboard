import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
#from app import app

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

layout = html.Div([
    html.H1('Top 10 Airlines', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='genre-dropdown', value='SP', clearable=False,
            options=[{'label': x, 'value': x} for x in states]
        ), className='six columns'),

        html.Div(dcc.Dropdown(
            id='sales-dropdown', value='EU Sales', clearable=False,
            persistence=True, persistence_type='memory',
            options=[{'label': x, 'value': x} for x in sales_list]
        ), className='six columns'),
    ], className='row'),

    dcc.Graph(id='my-bar', figure={}),
])


@app.callback(
    Output(component_id='my-bar', component_property='figure'),
    [Input(component_id='genre-dropdown', component_property='value'),
     Input(component_id='sales-dropdown', component_property='value')]
)
def display_value(genre_chosen, sales_chosen):
    dfv_fltrd = dfv[dfv['Genre'] == genre_chosen]
    dfv_fltrd = dfv_fltrd.nlargest(10, sales_chosen)
    fig = px.bar(dfv_fltrd, x='Video Game', y=sales_chosen, color='Platform')
    fig = fig.update_yaxes(tickprefix="$", ticksuffix="M")
    return fig