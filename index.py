import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests

from dash.dependencies import Input, Output
from bs4 import BeautifulSoup as BS

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import airlines, movements, map, bump, traffic
import update

# Define bootstrap theme as Cosmo
#app = dash.Dash(__name__)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dash", className="display-4"),
        html.Hr(),
        html.P(
            "Information about airports, airlines and travel websites traffic", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Map", href="/apps/map", active="exact"),
                dbc.NavLink("Aircraft Movements", href="/apps/movements", active="exact"),
                dbc.NavLink("Airline Departures", href='/apps/airlines', active="exact"),
                dbc.NavLink("Travel Websites Traffic", href='/apps/traffic', active="exact"),
                dbc.NavLink("Airline Ranking", href='/apps/bump', active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    if pathname == "/":
        return [
                html.H1('A Visual Analytics System for Understanding and Predicting Flying Intentions From Airports',
                        style={'textAlign':'left'}),
                html.Div([
                    html.Hr(),
                    html.P('One of the main challenges of an airport administrator is managing the number of flights required to transport a certain number of passengers, especially during the Covid-19 pandemic, where air traffic was dramatically reduced. This work aims to create a social network and web traffic sensing model to predict peoples willingness to travel in the months to come, providing support for decision-making managers of airports. The model will rely on data provided by ANAC (Brazilian National Civil Aviation Agency), as well as information collected from travel-related search engines and social-network sensing.'),
                    html.P('This project is part of Gabriel\'s undergraduate thesis for his bachelor\'s degree in Computer Engineering at UFRGS.'),
                    html.P('Student: Gabriel Alexandre Zillmer'),
                    html.P('Advisor: João Luiz Dihl Comba')
                    
                ])
        ]
    elif pathname == '/apps/map':
        return map.layout
    elif pathname == '/apps/movements':
        return movements.layout
    elif pathname == '/apps/airlines':
        return airlines.layout
    elif pathname == '/apps/bump':
        return bump.layout 
    elif pathname == '/apps/traffic':
        return traffic.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"For sure, the coder is an idiot."),
        ]
    )

if __name__=='__main__':
    app.run_server(debug=True, port=3001)

