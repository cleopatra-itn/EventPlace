import map_visualization as mv
import pandas as pd
import plotly.graph_objects as go

v = mv.Visualize("arab_spring", "it", "entities")

visualization_data = v.visualization_data
entity_types = v.types
months = list(visualization_data.keys())
start_month = months[0]

def get_monthly_type_split_data():
    # split the data this way:
    # each month has a dictionary, where each key is a type (e.g. "Country") with its corresponding entities (e.g. "Iraq")
    # this is needed for the animation visualization. 

    month_types_dict = {}
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
                for indx in indices:
                
                    type_dict["entities"].append(visualization_data[month]["entities"][indx])
                    type_dict["latitudes"].append(visualization_data[month]["latitudes"][indx])
                    type_dict["longitudes"].append(visualization_data[month]["longitudes"][indx])
                    type_dict["frequencies"].append(visualization_data[month]["frequencies"][indx])

            if len(type_dict["entities"]) < 1: continue
            month_dict[entity_type] = type_dict
        month_types_dict[month] = month_dict
    return month_types_dict

def setup_fig_slider_dicts():
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    fig_dict["layout"]["width"] = 1400
    fig_dict["layout"]["height"] = 900
    fig_dict["layout"]["autosize"] = False
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["margin"] = {"l": 0,"t": 0,"b": 0,"r": 0}
    fig_dict["layout"]["mapbox"] = {
            "style": "stamen-terrain",
            "center": {"lon": 15, "lat": 18},
    		"zoom": 1
    	}
    fig_dict["layout"]["sliders"] = {
        "args": [
            "transition", {
                "duration": 0,
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
        "x": 0.02,
        "y": 0, 
        "currentvalue": {
       		"font": {"size": 20},
       		"prefix": "Month: ", 
            "visible": True, 
            "xanchor": "right"
        },  
        "len": 0.96
    }
    return fig_dict, sliders_dict

fig_dict, sliders_dict = setup_fig_slider_dicts()
# ------ FRAMES and DATA --------

month_types_dict = get_monthly_type_split_data()

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
import difflib
 
def make_frames():

    prev_month_frame = {"data": {}, "name": str()}
    for n,month in enumerate(months):
        frame = {"data": [], "name": str(month)}

        for entity_type in sorted(entity_types):
            if entity_type not in month_types_dict[month]:
                data_dict = {
                    "type": 'scattermapbox',
                    "mode": "markers",
                    "lat": [0.0],
                    "lon": [0.0],
                    "text": [],
                    "showlegend": True,
                    "opacity": 0,
                    "marker": {
                        "size": 0
                    },
                }
            else:
                data_dict = make_data_dict(month_types_dict[month][entity_type]) 
            data_dict["name"] = entity_type
            frame["data"].append(data_dict)    

            # month_0 is also the input for the start map, which can be animated by pressing "play"
            if n == 0:
                fig_dict["data"].append(data_dict)
        
        # Filter out months without changes
        if prev_month_frame["data"] == frame["data"]: continue

        fig_dict["frames"].append(frame)
        prev_month_frame = frame

        slider_step = {"args": [
        	[month],
        	{"frame": {"duration": 25, "redraw": True},
        	"mode": "immediate",
        	"transition": {"duration": 0}}
        ],
        	"label": month,
        	"method": "animate"}
        sliders_dict["steps"].append(slider_step)


def update_fig_dict():
    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig_dict["layout"]["legend"] = {
            "title": {"text": "Entity types"},
            "y": 0.5
    }
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [{
    			"args": [None, {"frame": {"duration": 100, "redraw": True},
                        "fromcurrent": True, 
                        "transition": {"duration": 0,
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
            "showactive": True,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": -0.2,
            "yanchor": "top"
    	}
    ]
    return fig_dict

make_frames() 
fig_dict = update_fig_dict()

fig = go.Figure(fig_dict)
fig.show() 


