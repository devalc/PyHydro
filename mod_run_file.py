# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:35:05 2018

@author: Chinmay Deval
"""
#import all modules 

from functions import *
import matplotlib.pyplot as plt


#locate snoel file
filepath= 'D:/Chinmay/Hydro_modeling_erin_fall_2018/snotel_623_pre_mgmt.csv'


# Latitude in Angular degrees
lat = 47.15


#optimized parameters
k = 1.1456 #length/degree/day
tbase = 4.77 #degC
train = 2.22 #degC
tsnow = 0.76 #degC


### 

data, P, T_avg, SWE_obs, J, T_max, T_min = process_data(filepath)
meltflux = Snowmelt_DD_usace(k, T_avg)
Ps, Pr = P_to_Snow_and_Rain(P,T_avg)
simSWE,actmelt = simSWE(Ps,meltflux)
#P_in = np.add(Pr, actmelt)

Ra = extrarad(J, lat)

RefEt = RefET_Hargreaves(T_max, T_min, Ra)
