# This is a group project that is part of the Metis Data Science Bootcamp

## Members:
+ Jung-A Kim
+ Allen Chen
+ Cianan Murphy
+ Brendan Lafferty

## Proposal
Dear political action group,\
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
  - Adds latitude, longitude, census block, census tract, census information (e.g. poverty)
- Clean subway turnstile data
  - Created Data Fields: Instantaneous Entries and Exits (instead of cumulative), Hours between readings
  
**3. Data Analysis**
- NEED TO ADD


## Deliverables
- NEED TO ADD

## Data Sources

|Description|Source|Link|Notes|
|------------|------|-----|----|
|NYC Census Tracts | Kaggle | https://www.kaggle.com/muonneutrino/new-york-city-census-data?select=nyc_census_tracts.csv | 2015 ACS data estimates for each census tract in New York city, includes demographic info (e.g. poverty)|
|NYC Census Blocks | Kaggle | https://www.kaggle.com/muonneutrino/new-york-city-census-data?select=census_block_loc.csv | Maps census blocks to latitude and longitude |
|Subway Station Data | MTA | insert Link | Maps stations with latitude and longitude |
|Subway Turnstile Data | MTA |insert Link | NYC MTA turnstile data with entries and exits, for 7/6/2019-10/4/2019|


## Technologies Used
* Jupyter Notebook
* Python
* Pandas
* Numpy
* Matplotlib
* Seaborn
* Fuzzywuzzy
* FCC API

