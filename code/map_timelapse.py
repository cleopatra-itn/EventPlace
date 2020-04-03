import map_visualization as mv
import pandas as pd
import plotly.graph_objects as go

v = mv.Visualize("arab_spring", "it", "entities")
visualization_data = v.visualization_data

entity_types = v.types
months = list(visualization_data.keys())

month_types_dict = {}
#all entities and their lon, lat and frequency for the type in the month
for month in months:
    month_dict = {}
    for entity_type in entity_types:
        type_dict = {  
            "entities": [],
            "latitudes": [],
            "longitudes": [],
            "frequencies": []
        }
        if entity_type in visualization_data[month]["entity_types"]:
            indices = [i for i, x in enumerate(visualization_data[month]["entity_types"]) if x == entity_type]
            for indx in indices: #= visualization_data[month]["entity_types"].index(entity_type)
            
                type_dict["entities"].append(visualization_data[month]["entities"][indx])
                type_dict["latitudes"].append(visualization_data[month]["latitudes"][indx])
                type_dict["longitudes"].append(visualization_data[month]["longitudes"][indx])
                type_dict["frequencies"].append(visualization_data[month]["frequencies"][indx])
        if len(type_dict["entities"]) < 1: continue
        month_dict[entity_type] = type_dict
    month_types_dict[month] = month_dict

start_month = months[0]

fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

fig_dict["layout"]["width"] = 800
fig_dict["layout"]["autosize"] = True
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["mapbox"] = {
        "center": {"lon": 10, "lat": 10},
        "style": "stamen-terrain",
        "center": {"lon": -20, "lat": -20},
		"zoom": 3
	}
fig_dict["layout"]["sliders"] = {
    "args": [
        "transition", {
            "duration": 400,
            "easing": "cubic-in-out"
        }
    ],
    "initialValue": start_month,
    "plotlycommand": "animate",
    "values": months,
    "visible": True
}

sliders_dict = {
	"steps": [], 
    "transition": {"duration": 0},
    "x": 0,#slider starting position  
    "y": 0, 
    "currentvalue": {
   		"font": {"size": 20},
   		"prefix": "Month:", 
        "visible": True, 
        "xanchor": "right"
    },  
    "len": 1.0
}

def make_data_dict(month_data):
    return {
        "type": 'scattermapbox',
        "mode": "markers",
        "lat": month_data["latitudes"],
        "lon": month_data["longitudes"],
        "text": month_data["entities"],
        "marker": {
            "size": month_data["frequencies"]
        },
    } 

# data
for entity_type in month_types_dict[start_month]:
    data_dict = make_data_dict(month_types_dict[start_month][entity_type]) 
    data_dict["name"] = entity_type    
    fig_dict["data"].append(data_dict)

# frames
for n,month in enumerate(months):
    frame = {"data": [], "name": str(month)}
    for entity_type in month_types_dict[month]:
        data_dict = make_data_dict(month_types_dict[month][entity_type]) 
        data_dict["name"] = entity_type
        frame["data"].append(data_dict)    
    fig_dict["frames"].append(frame)
        # if n == 0:
        #     fig_dict["data"].append(data_dict)

    slider_step = {"args": [
    	[month],
    	{"frame": {"duration": 300, "redraw": True},
    	"mode": "immediate",
    	"transition": {"duration": 300}}
    ],
    	"label": month,
    	"method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [{
			"args": [None, {"frame": {"duration": 500, "redraw": True},
                    "fromcurrent": True, 
                    "transition": {"duration": 300,
                    "easing": "quadratic-in-out"}}],
            "label": "Play",
            "method": "animate"
            },
            {
            "args": [[None], {"frame": {"duration": 0, "redraw": True},
                    "mode": "immediate",
                    "transition": {"duration": 0}}],
            "label": "Pause",
            "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
	}]

fig=go.Figure(fig_dict) #["data"], layout=layout, frames=fig_dict["frames"])
fig.show() 


