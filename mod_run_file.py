# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:35:05 2018

@author: Chinmay Deval
"""
#import all modules 

from functions import *
import matplotlib.pyplot as plt


#locate snoel file
filepath= 'D:/Chinmay/Hydro_modeling_erin_fall_2018/Day1_snowmelt/snotel_623_pre_mgmt.csv'


# Latitude in Angular degrees
lat = 47.15


#optimized parameters
k = 4.6 #length/degree/day
tbase = 0.0 #degC
train = 3 #degC
tsnow = 0 #degC

#Soil Properties

wp = 0.12 #wiltin point in percent
wc = 3.0     # water content in percent
fc = 0.36 # field capacity in percent



## 

data, P, T_avg, SWE_obs, J, T_max, T_min = process_data(filepath)
meltflux = Snowmelt_DD_usace(k, T_avg)
Ps, Pr = P_to_Snow_and_Rain(P,T_avg)
simSWE,actmelt = simSWE(Ps,meltflux)
#P_in = np.add(Pr, actmelt)

Ra = extrarad(J, lat)

RefEt = RefET_Hargreaves(T_max, T_min, Ra)

simET = simET(wp,wc,RefEt,fc)

#Calc Runoff 
Q = (Pr + actmelt)- simET

### plots
def plots():
    plt.figure(figsize=(14,24))
    plt.subplot(411)
    plt.plot(data['Date'],P,'r-')
    plt.ylabel('Precipitation [mm]')
    plt.subplot(413)
    plt.plot(data['Date'],meltflux,'b-')
    plt.ylabel('Melt flux [mm/day]')
    plt.subplot(412)
    plt.plot(data['Date'],simSWE,'b-')
    plt.plot(data['Date'],SWE_obs,'ko')
    plt.xlabel('Date')
    plt.ylabel('SWE [mm]')
    plt.legend(('Modeled SWE','Observed SWE'))
    plt.subplot(414)
    plt.plot(data['Date'], Q, 'b-')
    plt.ylabel('Qsurf [mm/day]')
    return plt.show()

plots()