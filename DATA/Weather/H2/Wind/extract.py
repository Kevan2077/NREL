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


#Lat = np.array([-33.78,-34.47,-32.92,-23.84,-27.436,-34.77,-35.01,-32.99,-38.07,-38.33,-28.78,-32.24,-32.23])
#Long = np.array([151.13,150.89,151.75,151.25,153.12,138.59,138.57,137.77,144.39,141.60,114.61,115.81,115.76])

#Location = np.array(['Burnie 1', 'Burnie 2', 'Burnie 3', 'Burnie 4', 'Gladstone 1', 'Gladstone 2', 'Gladstone 3', 'Pilbara 1', 'Pilbara 2', 'Pilbara 3', 'Pilbara 4', 'Pinjara 1', 'Pinjara 2', 'Pinjara 3', 'Pinjara 4', 'Upper Spencer Gulf 1', 'Upper Spencer Gulf 2', 'Upper Spencer Gulf 3', 'Upper Spencer Gulf 4'])


#Lat = np.array([-40.89, -40.73, -40.83, -40.99, -24.08, -23.94, -24.33, -22.12, -22.61, -24.17, -24.08, -32.50, -32.59, -33.08, -33.10, -32.94, -33.61, -32.65, -32.96])
#Long = np.array([145.25, 144.69, 145.38, 145.72, 151.28, 151.17, 151.95, 119.83, 117.80, 119.44, 117.11, 115.96, 115.84, 115.63, 115.87, 137.45, 136.71, 136.56, 137.62])

#Location = np.array(['Burnie 1', 'Burnie 2', 'Burnie 3', 'Burnie 4', 'Gladstone 1', 'Gladstone 2', 'Gladstone 3', 'Pilbara 1', 'Pilbara 2', 'Pilbara 3', 'Pilbara 4', 'Pinjara 1', 'Pinjara 2', 'Pinjara 3', 'Pinjara 4', 'Upper Spencer Gulf 1', 'Upper Spencer Gulf 2', 'Upper Spencer Gulf 3', 'Upper Spencer Gulf 4'])
#Location = np.array(['Worsley Alumina','Cockburn Cement Kwinana','Cockburn Cement Dongara'])
#df = pd.read_csv(os.getcwd() + os.sep + 'Input_H2.csv')
df = pd.read_csv(os.getcwd() + os.sep + 'Input_H2.csv')
Lat = df['Lat'].values
Long = df['Long'].values

df['Start year'] = 2024
df['End year'] = 2024

Startyear = df['Start year'].values
Endyear = df['End year'].values

print(Startyear)
print(Endyear)

#Startyear = 2023
#Endyear = 2023
#Year = np.linspace(startyear,endyear,endyear-startyear+1,dtype = int)
Token = ['cc8a916709d888182f1a6ead40f6a5d11771524b',
    'f47570af8d4b7fa48b725bd5c5122cfbb7530b82',
    '19290b3e281ff30f7a8447eb633699daa4f29f73', 
    '096b4a4cd8bbe7c7c77a74c39006be57e951bbfe',
    '19a6e1b6060b3e512f2d2bacc3d7f11ceec2de9e',
    'eb48c347af51e50f2c952b2d47996c49ff723448',
    '9eb776de62294f8c4c1837c83dae5a73b19e8d88',
    "5fcf83e73d4db25af5c98df90ac0e58170fc2810",
    "e9fd74ecc008cc5606f265dea1b28260ee799984",
    "1dcc9831ca9f7aab400c470abfd039b4e4614e84",
    "b9d9a6002725514adf8dc84044e92083980d913d",
    "a4281e2c33f8bd645a32a76e7b93ca25d284666a",
    "d21cae6a093c9dfc7922526002b655f1e67f4387",
    "d80d301de8c4df4de9b7d582b6512ef250da8fe6",
    "085112407fdbb233cb4553467868df9c62509e5d",
    "d0ecb8a47c57c97363453b4545e35821fb4a96ef",
    "dcfa26e53c12c0e0fd6e9aeed7aa1f26c8781abe",
    "137250da368eb1e9fcf32bf65e9e228598cb6045",
    "ec02420a0cb4ec0f71f259e975c84ef3ab9db0cd",
    "8f2ade7c7189351526f3d0347378c9dee31ff954"]


max_retries = len(Token)  # Define the maximum number of retries based on the number of tokens

s = requests.session()  # Reuse session for all requests
k = 0  # Initialize token index

for i in range(len(Lat)):
    lat = Lat[i]
    long = Long[i]
    start_year = Startyear[i]
    end_year = Endyear[i]
    Year = range(start_year, end_year + 1)  # Use range for simplicity

    for year in Year:
        retries = 0  # Initialize retry counter for each request

        while retries < max_retries:  # Retry loop
            token = Token[k]
            print(lat, long, year, token)
            api_base = 'https://www.renewables.ninja/api/'

            # Send token header with each request
            s.headers = {'Authorization': 'Token ' + token}

            url = api_base + 'data/wind'
            args = {
                'lat': lat,
                'lon': long,
                'date_from': '%s-12-31' % str(year - 1),
                'date_to': '%s-12-31' % str(year),
                'capacity': 1.0,
                'height': 150,
                'turbine': 'Vestas V80 2000',
                'format': 'json',
                'raw': True
            }

            r = s.get(url, params=args)

            if r.status_code == 200:  # If the request is successful
                try:
                    parsed_response = json.loads(r.text)
                    data = pd.read_json(json.dumps(parsed_response['data']), orient='index')
                    metadata = parsed_response['metadata']

                    # Ensure directory exists
                    directory = '%s/Kevan/Raw/%s' % (os.getcwd(),year)
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    # Save data to CSV
                    data.to_csv('%s/Kevan/Raw/%s/Raw_data_%s_%s_%s.csv' % (os.getcwd(), year,lat, long, year), index=False)
                    print('Done for %s %s %s' % (lat, long, year))
                    break  # Exit retry loop on success
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON response for {lat}, {long}, {year}")
                    break  # If decoding fails, move to the next year and location
            else:
                # If request fails (e.g., 401 Unauthorized), retry with the next token
                print(f"Error {r.status_code} for {lat}, {long}, {year}: {r.reason}")
                retries += 1
                k = (k + 1) % len(Token)  # Move to the next token

                if retries == max_retries:
                    print(f"Failed after {max_retries} attempts for {lat}, {long}, {year}")



      