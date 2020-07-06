# This is a group project that is part of the Metis Data Science Bootcamp

## Members:
+ Jung-A Kim
+ Allen Chen
+ Cianan Murphy
+ Brendan Lafferty

## Proposal
Dear Reaching Up Reaching Out,\
With the election season coming up, we understand you may be interested in developing a strategy for registering voters.

It may be efficient for a team of volunteers to target locations that have high foot traffic. For example, the subway stations in New York.

Leveraging MTA data, we can identify the time and location of high traffic areas. Furthermore, by combining this data with other sources, such as voter registration and demographic information, we can help you to target the population that most closely aligns with your purpose of reaching low income residents.

Regards,\
Data Team

## Methodologies
**1. Obtain data**
- See below for data sources
- Generate "stations_with_tract_id", by using FCC API to append MTA Subway Station Data with census tract and block id based on latitude and longitude
- Generate "stations_with_census", by merging stations data with NYC Census Tracts

**2. Clean and prepare data**
- Identify stations of interest to subset the subway turnstile data
  - Determined top stations based on total population below poverty for each census tract
- Merge subway turnstile data with stations_with_census information
  - Used Fuzzywuzzy to help with merging because names of stations inconsistent between the two files
  - Adds latitude, longitude, census block, census tract, census information (e.g. poverty)
- Clean subway turnstile data
  - Created Data Fields for analysis: Diff Entries and Exits (instantaneous instead of cumulative), Hours between readings, Day of week, Per Hour entries and exits
  - Accounting for irregularities:
    - Remove negative values for instantaneous entries/exits
    - Remove non-standard time windows. This is generally for those not in 4 hour increments between readings.
    - Remove outliers for traffic (after comparing median data with and without ridership, determined it is reasonable to remove)
  
**3. Data Analysis**
- Identifying Stations:
  - NYC Heat Map for Poverty Level by census tracts
  - Table of top subway stations based on total population under poverty per census tract
- Subway Traffic:
  - Compare subway stations by traffic by day
  - Analyze distribution of traffic by day and time for each subway station
  - Compare entries vs exits by time
- Boxplots:
  - Show distribution of traffic by day by station

## Deliverables
- [Presentation](MTA_voter_registration.pdf)
- [Jupyter Notebook for MTA data prep](01-mta-project1.ipynb)
- [Jupyter Notebook for Station bar charts and heatmap](Bar_heat_maps.ipynb)
- [Scripts for additional code](docs/scripts)
  - [FCC API Interface](docs/scripts/fcc_api_interface.py)
  - [MTA Station data](docs/scripts/mta_station_data.py)
  - [Poverty Plotting](docs/scripts/poverty_plotting.py)


## Data Sources

|Description|Source|Link|Notes|
|------------|------|-----|----|
|NYC Census Tracts | Kaggle | https://www.kaggle.com/muonneutrino/new-york-city-census-data?select=nyc_census_tracts.csv | 2015 ACS data estimates for each census tract in New York city, includes demographic info (e.g. poverty)|
|NYC Census Blocks | Kaggle | https://www.kaggle.com/muonneutrino/new-york-city-census-data?select=census_block_loc.csv | Maps census tracts to latitude and longitude |
|Subway Station Data | MTA | http://web.mta.info/developers/data/nyct/subway/Stations.csv | Station information with latitude and longitude |
|Subway Turnstile Data | MTA | http://web.mta.info/developers/turnstile.html | NYC MTA turnstile data with entries and exits, for 7/6/2019-10/4/2019|
|FCC Area Api | FCC | https://geo.fcc.gov/api/census/ | Returns census blocks for given coordinates

## Technologies Used
* Jupyter Notebook
* Python
* Libraries
  * Pandas
  * Numpy
  * Matplotlib
  * Seaborn
  * Fuzzywuzzy
* FCC API: https://geo.fcc.gov/api/census/

