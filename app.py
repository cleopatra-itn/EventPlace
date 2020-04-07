#!/usr/bin/python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import map_code.map_visualization as mv
import map_code.map_timelapse as mt
import os
import pandas as pd

from dash.dependencies import Input, Output

def get_figure(event, language, method, duration):
	print("event", event, "language", language, "method", method)
	if duration == "single_month":
		return mv.Visualize(event, language, method, "2014_08", show=False).fig
	else:
		return mt.Timelapse(event, language, method, show=False).fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # the Flask app

introduction = '''
### EventPlace map visualizations

Use the options to create animations of the development of a Wikipedia page.
'''
    
app.layout = html.Div([

	dcc.Markdown(children=introduction), 

	html.Div([
    	dcc.Dropdown(
    		id = "event",
        	options = [
	            {'label': 'Arab Spring', 'value': 'arab_spring'},
	            {'label': 'Refugee Crisis', 'value': 'refugee_crisis'},
	            {'label': 'COVID-19', 'value': 'covid19'}
	        ],
	        value = 'arab_spring'
		),
		dcc.RadioItems(
        	id = "method",
	        options = [
	            {'label': 'Entity based', 'value': 'entities'},
	            {'label': 'Location based', 'value': 'location'}
	        ],
	        value = 'entities'
	    )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
        	id = "language",
	        options = [
	            {'label': 'Dutch', 'value': 'nl'},
	            {'label': 'Italian', 'value': 'it'},
	            {'label': 'German', 'value': 'de'}
	        ],
	        value = 'nl'
	    ),
	    dcc.RadioItems(
        	id = "duration",
	        options = [
	            {'label': 'Month', 'value': 'single_month'},
	            {'label': 'Timelapse', 'value': 'timelapse'}
	        ],
	        value = 'timelapse'
	    )
    ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

    html.Div([
        
    ]),
	
	dcc.Graph(id = "visualization")
])
	
@app.callback(
    Output('visualization', 'figure'),
    [Input('event', 'value'),
     Input('language', 'value'),
     Input('method', 'value'),
     Input('duration', 'value')])

def update_graph(event, language, method, duration):
	return get_figure(event, language, method, duration)

if __name__ == '__main__':
    app.run_server(debug=True)