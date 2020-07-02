"""
Module interfaces with the FCC api that takes lat and long data and return census block ids
documentation for the api is found here: https://geo.fcc.gov/api/census/
"""
import requests


def poll_fcc_api(lat: float, lon: float):
    """
    makes request of the FCC api the takes latitudes and longitudes and returns block ids

    :param lat: Latitude in decimal degrees
    :param lon: Longitude in decimal degrees
    :return: Census block number
    """
    url = 'https://geo.fcc.gov/api/census/area'
    params = {'lat': str(lat), 'lon': str(lon)}
    response = requests.get(url=url, params=params)
    data_dict = response.json()

    # most coordinates give 2 block numbers but just give the first
    # if there is no Census block (e.g. ocean) it does have the expected structure
    try:
        block_id = int(data_dict['results'][0]['block_fips'])
    except IndexError:
        block_id = 0

    return block_id


def poll_fcc_from_df(lat_lon_df):
    """
    Takes a data frame where the first column is latitudes and the second column is longitudes
    and returns a list of the block ids
    :param lat_lon_df: data frame where columns are: latitude, longitude
    :return: list of corresponding block_ids
    """
    block_ids = []
    for row in lat_lon_df.iterrows():
        lat = row[1][0]
        lon = row[1][1]
        block_id = poll_fcc_api(lat, lon)
        block_ids.append(block_id)
        print('lat: {0}\nlon: {1}\nblock id: {2}\n'.format(lat, lon, block_id))
    return block_ids

if __name__ == '__main__':
    print(poll_fcc_api(40.775036, -73.912034))
