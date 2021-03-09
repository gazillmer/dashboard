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
    html.H1('Airline Ranking', style={"textAlign": "center"}),
    html.H2('Bump chart needs improvements', style={"textAlign": "center"}),

    html.Div([
        html.Div(dcc.Dropdown(
            id='states-dropdown', value='SP', clearable=False,
            options=[{'label': x, 'value': x} for x in states]
        ), className='six columns'),
    ], className='row'),
    dcc.Graph(id='my-bump', figure={}),
])

@app.callback(
    Output(component_id='my-bump', component_property='figure'),
    [Input(component_id='states-dropdown', component_property='value')]
)

def display_value(state_choice):

    # Filter flights with origin on selected state
    flights_state = flight_data[flight_data['airport_origin_state'] == state_choice]
    flights_state = flights_state.groupby(['airline_name', 'year_month']).sum('departures')
    flights_state.reset_index(inplace=True)

    voos_por_aerea = flight_data[flight_data['airport_origin_state'] == state_choice]
    voos_por_aerea = voos_por_aerea.groupby(['airline_name', 'year_month']).sum('departures')[['departures']]
    voos_por_aerea = voos_por_aerea.unstack(level = -1)
    voos_por_aerea = voos_por_aerea.fillna(0)
    voos_por_aerea.columns = voos_por_aerea.columns.droplevel(level = 0)

    max_month = pd.DataFrame()

    for column in voos_por_aerea:
        max_month[column] = voos_por_aerea[column].nlargest(10).index.to_list()

    month = pd.DataFrame(max_month.stack())
    month.reset_index(inplace=True) 

    month.rename(columns = {'level_0': 'Position', 'level_1':'Month', 0: 'Airline'}, inplace=True)

    month = month.sort_values('Month',ascending = True)
    month['Position'] = month['Position'] + 1

    # Create plot with flight information, summarized by year and month
    fig = px.line(
        month,
        x = 'Month',
        y = 'Position',
        color = 'Airline',
    )

    fig.update_layout(
        title={
            'text': "Top 10 airlines (considering departures from the selected state)",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        yaxis = dict(
            tickmode = 'array',
            tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        )
    )

    fig.update_traces(mode="markers+lines")
    fig.update_yaxes(autorange="reversed")

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

    return fig

