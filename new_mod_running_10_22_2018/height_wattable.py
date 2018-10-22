# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:42:57 2018

@author: Chinmay
"""

import numpy as np

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