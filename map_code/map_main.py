import argparse
import map_visualization as mv
import map_timelapse as mt

parser = argparse.ArgumentParser(description='''Make and save images/timelapse for Demonstrator.''')
parser.add_argument("event", help="The event to visualize, e.g. 'arab_spring'.")
parser.add_argument("method", help="The method to apply to the visualizations, either 'entities' or 'location'.")
parser.add_argument("language", help="The language to visualize, e.g. 'nl'.")
parser.add_argument("output_format", help="The format of the output, either 'images' or 'timelapse'.")

args = parser.parse_args()

def main():
	print("event", args.event, "language", args.language, "method", output_format)
	if output_format == "images":
		mv.Visualize(event, language, method, show=False)
	else:
		mt.Timelapse(event, language, method, show=False)

if __name__ == '__main__':
	main()