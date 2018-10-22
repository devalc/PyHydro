# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:13:56 2018

@author: Chinmay
"""
import numpy as np
from unit_converter import *


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
