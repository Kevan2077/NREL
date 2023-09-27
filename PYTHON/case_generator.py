#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 17:40:36 2023

@author: admin-shuang
"""
import numpy as np
import os
PV_capex = np.array([842.05,1122.73,1403.41])
PV_FOM = np.array([9.512,12.682,15.853])
			
Wind_capex = np.array([1091.585,1455.446,1819.308])
Wind_FOM = np.array([13.988,18.650,23.313])
			
EL_CAPEX = np.array([835.0,1067.5,1300.0])
EL_FOM = np.array([29.225,37.363,45.500])

UG_capex = np.array([0.75,1.0,1.25])

titles = ['PV_capex', 'Wind_capex', 'EL_CAPEX', 'UG_capex', 'PV_FOM', 'Wind_FOM', 'EL_FOM']

# Create an array to hold the data
data = np.empty((len(PV_capex) * len(Wind_capex), len(titles)))

# Populate the data array
index = 0
for i in range(len(PV_capex)):
    for j in range(len(Wind_capex)):
        data[index] = [PV_capex[i], Wind_capex[j], EL_CAPEX[1], UG_capex[1],
                       PV_FOM[i], Wind_FOM[j], EL_FOM[1]]
        index += 1

# Save titles and data to a text file
with open('%s/input.txt' % os.getcwd(), 'w') as file:
    file.write(','.join(titles) + '\n')
    np.savetxt(file, data, delimiter=',', fmt='%.2f')
