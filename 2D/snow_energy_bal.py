# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 11:02:33 2018

@author: deva4998
"""

import numpy as np
from unit_converter import deg2rad

##### Def constants

pi = np.pi
G_Sc_d = 118.1 ##### Solar constant in  MJ/m2.day
G_sc_min= 0.0820 ##### Solar constant in  MJ/m2.min
LHV = 0.408 #### latent heat of vaporization in MJ/kg


###########################


def extrarad(J, lat, units = 'degrees'):
     
    """ 
    args:
        J: day of year
        lat: Latitude in angular degrees (converted to rad in func)
    
    Calculates:
        inverse relative distance Earth-sun (dr) and\
        solar declination (delta)
        Sunset hour angle (Ws)
    returns:
        Ra: Extraterrestrial radiation in mm/day
        
        """
    if units == 'degrees':
        lat = deg2rad(lat)
    else:
        lat = lat
    
    dr = 1 + (0.033*np.cos((2*pi/365)*int(J)))
    delta = 0.4093 * np.sin(((2*np.pi/365)*int(J))-1.39)
    Ws = np.arccos(-np.tan(lat)*np.tan(delta))
    extrarad = ((24 * 60) /pi) * G_sc_min * dr * (Ws * np.sin(lat) * np.sin(delta) +\
                np.cos(lat) * np.cos(delta) * np.sin(Ws))
    extrarad = np.multiply(extrarad, LHV)
    
    return extrarad
    
    
def albedo (TS):
    """
    Computes albedo as a function of 
    number of days since the last snowfall (TS)
    """
    
    a = np.multiply(0.738, np.power(TS, -0.1908))
    
    return a


#def solar_declination(J):
#    
#    """
#    Computes solar declination angle (in radians) given the jay of year 
#    
#    """
#    delta = np.multiply(0.4093, np.sin(np.subtract(np.multiply(np.divide(2*np.pi, 365), J), 1.39)))
#    
#    return delta


def solar_elevationangle(lat, delta, Td = 12.0, Sn = 12.0 , units= 'degrees'):
    
    """
    computes solar elevatio angle (in radians)
    It is the angle between solar rays and horizontal surface
    
    args:
        lat: latitude in angular degrees ( converted to rads in this func)
        delta: solar declination angle (in radians)
        Td: Time of day in (hrs)
        Sn: time of solar noon (hrs)
        units: "radians" or "degrees"  default is degrees
    
    """
    if units == 'degrees':
        lat = deg2rad(lat)
    else:
        lat = lat

    sinphi = np.add(np.multiply(np.sin(lat), np.sin(delta)),\
                    np.multiply((np.multiplty(np.cos(lat), np.cos(delta)),np.cos(np.divide(np.multiply(pi, np.subtract(Td-Sn)),12.0)))))    
   
    return np.arcsin(sinphi)


    
def solar_azimuthangle(Sphi, lat, delta, units = 'degrees', Td = 12, Sn = 12 ):
        
    
    """
    
    Computes solar azimuth angle (horizontal angle between 
    due south and the sun; radians)
    
    args:
        Sphi : solar elevation/ altitude angle (in degrees; converted to radians within the fucn)
        J: day of year
        delta: solar declination angle (in degrees converted to radians within the fucn)
        Td: Time of day in (hrs)
        Sn: time of solar noon (hrs)
        units: "radians" or "degrees" 
    """
    
    if units == 'degrees':
        lat = deg2rad(lat)
    else:
        lat = lat
        
    azs = np.arccos(np.divide((np.subtract(np.multiply(np.sin(Sphi), np.sin(lat)), np.sin(delta))),np.multiply(np.cos(Sphi), np.cos(lat))))
    azs = np.where(Td > Sn, np.add(pi, azs), np.subtract(pi, azs))
    
    return azs
    

def solar_incidenceangle(slope, aspect, az, Sphi, units = 'degrees'):
    """
    computes angle between insolation and horizontal surface
    
    args:
        slope: slope of land surface
        aspect: aspect of land surface
        az: solar azimuth angle (horizontal angle between 
    due south and the sun; radians)
        Sphi: solar elevatio angle (in radians)
        units: "radians" or "degrees"
        
    """
    if units == 'degrees':
        slope = deg2rad(slope)
        aspect = deg2rad(aspect)
    else:
        slope = slope
        aspect = aspect
    
    i = np.arcsin(np.multiply(np.sin(np.arctan(slope)), np.multiply(np.cos(Sphi), np.cos(np.subtract(az, slope)))))
    np.where(i>0.0, i, 0.0)
    
    return i



def qs(lat, J, slope, aspect, TS =0.0, C_f = 0.0, units = 'degrees'):
    
    """
    Calcualtes Incident solar radiaiton on sloping surface(MJ/m2)
    
    args:
        lat: latitude (in angular degrees)
        J: day of year
        C_f: forest Canopy Factor
        a = albedo of snow
        qd: direct solar radiation on falt surface (MJ/m2) / Extraterrestrial Rad
        Si : solar incidence angle (in radians)
        Sphi : solar elevation/ altitude angle (in radians)
        
        
    
    """
    if units == 'degrees':
        lat = deg2rad(lat)
        slope = deg2rad(slope)
        aspect = deg2rad(aspect)
    else:
        lat = lat
        slope = slope
        aspect = aspect
    #solar declination angle
    delta = 0.4093 * np.sin(((2*np.pi/365)*int(J))-1.39)
    #solar elevation angle
    Sphi = solar_elevationangle(lat, delta)
    # solar azimuth angle
    azs = solar_azimuthangle(Sphi, lat, delta)
    #solar radiation incident on a flat surface
    qd = extrarad(J ,lat)
    # albedo of snow
    a = albedo(TS)
    # solar incidence angle
    i = solar_incidenceangle(slope, aspect, azs, Sphi)
    
    qs = np.multiply(max(0.1,(1-C_f)), (1-a)*qd*max(0,(np.sin(i)/np.sin(Sphi))))
    
    return qs