# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:37:34 2018

@author: Chinmay
"""
import numpy as np

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


def P_to_Snow_and_Rain_2d(P, T, Tsnow = 3.0, Train=3.0):
    """
    Calculates precipitation falling as snow
    takes in:
        precip: Daily precipitation 
        temp: Daily mean or min or max air temperature in degree C
        train: Temperature at which precipitation is assumed to be rain (default = 3.0 degreeC)
        tsnow: Temperature at which precipitation isassumed to be snow (default = 0.0 degreeC)

    """
    snow = np.zeros(P.shape)
    for i in np.arange(0, P.shape[1]):
        for j in np.arange(0, P.shape[2]):
            snow[:,i,j] = np.where(T[:,i,j] < Train, np.where(T[:,i,j]>Tsnow,
                np.multiply(P[:,i,j], np.divide(np.subtract(T[:,i,j],Tsnow),
                            (Train-Tsnow))), P[:,i,j]), 0.0)
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



def simSWE_2d(Psnow, meltflux):
    """
    calcualtes change in SWE when accounting for melt
    Takes in:
        Psnow: Precipitation that falls as snow
        meltflux: Snowmelt
    throws out:
        Cumulative snow water equivalent (SWE), and the actual amount of melted snow
    """
    cumSWE = np.zeros(Psnow.shape, dtype=np.float32)
    act_melt = np.zeros(meltflux.shape, dtype=np.float32)
    for i in range(0, Psnow.shape[1]):
        for j in range(0, Psnow.shape[2]):
            for k in range(1, Psnow.shape[0]):
                swe_inc = cumSWE[k-1, i, j] + Psnow[k, i, j] - meltflux[k, i, j]
                if swe_inc > 0.0:
                    cumSWE[k, i, j] = swe_inc
                    act_melt[k, i, j] = meltflux[k, i, j]
                else:
                    act_melt[k, i, j] = cumSWE[k-1, i, j]

    return cumSWE, act_melt




