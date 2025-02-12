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
import pytz
from timezonefinder import TimezoneFinder 

location = 'Kevan'
casedir = os.getcwd() + os.sep + location
df = pd.read_csv(os.getcwd() + os.sep + 'Input_H2.csv')
Lat = df['Lat'].values
Long = df['Long'].values

startyear = 2023
endyear = 2023
Year = np.linspace(startyear,endyear,endyear-startyear+1,dtype = int)
#Year = [2014,2017,2019]
#Year = [2014,2019,2020]
for i in range(len(Lat)):
    lat = Lat[i]
    long =Long[i]
    try:
        tz = TimezoneFinder()
        timezone_str = tz.timezone_at(lat=lat, lng=long)
        #timezone_str = tzwhere1.tzNameAt(lat, long)
        timezone1 = pytz.timezone(timezone_str)
        dt = datetime.datetime.now()
        delta_t = timezone1.utcoffset(dt)
        
    except:
        print ('Broken')
        delta_t = delta_t
        
    print (lat,long,str(delta_t))
    
    for year in Year:
        #print (year)
        # Create an observer location (latitude and longitude)
        observer = ephem.Observer()
        observer.lat = '%s'%lat  # Latitude (for example, Berlin's latitude)
        observer.lon = '%s'%long  # Longitude (for example, Berlin's longitude)
        
        # Define the target celestial body (in this case, the Sun)
        sun = ephem.Sun()
        
        # Define the start and end times
        if year % 4 ==0:
            year_1 = 2012
        else:
            year_1 = 2011
        start_time = '%s-12-31 00:00:00'%str(year_1-1)
        end_time = '%s-12-31 23:00:00'%str(year_1)
        #print (start_time,end_time)
        # Convert start and end times to ephem date format
        start_date = ephem.Date(start_time)
        end_date = ephem.Date(end_time)
        # Loop through the time range and calculate zenith angle for each time step
        current_date = start_date
        Alt = np.array([])
        while current_date <= end_date:
            observer.date = current_date
            sun.compute(observer)
            current_date += ephem.hour
            Alt = np.append(Alt,sun.alt/np.pi*180)
            
        Alt[Alt<0] = 0
        Zenith = 90 - Alt
        
        data = pd.read_csv('%s/Raw/%s/Raw_data_%s_%s_%s.csv'%(casedir,year,lat,long,year))
        data['zenith'] = Zenith
        # Create a range of datetime values
        start_date = datetime.datetime(year-1, 12, 31, 0, 0, 0)
        end_date = datetime.datetime(year, 12, 31, 23, 0, 0)
        date_range = pd.date_range(start=start_date, end=end_date, freq='h')
        
        #time_duration = pd.Timedelta(hours=10)
        
        #data['datetime'] = date_range+pd.to_timedelta(delta_t)
        data['datetime'] = date_range + pd.to_timedelta(delta_t)
        data = data[data['datetime'] >= pd.Timestamp('%s-01-01'%(year))]
        data = data[data['datetime'] < pd.Timestamp('%s-01-01'%(year+1))]
        data.set_index('datetime', inplace=True)
                
        data['DNI'] = data['irradiance_direct']*1000
        data[data['DNI']>1200] = 0
        data['GHI'] = data['DNI']*np.cos(data['zenith']/180*np.pi)+data['irradiance_diffuse']*1000
        data[data['GHI']<1] = 0
        data = data.drop('electricity', axis=1)
        data = data.drop('irradiance_direct', axis=1)
        data = data.drop('irradiance_diffuse', axis=1)
        data = data.drop('temperature', axis=1)

        path='%s/Kevan/Processed/%s'% (os.getcwd(),year)
        if not os.path.exists(path):
            os.makedirs(path)
            print('Folder created successfully!')
        directory = '%s/Kevan/Processed/%s/Solar-processed-%s-%s-%s.csv' % (os.getcwd(), year, lat, long, year)
        data.to_csv(directory, index=True)
        print(lat, long, year, 'output successfully!')
        #data.to_csv('Solar-processed-%s-%s.csv'%(lat,long), index=True)



      