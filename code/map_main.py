#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import map_visualization as mv
import map_timelapse as mt

parser = argparse.ArgumentParser(description="Visualize entity locations in Wikipedia revision histories")
parser.add_argument("input_folder", default="arab_spring", help="folder with input data.")
parser.add_argument("language", default="nl", help="two/three letter language code, e.g. 'nl'.")
parser.add_argument("visualization_focus", default="entities", help="visualize focus can be 'entities' or 'location' based.")
parser.add_argument("visualization_type", default="visualization", help="visualizatioin or timelapse.")

args = parser.parse_args()

if args.visualization_type == "visualization":
	v = mv.Visualize(args.input_folder, args.language, args.visualization_focus, "2014_08", show=True)
else:
	v = mt.Timelapse(args.input_folder, args.language, args.visualization_focus, show=True)
