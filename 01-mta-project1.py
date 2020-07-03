#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gmaps
import gmaps.datasets
get_ipython().run_line_magic('matplotlib', 'inline')
from datetime import datetime
from fuzzywuzzy import fuzz
import re


# In[3]:


# Source: http://web.mta.info/developers/turnstile.html
# def get_data(week_nums):
#     url = "http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt"
#     dfs = []
#     for week_num in week_nums:
#         file_url = url.format(week_num)
#         dfs.append(pd.read_csv(file_url))
#     return pd.concat(dfs)
        
# week_nums = [190713, 190720, 190727, 190803, 190810, 190817, 190824, 190831, 190907, 190914, 190921, 190928 ,191005]
# df2019 = get_data(week_nums)


# In[4]:


# Load datasets
station_data = pd.read_csv('data/stations_with_tract_id.csv') # Locations of stations
census_block_loc = pd.read_csv('data/census_block_loc.csv') # Locations of census block(sub-level of tract)
nyc_census_tracts = pd.read_csv('data/nyc_census_tracts.csv') # Census tract code and Poverty proportion
df2019 = pd.read_pickle('df2019.pkl')
# Plan:
# 1. Get the census tract number we want(nyc_census_tracts)
# 2. Find the blocks within the census tract(census_block_loc)
# 3. Find the station+line combo's within those blocks(station_data)
# 4. Find the matching station+line combo's in MTA dataset(df2020)


# In[5]:


census_block_loc['CensusTract'] = census_block_loc.BlockCode.map(lambda x: x // 10000)


# In[6]:


# code from brendanlafferty 'stations_census_data.ipynb'
nyc_census_tracts['Total_Poverty'] = nyc_census_tracts['Poverty'].multiply(nyc_census_tracts['TotalPop']).multiply(1/100)
stations_with_census = pd.merge(station_data,
                                nyc_census_tracts[['CensusTract', 'Poverty', 'TotalPop', 'Total_Poverty']],
                                left_on='Census Tract', 
                                right_on='CensusTract')

# Get the tract numbers of top 12 Total_Poverty census tracts
tract_numbers = stations_with_census.sort_values('Total_Poverty', ascending=False).head(12)['Census Tract'].values
stations_with_census.sort_values('Total_Poverty', ascending=False).head(12)


# In[7]:


tract_numbers


# In[8]:


# Find blocks within the top poverty census tract
blocks = census_block_loc[census_block_loc.CensusTract.map(lambda x: x in tract_numbers)].sort_values('BlockCode')
print(len(blocks))


# In[9]:


# Find the stations within the selected census tracts
stations = station_data[station_data['Census Tract'].map(lambda x: x in tract_numbers)]


# In[10]:


# There are 12 stations in the census tracts
stop_name_list = list(stations['Stop Name'].unique())
station_list = df2019.STATION.unique() # Create a station list

# Strip puncutations and uppercase Stop Name's and STATION's
stripped_station = pd.Series(station_list).map(lambda x: ''.join(re.findall(r'[\w\.]', x)))
stripped_stop_name_list = [''.join(re.findall(r'[\w\.]', x)).upper() for x in stop_name_list]


# In[11]:


# Match the Stop Name to STATION using fuzzywuzzy module
closest_index = []
for stop_name in stripped_stop_name_list:
    closest_index.append(stripped_station.map(lambda x: fuzz.ratio(x, stop_name)).idxmax())
print(stop_name_list)
station_list[closest_index]


# In[12]:


# Find the 12 stations from MTA dataset that match the stations' names in Stations.csv
top_stations = station_list[closest_index]


# In[13]:


# For each Stop Name(STATION), there is a list of Daytime Routes(LINENAME) in Stations.csv
stations.set_index(['Stop Name', 'Daytime Routes']).sort_index()


# In[14]:


# For each STATION, there is a list of LINENAME's in MTA dataset (We need to filter out irrelevant STATION+LINENAME's)
# mta = df2019[df2019.STATION.map(lambda x: x in top_stations)]
mta = pd.read_pickle('mta.pkl')
sorted(mta.set_index(['STATION','LINENAME']).index.unique())


# In[15]:


len(mta)


# In[16]:


# Reformat values of 'Daytime Routes' and 'Stop Name' as 'LINENAME' and 'STATION' like MTA dataset
pd.options.mode.chained_assignment = None  # default='warn'

stations['Daytime Routes'] = stations['Daytime Routes'].apply(lambda x: x.replace(" ",""))

for index in range(len(stop_name_list)):
    stations.loc[stations['Stop Name'] == stop_name_list[index], 'Stop Name'] = top_stations[index]
stations


# In[17]:


# Store the combinations in 'locations' variable
from collections import defaultdict
locations = defaultdict(list)
for station_name in top_stations:
    stations_set = set(stations.loc[stations['Stop Name'] == station_name, 'Daytime Routes'])
    mta_set = set(mta.loc[mta.STATION == station_name, 'LINENAME'])
    for daytime_route in stations_set:
        mask = [set(daytime_route).issubset(set(item)) for item in mta_set]
        locations[station_name] += [target for boolean, target in zip(mask, mta_set) if boolean]
sorted(locations.items())


# In[18]:


stations[['Stop Name', 'Daytime Routes']].sort_values(['Stop Name', 'Daytime Routes'])


# In[19]:


# Finally, find the rows in MTA dataset corresponding to each combo
final_df = pd.DataFrame()
for station_name, line_list in locations.items():
    for line in line_list:
        final_df = final_df.append(mta[(mta.LINENAME == line) & (mta.STATION == station_name)])
final_df = final_df.rename(columns = {final_df.columns[-1] : final_df.columns[-1].strip()})# Strip whitespace from 'EXITS' column


# In[20]:


# Create new column 'STATION_LINENAME' in final_df and df2019
final_df['STATION_LINENAME'] = list(zip(final_df.STATION, final_df.LINENAME))
df2019['STATION_LINENAME'] = list(zip(df2019.STATION, df2019.LINENAME))
print(final_df.STATION_LINENAME.unique())


# In[21]:


final_df.head()


# # Traffic

# In[22]:


# Create DATETIME, DIFF, and DAY columns. DIFF columns are treated as Traffic
final_df = final_df.reset_index()
final_df['DATETIME'] = pd.to_datetime(final_df[['DATE', 'TIME']].apply(lambda x: ' '.join(x), axis = 1))
final_df['DIFF_HRS'] = final_df.sort_values(['C/A','UNIT','SCP','STATION','DATETIME']).groupby(['C/A','UNIT','SCP','STATION'])['DATETIME'].transform(pd.Series.diff)
final_df['DIFF_ENTRIES'] = final_df.sort_values(['C/A','UNIT','SCP','STATION','DATETIME']).groupby(['C/A','UNIT','SCP','STATION'])['ENTRIES'].transform(pd.Series.diff)
final_df['DIFF_EXITS'] = final_df.sort_values(['C/A','UNIT','SCP','STATION','DATETIME']).groupby(['C/A','UNIT','SCP','STATION'])['EXITS'].transform(pd.Series.diff)
final_df['DAY'] = final_df['DATETIME'].dt.dayofweek # 0 = Monday

print("NUMBER OF NEGATIVE DIFF_ENTRIES: ",final_df.loc[final_df.DIFF_ENTRIES < 0, 'DIFF_ENTRIES'].count())
print("NUMBER OF NEGATIVE DIFF_EXITS: ",final_df.loc[final_df.DIFF_EXITS < 0, 'DIFF_EXITS'].count())

# Replace negative DIFF_ENTRIES and DIFF_EXITS with ENTRIES and EXITS (turnstiles have been reset)
final_df.loc[final_df.DIFF_ENTRIES < 0, 'DIFF_ENTRIES'] = final_df.loc[final_df.DIFF_ENTRIES < 0, 'ENTRIES'] 
final_df.loc[final_df.DIFF_EXITS < 0, 'DIFF_EXITS'] = final_df.loc[final_df.DIFF_EXITS < 0, 'EXITS']

print('final_df has',len(final_df),'rows')


# In[23]:


# How many of TIME's have minutes or seconds?
sum(final_df.TIME.map(lambda x: str(x)[-5:] != '00:00'))
# final_df.loc[final_df.TIME.map(lambda x: str(x)[-5:] != '00:00'),'DIFF_HRS'].value_counts().sort_index()


# In[24]:


# Round the DIFF_HRS to the nearest hours and create new column 'DIFF_HRS_ROUND'
final_df['DIFF_HRS_ROUND'] = final_df.loc[:,'DIFF_HRS'].dt.round('H').map(lambda x: np.timedelta64(x, 'h').astype(int) if pd.notnull(x) else x)

# Divide DIFF_ENTRIES by DIFF_HRS_ROUND and call it DIFF_ENTRIES_PER_HR as a new column
final_df['DIFF_ENTRIES_PER_HR'] = np.insert(final_df['DIFF_ENTRIES'].values[1:] / final_df['DIFF_HRS_ROUND'].values[1:], 0, np.nan)


# In[25]:


final_df.head()


# In[ ]:


# Sanity check: NaN entries_diff's are very first rows of each turnstile (nothing can be done about)
df = final_df.groupby(['C/A','UNIT','SCP','STATION'])[['DIFF_ENTRIES']].apply(np.isnan)
final_df.loc[df.values,['DATE','TIME']].sort_values('TIME').T 


# In[ ]:


# Sanity check for DIFF values with two different turnstiles in a row
# H037	R349	00-00-00	SUTTER AV
# H037	R349	00-00-01	SUTTER AV
final_df[(final_df['C/A'] == 'H037') & (final_df.UNIT == 'R349') & (final_df.SCP == '00-00-01') & (final_df.STATION == 'SUTTER AV') & (final_df.DATE == '07/06/2019')]
final_df.loc[[41, 42],:]


# In[ ]:


# Station+line's in the census tract(about 1% of all turnstiles in the past 12 wks)
print(len(final_df.groupby(['C/A', 'UNIT', 'SCP', 'STATION']).count())) # 62 turnstiles in top 1 tract
len(df2019.groupby(['C/A', 'UNIT', 'SCP', 'STATION']).count()) # 4955 turnstiles in total


# In[26]:


plt.figure(figsize=(20,3))
g = sns.distplot(final_df.DIFF_ENTRIES[final_df.DIFF_ENTRIES], bins = np.linspace(0, 1400, 29),kde = False, hist_kws=dict(edgecolor="k"));
g.set_xticks(range(0,1450,50))
g.set_xticklabels(list(range(0,1450,50)))
g.set_yticks(range(0, 7000, 1000))
g.set_yticklabels([round(x/final_df.DIFF_ENTRIES.count(),2) for x in list(range(0, 7000, 1000))])
g.set_title('Distribution of difference in entries');


# In[27]:


statline_names = final_df.STATION_LINENAME.unique()


# About 20% of the entries are between 0 and 50 in low-income districts.

# In[ ]:


diff_statline_time = final_df.groupby(['STATION_LINENAME', 'TIME']).sum()['DIFF_ENTRIES'].sort_values(ascending = False) # Entries per statline & time in descending order
labels = diff_statline_time.index.map(lambda x: str(x))

diff_statline = final_df.groupby(['STATION_LINENAME']).sum()['DIFF_ENTRIES'].sort_values(ascending = False) # Entries per statline in descending order

fig, ax = plt.subplots(2, 1, figsize = (20, 5))
fig.set_figwidth(20)
fig.set_figheight(10)

ax[0].pie(diff_statline, labels = diff_statline.index, 
          autopct='%1.0f%%', textprops = {'fontsize': 10});# ('5 AV/59 ST', 'NQRW') and ('81 ST-MUSEUM', 'BC') account for 77% of the traffic
ax[0].set_title('Proportion of DIFF_ENTRIES in Station & Line')
ax[1].bar(labels, diff_statline_time//1000)
ax[1].tick_params(labelrotation=90)
ax[1].set_ylabel('DIFF_ENTRIES (in 1000)')
ax[1].set_title('DIFF_ENTRIES in Station & Line & Time');
# Barplot: proportion out of total traffic
print(list(round(100*diff_statline_time/sum(diff_statline_time),1)), 'in %')


# In[ ]:


get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'svg'")
final_df.loc[final_df.STATION_LINENAME == ('5 AV/59 ST', 'NQRW'), ['TIME','DIFF_ENTRIES']].boxplot(by = ['TIME'],figsize=(16,3))
plt.xlabel('Time'); plt.ylabel('DIFF_ENTRIES'); plt.title("Traffic at 5 AV/59 ST with NQRW line across times")
plt.suptitle('');


# In[ ]:


plt.figure(figsize=(10,4))
for statline_name in statline_names:
    plt.plot(final_df.loc[final_df.STATION_LINENAME == statline_name, ['DAY','DIFF_ENTRIES']].groupby('DAY').sum(), label = statline_name)
plt.legend(loc=1)
plt.xticks(list(range(7)),['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
plt.ylabel('DIFF_ENTRIES')
plt.title('DIFF_ENTRIES across days at Station & Line between 7/06/2019 and 10/5/2019');


# In[ ]:


plt.figure(figsize=(20,3))
plt.plot(final_df.loc[final_df.STATION_LINENAME == ('5 AV/59 ST', 'NQRW'), ['TIME', 'DIFF_ENTRIES']].groupby('TIME').sum());
plt.xlabel('Time window')
plt.ylabel('DIFF_ENTRIES')
plt.title("DIFF_ENTRIES at 5 AV/59 ST with NQRW line across times between 7/13/2019 and 10/5/2019");


# In[ ]:


# Traffic per station_line for the whole dataset
final_df.groupby(['STATION_LINENAME']).sum().sort_values('DIFF_ENTRIES',ascending=False)


# In[ ]:


final_df.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


station_data['CensusTract'] = station_data['Census Block']//10000
stations_with_census = pd.merge(station_data,
                                nyc_census_tracts[['CensusTract', 'Poverty']],
                                on = 'CensusTract')
stations_with_census.sort_values('Poverty', ascending = False)


# In[ ]:


# (not free to use google api)
gmaps.configure(api_key = 'AIzaSyDZBFZYNXkBRUF8D9mF9MaTe_eVdqHUrl0')
fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(stations_with_census[['GTFS Latitude', 'GTFS Longitude']], weights = stations_with_census['Poverty']))
fig


# In[ ]:


new_york_coordinates = (40.75, -74.00)
gmaps.figure(center = new_york_coordinates, zoom_level = 12)

