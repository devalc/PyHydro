# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 11:02:33 2018

@author: deva4998
"""

import numpy as np
from unit_converter import *

##### Def constants

GSc = 118.1 ##### Solar constant in  MJ/m2 day

######
    
def albedo (TS):
    """
    Computes albedo as a function of 
    number of days since the last snowfall (TS)
    """
    
    a = np.multiply(0.738, np.power(TS, -0.1908))
    
    return a


def solar_declination(J):
    
    """
    Computes solar declination angle (in radians) given the jay of year 
    
    """
    delta = np.multiply(0.4093, np.sin(np.subtract(np.multiply(np.divide(2*np.pi, 365), J), 1.39)))
    
    return delta








def qs(lat, J, slope, aspect, TS, C_f ):
    
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