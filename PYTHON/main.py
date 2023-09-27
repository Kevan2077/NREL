#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 15:41:16 2023

@author: admin-shuang
"""

import pandas as pd
import numpy as np
import os
from projdirs import datadir #load the path that contains the data files 
from PACKAGE.optimisation import Optimise
from PACKAGE.component_model import pv_gen, wind_gen, SolarResource, WindSource,WindSource_windlab
import random

def update_resource_data():
    #Choose the location
    Location = 'Darwin' 
    
    #Update the weather data files
    SolarResource(Location)
    
    # # WindSource(Location)
    WindSource_windlab(Location)
    
def optimisation(Input):
    # create a dictionary that contains the inputs for optimisation.
    #these inputs are used by make_dzn_file function to create an input text file called hydrogen_plant_data.dzn.                 
    
    # Pipe storage costs
    # line packing: 516 USD/kgH2
    # Ardent UG storage: 110-340 USD/kgH2
    # vessel storage: 1000 USD/kgH2
    
    
    #for 2020
    simparams = dict(EL_ETA = 0.70,       #efficiency of electrolyser
                     BAT_ETA_in = 0.95,   #charging efficiency of battery
                     BAT_ETA_out = 0.95,  #discharg efficiency of battery
                     C_PV = 1122.7,          #[USD/kW] unit cost of PV
                     C_WIND = 1455,           #[USD/kW] unit cost of Wind
                     C_EL = 1067,          #[USD/W] unit cost of electrolyser
                     UG_STORAGE_CAPA_MAX = 1e10,   #maximum available salt caevern size (kg of H2)
                     C_PIPE_STORAGE = 516, #unit cost of line packing (USD/kg of H2)
                     PIPE_STORAGE_CAPA_MIN = 0, #minimum size of linepacking (kg of H2)
                     C_BAT_ENERGY = 196,        #[USD/kWh] unit cost of battery energy storage
                     C_BAT_POWER = 405,        #[USD/kW] unit cost of battery power capacpity
                     OM_EL = 37.40,    # O&M for electrolyzer ($/kw)
                     OM_PV = 12.70,    # O&M for PV ($/kw)
                     OM_WIND = 18.65,    # O&M for wind ($/kw)
                     OM_UG = 1.03,        # O&M for underground storage ($/kg)
                     DIS_RATE = 0.08        #discount rate 8%
                     )
    simparams['C_PV'] = Input[0]
    simparams['C_WIND'] = Input[1]
    simparams['C_EL'] = Input[2]
    simparams['OM_PV'] = Input[4]
    simparams['OM_WIND'] = Input[5]
    simparams['OM_EL'] = Input[6]
    simparams['OM_UG'] = simparams['OM_UG'] * Input[3]
    
    #print (simparams)
    
    # # for 2030
    # simparams = dict(EL_ETA = 0.70,       #efficiency of electrolyser
    #                  BAT_ETA_in = 0.95,   #charging efficiency of battery
    #                  BAT_ETA_out = 0.95,  #discharg efficiency of battery
    #                  C_PV = 696,          #[USD/kW] unit cost of PV
    #                  C_WIND = 1390,           #[USD/kW] unit cost of Wind
    #                  C_EL = 385,          #[USD/W] unit cost of electrolyser
    #                  UG_STORAGE_CAPA_MAX = 0,   #maximum available salt caevern size (kg of H2)
    #                  C_PIPE_STORAGE = 1000, #unit cost of line packing (USD/kg of H2)
    #                  PIPE_STORAGE_CAPA_MIN = 0, #minimum size of linepacking (kg of H2)
    #                  C_BAT_ENERGY = 164,        #[USD/kWh] unit cost of battery energy storage
    #                  C_BAT_POWER = 338,        #[USD/kW] unit cost of battery power capacpity
    #                  ) 
    
    # # for 2050
    # simparams = dict(EL_ETA = 0.70,       #efficiency of electrolyser
    #                  BAT_ETA_in = 0.95,   #charging efficiency of battery
    #                  BAT_ETA_out = 0.95,  #discharg efficiency of battery
    #                  C_PV = 465,          #[USD/kW] unit cost of PV
    #                  C_WIND = 1323,           #[USD/kW] unit cost of Wind
    #                  C_EL = 295,          #[USD/W] unit cost of electrolyser
    #                  UG_STORAGE_CAPA_MAX = 0,   #maximum available salt caevern size (kg of H2)
    #                  C_PIPE_STORAGE = 1000, #unit cost of line packing (USD/kg of H2)
    #                  PIPE_STORAGE_CAPA_MIN = 0, #minimum size of linepacking (kg of H2)
    #                  C_BAT_ENERGY = 131,        #[USD/kWh] unit cost of battery energy storage
    #                  C_BAT_POWER = 270,        #[USD/kW] unit cost of battery power capacpity
    #                  ) 
    
    
    #Choose the location
    
    # #Update the weather data files
    # SolarResource(Location)
    
    # # # WindSource(Location)
    # WindSource_windlab(Location)
    
    # storage_type = 'Lined Rock'
    # results = Optimise(5, 100, storage_type, simparams)
    
    import multiprocessing as mp
    
    for Location in ['Pilbara 2', 'Pilbara 3', 'Pilbara 4', 'Burnie 1', 'Burnie 2', 'Burnie 3', 'Burnie 4',
                   'Pinjara 1', 'Pinjara 2', 'Pinjara 3', 'Pinjara 4',
                   'Upper Spencer Gulf 1', 'Upper Spencer Gulf 2', 'Upper Spencer Gulf 3', 'Upper Spencer Gulf 4',
                   'Gladstone 1', 'Gladstone 2', 'Gladstone 3']:
                
        random_number = random.random()
        #Update the weather data files
        SolarResource(Location,random_number)
    
        # # WindSource(Location)
        WindSource_windlab(Location,random_number)
        
        pool = mp.Pool(mp.cpu_count()-2)
        #print (mp.cpu_count())
        pool = mp.Pool(mp.cpu_count()-1)
        print('Start %s %s!'%(Location,Input))
        output = [pool.apply_async(Optimise, args=(load, CF, storage_type, params,random_number,Input[3]))
                   for load in [5]
                   for CF in [50]#,60,70,80,90,100]
                   for storage_type in ['Salt Cavern'] 
                   for params in [simparams]]
        
        pool.close()
        pool.join()
        #print('Completed!')
        #for i in range(6):
        #    CF = CF_group[i]
        #    feedback = Optimise(load=5, cf=CF, storage_type='Salt Cavern', simparams=simparams,random_number=random_number)
        #    output.append(feedback)

        print('Completed %s %s!'%(Location,Input))
        
        RESULTS = pd.DataFrame(columns=['cf','capex[USD]','lcoh[USD/kg]','FOM_PV[USD]',
                                        'FOM_WIND[USD]','FOM_EL[USD]','FOM_UG[USD]',
                                        'H_total[kg]','pv_capacity[kW]',
                                        'wind_capacity[kW]','el_capacity[kW]',
                                        'ug_capcaity[kgH2]','pipe_storage_capacity[kgH2]',
                                        'bat_e_capacity[kWh]','bat_p_capacity[kW]',
                                        'pv_cost[USD]', 'wind_cost[USD]','el_cost[USD]',
                                        'ug_storage_cost[USD]','pipe_storage_cost[USD]',
                                   'bat_cost[USD]', 'load[kg/s]'])
        for i in output:
            results = i.get()
            RESULTS = pd.concat([RESULTS, pd.DataFrame([{'cf': results['CF'],
                                'capex[USD]': results['CAPEX'][0],
                                'lcoh[USD/kg]': results['lcoh'][0],
                                'FOM_PV[USD]':results['FOM_PV'][0],
                                'FOM_WIND[USD]':results['FOM_WIND'][0],
                                'FOM_EL[USD]':results['FOM_EL'][0],
                                'FOM_UG[USD]':results['FOM_UG'][0],
                                'H_total[kg]':results['H_total'][0],
                                'pv_capacity[kW]': results['pv_max'][0],
                                'wind_capacity[kW]': results['wind_max'][0],
                                'el_capacity[kW]': results['el_max'][0],
                                'ug_capcaity[kgH2]': results['ug_storage_capa'][0],
                                'pipe_storage_capacity[kgH2]': results['pipe_storage_capa'][0],
                                'bat_e_capacity[kWh]': results['bat_e_capa'][0],
                                'bat_p_capacity[kW]': results['bat_p_max'][0],
                                'pv_cost[USD]': results['pv_max'][0]*simparams['C_PV'],
                                'wind_cost[USD]': results['wind_max'][0]*simparams['C_WIND'],
                                'el_cost[USD]': results['el_max'][0]*simparams['C_EL'],
                                'ug_storage_cost[USD]': results['ug_storage_capa'][0]*results['C_UG_STORAGE'],
                                'pipe_storage_cost[USD]':results['pipe_storage_capa'][0]*simparams['C_PIPE_STORAGE'],
                                'bat_cost[USD]': results['bat_p_max'][0]*simparams['C_BAT_ENERGY'],
                                'load[kg/s]':results['LOAD'][0] }])], ignore_index=True)
            
            
        #RESULTS
        parent_directory = os.path.dirname(os.getcwd())
        path_to_file = parent_directory + os.sep + 'DATA' + os.sep + 'OPT_OUTPUTS' + os.sep 
        result_file = 'results(%s-UG_windlab)_2020_%s_%s_%s_%s.csv'%(Location,round(Input[0],2),round(Input[1],2),round(Input[2],2),round(Input[3],2))
    
        RESULTS.to_csv(path_to_file+result_file, index=False)
        
        # clean up template weather data
        dir = datadir + os.sep + 'SAM_INPUTS' + os.sep + 'SOLAR' + os.sep 
        if os.path.exists(dir + 'SolarSource_%s.csv'%random_number):
            os.remove(dir + 'SolarSource_%s.csv'%random_number)
            
        dir = datadir + os.sep + 'SAM_INPUTS' + os.sep + 'WIND' + os.sep 
        if os.path.exists(dir + 'WindSource_%s.srw'%random_number):
            os.remove(dir + 'WindSource_%s.srw'%random_number)

if __name__=='__main__':
    #from mpi4py import MPI
    inputFileName = os.getcwd()+'/input.txt'
    f = open( inputFileName )    
    lines = f.readlines()
    f.close()    
    Input = np.array([])
    for line in lines:
        cleanLine = line.strip() 
        if cleanLine[0] == "P" or cleanLine[0] == "#": 
            continue
        splitReturn = splitReturn = cleanLine.split(",")
        Input = np.append(Input,[float(splitReturn[0]),float(splitReturn[1]),float(splitReturn[2]),float(splitReturn[3]),
                                 float(splitReturn[4]),float(splitReturn[5]),float(splitReturn[6])])
    Input = Input.reshape(int(len(Input)/7),7)
    optimisation(Input[0])
    '''
    for i in range(len(Input)):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        if rank == i:
            optimisation(Input[i])
    '''
