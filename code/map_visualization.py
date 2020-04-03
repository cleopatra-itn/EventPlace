#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import argparse
import pandas as pd
import plotly.graph_objects as go
import random
import re

parser = argparse.ArgumentParser(description="Visualize entity locations in Wikipedia revision histories")
parser.add_argument("language", help="two/three letter language code, e.g. 'nl'.")
parser.add_argument("input_folder", default="arab_spring", help="folder with input data.")
parser.add_argument("visualization_focus", default="entities", help="visualize focus can be 'entities' or 'location' based.")

args = parser.parse_args()

class Visualize:

    def __init__(self):
        with open("resources/%s/%s.json" % (args.input_folder, args.language)) as f:
            self.data = json.load(f)
        self.focus = args.visualization_focus
        
        if self.focus == "entities":
            self.entitiesDB = dict() 
        
        # get visualization data for each month, and make visualization:
        for month in sorted(list(self.data.keys())): 
            if month != "2014_08": continue
            print(month)
            visualization_data = self._make_visualization_data(month)
            self._make_visualization(visualization_data)

    def _get_color(self, entity_type): 
        types_master = ['city', 'conflict', 'country', 'ethnic group', 'geographic region', 'human', 'organization', 'referendum', 'religion', 'resolution', 'social movement', 'square']
        colors = [i for i in range(len(types_master))] 
        color_n = types_master.index(entity_type)
        color = colors[color_n]
        return(color)

    def _check_entity_type(self, entity_type):
        type_mapping = {'resistance movement': 'conflict',
                        'civil resistance': 'conflict',
                        'civil disobedience': 'conflict',
                        'protest': 'conflict',
                        'war': 'conflict',
                        'continent': 'geographic region',
                        'county': 'geographic region',
                        'occupied territory': 'geographic region',
                        'geographic location': 'geographic region',
                        'geographic object': 'geographic region',
                        'geographical region': 'geographic region',
                        'district of libya': 'geographic region',
                        'province': 'geographic region',
                        'website': 'organization',
                        'organisation': 'organization',
                        'nonprofit organization': 'organization',
                        'terrorist organisation': 'organization',
                        'terrorrst organisation': 'organization',
                        'political party': 'organization',
                        'political union': 'organization',
                        'government agency': 'organization',
                        'islamic denomination': 'religion', #
                        'united nations security council resolution': 'resolution'}
        
        if entity_type in list(type_mapping.keys()):
            return type_mapping[entity_type]
        else:
            return entity_type

    def _check_same_location(self, lat, lon, stored_entity_info):
        return (   
            lat == stored_entity_info["latitude"] and 
            lon == stored_entity_info["longitude"]
        )

    def _make_visualization_data(self, month):

        if self.focus == "locations":
            visualization_data = self.locations_data(self.data[month])
            
        if self.focus == "entities":
            return self.entities_data(self.data[month])

    def _make_visualization(self, visualization_data):
        # todo: add title and legend

        if self.focus == "locations":
            self.locations_visualization(visualization_data)
            
        if self.focus == "entities":
            self.entities_visualization(visualization_data)

    def locations_data(self):
        visualization_data = dict()
        return visualization_data

    def entities_data(self, month_data):

        visualization_data = {"entities": [],
                        "latitudes": [],
                        "longitudes": [],
                        "entity_types": [],
                        "frequency": [],
                        "colors": []
                        }

        coordinates = set()

        entities_in_data = sorted(list(month_data.keys()))
        for entity in entities_in_data:

            lat = float(month_data[entity]["latitude"])
            lon = float(month_data[entity]["longitude"])
            
            # check if entity has been used in previous months with same location:
            if entity in self.entitiesDB.keys():

                if self._check_same_location(lat, lon, self.entitiesDB[entity]):
                    visualization_lat = self.entitiesDB[entity]["visualization_latitude"]
                    visualization_lon = self.entitiesDB[entity]["visualization_longitude"]

                    coordinates.add((lat, lon))
                else: 
                    print("%s has a new location!" % entity) 

            # check if the location has already been used in this month: 
            else:
                
                if (lat, lon) in coordinates:
                    smoothing = random.uniform(-2, 2)
                    visualization_lat = lat+smoothing
                    visualization_lon = lon-smoothing

                else:
                    visualization_lat = lat
                    visualization_lon = lon
                    coordinates.add((lat, lon))

                self.entitiesDB[entity] = {}
                self.entitiesDB[entity]["latitude"] = lat
                self.entitiesDB[entity]["longitude"] = lon
                self.entitiesDB[entity]["visualization_latitude"] = visualization_lat
                self.entitiesDB[entity]["visualization_longitude"] = visualization_lon

            visualization_data["entities"].append(entity)
            visualization_data["latitudes"].append(visualization_lat)
            visualization_data["longitudes"].append(visualization_lon)
            visualization_data["frequency"].append(month_data[entity]["frequency"]*8)

            entity_type = self._check_entity_type(month_data[entity]["type"].lower())
            visualization_data["entity_types"].append(entity_type)
            visualization_data["colors"].append(self._get_color(entity_type))

        assert(len(visualization_data["latitudes"]) == len(visualization_data["longitudes"]) == len(visualization_data["entities"]) == len(visualization_data["colors"]) == len(visualization_data["frequency"]))
        return visualization_data

    def entities_visualization(self, visualization_data):

        fig = go.Figure(go.Scattermapbox(
            mode = "markers",
            lon = visualization_data["longitudes"],
            lat = visualization_data["latitudes"],
            text = visualization_data["entities"],
            marker = go.scattermapbox.Marker(
                color = visualization_data["colors"],
                size = visualization_data["frequency"]
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

    def location_visualization(self, visualization_data):

        fig = go.Figure(go.Scattermapbox(
            mode = "markers",
            lon = visualization_data["longitudes"],
            lat = visualization_data["latitudes"],
            text = visualization_data["locations"],
            marker = go.scattermapbox.Marker(
                size = visualization_data["frequency"]
            )
        ))

        fig.update_layout(
            margin ={"l":0,"t":0,"b":0,"r":0},
            mapbox = {
                "center": {"lon": 10, "lat": 10},
                "style": "stamen-terrain",
                "center": {"lon": -20, "lat": -20},
                "zoom": 1}
        )

        fig.show()

v = Visualize()

# --------- for location based
# def get_locations_plotting_data(data):
#     # Get data for plotting locations. 
#     # The marker size is determined by the number of entities with that location.    
#     locations = list(data.keys())
#     latitudes = []
#     longitudes = []
#     entities = []
#     mentions = []

#     for entity in data:
#         latitudes.append(data[entity]["latitude"])
#         longitudes.append(data[entity]["longitude"])
#         entities.append(entity) #", ".join(list(data[location]["entity"].keys())))
#         mentions.append(data[entity]["mentions"]*10)
        
#     assert(len(latitudes) == len(longitudes) == len(locations) == len(entities) == len(mentions))

#     return latitudes, longitudes, locations, entities, mentions


# def plot_locations(month_data):
#     # Plot locations, with mentions as marker size 
#     latitudes, longitudes, locations, entities, mentions = get_locations_plotting_data(month_data)
    
