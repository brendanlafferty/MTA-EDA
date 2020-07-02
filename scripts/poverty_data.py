import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import fcc_api_interface as fai
from mta_station_data import convert_block_to_tract
import pickle

x_size = 20
y_size = 20

census_loc_data = pd.read_csv('../data/census_block_loc.csv')
census_loc_data_ny = census_loc_data[census_loc_data['State']=='NY']

census_data = pd.read_csv('../data/nyc_census_tracts.csv')

# census_data_list = census_data[['CensusTract', 'Poverty']].to_dict(orient='records')
census_data_dict = dict(zip(census_data['CensusTract'].to_list(), census_data['Poverty']))
# for item in census_data_list:
#     census_data_dict.update(item)

lons = np.linspace(census_loc_data_ny['Longitude'].min(), census_loc_data_ny['Longitude'].max(), x_size)
lats = np.linspace(census_loc_data_ny['Latitude'].min(), census_loc_data_ny['Latitude'].max(), y_size)

tract_ids = np.zeros([x_size, y_size], dtype=int)
poverty = np.zeros([x_size, y_size])

# poverty = pickle.load(open("poverty_array_small.pkl", "rb"))
# tract_ids = pickle.load(open("census_tracts_small.pkl", "rb"))
for ind_1 in range(x_size):
    for ind_2 in range(y_size):
        lat = lats[ind_2]
        lon = lons[ind_1]
        print('lat: {}\nlon: {}'.format(lat, lon))
        print('lat index: {}\nlon index: {}'.format(ind_2, ind_1))
        census_tract = convert_block_to_tract(fai.poll_fcc_api(lats[ind_2], lons[ind_1]))
        # census_tract = tract_ids[ind_1][ind_2]
        print(census_tract)
        tract_ids[ind_1][ind_2] = census_tract
        poverty_rate = census_data_dict.get(census_tract, 0)
        print(poverty_rate)
        poverty[ind_1][ind_2] = poverty_rate

pickle.dump(poverty, open("poverty_array_small.pkl", "wb"))
pickle.dump(tract_ids, open("census_tracts_small.pkl", "wb"))

poverty_clean = np.nan_to_num(poverty)

c_map = plt.imshow(poverty_clean)
c_map.set_cmap('hot')
plt.colorbar()
plt.savefig('../data/heatmap_poverty.svg')