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
wp = 0.12 #wilting point in percent
wc = 0.3     # water content in percent
fc = 0.36 # field capacity in percent

D= 100 # depth of soil layer in mm
Porosity = 0.45 # porosity in perent

Sat_wc = D * Porosity


## 

data, P, T_avg, SWE_obs, J, T_max, T_min = process_data(filepath)
meltflux = Snowmelt_DD_usace(k, T_avg)
Ps, Pr = P_to_Snow_and_Rain(P,T_avg)
simSWE,actmelt = simSWE(Ps,meltflux)
#P_in = np.add(Pr, actmelt)

# Compute ET

Ra = extrarad(J, lat)

RefEt = RefET_Hargreaves(T_max, T_min, Ra)


simET = simET(wp,wc,RefEt,fc)


#SM storage if multiplied by the depth of layer

SM, Qsurf = SM(Pr, actmelt, simET)

#Calc Runoff 

#Q = Qsurf(Pr, actmelt, simET)

# Check Water Balance

deltaS = checkWbal(Pr, simET, Q)
print deltaS


### plots
def plots1():
    plt.figure(figsize=(14,24))
    plt.subplot(411)
    plt.plot(data['Date'],P,'r-')
    plt.ylabel('Precipitation [mm]')
    plt.subplot(413)
    plt.plot(data['Date'],actmelt,'b-')
    plt.ylabel('Melt flux [mm/day]')
    plt.subplot(412)
    plt.plot(data['Date'],simSWE,'b-')
    plt.plot(data['Date'],SWE_obs,'ko')
    plt.xlabel('Date')
    plt.ylabel('SWE [mm]')
    plt.legend(('Modeled SWE','Observed SWE'))
    plt.subplot(414)
    plt.plot(data['Date'], Qsurf, 'b-')
    plt.ylabel('Qsurf [mm/day]')
    return plt.show()

def plotET():
     plt.figure(figsize=(14,24))
     plt.subplot(411)
     plt.plot(data['Date'],RefEt,'b-')
     plt.plot(data['Date'],simET,'ko')
     plt.xlabel('Date')
     plt.ylabel('ET [mm]')
     plt.legend(('Hargreaves_Ref_ET','simulate ET'))

plots1()
plotET()