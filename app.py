#!/usr/bin/python3
# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import map_code.map_visualization as mv
import map_code.map_timelapse as mt
import os
import pandas as pd
import plotly.graph_objects as go

from dash.dependencies import Input, Output

def get_figure(language, focus):
	print("\nlanguage:", language, "\nfocus:", focus, "\n")
	if language == "initial" or focus == "initial":
		
		fig = go.Figure(go.Scattermapbox(
			mode = "markers"))

		fig.update_layout(
			margin = {"l":200,"t":0,"b":0,"r":300},
			mapbox = {
				"style": "stamen-terrain",
				"center": {"lon": 15, "lat": 18},
				"zoom": 1}
		)
		return fig
	#if duration == "single_month":
	#	return mv.Visualize(event, language, focus, "2014_08", show=False).fig # 2014_08 | 2011_05
	#else:
	return mt.Timelapse("arab_spring", language, focus, show=False).fig

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # the Flask app

introduction = '''
### EventPlace timelapse map visualizations

Explore the Arab Spring through timelapse visualizations.

This tool allows you to scroll through the development of the Arab Spring and compare the narration of the event across different languages.

The visualizations are built using the revision histories of Wikipedia and you can choose which language version you want to visualize.

You can also choose whether you want the entities to be in focus or the locations.
The size of the dots indicate the importance of the entity or location at each time point.

Play around with the tool to discover its capabilities!

Once the timelapse is visible, use the play/pause buttons and the slider below to scroll through the movement of the event over time.

You can download individual frames of the visualization, and you are welcome to use them under the MIT licence. 

'''

outro = ''' 
The visualizations have been built using all open source data and software: Wikipedia, Wikidata, Plotly, Dash, Pandas, WikiRevParser, the Wikipedia API.

Copyright (c) Sara Abdollahi and Anna Jørgensen. Contact a \[dot\] jorgensen \[at\] uva \[dot\] nl for issues and questions.

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No 812997.
''' 
    
app.layout = html.Div([

	dcc.Markdown(children=introduction), 

	# html.Div([
 #        dcc.Dropdown(
        	
	#         ],
	#         value = 'initial'
	#     ),
 #    ], style={'width': '90%', 'display': 'inline-block'}),
	

	html.Div([
    	dcc.Dropdown(
    		# id = "event",
      #   	options = [
	     #        {'label': 'Choose event', 'value': 'initial'},
	     #        {'label': 'Arab Spring', 'value': 'arab_spring'},
	     #        {'label': 'Refugee Crisis \[coming\]', 'value': 'refugee_crisis'},
	     #        {'label': 'COVID-19 \[coming\]', 'value': 'covid19'}
	        id = "language",
	        options = [
	            {'label': 'Choose language', 'value': 'initial'},
	            {'label': 'Dutch', 'value': 'nl'},
	            {'label': 'Italian', 'value': 'it'},
	            {'label': 'German', 'value': 'de'},
	            {'label': 'Greek', 'value': 'el'}
	        ],
	        value = 'initial'
		),
	], style={'width': '45%', 'display': 'inline-block'}),

	html.Div([
    	dcc.Dropdown(
        	id = "focus",
	        options = [
	        	{'label': 'Choose focus', 'value': 'initial'},
	            {'label': 'Entity based', 'value': 'entity'},
	            {'label': 'Location based', 'value': 'location'}
	        ],
	        value = "initial"
	    )
    ], style={'width': '45%', 'display': 'inline-block', 'justify-content': 'right'}),

	dcc.Graph(id = "visualization"),

	dcc.Markdown(children=outro)
])

@app.callback(
    Output('visualization', 'figure'),
    [Input('language', 'value'),
     Input('focus', 'value')])


def update_graph(language, focus):
	return get_figure(language, focus)

if __name__ == '__main__':
    app.run_server(debug=True)