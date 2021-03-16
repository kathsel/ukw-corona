# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from colorhash import ColorHash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src import plots

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

data = pd.read_csv('./data/all-series.csv')
data['Datum'] = pd.to_datetime(data['Datum'], format='%d.%m.%Y')
data.set_index('Datum', inplace=True)

lk_value_list = list(data.Landkreis.unique())
lk_value_list.remove('Deutschland')
lk_value_list.sort()

fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3], shared_xaxes=True, vertical_spacing=0.05)
fig.update_xaxes(rangeslider_visible=True, row=2, col=1)

app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col(width={'size':1}),
        dbc.Col(html.Div([
            html.H1('Corona Zahlen Deutschland nach Ländern und Kreisen'), 
            html.P(['Visualisierung der Zahlen von ', html.A('https://pavelmayer.de/covid/risks/', href='https://pavelmayer.de/covid/risks/')])
            ])
        ),        
    ]),

    dbc.Row([
        dbc.Col(width={'size':1}),
        dbc.Col(html.Div([
            html.Label('Angezeigte Daten:'),
            dbc.Checklist(
                id='checklist-anzahl',
                options=[
                    {'label': 'Fälle', 'value': 'MeldeTag_AnzahlFallNeu'},
                    {'label': 'Todesfälle', 'value': 'MeldeTag_AnzahlTodesfallNeu'},
                    {'label': 'Genesene', 'value': 'AnzahlGenesenNeu'}
                    ],
                value=['MeldeTag_AnzahlFallNeu'], 
                inline=True
                ),

            html.Br(),
            html.Label('Angezeigter Modus:'),
            dbc.RadioItems(
                id='radio-modus',
                options=[                        
                    {'label': 'Summe', 'value': 'summe'},
                    {'label': 'Neue Fälle', 'value': 'neu'}                    
                    ],
                value='neu', 
                inline=True
                ),
            dbc.RadioItems(
                id='radio-zahlenmodus',
                options=[                        
                    {'label': 'Absolute Zahlen', 'value': 'absolut'},
                    {'label': 'Pro 100k Einwohner (7 Tage Inzidenz)', 'value': '100k'}
                    ],
                value='absolut', 
                inline=True
                ),

            html.Br(),
            html.Label('Welche Bereiche anzeigen?'),
            dbc.Checklist(
                id="switches-input",
                options=[
                    {"label": "Deutschland", "value": 'BR'}
                    ],
                value=['BR'],
                switch=True,
                ),

            html.Br(),
            html.Label('Weitere Bundesländer / Städte / Landkreise:'),
            dcc.Dropdown(
                id='dropdown-lk',
                options=[{'label': lk, 'value': lk} for lk in lk_value_list],
                value=[],
                multi=True
            ),                 
            ]), 
            width={'size':3}
        ),

        dbc.Col(html.Div([dcc.Graph(
            id='AnzahlGraph',
            figure=fig),
            ]), 
            width={'size':8}  
        ),

        dbc.Col(width={'size':1}),
    ]),
])

@app.callback(
    dash.dependencies.Output('AnzahlGraph', 'figure'),
    dash.dependencies.Input('checklist-anzahl', 'value'), 
    dash.dependencies.Input('radio-modus', 'value'), 
    dash.dependencies.Input('radio-zahlenmodus', 'value'), 
    dash.dependencies.Input('dropdown-lk', 'value'), 
    dash.dependencies.Input('switches-input', 'value'))
def update_figure(data_value, modus_value, zahlenmodus_value, lk_values, br_value):
    if 'BR' in br_value: 
        lk_values = lk_values + ['Deutschland']

    fig = plots.create_timeline_plot(data, data_value, lk_values, modus_value, zahlenmodus_value)
    fig.update_xaxes(rangeslider_visible=True, row=2, col=1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)