import pandas as pd
import fcc_api_interface as fai
# import matplotlib.pyplot as plt


def get_mta_data(dates):
    file_path_string = 'http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt'
    dfs = []
    for date in dates:
        df = pd.read_csv(file_path_string.format(date))
        dfs.append(df)
    return pd.concat(dfs)


def get_station_info(file_path: str = '../data/stations.csv', from_local: bool = True) -> pd.DataFrame:
    if from_local:
        return pd.read_csv(file_path)

    file_path_string = 'http://web.mta.info/developers/data/nyct/subway/Stations.csv'
    return pd.read_csv(file_path_string)


def convert_block_to_tract(block_id):
    tract_id = block_id // 10000
    return tract_id


if __name__ == '__main__':
    # dates = ['200627', '200620']
    # df = get_mta_data(dates)
    stations = get_station_info()
    # stations['Census Block'] = fai.poll_fcc_series(stations[['GTFS Latitude', 'GTFS Longitude']])
    stations['Census Tract'] = stations['Census Block'].apply(convert_block_to_tract)
    stations.to_csv('../data/stations_with_tract_id.csv', index=False)


