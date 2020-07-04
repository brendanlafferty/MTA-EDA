# Scripts
## Description of Files
### 1. *fcc_api_interface.py*
this scripts manages the get request to the FCC api that maps latitude and longitude coordinates to census block ids.

### 2. *mta_station_data.py*
this script uses the *fcc_api_interface.py* to get census block ids and census tract ids for each mta stations

### 3. *poverty_plotting.py*
handles generating heat maps of poverty data (poverty rate and total population below the poverty line) for all census 
blocks in NYC. This is achieved through creating an array of the span of the extrema in latitude and longitude for the 
census tracts in NYC.  Each id is then polled to the FCC api to get census tract ids then the corresponding poverty 
data is mapped to the array and plotted.  The polling of the fcc api can take a considerable amount of time. The results
from the api are pickled in a numpy array to save time  

## Outputs

1. stations_with_tract_id.csv

2. census_tracks.pkl/census_tracts_small.pkl
    census_tracts is a 100x100 array of census tract ids
    census_tracts_small is a 10x10 array of census tract ids
3. Plots:

Map of Poverty Rate                          | Map of Total Population in Poverty
:-------------------------------------------:|:-----------------------------------:
![poverty rate](../data/heatmap_poverty.svg) | ![total population in poverty](../data/heatmap_poverty_pop.svg)


## Using these files
```bash
$ python fcc_api_interface.py  # This runs a test of the api
$ python mta_station_data.py  # This creates the station_with_tract_id.csv
$ python poverty_ploting.py  # Creates the plots 
```