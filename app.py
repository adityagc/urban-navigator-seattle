import plotly.express as px
from dash import  dcc, html
import pandas as pd
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import json
import os

dirname = os.path.dirname(__file__)
csv_file = os.path.join(dirname, 'census.csv')
geojson_file = os.path.join(dirname, 'census.geojson')
# Load Data
df = pd.read_csv(csv_file)
# Select population columns
population_columns = ['NAMELSAD10','TOTAL_POPULATION','WHITE', 'BLACK', 'AMER-INDIAN', 'ASIAN', 'HAWAIAN-PI', 'OTHER', 'TWO_OR_MORE_RACE', 'HISPANIC_OR_LATINO_OF_ANY_RACE']
df_population = df[population_columns].copy()

# Load GeoJSON data 
with open(geojson_file) as file:
    counties = json.load(file)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# Define the app layout
app.layout = html.Div([
    html.H1(children='Population Choropleth Map', style={'text-align': 'center', 'margin-bottom': '10px'}),
    html.Div([
        dcc.Graph(id='choropleth-map')
    ], style={'width': '80%', 'margin': 'auto'}),
    html.Div([
        html.P('Select a population race:'),
        dcc.RadioItems(
            id='race-selector',
            options=[{'label': race, 'value': race} for race in population_columns[1:]],  
            value=population_columns[1],
            labelStyle={'display': 'inline-block', 'margin': '10px'}
        )
    ], style={'width': '80%', 'margin': 'auto'})
])

# Define the callback function
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('race-selector', 'value')
)
def update_choropleth_map(selected_race):
    fig = px.choropleth(df_population, geojson=counties, color=df_population[selected_race],
                        locations=df_population['NAMELSAD10'], featureidkey="properties.NAMELSAD10",
                        projection="mercator"
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(mode='inline')
