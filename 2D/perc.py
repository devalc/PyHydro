# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:44:00 2018

@author: Chinmay Deval
"""

import numpy as np

#def perc(soilmoist, fc, D=100, n=0.45, Kv= 1.0):
#    """
#    Kv: vertical conductivity in mm/day
#    
#    
#    """
#    perc = np.zeros(soilmoist.shape)
##    sat_wc = D*n
#    for i in range(1,len(soilmoist)):
#        if soilmoist[i] > fc:
#            perc[i] = Kv
#        else:
#            perc[i] = 0
#    return perc

def perc(Kv):
    return Kv

def Perc_2d(kv, hwt):
    perc = np.where(hwt > 0.0, kv, 0.0)
    return perc