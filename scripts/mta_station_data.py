"""
This module takes station location data and maps them to census tracts
Station Data taken from 'http://web.mta.info/developers/data/nyct/subway/Stations.csv'
"""
import pandas as pd
import fcc_api_interface as fai


def get_station_info(file_path: str = '../data/stations.csv', from_local: bool = True) -> pd.DataFrame:
    """
    This reads in the station info from the MTA website or from a local copy of the data
    :param file_path: file path to local copy of the data
    :param from_local: boolean on whether to look locally or retrieve from the internet
    :return: data frame of station data
    """
    if from_local:
        return pd.read_csv(file_path)

    file_url_string = 'http://web.mta.info/developers/data/nyct/subway/Stations.csv'
    return pd.read_csv(file_url_string)


def convert_block_to_tract(block_id):
    """
    quick function to truncate the block ids to tract ids
    :param block_id: 15 digit Census Block Id
    :return: Census Tract (first eleven digits of the block id)
    """
    tract_id = block_id // 10000
    return tract_id


if __name__ == '__main__':
    stations = get_station_info()
    stations['Census Block'] = fai.poll_fcc_from_df(stations[['GTFS Latitude', 'GTFS Longitude']])
    stations['Census Tract'] = stations['Census Block'].apply(convert_block_to_tract)
    stations.to_csv('../data/stations_with_tract_id.csv', index=False)
