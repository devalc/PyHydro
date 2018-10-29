# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:35:13 2018

@author: Chinmay
"""

import matplotlib.pyplot as plt
import numpy as np
from evaluate import md, nse, rmse
from process_input import process_data
from snow import *
from ET import *
from height_wattable import *
from perc import *
from baseflow import *
from latq import *

#locate snoel file
filepath= 'C:/Chinmay/GitHub/Hydro_moddev/data/snotel_623_pre_mgmt.csv'

def run_model(filepath):
    
    ########### INIT Parameters##################
    # Latitude in Angular degrees
    lat = 47.15


    #optimized parameters
    k = 4.6 #length/degree/day
    tbase = 0.0 #degC
    train = 3 #degC
    tsnow = 0 #degC
    
    #Soil Properties
    D= 1000 # depth of soil layer in mm
    Pond_D = 1000-D  # mm
    wp_p = 0.12 #wilting point in percent
    wp = wp_p * D
#    wc = 0.3     # water content in percent
    fc_p = 0.36 # field capacity in percent
    fc = fc_p * D
    Porosity = 0.45 # porosity in perent
    
    Sat_wc = D * Porosity
    Smax = Sat_wc + Pond_D # maximum storage that can occur
    
    Kv = 1.0 #mm # vertical condutivity
    
    alpha = 0.02 #baseflow recession coefficient
    
    Ksat= 1000.0  #saturated hydraulic conductivity mm/day
    slope = 0.1
    
    
    data, P, T_avg, SWE_obs, J, T_max, T_min = process_data(filepath)
    
    
    
    #Storage and runoff
    s = np.zeros(P.shape) #array of storage
    q = np.zeros(P.shape) # array  runoff 
    hwt = np.zeros(P.shape) #height of water table
    latq = np.zeros(P.shape) # lateral flow
    latq_in = np.zeros(P.shape) # lat flow in from upstream
    Perc = np.zeros(P.shape) # percolation
    sb = np.zeros(P.shape) #baseflow storage
    bf = np.zeros(P.shape) #baseflow
    Q = np.zeros(P.shape)  #Discharge
    et = np.zeros(P.shape) # Evapotranspiration
    
    
    meltflux = Snowmelt_DD_usace(k, T_avg)
    Ps, Pr = P_to_Snow_and_Rain(P,T_avg)
    SWEsim,actmelt = simSWE(Ps,meltflux)
    P_s = Pr + actmelt # water stored in system from Precip and melt
    # Compute ET
    Ra = extrarad(J, lat)
    RefEt = RefET_Hargreaves(T_max, T_min, Ra)
    PotET = ETpot(RefEt)
    
    et[0]= simET(wp, s[0] ,PotET[0],fc)
    s[0] = s[0] + P_s[0] - et[0]
    
    for i in range(1,P.shape[0],1):
        et[i] = simET(wp, s[i-1] ,PotET[i],fc)
        hwt[i] = ht_wattab(s[i-1]/1000.0 ,fc_p ,Porosity ,D)
        if hwt[i] > 0:
            Perc[i] = perc(Kv)
        bf[i]= baseflow(sb[i-1], alpha)
        sb[i] = sb[i-1] + Perc[i] - bf[i]
        latq[i] = qlat(Ksat,slope,hwt[i],l=10000.0)
        latq_in [i] = latq[i]*1.0
        s[i] = s[i-1] + P_s[i] + latq_in[i] - et[i] - latq[i] - Perc[i]
        if s[i] > Smax:
            q[i] = s[i] - Smax
            s[i] = Smax
        Q[i] = q[i] + latq[i] + bf[i]
    
    print (SWEsim, PotET, et, hwt, Q)
    
    p = np.where(s>Sat_wc, s-Sat_wc, 0.0)
    swc = np.subtract(s,p)
    
#   
    plt.plot(data['Date'], SWE_obs, 'r', data['Date'], SWEsim, 'k')
    plt.show()
    
    plt.subplot(2,1,1)
    plt.plot(data['Date'], s, 'r', data['Date'], swc, 'k', data['Date'], p, 'b')
    plt.subplot(2,1,2)
    plt.plot(data['Date'], PotET, 'r', data['Date'], et, 'k')
    plt.show()

    plt.plot(data['Date'], bf, 'r', data['Date'], latq, 'g', data['Date'], q, 'c', data['Date'], Q, 'b')
    plt.show()
    plt.plot(data['Date'], ((Q/1000.0)*10.0*10.0)/(60.0*60.0*24.0), 'b')
    plt.show()
    
    print("Checking Water Balance")
    print("P", np.sum(P_s))
    print("ET", np.sum(et))
    print("q", np.sum(q))
    print("storage", s[-1])
    print("balance", s[-1]+np.sum(et)+np.sum(q)-s[0]+np.sum(np.subtract(latq, latq_in))+np.sum(Perc))
    
run_model(filepath)