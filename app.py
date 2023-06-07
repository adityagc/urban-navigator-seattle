import plotly.express as px
from dash import dcc, html, ctx
import pandas as pd
import dash
from dash.dependencies import Input, Output
import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random 

# Load Data
df = pd.read_csv('A_Census_Tract_(2010)_Profile_ACS_5-year_Estimates_2013-2017.csv')
df_small = pd.read_csv('2010_Census_Tract_Seattle_-_Household_Statistics.csv')
df_new = pd.read_csv('Racial_and_Social_Equity_Composite_Index_Current.csv')

# Limit to geoids in Seattle
df = pd.merge(df, df_small, how='inner', on=['GEOID10'])
df_health_initial = pd.merge(df, df_new, how='inner', on=['GEOID10'])

# Select population columns
population_abs_columns = ['NAMELSAD10','TOTAL_POPULATION','WHITE',  'BLACK', 'AMER-INDIAN', 
 'ASIAN',   'HAWAIAN-PI', 'TWO_OR_MORE_RACE',  'HISPANIC_OR_LATINO_OF_ANY_RACE', 'OTHER']

df_abs_population = df[population_abs_columns].copy()

# Load GeoJSON data
with open('A_Census_Tract_(2010)_Profile_ACS_5-year_Estimates_2013-2017.geojson') as file:
    counties = json.load(file)

# Select population columns
population_abs_columns = ['NAMELSAD10','TOTAL_POPULATION','WHITE',  'BLACK', 'AMER-INDIAN', 
 'ASIAN',   'HAWAIAN-PI', 'TWO_OR_MORE_RACE',  'HISPANIC_OR_LATINO_OF_ANY_RACE', 'OTHER']

# Select population percentage columns
population_columns = ['NAMELSAD10', 'PCT_WHITE','PCT_BLACK', 
'PCT_AMER-INDIAN', 'PCT_ASIAN',   'PCT_HAWAIAN-PI','PCT_TWO_OR_MORE', 'PCT_HISP_ANY_RACE', 'PCT_OTHER']

df_population = df[population_columns].copy()

# Select income and housing columns
income_housing_columns = ['NAMELSAD10', 'TOTAL_POPULATION', 'PERSON_OF_COLOR', 'MEDIAN_GROSS_RENT', 'MEDIAN_HH_INC_PAST_12MO_DOLLAR',  
                          'RENT_GRAPI_COMPUTED', 'GRAPI_35_0_OR_MORE', 'GRAPI_30_0_TO_34_9', 'PCT_OWN_OCC_HU', 'HU_VALUE_MEDIAN_DOLLARS']
df_income_housing = df[income_housing_columns].copy()

df_income_housing['PCT_BPOC'] = df_income_housing["PERSON_OF_COLOR"]/df_income_housing["TOTAL_POPULATION"]
df_income_housing['PCT_GRAPI_30'] = (df_income_housing["GRAPI_35_0_OR_MORE"]+df_income_housing["GRAPI_30_0_TO_34_9"])/df_income_housing["RENT_GRAPI_COMPUTED"]*100
df_population['PCT_Other_BPOC'] = df_population["PCT_HAWAIAN-PI"] + df_population["PCT_AMER-INDIAN"] + df_population["PCT_OTHER"]+ df_population["PCT_TWO_OR_MORE"]

# Select health related columns 

health_columns = ['NAMELSAD10', 'PCT_WHITE','PCT_BLACK', 
'PCT_AMER-INDIAN', 'PCT_ASIAN',   'PCT_HAWAIAN-PI','PCT_TWO_OR_MORE', 'PCT_HISP_ANY_RACE', 'PCT_OTHER','TOTAL_POPULATION', 'PERSON_OF_COLOR','PCT_ADULT_NOLEISUREPHYSACTIV', 'PCT_ADULT_WITH_DIABETES', 'PCT_ADULT_WITH_OBESITY',	'PCT_ADULT_MENTALHLTHNOTGOOD',	'PCT_ADULT_WITH_ASTHMA', 'LIFE_EXPECTANCY_AT_BIRTH', 'PCT_ADULT_WITH_DISABILITY' ,'SOCIOECON_DISADV_SCORE', 'HEALTH_DISADV_SCORE'
  ]

df_health = df_health_initial[health_columns].copy()
df_health['PCT_BPOC'] = df_health["PERSON_OF_COLOR"]/df_health["TOTAL_POPULATION"]

columns_to_multiply = ['PCT_ADULT_NOLEISUREPHYSACTIV', 'PCT_ADULT_WITH_DIABETES', 'PCT_ADULT_WITH_OBESITY',
                       'PCT_ADULT_MENTALHLTHNOTGOOD', 'PCT_ADULT_WITH_ASTHMA', 'PCT_ADULT_WITH_DISABILITY']

df_health.loc[:, columns_to_multiply] *= 100

# Display the first 6 rows of the new DataFrame

df_school_ass = pd.read_csv('Report_Card_Assessment_Data_2017-18_School_Year.csv')
df_school_teach = pd.read_csv('Report_Card_Teacher_Ratio_Program_Certificate_2017-18_School_Year.csv')
df_school_sites = pd.read_csv('School_Sites_in_King_County___schsite_point.csv')
df_school_pov = pd.read_csv('School_poverty.csv')
df_school_enroll = pd.read_csv('Report_Card_Enrollment_2017-18_School_Year.csv')
df_school_exp= pd.read_csv('expenditure.csv')



df_school_pov = df_school_pov[df_school_pov.DistrictName =='Seattle']
df_school_exp = df_school_exp[df_school_exp.DistrictName =='Seattle School District #1']
df_school_exp = df_school_exp[df_school_exp.OrganizationalLevel =='School']
df_school_exp = df_school_exp[df_school_exp.Activity =='Instruction']
df_school_exp = df_school_exp[df_school_exp.Source =='State/Local']
df_school_ass = df_school_ass[df_school_ass.GradeLevel =='All Grades']
df_school_ass = df_school_ass[df_school_ass.StudentGroup =='All Students']
df_school_ass = df_school_ass[df_school_ass.DistrictName =='Seattle School District No. 1']
df_school_enroll = df_school_enroll[df_school_enroll.County =='King']
df_school_enroll = df_school_enroll[df_school_enroll.GradeLevel =='AllGrades']


df_school_teach = df_school_teach[['SchoolName', 'AverageClassSize','DistrictName']]
df_school_teach = df_school_teach.drop_duplicates()
df_school_ass = df_school_ass[['SchoolName','PercentMetStandard', 'DistrictName', 'TestSubject']]
df_school = pd.merge(df_school_ass, df_school_teach, how='inner', on=['SchoolName', 'DistrictName'])
df_school = df_school.dropna(subset=['AverageClassSize'])

df_school = pd.merge(df_school, df_school_enroll, how='inner', on=['SchoolName', 'DistrictName'])
df_school = pd.merge(df_school, df_school_pov, how='inner', on=['SchoolName'])
df_school = pd.merge(df_school, df_school_exp, how='inner', on=['SchoolName'])



school_columns = ['SchoolName','PercentMetStandard','All Students', 'Homeless', 'Poverty - 10/1/2016', 'AverageClassSize', 'TestSubject', 'Expenditure']
df_school = df_school[school_columns]

df_school = df_school[df_school.PercentMetStandard.str.contains('%')]
df_school = df_school[df_school.PercentMetStandard.str.contains('<')==False]


school_tract= {'North Beach Elementary School': 'Census Tract 16', 'Seattle World School': 'Census Tract 79', 'Whitman Middle School': 'Census Tract 16', 'Chief Sealth International High School': 'Census Tract 114.01', 'Dunlap Elementary School': 'Census Tract 118', 'Bailey Gatzert Elementary School': 'Census Tract 90', 'Bryant Elementary School': 'Census Tract 42', 'West Seattle Elementary School': 'Census Tract 97.02', 'Private School Services': 'Census Tract 93', 'Laurelhurst Elementary School': 'Census Tract 41', 'Green Lake Elementary School': 'Census Tract 36', 'Viewlands Elementary School': 'Census Tract 36', 'Bridges Transition': 'Census Tract 89', 'Licton Springs K-8': 'Census Tract 32', 'Genesee Hill Elementary': 'Census Tract 97.02', 'Leschi Elementary School': 'Census Tract 78', 'John Hay Elementary School': 'Census Tract 68', 'Hamilton International Middle School': 'Census Tract 50', 'John Rogers Elementary School': 'Census Tract 8', 'Roxhill Elementary School': 'Census Tract 115', 'Maple Elementary School': 'Census Tract 93', 'McDonald International School': 'Census Tract 45', 'Gatewood Elementary School': 'Census Tract 106', 'Wing Luke Elementary School': 'Census Tract 117', 'Ingraham High School': 'Census Tract 6', 'Eckstein Middle School': 'Census Tract 38', 'Cascade Parent Partnership Program': 'Census Tract 36', 'Rainier View Elementary School': 'Census Tract 119', 'Ballard High School': 'Census Tract 33', 'Fairmount Park Elementary School': 'Census Tract 105', 'Lafayette Elementary School': 'Census Tract 98', 'Louisa Boren STEM K-8': 'Census Tract 108', 'Tops K-8 School': 'Census Tract 61', 'Mercer International Middle School': 'Census Tract 100.01', 'B F Day Elementary School': 'Census Tract 49', 'Alki Elementary School': 'Census Tract 97.01', 'Cleveland High School STEM': 'Census Tract 104.02', 'Washington Middle School': 'Census Tract 90', 'Garfield High School': 'Census Tract 88', 'The Center School': 'Census Tract 71', 'West Seattle High School': 'Census Tract 98', 'View Ridge Elementary School': 'Census Tract 39', 'Greenwood Elementary School': 'Census Tract 29', 'Daniel Bagley Elementary School': 'Census Tract 27', 'Madison Middle School': 'Census Tract 97.02', 'Olympic View Elementary School': 'Census Tract 19', 'Kimball Elementary School': 'Census Tract 110.02', 'Arbor Heights Elementary School': 'Census Tract 120', 'Concord International School': 'Census Tract 112', 'Franklin High School': 'Census Tract 95', 'Orca K-8 School': 'Census Tract 103', 'Lawton Elementary School': 'Census Tract 58.01', 'Jane Addams Middle School': 'Census Tract 10', 'Whittier Elementary School': 'Census Tract 30', 'Catharine Blaine K-8 School': 'Census Tract 57', 'McClure Middle School': 'Census Tract 68', 'Sacajawea Elementary School': 'Census Tract 20', 'Dearborn Park International School': 'Census Tract 104.01', 'Sand Point Elementary': 'Census Tract 41', 'Thurgood Marshall Elementary': 'Census Tract 95', 'Stevens Elementary School': 'Census Tract 64', 'Salmon Bay K-8 School': 'Census Tract 33', 'Interagency Open Doors': 'Census Tract 103', 'Adams Elementary School': 'Census Tract 32', 'David T. Denny International Middle School': 'Census Tract 114.01', 'Thornton Creek Elementary School': 'Census Tract 24', 'Loyal Heights Elementary School': 'Census Tract 31', 'Aki Kurose Middle School': 'Census Tract 103', 'Broadview-Thomson K-8 School': 'Census Tract 4.01', 'Emerson Elementary School': 'Census Tract 118', 'John Stanford International School': 'Census Tract 52', 'Pathfinder K-8 School': 'Census Tract 99', 'Queen Anne Elementary': 'Census Tract 67', 'Martin Luther King Jr. Elementary School': 'Census Tract 111.01', 'Roosevelt High School': 'Census Tract 26', 'Sanislo Elementary School': 'Census Tract 108', 'Highland Park Elementary School': 'Census Tract 113', 'Rainier Beach High School': 'Census Tract 118', 'Cascadia Elementary': 'Census Tract 50', 'Lowell Elementary School': 'Census Tract 65', 'Beacon Hill International School': 'Census Tract 94', 'Graham Hill Elementary School': 'Census Tract 111.02', 'Middle College High School': 'Census Tract 19', 'Northgate Elementary School': 'Census Tract 6', 'South Shore PK-8 School': 'Census Tract 118', 'Montlake Elementary School': 'Census Tract 62', 'McGilvra Elementary School': 'Census Tract 63', 'Nova High School': 'Census Tract 88', 'Hazel Wolf K-8': 'Census Tract 6', 'West Woodland Elementary School': 'Census Tract 34', 'John Muir Elementary School': 'Census Tract 95', 'Olympic Hills Elementary School': 'Census Tract 2', 'Frantz Coe Elementary School': 'Census Tract 59', 'Nathan Hale High School': 'Census Tract 10'}


df_school['PercentMetStandard'] = df_school.apply(lambda row: float(row.PercentMetStandard[:-1]), axis=1)


temp = df_school_sites ['SchoolName'].tolist()
temp = set(temp)

temp2 = df_school ['SchoolName'].tolist()
temp2 = set(temp2)

school_names = {}
for x in temp2:
     for y in temp:
        if y.casefold() in x.casefold() or x.casefold() in y.casefold():
             school_names[x] = y

df_school = df_school[df_school['SchoolName'].isin(school_names.keys())]


df_school['NAMELSAD10'] = df_school.apply(lambda row: school_tract[row.SchoolName], axis=1)



# Select income and housing columns
poc_columns = ['NAMELSAD10', 'TOTAL_POPULATION', 'PERSON_OF_COLOR']
df_poc_temp = df[poc_columns].copy()
df_poc_temp['PCT_BPOC'] = df_poc_temp["PERSON_OF_COLOR"]/df_poc_temp["TOTAL_POPULATION"]



df_school = pd.merge(df_school, df_poc_temp, how='inner', on=['NAMELSAD10'])




# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

fig_scatter_health = px.scatter(df_health, x='SOCIOECON_DISADV_SCORE', y='HEALTH_DISADV_SCORE', color='PCT_BPOC', opacity=0.3, color_continuous_scale='matter')
factors = ['PCT_ADULT_NOLEISUREPHYSACTIV', 'PCT_ADULT_WITH_DIABETES', 'PCT_ADULT_WITH_OBESITY',
               'PCT_ADULT_MENTALHLTHNOTGOOD', 'PCT_ADULT_WITH_ASTHMA', 'PCT_ADULT_WITH_DISABILITY']
fig_box_health = px.box(df_health, y=factors, title='Box Plot', labels={'value': 'Value of Factor'}, points=False)


fig_scatter_housing = px.scatter(df_income_housing, x='MEDIAN_HH_INC_PAST_12MO_DOLLAR', trendline='ols',y='PCT_GRAPI_30', color='PCT_BPOC', opacity=0.3,   color_continuous_scale='matter')
fig2_scatter_housing = px.scatter(df_income_housing, x='HU_VALUE_MEDIAN_DOLLARS', y='PCT_OWN_OCC_HU', color='PCT_BPOC', opacity=0.3,  color_continuous_scale='matter')


fig_box_education = px.scatter(df_income_housing, x='HU_VALUE_MEDIAN_DOLLARS', y='PCT_OWN_OCC_HU', color='PCT_BPOC', opacity=0.3,  color_continuous_scale='matter')
df_school_1 = df_school[df_school['TestSubject']=='ELA']
df_school_2 = df_school[df_school['TestSubject']=='Math']
fig_scatter_education= px.scatter(df_school_1, x='Expenditure', trendline='ols',y='PercentMetStandard', color='PCT_BPOC', opacity=0.3,   color_continuous_scale='matter')
fig_scatter_education2= px.scatter(df_school_2, x='Expenditure', trendline='ols',y='PercentMetStandard', color='PCT_BPOC', opacity=0.3,   color_continuous_scale='matter')

#fig_scatter_education.update_layout(coloraxis=dict(colorscale='matter'))



fig_scatter_education.update_coloraxes(showscale=False)

fig_scatter_education.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                              xaxis_title='Expenditure per Student',
                              yaxis_title='Pct. of Students Who Passed SBAC ELA Test',
                              width=230, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})
fig_scatter_education2.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                              xaxis_title='Expenditure per Student',
                              yaxis_title='Pct. of Students Who Passed SBAC Math Test',
                              width=400, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})
fig_scatter_education2.update_coloraxes(colorbar_thickness=15, colorbar_title='Percentage of BIPOC')
fig_box_education.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                         width=500, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})


# Define the app layout
app.layout = html.Div([dcc.Tabs(id='tabs', value='tab-1', children=[
    dcc.Tab(label='Housing', value='tab-1', children=[
        html.Div([
            html.Div([
                html.Div([
                    html.P(children='Click on the red brush (lasso select) and then select districts.', style={'font-family': 'Optima'}),
                    html.P(children='To add multiple selections, press Shift when making new selections. To clear a selection, double-click on the page.', style={'font-size': '13px', 'font-family': 'Optima'}),
                    dcc.Graph(id='choropleth-map-1', config={'displayModeBar': True}),
                ], style={'width': '100%'}),
                html.Div([
                    html.Div([
                        html.P('Select demographic groups:', style={'font-family': 'Optima'}),
                        dcc.Checklist(
                            id='race-selector-1',
                            options=[
                                {'label': [html.Span("Asian", style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_ASIAN'},
                                {'label': [html.Span('Black Non-Hispanic', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_BLACK'},
                                {'label': [html.Span('Latinx', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_HISP_ANY_RACE'},
                                {'label': [html.Span('Other BIPOC', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_Other_BPOC'},
                                {'label': [html.Span('White', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_WHITE'}
                            ],
                            value=['PCT_ASIAN'],
                        )
                    ]),
                    html.Div([
                        dcc.Graph(id='population-pie-1')
                    ]),
                ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'}),
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
            html.Div([
                html.Div([
                    dcc.Graph(id="income-rent-scatter-plot", figure=fig_scatter_housing),
                    
                ]),
                html.Div([
                    dcc.Graph(id="HU-price-owner-occupied-scatter-plot", figure=fig2_scatter_housing),
                ])
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'})
     ]),   
    dcc.Tab(label='Health', value='tab-2', children=[
        html.Div([
            html.Div([
                html.Div([
                    html.P(children='Click on the red brush (lasso select) and then select districts.', style={'font-family': 'Optima'}),
                    html.P(children='To add multiple selections, press Shift when making new selections. To clear a selection, double-click on the page.', style={'font-size': '13px', 'font-family': 'Optima'}),
                    dcc.Graph(id='choropleth-map-2', config={'displayModeBar': True}),
                ], style={'width': '100%'}),
                html.Div([
                    html.Div([
                        html.P('Select demographic groups:', style={'font-family': 'Optima'}),
                        dcc.Checklist(
                            id='race-selector-2',
                            options=[
                                {'label': [html.Span("Asian", style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_ASIAN'},
                                {'label': [html.Span('Black Non-Hispanic', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_BLACK'},
                                {'label': [html.Span('Latinx', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_HISP_ANY_RACE'},
                                {'label': [html.Span('Other BIPOC', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_Other_BPOC'},
                                {'label': [html.Span('White', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_WHITE'}
                            ],
                            value=['PCT_ASIAN'],
                        )
                    ]),
                    html.Div([
                        dcc.Graph(id='population-pie-2')
                    ]),
                ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'}),
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
            html.Div([
                html.Div([
                    dcc.Graph(id="scatter-plot-health",  figure=fig_scatter_health),
                   
                ]),
                html.Div([
                    dcc.Graph(id="box-plot-health", figure=fig_box_health),
                  
                ])
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'})
    ]),
    dcc.Tab(label='Education', value='tab-3', children=[
        html.Div([
            html.Div([
                html.Div([
                    html.P(children='Click on the red brush (lasso select) and then select districts.', style={'font-family': 'Optima'}),
                    html.P(children='To add multiple selections, press Shift when making new selections. To clear a selection, double-click on the page.', style={'font-size': '13px', 'font-family': 'Optima'}),
                    dcc.Graph(id='choropleth-map-3', config={'displayModeBar': True}),
                ], style={'width': '100%'}),
                html.Div([
                    html.Div([
                        html.P('Select demographic groups:', style={'font-family': 'Optima'}),
                        dcc.Checklist(
                            id='race-selector-3',
                            options=[
                                {'label': [html.Span("Asian", style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_ASIAN'},
                                {'label': [html.Span('Black Non-Hispanic', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_BLACK'},
                                {'label': [html.Span('Latinx', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_HISP_ANY_RACE'},
                                {'label': [html.Span('Other BIPOC', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_Other_BPOC'},
                                {'label': [html.Span('White', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_WHITE'}
                            ],
                            value=['PCT_ASIAN'],
                        )
                    ]),
                    html.Div([
                        dcc.Graph(id='population-pie-3')
                    ]),
                ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'}),
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id="scatter-plot-education",  figure=fig_scatter_education),
                    ]),
                    html.Div([
                        dcc.Graph(id="scatter-plot-education2",  figure=fig_scatter_education2),
                    ])
                ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'}),
                html.Div([
                    dcc.Graph(id="box-plot-education", figure=fig_box_education),
                  
                ])
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'})
    ]),
    dcc.Tab(label='Summary', value='tab-4', children=[
        html.Div([
            html.Div([
                html.Div([
                    html.P(children='Click on the red brush (lasso select) and then select districts.', style={'font-family': 'Optima'}),
                    html.P(children='To add multiple selections, press Shift when making new selections. To clear a selection, double-click on the page.', style={'font-size': '13px', 'font-family': 'Optima'}),
                    dcc.Graph(id='choropleth-map-4', config={'displayModeBar': True}),
                ], style={'width': '100%'}),
                html.Div([
                    html.Div([
                        html.P('Select demographic groups:', style={'font-family': 'Optima'}),
                        dcc.Checklist(
                            id='race-selector-4',
                            options=[
                                {'label': [html.Span("Asian", style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_ASIAN'},
                                {'label': [html.Span('Black Non-Hispanic', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_BLACK'},
                                {'label': [html.Span('Latinx', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_HISP_ANY_RACE'},
                                {'label': [html.Span('Other BIPOC', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_Other_BPOC'},
                                {'label': [html.Span('White', style={"font-size": '13px', 'font-family': 'Optima'})], 'value': 'PCT_WHITE'}
                            ],
                            value=['PCT_ASIAN'],
                        )
                    ]),
                    html.Div([
                        dcc.Graph(id='population-pie-4')
                    ]),
                ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'}),
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
            html.Div([
                html.Div([
                    dcc.Graph(id="radar-plot-summary"),
                   
                ]),
                html.Div([
                    dcc.Graph(id="box-plot-summary"),
                  
                ])
            ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '0px'}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '0px'})
    ])
  ])
])


# Function to update the choropleth map in Tab 1
@app.callback(
    Output('choropleth-map-1', 'figure'),
    Input('race-selector-1', 'value')
)
def update_choropleth_map_1(selected_race):
    selected_race.append('NAMELSAD10')
    df_population['Percentage'] = round(df_population [selected_race].sum(axis=1), 0)
    fig = px.choropleth(df_population, geojson=counties, color=df_population['Percentage'],
                        color_continuous_scale='deep', 
                        range_color=(min(df_population['Percentage'])-1,max(df_population['Percentage'])),
                        locations=df_population['NAMELSAD10'], featureidkey="properties.NAMELSAD10",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},width=450, height = 320, margin_pad=0)
    fig.update_layout(modebar_remove=['pan', 'select2d', 'toImage', 'zoomIn', 'zoomOut', 'autoScale','resetGeo', 'resetViewMapbox'], modebar_activecolor= 'red', modebar_color='#FF8A8A')
    fig.update_coloraxes(colorbar_thickness=10, colorbar_len=0.5, colorbar_dtick =10 ) 
    fig.update_layout(clickmode='event+select')
    
    return fig

# Function to update the pie chart in based on one selected district
@app.callback(
    Output('population-pie-1', 'figure'),
    Input('choropleth-map-1', 'selectedData')
)
def update_pie_chart_1(select_data):
    if  select_data is None:
        # If no district is selected, show an empty pie chart
        fig = go.Figure(data=go.Pie())
   
    else:
        temp_list = []
        for point in select_data['points']:
            temp_list.append(point['location'])
        district_data = df_abs_population[df_abs_population['NAMELSAD10'].isin(temp_list)]
        district_data = district_data.drop(columns='NAMELSAD10')
        if not district_data.empty:
            district_data_sum = district_data.sum()
            total_pop = district_data_sum['TOTAL_POPULATION']
            temp_array = np.array([
                district_data_sum['WHITE'] / total_pop,
                district_data_sum['BLACK'] / total_pop,
                district_data_sum['AMER-INDIAN'] / total_pop,
                district_data_sum['ASIAN'] / total_pop,
                district_data_sum['HAWAIAN-PI'] / total_pop,
                district_data_sum['TWO_OR_MORE_RACE'] / total_pop,
                district_data_sum['HISPANIC_OR_LATINO_OF_ANY_RACE'] / total_pop,
                district_data_sum['OTHER'] / total_pop
            ])
            fig = go.Figure(data=go.Pie(
                values=temp_array,
                labels=['White',  'Black Non-Hispanic', 'Indegenous', 'Asian', 'Pacific Islander', 'Multiracial', 'Latinx', 'Other'],
                #title="Population Distribution in Selected Census Tracts",
                marker=dict(
                    colors=['#FF6347', '#A52A2A', '#1E90FF', '#66CDAA', '#BA55D3', '#9ACD32', '#FFD700', '#4B0082']  # Fixed colors for each category
                ),
                #textfont_size=8,
                textinfo='none'
                
            ))
        else:
            # If no data is available for the selected district, show an empty pie chart
            fig = go.Figure(data=go.Pie())
    fig.update_layout(
        title_font_size=16,
        legend_font_size=9,
        title_font_family='Optima',
        width=300,
        height=300,
        margin={"r": 20, "t": 0, "l": 0, "b": 0},
        autosize=False
    )

    return fig

# Function to update the income-rent scatter plot
@app.callback(
    [Output('income-rent-scatter-plot', 'figure'), Output('HU-price-owner-occupied-scatter-plot', 'figure')],
    Input('choropleth-map-1', 'selectedData')
)
def update_scatter(select_data): #click_data is for clicking on a single district. Select data is for lasso selec
    fig = px.scatter(df_income_housing, x='MEDIAN_HH_INC_PAST_12MO_DOLLAR', trendline='ols',y='PCT_GRAPI_30', color='PCT_BPOC', opacity=0.3,   color_continuous_scale='matter')

    fig2 = px.scatter(df_income_housing, x='HU_VALUE_MEDIAN_DOLLARS', y='PCT_OWN_OCC_HU', color='PCT_BPOC', opacity=0.3,  color_continuous_scale='matter')


    selected_opacity = 1.0
    unselected_opacity = 0.3

    selected_geoids = []



    if select_data is not None:
        selected_geoids.extend([point['location'] for point in select_data['points']])

    if selected_geoids:
        selected_df = df_income_housing[df_income_housing['NAMELSAD10'].isin(selected_geoids)]
        fig.add_trace(go.Scatter(
            x=selected_df['MEDIAN_HH_INC_PAST_12MO_DOLLAR'],
            y=selected_df['PCT_GRAPI_30'],
            mode='markers',
            marker=dict(color=selected_df['PCT_BPOC'], opacity=selected_opacity, size = 10, colorscale='matter')
        ))
        
    if selected_geoids:
        selected_df = df_income_housing[df_income_housing['NAMELSAD10'].isin(selected_geoids)]
        fig2.add_trace(go.Scatter(
            x=selected_df['HU_VALUE_MEDIAN_DOLLARS'],
            y=selected_df['PCT_OWN_OCC_HU'],
            mode='markers',
            marker=dict(color=selected_df['PCT_BPOC'], opacity=selected_opacity, size = 10, colorscale='matter')
        ))



    fig.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima', width=500, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0},
                      xaxis_title="Median income of district in a year",
                      yaxis_title="Pct. of households with GRAPI > 30")
    fig.update_coloraxes(colorbar_thickness=15,  colorbar_title="Percentage of BIPOC" ) 

    
    
    fig2.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima', width=500, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0},
                       xaxis_title="Median house unit value",
                       yaxis_title="Pct. of houses occupied by owners")
    fig2.update_coloraxes(colorbar_thickness=15,  colorbar_title="Percentage of BIPOC" ) 


    return fig, fig2



# Function to update the choropleth map in Tab b
@app.callback(
    Output('choropleth-map-2', 'figure'),
    Input('race-selector-2', 'value')
)

def update_choropleth_map_2(selected_race):
    selected_race.append('NAMELSAD10')
    df_health['Percentage'] = round(df_health [selected_race].sum(axis=1), 0)
    fig = px.choropleth(df_health, geojson=counties, color=df_health['Percentage'],
                        color_continuous_scale='deep', 
                        range_color=(min(df_health['Percentage'])-1,max(df_health['Percentage'])),
                        locations=df_health['NAMELSAD10'], featureidkey="properties.NAMELSAD10",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},width=450, height = 320, margin_pad=0)
    fig.update_layout(modebar_remove=['pan', 'select2d', 'toImage', 'zoomIn', 'zoomOut', 'autoScale','resetGeo', 'resetViewMapbox'], modebar_activecolor= 'red', modebar_color='#FF8A8A')
    fig.update_coloraxes(colorbar_thickness=10, colorbar_len=0.5, colorbar_dtick =10 ) 
    fig.update_layout(clickmode='event+select')
    
    return fig



# Function to update the pie chart in based on one selected district
@app.callback(
    Output('population-pie-2', 'figure'),
   Input('choropleth-map-2', 'selectedData')
)
def update_pie_chart_2(select_data):
    if  select_data is None:
        # If no district is selected, show an empty pie chart
        fig = go.Figure(data=go.Pie())
   
    else:
        temp_list = []
        for point in select_data['points']:
            temp_list.append(point['location'])
        district_data = df_abs_population[df_abs_population['NAMELSAD10'].isin(temp_list)]
        district_data = district_data.drop(columns='NAMELSAD10')
        if not district_data.empty:
            district_data_sum = district_data.sum()
            total_pop = district_data_sum['TOTAL_POPULATION']
            temp_array = np.array([
                district_data_sum['WHITE'] / total_pop,
                district_data_sum['BLACK'] / total_pop,
                district_data_sum['AMER-INDIAN'] / total_pop,
                district_data_sum['ASIAN'] / total_pop,
                district_data_sum['HAWAIAN-PI'] / total_pop,
                district_data_sum['TWO_OR_MORE_RACE'] / total_pop,
                district_data_sum['HISPANIC_OR_LATINO_OF_ANY_RACE'] / total_pop,
                district_data_sum['OTHER'] / total_pop
            ])
            fig = go.Figure(data=go.Pie(
                values=temp_array,
                labels=['White',  'Black Non-Hispanic', 'Indegenous', 'Asian', 'Pacific Islander', 'Multiracial', 'Latinx', 'Other'],
                #title="Population Distribution in Selected Census Tracts",
                marker=dict(
                    colors=['#FF6347', '#A52A2A', '#1E90FF', '#66CDAA', '#BA55D3', '#9ACD32', '#FFD700', '#4B0082']  # Fixed colors for each category
                ),
                #textfont_size=8,
                textinfo='none'
                
            ))
        else:
            # If no data is available for the selected district, show an empty pie chart
            fig = go.Figure(data=go.Pie())
    fig.update_layout(
        title_font_size=16,
        legend_font_size=9,
        title_font_family='Optima',
        width=300,
        height=300,
        margin={"r": 20, "t": 0, "l": 0, "b": 0},
        autosize=False
    )

    return fig

# Function to update the scatter plot and box plot
@app.callback(
    [Output('scatter-plot-health', 'figure'), Output('box-plot-health', 'figure')],
    Input('choropleth-map-2', 'selectedData')
)
def update_plots(select_data):
    # Scatter plot
    fig_scatter = px.scatter(df_health, x='SOCIOECON_DISADV_SCORE', y='HEALTH_DISADV_SCORE', color='PCT_BPOC', opacity=0.3, color_continuous_scale='matter')

    # Box plot
    factors = ['PCT_ADULT_NOLEISUREPHYSACTIV', 'PCT_ADULT_WITH_DIABETES', 'PCT_ADULT_WITH_OBESITY',
           'PCT_ADULT_MENTALHLTHNOTGOOD', 'PCT_ADULT_WITH_ASTHMA', 'PCT_ADULT_WITH_DISABILITY']

    labels = {
    'PCT_ADULT_NOLEISUREPHYSACTIV': 'Sedentary Lifestyle',
    'PCT_ADULT_WITH_DIABETES': 'Diabetes',
    'PCT_ADULT_WITH_OBESITY': 'Obesity',
    'PCT_ADULT_MENTALHLTHNOTGOOD': 'Mental Distress',
    'PCT_ADULT_WITH_ASTHMA': 'Asthma',
    'PCT_ADULT_WITH_DISABILITY': 'Disability'
    }

    fig_box = px.box(df_health, y=factors, labels={'value': 'Percentage'}, points=False )

    fig_box.update_xaxes(
    tickmode='array',
    tickvals=factors,
    ticktext=[labels[factor] for factor in factors], 
    tickangle=-45

    )

    # Add interactive features
    selected_geoids = []
    if select_data is not None:
        selected_geoids.extend([point['location'] for point in select_data['points']])
    if selected_geoids:
        selected_df = df_health[df_health['NAMELSAD10'].isin(selected_geoids)]

        # Add the scatter point
        fig_scatter.add_trace(go.Scatter(x=selected_df['SOCIOECON_DISADV_SCORE'], y=selected_df['HEALTH_DISADV_SCORE'],
                                         mode='markers', marker=dict(color=selected_df['PCT_BPOC'], opacity=1.0, size=10, colorscale='matter'), showlegend=False))
        

        # Generate a list of random colors
        #num_colors = len(selected_geoids)
        #colors = [f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})' for _ in range(num_colors)]

        # Add a single point to the box plot for each selected district
        for i, district_geoid in enumerate(selected_geoids):
            district_data = df_health[df_health['NAMELSAD10'] == district_geoid]
            #color = colors[i]

            # Create a trace for all factors within the selected district
            factor_trace = go.Scatter(
                x=factors,
                y=district_data[factors].values[0],
                mode='markers',
                marker=dict(color='red', size=4),
                text = '',
                name = '',
                hovertemplate =str(district_geoid),  showlegend=False)
            

            fig_box.add_trace(factor_trace)

    fig_scatter.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                              xaxis_title='Socioeconomic Disadvantage Score',
                              yaxis_title='Health Disadvantage Score',
                              width=500, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})
    fig_scatter.update_coloraxes(colorbar_thickness=15, colorbar_title='Percentage of BIPOC')
    fig_box.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                         width=500, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})

    return fig_scatter, fig_box
    



# Function to update the choropleth map in Tab 
@app.callback(
    Output('choropleth-map-3', 'figure'),
    Input('race-selector-3', 'value')
)
def update_choropleth_map_3(selected_race):
    selected_race.append('NAMELSAD10')
    df_population['Percentage'] = round(df_population [selected_race].sum(axis=1), 0)
    fig = px.choropleth(df_population, geojson=counties, color=df_population['Percentage'],
                        color_continuous_scale='deep', 
                        range_color=(min(df_population['Percentage'])-1,max(df_population['Percentage'])),
                        locations=df_population['NAMELSAD10'], featureidkey="properties.NAMELSAD10",
                        projection="mercator")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},width=450, height = 320, margin_pad=0)
    fig.update_layout(modebar_remove=['pan', 'select2d', 'toImage', 'zoomIn', 'zoomOut', 'autoScale','resetGeo', 'resetViewMapbox'], modebar_activecolor= 'red', modebar_color='#FF8A8A')
    fig.update_coloraxes(colorbar_thickness=10, colorbar_len=0.5, colorbar_dtick =10 ) 
    fig.update_layout(clickmode='select')
    
    return fig

# Function to update the pie chart in based on one selected district
@app.callback(
    Output('population-pie-3', 'figure'),
    Input('choropleth-map-3', 'selectedData')
)
def update_pie_chart_3(select_data):
    if select_data is None:
        # If no district is selected, show an empty pie chart
        fig = go.Figure(data=go.Pie())
   
    else:
        temp_list = []
        for point in select_data['points']:
            temp_list.append(point['location'])
        district_data = df_abs_population[df_abs_population['NAMELSAD10'].isin(temp_list)]
        district_data = district_data.drop(columns='NAMELSAD10')
        if not district_data.empty:
            district_data_sum = district_data.sum()
            total_pop = district_data_sum['TOTAL_POPULATION']
            temp_array = np.array([
                district_data_sum['WHITE'] / total_pop,
                district_data_sum['BLACK'] / total_pop,
                district_data_sum['AMER-INDIAN'] / total_pop,
                district_data_sum['ASIAN'] / total_pop,
                district_data_sum['HAWAIAN-PI'] / total_pop,
                district_data_sum['TWO_OR_MORE_RACE'] / total_pop,
                district_data_sum['HISPANIC_OR_LATINO_OF_ANY_RACE'] / total_pop,
                district_data_sum['OTHER'] / total_pop
            ])
            fig = go.Figure(data=go.Pie(
                values=temp_array,
                labels=['White',  'Black Non-Hispanic', 'Indegenous', 'Asian', 'Pacific Islander', 'Multiracial', 'Latinx', 'Other'],
                #title="Population Distribution in Selected Census Tracts",
                marker=dict(
                    colors=['#FF6347', '#A52A2A', '#1E90FF', '#66CDAA', '#BA55D3', '#9ACD32', '#FFD700', '#4B0082']  # Fixed colors for each category
                ),
                #textfont_size=8,
                textinfo='none'
                
            ))
        else:
            # If no data is available for the selected district, show an empty pie chart
            fig = go.Figure(data=go.Pie())
    fig.update_layout(
        title_font_size=16,
        legend_font_size=9,
        title_font_family='Optima',
        width=300,
        height=300,
        margin={"r": 20, "t": 0, "l": 0, "b": 0},
        autosize=False
    )

    return fig

# Function to update the scatter plot and box plot
@app.callback(
    [Output('scatter-plot-education', 'figure'), Output('box-plot-e', 'figure')],
   Input('choropleth-map-3', 'selectedData')
)
def update_plots_education(select_data):
    
    fig_box_education = px.scatter(df_income_housing, x='HU_VALUE_MEDIAN_DOLLARS', y='PCT_OWN_OCC_HU', color='PCT_BPOC', opacity=0.3,  color_continuous_scale='matter')
    df_school_1 = df_school[df_school['TestSubject']=='ELA']
    df_school_2 = df_school[df_school['TestSubject']=='Math']
    fig_scatter_education= px.scatter(df_school_1, x='Expenditure', trendline='ols',y='PercentMetStandard', color='PCT_BPOC', opacity=0.3,   color_continuous_scale='matter')
    fig_scatter_education2= px.scatter(df_school_2, x='Expenditure', trendline='ols',y='PercentMetStandard', color='PCT_BPOC', opacity=0.3,   color_continuous_scale='matter')

    
    fig_scatter_education.update_coloraxes(showscale=False)

    fig_scatter_education.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                              xaxis_title='Expenditure per Student',
                              yaxis_title='Pct. of Students Who Passed SBAC ELA Test',
                              width=230, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})
    fig_scatter_education2.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                              xaxis_title='Expenditure per Student',
                              yaxis_title='Pct. of Students Who Passed SBAC Math Test',
                              width=400, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})
    fig_scatter_education2.update_coloraxes(colorbar_thickness=15, colorbar_title='Percentage of BIPOC')
    fig_box.update_layout(title_font_size=16, legend_font_size=9, title_font_family='Optima',
                         width=500, height=300, margin={"r": 0, "t": 10, "l": 0, "b": 0})







  
    return fig_scatter_education, fig_box_education
    

if __name__ == '__main__':
    app.run_server(mode='inline')