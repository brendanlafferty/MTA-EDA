import requests


def poll_fcc_api(lat: float, lon: float):
    """

    :param lat: Latitude in decimal degrees
    :param lon: Longitude in decimal degrees
    :return: Census block number
    """
    url = 'https://geo.fcc.gov/api/census/area'
    params = {'lat': str(lat), 'lon': str(lon)}
    response = requests.get(url=url, params=params)
    data_dict = response.json()
    block_id = data_dict['results'][0]['block_fips']
    return block_id


def poll_fcc_series(data_frame):
    block_ids = []
    for row in data_frame.iterrows():
        lat = row[1][0]
        lon = row[1][1]
        block_id = poll_fcc_api(lat, lon)
        block_ids.append(block_id)
        print('lat: {0}\nlon: {1}\nblock id: {2}\n'.format(lat, lon, block_id))
    return block_ids

if __name__ == '__main__':
    print(poll_fcc_api(40.775036, -73.912034))
