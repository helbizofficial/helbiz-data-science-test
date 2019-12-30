# helbiz-data-science-test

This is the technical test for the position "Software Engineer, Data" at Helbiz. It's designed to show me your proficiency in API design, web scraping, cloud architecture, and general machine learning.

Design a system to read real-time data from all WASHINGTON GBFS feeds (see this repo: https://github.com/black-tea/swarm-of-scooters/blob/master/data/systems.csv), store in a db, and determine hotspots. A description of the design should include the tech stack, method of data collection and processing, cloud infrastructure used, and a general algorithm for hotspots - areas in the city that are most congested with scooters/bikes (hint: you should divide the map into equal hexagons of 75 meters to bunch coordinates together)

The components that should be developed are the web scraping and storing, as well as an API endpoint `/hotspots` that accepts parameters 
- geofence (string: `washington`)
- date (string: `2019-12-29`)

An example response for this endpoint could be a list of hexagon centers (lat/long) and their weight (relative to others) in terms of how congested they were for the given day.

You shouldn't take more than 5 hours to complete this, and any portion of it can be pseudo-code and/or generalized. Be prepared to discuss your solution during the follow-up call scheduled. 
