# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:28:44 2022

@author: Ahmad Mojiri
"""
from projdirs import optdir
import numpy as np
from PACKAGE.component_model import pv_gen, wind_gen
import os
import shutil
import pandas as pd

def make_dzn_file(DT, EL_ETA, BAT_ETA_in, BAT_ETA_out,
                  C_PV, C_WIND, C_EL, C_UG_STORAGE,UG_STORAGE_CAPA_MAX,
                  C_PIPE_STORAGE,  
                  PIPE_STORAGE_CAPA_MIN, C_BAT_ENERGY,
                  C_BAT_POWER,
                  OM_PV, OM_WIND, OM_EL, OM_UG,
                  CF, PV_REF, PV_REF_POUT, WIND_REF,
                  WIND_REF_POUT, LOAD, DIS_RATE, random):
    n_project = 25
    crf = DIS_RATE * (1+DIS_RATE)**n_project/((1+DIS_RATE)**n_project-1)
    # pdb.set_trace()    
    H_total = (CF/100)*sum(LOAD)*DT*3600
    
    string = """
    N = %i;
    
    DT = %.2f;      %% time difference between sample points (hr)
    
    EL_ETA = %.2f;  %% conversion factor of the electrolyser
    BAT_ETA_in = %.2f;   %%charging efficiency of electrochemical battery
    BAT_ETA_out = %.2f;  %%discharging efficiency of electrochemical battery 
    
    C_PV = %.2f;    %% unit cost of PV ($/kW)
    C_WIND =  %.2f;    %% unit cost of Wind farm ($/kW)
    C_EL =  %.2f;    %% unit cost of electrolyser ($/kW)
    C_UG_STORAGE = %.2f;    %% unit cost of hydrogen storage ($/kgH)
    UG_STORAGE_CAPA_MAX = %.2f; %%maximum size of underground storage $/(kg of H2)
    C_PIPE_STORAGE = %.2f; %% unit cost of storage with line packing $/(kg of H2)
    PIPE_STORAGE_CAPA_MIN = %.2f; %% minimum size of line packing (kg of H2)
    
    C_BAT_ENERGY = %.2f;   %% unit cost of electrochemical battery energy ($/kWh)
    C_BAT_POWER = %.2f;   %% unit cost of electrochemical battery power ($/kWh)

    OM_PV = %.2f;    %% Annual O&M cost of PV ($/kW)
    OM_WIND = %.2f;  %% Annual O&M cost of wind ($/kW)
    OM_EL = %.2f;    %% Annual O&M cost of electrolyser ($/kW)
    OM_UG = %.2f;    %% %% Annual O&M cost of underground storage ($/kg)
    
    RES_H_CAPA = %.2f;       %% reserved hydrogen for lowered capcaity factor
    
    PV_REF = %.2f;       %%the capacity of the reference PV plant (kW)
    
    %% Power output time series from reference PV plant (W)
    PV_REF_POUT = %s;                                  
     
     
    WIND_REF = %.2f;  %% the capacity of the refernce wind plant (kW)
    
    %% power output time series from the reference wind plant (W)
    WIND_REF_POUT = %s;  
    
    %% load timeseries (kgH/s)                             
    LOAD = %s;
    
    %% discount rate in absolute value not in percentage
    DIS_RATE = %s;
    
    %%capital recovery factor
    crf = %s;
    
    %%Hydrogen production
    H_total = %s;
    
    """ %(len(LOAD), DT, EL_ETA, BAT_ETA_in, BAT_ETA_out,
          C_PV, C_WIND, C_EL, C_UG_STORAGE, UG_STORAGE_CAPA_MAX, C_PIPE_STORAGE,
          PIPE_STORAGE_CAPA_MIN, C_BAT_ENERGY,
          C_BAT_POWER, OM_PV, OM_WIND, OM_EL, OM_UG,
          (1-CF/100)*sum(LOAD)*DT*3600, PV_REF, str(PV_REF_POUT), WIND_REF,
          str(WIND_REF_POUT), str(LOAD), DIS_RATE,crf,H_total )
    
    #filename = optdir + "hydrogen_plant_data_%s.dzn"%(str(CF))
    file_name_new = optdir + "hydrogen_plant_data_%s_%s.dzn"%(str(CF),random)
    #shutil.copy(filename,file_name_new)
    with open(file_name_new, "w") as text_file:
        text_file.write(string)
        
        
def Minizinc(simparams):
    """
    Parameters
    ----------
    simparams : a dictionary including the following parameters:
        DT, ETA_PV, ETA_EL, C_PV, C_W, C_E, C_HS, CF, pv_ref_capa,
                  W, pv_ref_out, L

    Returns
    -------
    a list of outputs including the optimal values for CAPEX, p-pv, p_w, p_e,
    e_hs

    """
    make_dzn_file(**simparams)
    
    #mzdir = parent_directory + os.sep + 'MiniZinc'
    # I commented out the mzdir command because it is annoyying to refer to the installation dir
    # in different systems. I think a better way is that we add minizinc to an environment variable 
    #during the installation
    
    minizinc_data_file_name = "hydrogen_plant_data_%s_%s.dzn"%(str(simparams['CF']),simparams['random'])
    from subprocess import check_output
    output = str(check_output([#mzdir + 
                               'minizinc', "--soln-sep", '""',
                               "--search-complete-msg", '""', "--solver",
                               "COIN-BC", optdir + "hydrogen_plant.mzn",
                               optdir + minizinc_data_file_name]))
    
    output = output.replace('[','').replace(']','').split('!')
    for string in output:
        if 'CAPEX' in string:
            results = string.split(';')
    
    results = list(filter(None, results))
    
    RESULTS = {}
    for x in results:
        RESULTS[x.split('=')[0]]=np.array((x.split('=')[1]).split(',')).astype(float)        
    
    #remove the minizinc data file after running the minizinc model
    
    mzfile = optdir + os.sep + minizinc_data_file_name
    
    if os.path.exists(mzfile):
        os.remove(mzfile)
    
    
    return(  RESULTS  )

def Optimise(random_number, Location):
    path=os.getcwd()+os.sep+'MERRA2'
    pv_ref = 1e3 #(kW)
    pv_ref_pout = list(np.trunc(100*np.array(pv_gen(pv_ref,random_number)))/100)
    pv = pd.DataFrame(pv_ref_pout , columns=['Solar'])
    pv.to_csv(path+os.sep+f'{Location}_PV.csv')

    wind_ref = 320e3 #(kW)
    wind_ref_pout = list(np.trunc(100*np.array(wind_gen(random_number)))/100)
    wind = pd.DataFrame(wind_ref_pout , columns=['Wind'])
    wind.to_csv(path+os.sep+f'{Location}_wind.csv')
    '''
    simparams.update(DT = 1,#[s] time steps
                     PV_REF = pv_ref, #capacity of reference PV plant (kW)
                     PV_REF_POUT = pv_ref_pout, #power output from reference PV plant (kW)
                     WIND_REF = wind_ref, #capacity of reference wind farm (kW)
                     WIND_REF_POUT = wind_ref_pout, #power output from the reference wind farm (kW)
                     C_UG_STORAGE = Cost_hs(initial_ug_capa, storage_type)*ug_storage_ratio,
                     LOAD = [load for i in range(len(pv_ref_pout))], #[kgH2/s] load profile timeseries
                     CF = cf,           #capacity factor
                     random = random_number)
 
    
    #print('Calculating for CF=', simparams['CF'])
    results = Minizinc(simparams)
    
    if simparams['UG_STORAGE_CAPA_MAX']>0:
        new_ug_capa = results['ug_storage_capa'][0]/1e3
        if np.mean([new_ug_capa,initial_ug_capa]) > 0:
            if abs(new_ug_capa - initial_ug_capa)/np.mean([new_ug_capa,initial_ug_capa]) > 0.05:
                initial_ug_capa = new_ug_capa
                print('Refining storage cost; new storage capa=', initial_ug_capa)
                simparams['C_UG_STORAGE'] = Cost_hs(initial_ug_capa, storage_type)*ug_storage_ratio
                results = Minizinc(simparams)
    
    results.update(CF=simparams['CF'],
                   C_UG_STORAGE=simparams['C_UG_STORAGE'])
    '''
    return()
    
def Cost_hs(size,storage_type):
    """
    This function calculates the unit cost of storage as a function of size
    
    Parameters
    ----------
    size: storage capacity in kg of H2
    storage_type: underground storage type; 
                one of ['Lined Rock', 'Salt Cavern']

    Returns unit cost of storage in USD/kg of H2
        
    """
    if size > 0:
        x = np.log10(size)
        if size > 100:
            if storage_type == 'Salt Cavern':
                cost=10 ** (0.212669*x**2 - 1.638654*x + 4.403100)
                if size > 8000:
                    cost = 17.66
            elif storage_type == 'Lined Rock':
                cost =10 ** (   0.217956*x**2 - 1.575209*x + 4.463930  )
                if size > 4000:
                    cost = 41.48
        else:
            cost = 10 ** (-0.0285*x + 2.7853)
    else:
        cost = 516
    return(cost)
