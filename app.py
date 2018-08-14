import numpy as np
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import bls
import pickle #using pickled dataframe to avoid over querying api

with open('bls-series-data.pickle', 'rb') as f:
    bls_data = pickle.load(f)

df = pd.read_excel('cesseriespub.xlsx',
    sheet_name='CES_Pub_NAICS_17',
    header=1,
    index_col=0)
super_sectors = df.index.str.contains('\d[0|5]-000000')

app = dash.Dash()
app.layout = html.Div([
    html.H1('BLS Series Report'),
    dcc.Dropdown(
        id='series-sel',
        options = [{'label': '{}{}'.format('-'*row.display_level,
            row.CES_Industry_Title), 'value': row.CES_Industry_Title }
            for row in df[df['display_level'] != 7 ]
            .itertuples()],
        multi=False,
        value='Total nonfarm'

    ),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    [Input('series-sel', 'value')]
)
def update_figure(sel):
    sel_code = df[df['CES_Industry_Title'] == sel].index[0]
    series = ['CES{}01'.format(i.replace('-',''))
        for i in df[df['Next_Highest_Pub_Level'] == sel_code].index.values]
    #import pdb; pdb.set_trace()
    #bls_api_df = bls.get_series(series, startyear=2017)
    bls_api_df = bls_data[series]
    traces = []
    for col in bls_api_df.columns:
        industry_code = str(col[3:5]) + '-' + str(col[5:11])
        traces.append(go.Scatter(
            x=bls_api_df.index.to_timestamp(),
            y=bls_api_df[col],
            name=df.loc[industry_code]['CES_Industry_Title']
        ))
    layout = go.Layout(
        xaxis={
            'title': 'Period'
        },
        yaxis={
            'title': 'Employment'
        }

    )
    #import pdb; pdb.set_trace()
    figure = go.Figure(data=traces)
    return figure
if __name__ == '__main__':
    app.run_server(debug=True)
