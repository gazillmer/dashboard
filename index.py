import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import airlines, movements, map, bump


app = dash.Dash(external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Passenger and Aircraft Movements |', href='/apps/movements'),
        dcc.Link(' Airline Traffic |', href='/apps/airlines'),
        dcc.Link(' Airport Map |', href='/apps/map'),
        dcc.Link(' Airline Ranking', href='/apps/bump'),
    ], className='row'),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))

def display_page(pathname):
    if pathname == '/apps/movements':
        return movements.layout
    if pathname == '/apps/airlines':
        return airlines.layout
    if pathname == '/apps/map':
        return map.layout
    if pathname == '/apps/bump':
        return bump.layout
    else:
        return "Something went wrong. For sure, the coder is an idiot."

if __name__ == '__main__':
    app.run_server(debug=False)
