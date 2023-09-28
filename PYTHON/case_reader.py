#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 17:40:36 2023

@author: admin-shuang
"""
import numpy as np
import os
import pandas as pd

Location = ['Pilbara 2', 'Pilbara 3', 'Pilbara 4']#, 'Burnie 1', 'Burnie 2', 'Burnie 3', 'Burnie 4',
#                'Pinjara 1', 'Pinjara 2', 'Pinjara 3', 'Pinjara 4',
#                'Upper Spencer Gulf 1', 'Upper Spencer Gulf 2', 'Upper Spencer Gulf 3', 'Upper Spencer Gulf 4',
#                'Gladstone 1', 'Gladstone 2', 'Gladstone 3']

df = pd.read_csv(os.getcwd()+'/input.txt', delimiter=',') 
print (len(df))

parent_directory = os.path.dirname(os.getcwd())
path_to_file = parent_directory + os.sep + 'DATA' + os.sep + 'OPT_OUTPUTS' + os.sep 

RESULTS = pd.DataFrame(columns=['cf','Location','PV_capex','Wind_capex','EL_CAPEX',
                                'UG_capex','PV_FOM','Wind_FOM','EL_FOM','capex[USD]',
                                'lcoh[USD/kg]','FOM_PV[USD]',
                                'FOM_WIND[USD]','FOM_EL[USD]','FOM_UG[USD]',
                                'H_total[kg]','pv_capacity[kW]',
                                'wind_capacity[kW]','el_capacity[kW]',
                                'ug_capcaity[kgH2]','pipe_storage_capacity[kgH2]',
                                'bat_e_capacity[kWh]','bat_p_capacity[kW]',
                                'pv_cost[USD]', 'wind_cost[USD]','el_cost[USD]',
                                'ug_storage_cost[USD]','pipe_storage_cost[USD]',
                                'bat_cost[USD]', 'load[kg/s]'])

for i in range(len(df)):
    for location in Location:
        result_file = 'results(%s-UG_windlab)_2020_%s_%s_%s_%s.csv'%(location,
            round(df['PV_capex'][i],2),round(df['Wind_capex'][i],2),round(df['EL_CAPEX'][i],2),round(df['UG_capex'][i],2))
        
        data = pd.read_csv((path_to_file + result_file), delimiter=',') 
        data['Location'] = location 
        data['PV_capex'] = df['PV_capex'][i]
        data['Wind_capex'] = df['Wind_capex'][i]
        data['EL_CAPEX'] = df['EL_CAPEX'][i]
        data['UG_capex'] = df['UG_capex'][i]
        data['PV_FOM'] = df['PV_FOM'][i]
        data['Wind_FOM'] = df['Wind_FOM'][i]
        data['EL_FOM'] = df['EL_FOM'][i]
        
        
        RESULTS = pd.concat([RESULTS, data], ignore_index=True)
    
print (RESULTS)
RESULTS.to_csv(path_to_file+'/Summary', sep=',', index=False)  # 'sep' specifies the delimiter, 'index=False' excludes the index column
    #for d in range(len(data)):
        
    
