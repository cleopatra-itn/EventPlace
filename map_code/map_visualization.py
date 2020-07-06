#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""



"""
import json
import pandas as pd
import plotly.graph_objects as go
import random
import re

class Visualize:

    def __init__(self, event, language, focus, visualize_month=False, show=False):
        self.event = event
        self.language = language
        self.focus = focus

        if self.focus == "entities":
            self.types = [
                'city', 'conflict', 'country', 'ethnic group', 'geographic region', 'human', 
                'organization', 'referendum', 'religion', 'resolution', 'social movement', 'square'
            ]
            self.entitiesDB = dict() 

        with open("plotting_data/%s/%s.json" % (self.event, self.language)) as f:
            self.input_data = json.load(f)
        
        self.data = dict()
        for month in sorted(list(self.input_data.keys())): 
            if visualize_month:
                if month != visualize_month: continue
            visualization_data = self._make_visualization_data(month)
            self.data[month] = visualization_data
            self.fig = self._make_visualization(visualization_data, show=show)
                
            if show == True:
                self.fig.show()

    def _get_color(self, entity_type): 
        colors = [i for i in range(len(self.types))] 
        color_n = self.types.index(entity_type)
        color = colors[color_n]
        return(color)

    def _get_label(self, entities, location):
        
        entities = sorted([x for x in entities if x != location])
        if len(entities) != 0:
            label = location + " -- " + ", ".join(entities)
        else:
            label = location
        return label

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
                        'islamic denomination': 'religion',
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
            return self.locations_data(self.input_data[month])
            
        if self.focus == "entities":
            return self.entities_data(self.input_data[month])

    def _make_visualization(self, visualization_data, show):

        if self.focus == "locations":
            return self.locations_visualization(visualization_data)
            
        if self.focus == "entities":
            return self.entities_visualization(visualization_data)
        
    def locations_data(self, month_data):

        visualization_data = {"locations": dict(),
                        "location_labels": [],
                        "latitudes": [],
                        "longitudes": [],
                        "frequencies": []
                        }

        entities_in_data = sorted(list(month_data.keys()))

        coordinates = set()
        for entity in entities_in_data:

            lat = float(month_data[entity]["latitude"])
            lon = float(month_data[entity]["longitude"])
            location = month_data[entity]["location"]
            frequency = month_data[entity]["frequencies"]

            if (lat, lon) not in coordinates:
                visualization_data["latitudes"].append(lat)
                visualization_data["longitudes"].append(lon)
                visualization_data["frequencies"].append(frequency)
                visualization_data["locations"][location] = set()

                coordinates.add((lat, lon))

            visualization_data["locations"][location].add(entity)
            indx = visualization_data["latitudes"].index(lat)
            visualization_data["frequencies"][indx] += frequency

        # increase marker size
        for n,frequency in enumerate(visualization_data["frequencies"]):
            frequency += 8  
            visualization_data["frequencies"][n] = frequency

        # make location label for visualization
        for location in visualization_data["locations"]:
            label = self._get_label(visualization_data["locations"][location], location)
            visualization_data["location_labels"].append(label) 

        assert(
            len(visualization_data["latitudes"]) == 
            len(visualization_data["longitudes"]) == 
            len(visualization_data["locations"]) == 
            len(visualization_data["frequencies"])
            )
        return visualization_data

    def entities_data(self, month_data):

        visualization_data = {"entities": [],
                        "latitudes": [],
                        "longitudes": [],
                        "entity_types": [],
                        "frequencies": [],
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
            visualization_data["frequencies"].append(month_data[entity]["frequency"]*8)

            entity_type = self._check_entity_type(month_data[entity]["type"].lower())
            visualization_data["entity_types"].append(entity_type)
            visualization_data["colors"].append(self._get_color(entity_type))

        assert(
            len(visualization_data["latitudes"]) == 
            len(visualization_data["longitudes"]) == 
            len(visualization_data["entities"]) == 
            len(visualization_data["colors"]) == 
            len(visualization_data["frequencies"])
        )
        return visualization_data

    def entities_visualization(self, visualization_data):

        fig = go.Figure(go.Scattermapbox(
            mode = "markers",
            lon = visualization_data["longitudes"],
            lat = visualization_data["latitudes"],
            text = visualization_data["entities"],
            marker = go.scattermapbox.Marker(
                color = visualization_data["colors"],
                size = visualization_data["frequencies"]
            )
        ))

        fig.update_layout(
            margin = {"l":0,"t":0,"b":0,"r":0},
            mapbox = {
                "style": "stamen-terrain",
                "center": {"lon": 15, "lat": 18},
                "zoom": 1}
        )
        return fig
        
    def locations_visualization(self, visualization_data):

        fig = go.Figure(go.Scattermapbox(
            mode = "markers",
            lon = visualization_data["longitudes"],
            lat = visualization_data["latitudes"],
            text = visualization_data["location_labels"],
            marker = go.scattermapbox.Marker(
                size = visualization_data["frequencies"]
            )
        ))

        fig.update_layout(
            margin = {"l":0,"t":0,"b":0,"r":0},
            mapbox = {
                "style": "stamen-terrain",
                "center": {"lon": 15, "lat": 18},
                "zoom": 1}
        )
        return fig
