# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 13:35:05 2018

@author: Chinmay Deval
"""

from functions import *
import matplotlib.pyplot as plt



filepath= 'D:/Chinmay/Hydro_modeling_erin_fall_2018/snotel_623_pre_mgmt.csv'


#optimized parameters
k = 1.1456
tbase = 4.77
train = 2.22
tsnow = 0.76


data, P, T_avg, SWE_obs = process_data(filepath)
meltflux = Snowmelt_DD_usace(k, T_avg)
Ps, Pr = P_to_Snow_and_Rain(P,T_avg)
simSWE,actmelt = simSWE(Ps,meltflux)
P_in = np.add(Pr, actmelt)
