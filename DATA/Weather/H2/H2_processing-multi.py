#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:41:16 2023

@author: admin-shuang
"""

import pandas as pd
import numpy as np
import os
plt.rcParams["font.family"] = "Times New Roman"
fontsize = 14
import time
import datetime
import pytz
from timezonefinder import TimezoneFinder 

def Resource_data(PV_location_g,Coor_PV_x_g,Coor_PV_y_g):
    import shutil
    location = 'Kevan'
    
    # read the lat and long from existing wind data
    raw_data_folder = os.getcwd() + os.sep + location
    #Wind_data = np.array([])
    
    startyear = 2023
    endyear = 2023
    Year = np.linspace(startyear,endyear,endyear-startyear+1,dtype = int)
    
    for i in range(len(PV_location_g)):
        #print (i)
        input_lat = Coor_PV_x_g[i]
        input_lon = Coor_PV_y_g[i]
        
        # NOTED! this is for a single timezone
        if i==0:
            tz = TimezoneFinder()
            timezone_str = tz.timezone_at(lat=input_lat, lng=input_lon)
            timezone1 = pytz.timezone(timezone_str)
            dt = datetime.datetime.now()
            delta_t = timezone1.utcoffset(dt)
            
        for year in Year:
            wind_data_file = os.getcwd() + os.sep + 'Wind'+os.sep+'%s/Processed/%s/Wind_data_%s_%s_%s.csv'%(location,year,input_lat,input_lon,year)
            df_wind = pd.read_csv(wind_data_file)
            
            #df_wind = pd.concat(df_list)
            df_wind.reset_index(drop=True, inplace=True)
            df_wind['datetime'] = pd.to_datetime(df_wind['datetime'])
            df_wind = df_wind[~((df_wind['datetime'].dt.month == 2) & (df_wind['datetime'].dt.day == 29))]
            df_wind = df_wind.reset_index(drop=True)
                    
            raw_data_file = os.getcwd() + os.sep+'Solar'+os.sep+'%s/Processed/%s/Solar-processed-%s-%s-%s.csv'%(location,year,input_lat,input_lon,year)
            df_solar = pd.read_csv(raw_data_file)
            df_solar.reset_index(drop=True, inplace=True)
            
            df_solar['datetime'] = pd.to_datetime(df_solar['datetime'])
            df_solar = df_solar[~((df_solar['datetime'].dt.month == 2) & (df_solar['datetime'].dt.day == 29))]
            df_solar = df_solar.reset_index(drop=True)

            directory = '%s/%s' % (raw_data_folder, year)
            if not os.path.exists(directory):
                os.makedirs(directory)
                print('Folder %s created Successfully'%(year))
            new_file = directory + os.sep + 'weather_data_%s_%s.csv'%(PV_location_g[i],year)
            shutil.copy(os.getcwd() + os.sep + 'weather_data_template.csv', new_file)
            df_new = pd.read_csv(os.getcwd() + os.sep + 'weather_data_template.csv')
    
            # change lat, long, wspd, and wdir, DNI and GHI
            df_new.loc[0, 'lat'] = Coor_PV_x_g[i]
            df_new.loc[0, 'lon'] = Coor_PV_y_g[i]
            df_new.loc[0, 'state'] = location
            df_new.loc[0, 'timezone'] = delta_t.total_seconds() / 3600
            df_new.loc[0, 'source'] = 'ninja'
            df_new.loc[2:, 'Snow Depth Units'] = df_wind['wdir'].values
            df_new.loc[2:, 'Pressure Units'] = df_wind['wspd'].values
            df_new.loc[2:, 'Dew Point Units'] = df_solar['DNI'].values
            df_new.loc[2:, 'country'] = year
            df_new.loc[2:, 'DNI Units'] = df_solar['GHI'].values


            df_new.to_csv(new_file, index=False)
            print('Done for %s %s %s %s' % (input_lat, input_lon,PV_location_g[i], year))
   
if __name__=='__main__':
    df = pd.read_csv(os.getcwd()+os.sep+'Input_H2.csv')
    Wind_location = PV_location = df['Location'].values
    Coor_wind_x = Coor_PV_x = df['Lat'].values
    Coor_wind_y = Coor_PV_y = df['Long'].values
    Resource_data(PV_location,Coor_PV_x,Coor_PV_y)