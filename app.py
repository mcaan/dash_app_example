
# coding: utf-8

# In[1]:

### Step 1

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)

server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv(
    'C://Users/Caanikaze/Documents/ESADE/CC/Final Project/nama_10_gdp_1_Data.csv')

df1 = df[df['UNIT'] == 'Current prices, million euro']
available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()

app.layout = html.Div([
    # Graph 1 - "scatterplot with two DropDown boxes for the different indicators. 
    # It will have also a slide for the different years in the data
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column-1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column-1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='scatterplot'),

    html.Div(dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(TIME): str(TIME) for TIME in df['TIME'].unique()}
    ),
            ),
    
    # Graph 2 - line chart with two DropDown boxes, one for the country 
    # and the other for selecting one of the indicators
    html.Div([
        
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column-2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '48%', 'marginTop': 40, 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column-2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
     dcc.Graph(id='line chart'),
    
    
    
])

# Callback for 'scatterplot'
@app.callback(
    dash.dependencies.Output('scatterplot', 'figure'),
    [dash.dependencies.Input('xaxis-column-1', 'value'),
     dash.dependencies.Input('yaxis-column-1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

# Callback for "line chart"
@app.callback(
    dash.dependencies.Output('line chart', 'figure'),
    [dash.dependencies.Input('xaxis-column-2', 'value'),
     dash.dependencies.Input('yaxis-column-2', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name):
    
    dff = df1[df1['GEO'] == yaxis_column_name]
    
    return {
        'data': [go.Scatter(
            x=dff['TIME'].unique(),
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

#run server for dashboard
if __name__ == '__main__':
    app.run_server()

