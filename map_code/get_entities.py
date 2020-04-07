#!/usr/bin/python3
"""
	Extract links from each timestamp in the edit history.
"""
import argparse
import json
from collections import Counter, defaultdict

parser = argparse.ArgumentParser(description='''''')
parser.add_argument("topic", help="e.g. 'refugee_crisis'.")
parser.add_argument("--language", help="e.g. 'nl' (for debugging).")

args = parser.parse_args()

languages = ["de", "el", "hu", "it", "nl"] 

def open_file(event, language):

	print("\nLanguage:\t", language)
	print("Event:\t\t", event)

	file_name = "../newswork/data/%s/%s.json" % (event, language)
	data = json.load(open(file_name))
	return data

def save_to_json(event, language, dictionary): 
	''' save JSON dump to file '''

	directory_name = "data/%s/" % event
	
	file_name = "%s.json" % language
	with open(directory_name + file_name, 'w') as outfile:
		json.dump(dictionary, outfile, sort_keys=True, indent=4)

def get_link_frequencies(language, data):

	links_history = defaultdict()
	timestamps = list(data.keys())

	for t in timestamps:
		links_counter = Counter(data[t]["links"])
		total_count_links = sum(links_counter.values())
		
		links_data = dict()
		length_of_content = len(data[t]["content"])

		for link in links_counter:

			link_data = dict()
			frequency = links_counter[link]
			link_data["frequency"] = frequency
			link_data["relative_frequency_entities"] = 100 * (frequency/total_count_links)
			link_data["relative_frequency_content"] = 100 * (frequency/length_of_content)
			links_data[link] = link_data

		links_history[t] = links_data

	save_to_json("%s/" % args.topic, language, links_history)
		
	return links_history

def extract_entities(visualize=False):

	for language in languages:
		if args.language:
			if language != args.language: continue

		input_data = open_file(args.topic, language)
		get_link_frequencies(language, input_data)

		
if __name__ == "__main__":
	extract_entities()
	get_link_frequencies()
	save_to_json()
	open_file()
