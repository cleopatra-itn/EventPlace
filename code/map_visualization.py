#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import re

import pandas as pd

import plotly.graph_objects as go

event = "mock_plotting_data2"
with open("%s.json" % event) as f:
  data = json.load(f)

def extract_plotting_data(data):

    locations = list(data.keys())
    latitudes = []
    longitudes = []
    mentions = []
    entities = []
    types = []

    for location in locations:
        latitudes.append(data[location]["longitude"])
        longitudes.append(data[location]["latitude"])
        mentions.append(data[location]["mentions"]*10)
        entities.append(data[location]["entity"].keys())
        types.append(data[location]["entity"].values())
        
    assert(len(latitudes) == len(longitudes) == len(mentions))

    return locations, latitudes, longitudes, mentions, entities, types

locations, latitudes, longitudes, mentions, entities, types = extract_plotting_data(data)

fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = longitudes,
    lat = latitudes,
    marker = {'size': mentions},
))

fig.update_layout(
    margin ={"l":0,"t":0,"b":0,"r":0},
    mapbox = {
        "center": {"lon": 10, "lat": 10},
        "style": "stamen-terrain",
        "center": {"lon": -20, "lat": -20},
        "zoom": 1})

fig.show()