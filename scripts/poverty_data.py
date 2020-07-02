"""
This is a module that generates a heatmap of poverty rates in census blocks across new york city

"""
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import fcc_api_interface as fai
import mta_station_data as msd


def get_and_filter_tract_locations(file_path='../data/census_block_loc.csv'):
    """
    gets the kaggle data set on census tract locations and filters for new york and returns the df along with the
    extrema for longitudes and latitudes
    :param file_path: census tract location data from the Kaggle data set
    :return: a df of the location of census tracts in New York,
            list of extrema for longitudes, list of extrema for latitudes
    """
    census_loc_data = pd.read_csv('../data/census_block_loc.csv')
    census_loc_data_ny = census_loc_data[census_loc_data['State'] == 'NY']
    lon_max = census_loc_data_ny['Longitude'].max()
    lon_min = census_loc_data_ny['Longitude'].min()
    lat_max = census_loc_data_ny['Latitude'].max()
    lat_min = census_loc_data_ny['Latitude'].min()
    lons = [lon_min, lon_max]
    lats = [lat_min, lat_max]
    return census_loc_data_ny, lons, lats


def get_census_tract_ids(lons=None, lats=None, resolution=100, file_path='../data/census_tracts.pkl',):
    """
    gets census tract ids either from a local source or from the FCC api.
    If the lon data is not provided then it will look for a local pickle of the data
    :param lons: min and max values for longitudes to span
    :param lats: min and max values for latitudes to span
    :param resolution: step size for the both lats and lons
    :param file_path: file path to local pickle, either the input(if getting from local) or output(if downloading data)
    :return: numpy array with census tract ids spanning the box of lats and lons
    """
    if not lons:
        census_tracts = pickle.load(open(file_path, 'rb'))
        return census_tracts
    census_tracts = download_census_tract_id(lons, lats, resolution)
    pickle.dump(census_tracts, 'wb')
    return census_tracts


def download_census_tract_id(lons: list, lats: list, resolution: int):
    """
    gets census tract ids from the FCC api.
    :param lons: min and max values for longitudes to span
    :param lats: min and max values for latitudes to span
    :param resolution: step size for the both lats and lons
    :return: numpy array with census tract ids spanning the box of lats and lons and the axes
    """
    tract_ids = np.zeros([resolution, resolution], dtype=int)
    lons = np.linspace(min(lons), max(lons), resolution)
    lats = np.linspace(min(lats), max(lats), resolution)
    for ind_1 in range(resolution):
        for ind_2 in range(resolution):
            lat = lats[ind_2]
            lon = lons[ind_1]
            print('Getting Tract ID for:\n Lon #{3}: {0}\nLat #{2}:{1}'.format(lon, lat, ind_1, ind_2))
            census_tract = msd.convert_block_to_tract(fai.poll_fcc_api(lat, lon))
            print('Retrieved ID:\n{}\n'.format(census_tract))
            tract_ids[ind_1][ind_2] = census_tract
    return tract_ids


def census_tract_to_poverty_data(census_tract_ids: np.array, census_poverty_dict: dict):
    """
    takes an array census tract id and returns an array of the same size with poverty data of that census tract
    :param census_tract_ids: an array of census tract ids
    :return:
    """
    size_1, size_2 = np.shape(census_tract_ids)
    poverty_data = np.zeros([size_1, size_2])
    for ind_1 in range(size_1):
        for ind_2 in range(size_2):
            census_tract = census_tract_ids[ind_1][ind_2]
            poverty_data[ind_1][ind_2] = census_poverty_dict.get(census_tract, 0)
    return poverty_data


def make_census_poverty_dict(file_path='../data/nyc_census_tracts.csv'):
    """
    takes the census data from the Kaggle data set
    :param file_path: census data from the Kaggle data set
    :return: a dictionary of {census_tract: poverty_data}
    """
    census_df = pd.read_csv(file_path)
    census_data_dict = dict(zip(census_df['CensusTract'], census_df['Poverty']))
    return census_data_dict


def plot_poverty_data(poverty, lons, lats, filepath='../data/heatmap_poverty.svg'):
    """
    creates a heatmap of the poverty data
    """
    lon_max = max(lons)
    lon_min = min(lons)
    lat_max = max(lats)
    lat_min = min(lats)
    scale_factor = (lon_max - lon_min) / (lat_max - lat_min)
    resolution = poverty.shape[0]
    extra = np.zeros([int(resolution*(scale_factor-1)/2), resolution])
    poverty_clean = np.nan_to_num(poverty)
    poverty_wide = np.concatenate([extra, poverty_clean.T, extra])
    fig = plt.figure()
    c_map = plt.imshow(poverty_wide, aspect='auto')
    plt.gca().invert_yaxis()
    c_map.set_cmap('cividis')
    cbar = plt.colorbar()
    cbar.set_label('Percentage of Population Below the Poverty Line', rotation=270)
    plt.title('Poverty Rates by Census Tracts in NYC')
    fig.axes[0].get_yaxis().set_visible(False)
    fig.axes[0].get_xaxis().set_visible(False)
    plt.savefig(filepath)


if __name__ == '__main__':
    census_loc_df, lons, lats = get_and_filter_tract_locations()
    census_tract_ids = get_census_tract_ids()
    census_poverty_dict = make_census_poverty_dict()
    poverty_data = census_tract_to_poverty_data(census_tract_ids, census_poverty_dict)
    plot_poverty_data(poverty_data, lons, lats)