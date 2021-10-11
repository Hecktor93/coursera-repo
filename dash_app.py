# Import required libraries
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Create a dash application
app = dash.Dash(__name__)
dropdown_list = [{'label': 'All Sites', 'value': 'ALL'}] + [ {'label':site, 'value' : 'site' + str(index)} for index, site in enumerate(pd.unique(spacex_df['Launch Site']))]
# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
        ),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
        dcc.Dropdown(id='site-dropdown',
            options=dropdown_list,
            value='ALL',
            placeholder="Select a Launch Site here",
            searchable=True
        ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id='success-pie-chart')),
        html.Br(),

        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
                value=[min_payload, max_payload]
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')
        ),
    ]
)

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        for index, site in enumerate(pd.unique(spacex_df['Launch Site'])):
            if 'site' + str(index) == entered_site:
                launch_site = site
        filtered_df1 = spacex_df[spacex_df['Launch Site'] == launch_site]
        filtered_df1['count'] = [1 for i in np.ones(filtered_df1[filtered_df1.columns[1]].count())]
        fig = px.pie(filtered_df1, values='count',
        names='class', 
        title='Total Success Launches for site ' + launch_site)
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_interval):
    print(payload_interval)
    filtered_df = spacex_df
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] > payload_interval[0]]
    filtered_df = filtered_df[filtered_df['Payload Mass (kg)'] < payload_interval[1]]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, y='class', 
        x='Payload Mass (kg)', color="Booster Version Category",
        title='Correlation between payload and success for all sites')
        return fig
    else:
        for index, site in enumerate(pd.unique(spacex_df['Launch Site'])):
            if 'site' + str(index) == entered_site:
                launch_site = site
        filtered_df1 = spacex_df[spacex_df['Launch Site'] == launch_site]
        filtered_df1 = filtered_df1[filtered_df1['Payload Mass (kg)'] > payload_interval[0]]
        filtered_df1 = filtered_df1[filtered_df1['Payload Mass (kg)'] < payload_interval[1]]
        filtered_df1['count'] = [1 for i in np.ones(filtered_df1[filtered_df1.columns[1]].count())]
        fig = px.scatter(filtered_df1, y='class', 
        x='Payload Mass (kg)', color="Booster Version Category",
        title='Correlation between payload and success for site ' + launch_site)
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
