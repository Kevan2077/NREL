#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 16:17:00 2023

@author: admin-shuang
"""

import requests
import pandas as pd
import numpy as np
import json
import os
import ephem
import datetime
from timezonefinder import TimezoneFinder 
import pytz

location = 'Kevan'
casedir = os.getcwd() + os.sep + location
df = pd.read_csv(os.getcwd()+os.sep+'Input_H2.csv')
Lat = df['lat'].values
Long = df['lon'].values
Location = df['Location'].values

df['Start year'] = 2021
df['End year'] = 2021
Startyear = df['Start year'].values
Endyear = df['End year'].values
    
for i in range(len(Lat)):
    lat = Lat[i]
    long = Long[i]
    start_year = Startyear[i]
    end_year = Endyear[i]
    Year = np.linspace(start_year, end_year, end_year - start_year + 1).astype(int)
    try:
        tz = TimezoneFinder()
        timezone_str = tz.timezone_at(lat=-23.8432, lng=151.2561)#exchange to AEST
        #timezone_str = tzwhere1.tzNameAt(lat, long)
        timezone1 = pytz.timezone(timezone_str)
        dt = datetime.datetime.now()
        delta_t = timezone1.utcoffset(dt)
        print(delta_t)

    except:
        print ('Broken')
        delta_t = delta_t

    for year in Year:
        location = Location[i]
        # Define the start and end times
        start_time = '%s-12-31 00:00:00'%str(year-1)
        end_time = '%s-12-31 23:00:00'%str(year)
        
        data = pd.read_csv('%s/Raw/%s/Raw_data_%s_%s_%s.csv'%(casedir,year,lat,long,year))
        # Create a range of datetime values
        start_date = datetime.datetime(year-1, 12, 31, 0, 0, 0)
        end_date = datetime.datetime(year, 12, 31, 23, 0, 0)
        date_range = pd.date_range(start=start_date, end=end_date, freq='h')

        #time_duration = pd.Timedelta(hours=10) 
        
        # change UTC to local!!
        data['datetime'] = date_range + pd.to_timedelta(delta_t) 
        #data['datetime'] = pd.to_datetime(data['datetime'])
        data = data[~((data['datetime'].dt.month == 2) & (data['datetime'].dt.day == 29))] # remove Feb 29
        
        data = data[data['datetime'] >= pd.Timestamp('%s-01-01'%(year))]
        data = data[data['datetime'] < pd.Timestamp('%s-01-01'%(year+1))]
        data.set_index('datetime', inplace=True)
        
        data = data.drop('electricity', axis=1)
        data.rename(columns={'wind_speed': 'wspd'}, inplace=True)
        
        # wdir
        ref_location='Burnie 1'
        if os.path.exists('%s/ref/weather_data_%s.csv'%(os.getcwd(),ref_location)):
            data_ref = pd.read_csv('%s/ref/weather_data_%s.csv'%(os.getcwd(),ref_location))
        else:
            location = location.split(' ')[0]+' 1'
            #print (location)
            data_ref = pd.read_csv('%s/ref/weather_data_%s.csv'%(os.getcwd(),ref_location))
            
        data['wdir'] = data_ref['Snow Depth Units'].values[2:]

        path='%s/Kevan/Processed/%s'% (os.getcwd(), year)
        if not os.path.exists(path):
            os.makedirs(path)
            print('Folder created successfully!')
        directory = '%s/Kevan/Processed/%s/Wind_data_%s_%s_%s.csv' % (os.getcwd(), year, lat, long, year)
        data.to_csv(directory)
        print(lat, long, year, 'output successfully!')
