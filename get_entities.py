#!/usr/bin/python3
"""
	Input event, language (optional). 
	It reads the event page title in the different languages from a tsv file (language\ttitle). This an be retrieved with the sparql query here below.
	Scrapes Wikipedia revision history from an event.
	Extract links from each timestamp in the edit history.
	Outputs JSON
"""
import argparse
import json
from collections import Counter, defaultdict
from WikiRevParser.wikirevparser import wikirevparser

parser = argparse.ArgumentParser(description='''''')
parser.add_argument("event", help="e.g. 'refugee_crisis'.")
parser.add_argument("--language", help="e.g. 'nl' (for debugging).")

args = parser.parse_args()

sparql_query = """
SELECT DISTINCT ?lang ?name WHERE {
  ?article schema:about wd:Q33761 ;  
           schema:inLanguage ?lang ;
           schema:name ?name ;
           schema:isPartOf [ wikibase:wikiGroup "wikipedia" ] .
  FILTER (!CONTAINS(?name, ':')) .
}
"""
languages = ["sl", "ro", "hr", "bg", "de", "el", "hu", "it", "nl"]

def save_to_json(event, language, dictionary): 
	''' save JSON dump to file '''

	directory_name = "entity_data/%s/" % args.event
	
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

	save_to_json("entity_data/%s" % args.event, language, links_history)
		
	return links_history

def main():

	input_data = open("resources/events/%s.tsv" % args.event).readlines()

	for line in sorted(input_data):
		try:
			language, title = line.split('\t')[0], line.split('\t')[1].strip()
		except IndexError:
			language, title = line.split(',')[0], line.split(',')[1].strip()
		if language not in languages: continue
		if args.language:
			if language != args.language: continue

		print("\nLanguage:\t", language)
		print("Title:\t\t", title)

		parser_instance = wikirevparser.ProcessRevisions(language, title)

		page = parser_instance.wikipedia_page()
		if page == None: continue

		data = parser_instance.parse_revisions()
		if data == None: continue

		get_link_frequencies(language, data)
		
if __name__ == "__main__":
	main()
