#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import re
import pandas as pd
import plotly.graph_objects as go

event = "mock"
with open("resources/%s.json" % event) as f:
  data = json.load(f)


def get_color(entity_type):
    types_master = ["EthnicGroup", "Country", "Event", "Person"]
    colors = ["darkorange", "cornflowerblue", "darkcyan", "plum"]

    color_n = types_master.index(entity_type)
    color = colors[color_n]
    return(color)

def get_entities_plotting_data(data):
    # Get data for plotting each entity. 
    # Entity types will be plotted in different colors.    
    locations = list(data.keys())
    latitudes = []
    longitudes = []
    entities = []
    colors = []

    for location in locations:
        entities_at_location = list(data[location]["entity"].keys())
        entity_types_at_location = list(data[location]["entity"].values())

        for e,t in zip(entities_at_location, entity_types_at_location):
            entities.append(e)
            regularizer = entities_at_location.index(e)*0.7
            latitudes.append(data[location]["latitude"]+regularizer)
            longitudes.append(data[location]["longitude"]+regularizer)
            colors.append(get_color(t))
        
    assert(len(latitudes) == len(longitudes) == len(entities) == len(colors))

    return latitudes, longitudes, entities, colors

def get_locations_plotting_data(data):
    # Get data for plotting locations. 
    # The marker size is determined by the number of entities with that location.    
    locations = list(data.keys())
    latitudes = []
    longitudes = []
    entities = []
    mentions = []

    for location in locations:
        latitudes.append(data[location]["latitude"])
        longitudes.append(data[location]["longitude"])
        entities.append(", ".join(list(data[location]["entity"].keys())))
        mentions.append(data[location]["mentions"]*10)
        
    assert(len(latitudes) == len(longitudes) == len(locations) == len(entities) == len(mentions))

    return latitudes, longitudes, locations, entities, mentions

def plot_entities():
    # Plot individual entities, with color per type
    latitudes, longitudes, entities, colors = get_entities_plotting_data(data)

    fig = go.Figure(go.Scattermapbox(
        mode = "markers",
        lon = longitudes,
        lat = latitudes,
        text = entities,
        marker = go.scattermapbox.Marker(
            color = colors,
            size = 10
        )
    ))

    fig.update_layout(
        margin ={"l":0,"t":0,"b":0,"r":0},
        mapbox = {
            "center": {"lon": 10, "lat": 10},
            "style": "stamen-terrain",
            "center": {"lon": -20, "lat": -20},
            "zoom": 1})

    fig.show()

def plot_locations():
    # Plot locations, with mentions as marker size 
    latitudes, longitudes, locations, entities, mentions = get_locations_plotting_data(data)
    
    fig = go.Figure(go.Scattermapbox(
        mode = "markers",
        lon = longitudes,
        lat = latitudes,
        text = entities,
        marker = go.scattermapbox.Marker(
            size = mentions
        )
    ))

    fig.update_layout(
        margin ={"l":0,"t":0,"b":0,"r":0},
        mapbox = {
            "center": {"lon": 10, "lat": 10},
            "style": "stamen-terrain",
            "center": {"lon": -20, "lat": -20},
            "zoom": 1})

    fig.show()

# ----- Plot individual entities, with color per type
#plot_entities()

# ----- Plot locations, with mentions as marker size 
plot_locations()
