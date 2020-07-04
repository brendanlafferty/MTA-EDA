# data
This directory contains both raw data sources and outputs.

## Contents
### Data Sources
* *nyc_census_tracts.csv*\
    Taken from Kaggle.com() original data source is the american communities survey of 2015
* *census_block_loc.csv*\
    Taken from Kaggle.com() original data source is the american communities survey of 2015
* *stations.csv*\
    Taken from mta website
### Outputs
* *stations_with_tract_id.csv*
    see [mta_station_data.py](../scripts/readme.md#2-mta_station_datapy)
* *census_tracts.pkl/ census_tracts_small.pkl*
    see [mta_station_data.py](../scripts/readme.md#2-mta_station_datapy)
    census_tracts.pkl is 100 x 100 px
    census_tracts_small.pxl is 10 x 10 px 
* *plots*

heatmap_poverty.svg                  | heatmap_poverty_pop.svg 
:-----------------------------------:|:-----------------------------------:
![poverty rate](heatmap_poverty.svg) | ![total population in poverty](heatmap_poverty_pop.svg)



Heatmaps                              |  barcharts
:------------------------------------:|:--------------------------------------------:
![heatmap](East_Broadway_heatmap.png) | ![barchart](East_Broadway_median_hourly.png)
:------------------------------------:|:--------------------------------------------:
![heatmap](103rd_Street_heatmap.png) | ![barchart](103rd_Street_median_hourly.png)
:------------------------------------:|:--------------------------------------------:
![heatmap](Junius_Street_heatmap.png) | ![barchart](Junius_Street_median_hourly.png)
:------------------------------------:|:--------------------------------------------:
![heatmap](Livonia_Avenue_heatmap.png) | ![barchart](Livonia_Avenue_median_hourly.png)
