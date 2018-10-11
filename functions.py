# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 12:51:29 2018

@author: Chinmay Deval
"""

import numpy as np
import pandas as pd




def process_data(filepath):
    data = pd.read_csv(filepath, nrows = 6954,parse_dates=['Date'], skiprows=1,\
                       names= ['Date', 'SWE_obs','P_accum','T_max','T_min',\
                               'T_avg','P_incremental']).dropna()
    data['Jday'] = data['Date'].apply(lambda x: x.strftime('%j'))
    J = data['Jday']
    P = data['P_incremental'].values
    T_avg = data['T_avg'].values
    T_max = data['T_max'].values
    T_min = data['T_min'].values
    SWE_obs= data['SWE_obs'].values
    return data, P, T_avg, SWE_obs, J, T_max, T_min




def P_to_Snow_and_Rain(P, T, Tsnow = 3.0, Train=3.0):
    """
    Calculates precipitation falling as snow
    takes in:
        precip: Daily precipitation 
        temp: Daily mean or min or max air temperature in degree C
        train: Temperature at which precipitation is assumed to be rain (default = 3.0 degreeC)
        tsnow: Temperature at which precipitation isassumed to be snow (default = 0.0 degreeC)

    """
    snow = np.where(T < Train, np.where(T>Tsnow, np.multiply(P, np.divide(np.subtract(T,Tsnow), (Train-Tsnow))), P), 0.0)
    rain = np.subtract(P, snow)
    return snow, rain


def Snowmelt_DD_usace(k, temp, tbase=0.0):
    """
    Temperature index Degree day snowmelt model based on USACE doc
    takes in:
        k: Empirically derived constant with units length/degree/day
        temp: Daily mean or min or max air temperature 
        tbase: Base temperature. USACE recommends 0.0 (C) for forested \
        areas and -4.4 (C) for open areas (default = 0.0)
    Returns:
        melt flux
    """
    melt = k*(temp-tbase)
    melt[melt < 0.0] = 0.0
    return melt



def simSWE(Psnow, meltflux):
    """
    calcualtes change in SWE when accounting for melt
    Takes in:
        Psnow: Precipitation that falls as snow
        meltflux: Snowmelt
    throws out:
        Cumulative snow water equivalent (SWE), and the actual amount of snow that melted
    """
    cumSWE = np.zeros(Psnow.shape, dtype=np.float32)
    act_melt = np.zeros(meltflux.shape, dtype=np.float32)
    for t in range(1,Psnow.shape[0]):
        swe_inc = (cumSWE[t-1] + Psnow[t]) - meltflux[t]
        if swe_inc > 0.0:
            cumSWE[t] = swe_inc
            act_melt[t] = meltflux[t]
        else:
            act_melt[t] = cumSWE[t-1]

    return cumSWE, act_melt



def md(sim, obs):
    """
    Mean difference 

    """
    return(np.mean(np.subtract(sim, obs)))

def nse(sim, obs):
    """
    Nash-Sutcliffe Efficiency

    """
    obs_mod2 = np.sum(np.square(np.subtract(obs, sim)))
    obs_mean2 = np.sum(np.square(np.subtract(obs, np.mean(obs))))
    nse = 1-(obs_mod2/obs_mean2)
    return nse

def rmse(sim, obs):
    """
    
    """
    return(np.nanmean(np.sqrt(np.square(np.subtract(sim, obs)))))



def celsius2kelvin(celsius):
    """
    Convert temperature in degrees Celsius to degrees Kelvin.
    :param celsius: Degrees Celsius
    :return: Degrees Kelvin
    :rtype: float
    """
    return celsius + 273.15


def kelvin2celsius(kelvin):
    """
    Convert temperature in degrees Kelvin to degrees Celsius.
    :param kelvin: Degrees Kelvin
    :return: Degrees Celsius
    :rtype: float
    """
    return kelvin - 273.15


def deg2rad(deg):
    """
    Convert angular degrees to radians
    :param degrees: Value in degrees to be converted.
    :return: Value in radians
    :rtype: float
    """
    return deg * (np.pi / 180.0)


def rad2deg(rads):
    """
    Convert radians to angular degrees
    :param radians: Value in radians to be converted.
    :return: Value in angular degrees
    :rtype: float
    """
    return rads * (180.0 / np.pi)


    
def extrarad(J, lat, G_sc= 0.0820):
    
    
        """ 
    args:
        J: day of year
        lat: Latitude in angular degrees
    
    Calculates:
        inverse relative distance Earth-sun (dr) and\
        solar declination (delta)
        Sunset hour angle (Ws)
    returns:
        Ra: Extraterrestrial radiation in MJ/m2/day
        
        """

        Ra = np.zeros(J.shape)
        for i in J:
            dr = 1 + (0.033*np.cos((2*np.pi/365)*int(i)))
            delta = 0.4093 * np.sin(((2*np.pi/365)*int(i))-1.39)
            Ws = np.arccos(-np.tan(deg2rad(lat))*np.tan(delta))
            extrarad = ((24 * 60) / np.pi) * G_sc * dr * (Ws * np.sin(deg2rad(lat)) * np.sin(delta) +\
        np.cos(deg2rad(lat)) * np.cos(delta) * np.sin(Ws))
            extrarad = np.divide(extrarad, 2.45)
            Ra = np.append(Ra, extrarad)
            Ra = Ra[1:]
        return Ra


def RefET_Hargreaves(Tmax, Tmin, Ra):
    """
    Args:
    Tmax : max daily air temperature degC
    Tmin : min daily air temperature degC
    Ra: Extraterrestrial radiation mm/day
    
    calculates:
    Tmean : mean daily air temperature degC calculated as (Tmax+Tmin)/2
    ETo: Reference ET mm/day
    
    """
    
    ETo = 0.0023*np.sqrt(Tmax-Tmin)*(((Tmax+Tmin)/2)+17.8)*Ra
    return ETo


def ETpot(ref_et, kc=1.0):
    """
    Calculates Potential ET as a funciton of crop coefficient Kc
    Kc is assumed to be 1 in this model for simplicity
    """
    etpot = ref_et * kc
    return etpot


def simET( wp, wc, potET, fc):
    """
    simulates actual evapotranspiration based on soil water stress
    soil water stress factor is calculated using wilting point, water content\
    and field capacity
    Args:    
    wp: Wilting point
    wc: Water content
    potET: Potential evapotranspiration
    fc: Field capacity
    
    throws out:
    Act ET
    """
    theta = 1.0
    if wc < 0.8*fc and wc > wp:
        theta = (0.8*fc - wc)/(0.8*fc-wp)
    elif wc <= wp:
        theta = 0.0
    return(potET*theta)



def SM(Precip, snowmelt, ET, D=100, n=0.45):
    """
    Computes soil moisture 
    
    where:
        D = depth of soil layer (mm)
        n= porocity of soil layer (%)
    """
    SM = np.zeros(Precip.shape)
    Qsurf = np.zeros(Precip.shape)
    #saturated water content
    sat_wc = D*n
    for i in range(1, len(Precip)):
        SM[i] = Precip[i] + snowmelt[i] + SM[i-1] -ET[i]
        if SM[i] > sat_wc:
            Qsurf [i] = SM[i] - sat_wc 
            SM[i] = sat_wc
    SM = np.where(SM<0,0,SM)
    return SM, Qsurf


def ht_wattab(soilmoist,fc,D= 100, n=0.45):
    """
        
   
    Computes height of water table
    
    where:
        D = depth of soil layer (mm)
        n= porocity of soil layer (%)
        fc = watercontent at field capacity
        
    
    """
    
    ht = np.zeros(soilmoist.shape)
    sat_wc = D*n
    for i in range(1, len(soilmoist)):
        if soilmoist[i] < fc:
            ht[i] = 0
        elif soilmoist[i] > sat_wc:
            ht[i] = D
        else:
            ht[i] = D*((soilmoist[i]-fc)/(sat_wc-fc))
    return ht
        

def perc(soilmoist, fc, D=100, n=0.45, Kv= 1.0):
    """
    Kv: vertical conductivity in mm/day
    
    
    """
    perc = np.zeros(soilmoist.shape)
#    sat_wc = D*n
    for i in range(1,len(soilmoist)):
        if soilmoist[i] > fc:
            perc[i] = Kv
        else:
            perc[i] = 0
    return perc
    
    
def qlat(ht,SM, fc, Ksat=10, D = 100, w=20):
    
    """
    w: width of soil over which we have ht
    """
    qlat = np.zeros(ht.shape)
    
    for i in range(1, len(ht)):
#        if SM[i] > fc:
#            k = 
#            
        qlat[i] =  ht[i] * Ksat 
    return qlat


def baseflow(storage, perc, alpha = 0.2):
    bflo = np.zeros(storage.shape)
    
    for i in range (1, len(storage)):
        bflo[i] = storage[i] * alpha
        storage[i]= storage[i-1] - bflo[i] + perc[i] 
    return bflo, storage



def checkWbal(Precip, ET, Qsurf):
    """
    Checks water balance by computing change in storage (deltaS)
    Precip: is the precipitation falling as Rain
    ET: simulated Evapotranspiration
    Qsurf: Surface runoff
    """
    
    deltaS = Precip - ET- Qsurf
    
    return deltaS



