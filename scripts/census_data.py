import pandas as pd

nyc_census_tracts = pd.read_csv('../data/nyc_census_tracts.csv')
census_block_loc = pd.read_csv('../data/census_block_loc.csv')
stations = pd.read_csv('../data/stations.csv')

stations_with_census = pd.merge(stations, nyc_census_tracts[['CensusTract', 'Poverty']], left_on='Census Tract', right_on='CensusTract'])