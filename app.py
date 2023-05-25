import plotly.express as px
from dash import dcc, html
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 328" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 327.02"]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 315.02" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 315.02" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 328" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 325" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 326.01" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 326.02" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 327.03" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 327.04" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 320.03" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 315.01" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 313.01" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 312.02" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 313.02" ]
df_population = df_population[df_population.NAMELSAD10 != "Census Tract 314" ]
# Display the first 6 rows of the new DataFrame
# print(df_population.head(6))


# Load GeoJSON data
with open(geojson_file) as file:
    counties = json.load(file)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# Define the app layout
app.layout = html.Div([
    html.H1(children='Population Choropleth Map',
             style={'text-align': 'center', 'margin-bottom': '10px', 'font-size': '28px', 'font-weight': 'bold'}),
    html.H2(children='Explore Demographic Distribution',
             style={'text-align': 'center', 'margin-bottom': '13px', 'font-size': '20px', 'font-weight': 'bold'}),
    html.P(children='Click the radio buttons to visualize the population of each district based for that demographic group.'
                    'Click on the district of interest visualize the relative contribution of each group to the population demographics.',
             style={'text-align': 'center', 'margin-bottom': '20px', 'font-size': '16px'}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Tab 1', value='tab-1', children=[
            html.Div([
                dcc.Graph(id='choropleth-map-1'),
                html.Div([
                    html.P('Select a population demographic group:'),
                    dcc.RadioItems(
                        id='race-selector-1',
                        options=[{'label': race, 'value': race} for race in population_columns[1:]],
                        value=population_columns[1],
                        labelStyle={'display': 'inline-block', 'margin': '10px'}
                    )
                ], style={'width': '80%', 'margin': 'auto'}),
                dcc.Graph(id='population-pie-1')
            ])
        ]),
        dcc.Tab(label='Tab 2', value='tab-2', children=[
            html.Div([
                dcc.Graph(id='choropleth-map-2'),
                html.Div([
                    html.P('Select a population demographic group:'),
                    dcc.RadioItems(
                        id='race-selector-2',
                        options=[{'label': race, 'value': race} for race in population_columns[1:]],
                        value=population_columns[1],
                        labelStyle={'display': 'inline-block', 'margin': '10px'}
                    )
                ], style={'width': '80%', 'margin': 'auto'}),
                dcc.Graph(id='population-pie-2')
            ])
        ])
    ])
])


# Function to update the choropleth map in Tab 1
@app.callback(
    Output('choropleth-map-1', 'figure'),
    Input('race-selector-1', 'value')
)
def update_choropleth_map_1(selected_race):
    fig = px.choropleth(df_population, geojson=counties, color=df_population[selected_race],
                        locations=df_population['NAMELSAD10'], featureidkey="properties.NAMELSAD10",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# Function to update the choropleth map in Tab 2
@app.callback(
    Output('choropleth-map-2', 'figure'),
    Input('race-selector-2', 'value')
)
def update_choropleth_map_2(selected_race):
    fig = px.choropleth(df_population, geojson=counties, color=df_population[selected_race],
                        locations=df_population['NAMELSAD10'], featureidkey="properties.NAMELSAD10",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

# Function to update the pie chart in Tab 1 based on selected district
@app.callback(
    Output('population-pie-1', 'figure'),
    Input('choropleth-map-1', 'clickData')
)
def update_pie_chart_1(click_data):
    if click_data is None:
        # If no district is selected, show an empty pie chart
        fig = px.pie()
    else:
        district_name = click_data['points'][0]['location']
        district_data = df_population[df_population['NAMELSAD10'] == district_name]
        if not district_data.empty:
            fig = px.pie(
                values=district_data[population_columns[2:]].values[0],
                names=population_columns[2:],
                title=f"Population Distribution in {district_name}"
            )
        else:
            # If no data is available for the selected district, show an empty pie chart
            fig = px.pie()
    return fig

# Function to update the pie chart in Tab 2 based on selected district
@app.callback(
    Output('population-pie-2', 'figure'),
    Input('choropleth-map-2', 'clickData')
)
def update_pie_chart_2(click_data):
    if click_data is None:
        # If no district is selected, show an empty pie chart
        fig = px.pie()
    else:
        district_name = click_data['points'][0]['location']
        district_data = df_population[df_population['NAMELSAD10'] == district_name]
        if not district_data.empty:
            fig = px.pie(
                values=district_data[population_columns[2:]].values[0],
                names=population_columns[2:],
                title=f"Population Distribution in {district_name}"
            )
        else:
            # If no data is available for the selected district, show an empty pie chart
            fig = px.pie()
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(mode='inline')
