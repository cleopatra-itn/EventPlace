# EventPlace Demonstrator

## Link to the demonstrator
[https://entity-place.herokuapp.com/](https://entity-place.herokuapp.com/)

## Contributors
- Anna Jørgensen (ESR13): data extraction and processing, [WikiRevParser](https://github.com/ajoer/WikiRevParser), [visualizations](https://github.com/ajoer/EntityPlace/tree/master/map_code), web development, [demonstrator](https://entity-place.herokuapp.com/) infrastructure and deployment, and documentation.
- Sara Abdollahi (ESR2): location estimation

## Summary
This README describes one of the demonstrators created during the Cleopatra project. The development of this demonstrator has been funded by the European Union’s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement no. 812997.
The goal of the demonstrator is to enable new and innovative way of analysing events in a cross-cultural and temporal setting. The demonstrator visualizes the geographical movement of an event according to the entities used to describe the event. 
The description of an event on Wikipedia inevitably includes the mention of other related entities, but these are nether stable over time or across languages. Visualizing the development in the entities used in the event description on Wikipedia enables the discovery of cultural and temporal specificities in the understanding and reproduction of the event. 
The demonstrator can be used in a number or lagnuages and social science and humanities researchers are encouraged to apply cross-lingual analysis to the visualizations of the events. 

## Supported Languages
Visualization of events is conducted in four European Union languages of varying sizes, language families and alphabets: 
- NL (Dutch)
- DE (German)
- IT (Italian)
- EL (Greek)
More to be developed and deployed in the future.

## UI Functionalities
Currently, the demonstrator only supports the languages listed above.
It has the following UI functionalities:
- Visualization of the events in each of the lagnuages listed above;
- Timelapse visualization of the event;
- Visualization of the event at a praticular timestamp; 
- The user can choose whether to create a location-based visualization (aggregation of entities in the same location) or an entity-based visualization (several entities in the same location possible)
- Extraction and download of the visualization;
- Cross-cultural comparison of event development;

## Relevant Publications
- Forthcoming. 

## About this Repository

This repository makes available:
- [The Data 1](entity_data/): The extracted entiteis and their weights from Wikipedia for the supported languages as well as a few extra (Bulgarian, Hungarian, Croatian and Romanian). We hope to serve these lagnuages in the future in support of the Cleopatra ITN initiative to support new EU languages.
- [The Data 2](plotting_data/): All extracted entities with their entity type, frequency and locaiton. We use this data in the visualizations.
- [The Resources](resources/): TSV files with the names of each event on Wikipedia in the supported languages. We use this file from the initial data extraction from Wikipedia. extracted entiteis and their weights from Wikipedia for the supported languages as well as a few extra (Bulgarian, Hungarian, Croatian and Romanian). We hope to serve these lagnuages in the future in support of the Cleopatra ITN initiative to support new EU languages.
- [The Visualization Code](map_code/): Code for creating map visualizations using the data in plotting_data/ and the user selections.
- [The Main Code](.): app.py runs the code in map_code/ to generate the visualizations.
get_entities.py extracts entities from the revision histories extracted from Wikipedia and outputs the data in entity_data/.
- Additional Files: Procfile and requirements.txt are necessary for the app.py. README is this file.