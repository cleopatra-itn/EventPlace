#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import map_visualization as mv

parser = argparse.ArgumentParser(description="Visualize entity locations in Wikipedia revision histories")
parser.add_argument("language", default="nl", help="two/three letter language code, e.g. 'nl'.")
parser.add_argument("input_folder", default="arab_spring", help="folder with input data.")
parser.add_argument("visualization_focus", default="entities", help="visualize focus can be 'entities' or 'location' based.")

args = parser.parse_args()

v = mv.Visualize(args.input_folder, args.language, args.visualization_focus, show=True)

