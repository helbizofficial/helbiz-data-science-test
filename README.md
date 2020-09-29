# helbiz-software-engineer-data-internship-test

This is the technical test for the position "Software Engineer Intern, Data" at Helbiz. It's designed to test your proficiency in web scraping, ETL design, data manupilation, cloud architecture, and data reporting.

Design a system to read the data from all Los Angeles GBFS feeds (see this repo: https://github.com/black-tea/swarm-of-scooters/blob/master/data/systems.csv), aggregate the data spatially + count the num. bikes in each spatially indexed area, and store it in a db. A description of the design should include the tech stack, method of data collection and processing, cloud infrastructure used, and a general algorithm for spatial data aggregation. 

The components that should be developed are the web scraping and storing, as well as a CSV report named `crowdedness.csv` that shows the average crowdedness of each spatially indexed area aggregated in 30 minutes frequency. 

#### Data format for the CSV report:
```
- date_and_time (string: Required) -> Date and time. Format: YYYY-mm-ddTHH:MM:SS
- hexagon_id (string: Optional) -> Id of the hexagon. (if available)
- hexagon_center (string: Required) -> Center point of the hexagon (latitude, longitude)
- num_bikes (integer: Required) -> Average # vehicles in the hexagon.
```
See `crowdedness_example.csv` for the report template. 

#### Hints: 
- You should divide the map into equal hexagons to bunch coordinates together (aggregating the data spatially). You can implement your own algorithm or use any open source library.
- You can deploy your ETL system as a cron job.
- You can choose 3-10 minutes execution frequency for your cron job. 
- Your ETL system should run at least > 1-2 hours. So you can have enough data to generate requested report.
- You can create a Free Tier account in AWS or GCP to deploy your services. 

## Get coding!
To start, fork this repository and submit a pull request with your finished system + report. We'll review and schedule a call so you can go over it with us. Be prepared to explain your code and why you made some of the decisions you made.
