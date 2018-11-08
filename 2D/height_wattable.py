# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:42:57 2018

@author: Chinmay
"""

import numpy as np

#def ht_wattab(soilmoist,fc,D= 100, n=0.45):
#    """
#        
#   
#    Computes height of water table
#    
#    where:
#        D = depth of soil layer (mm)
#        n= porocity of soil layer (%)
#        fc = watercontent at field capacity
#        
#    
#    """
#    
#    ht = np.zeros(soilmoist.shape)
#    sat_wc = D*n
#    for i in range(1, len(soilmoist)):
#        if soilmoist[i] < fc:
#            ht[i] = 0
#        elif soilmoist[i] > sat_wc:
#            ht[i] = D
#        else:
#            ht[i] = D*((soilmoist[i]-fc)/(sat_wc-fc))
#    return ht

#def ht_wattab(soilmoist,fc, porosity, D):
#    
#    """
#        
#   
#    Computes height of water table
#    
#    where:
#        D = depth of soil layer (mm)
#        fc = watercontent at field capacity in percent
#        porosity: in percent
#       
#    
#    """
#    if soilmoist < fc:
#        ht = 0
#    elif soilmoist >= porosity:
#        ht = D
#    else:
#        ht = D*((soilmoist-fc)/(porosity-fc))
#    return ht

def ht_wattab(soilmoist,fc, porosity, D):
    
    """
        
   
    Computes height of water table
    
    where:
        D = depth of soil layer 
        fc = watercontent at field capacity in percent
        porosity: in percent
        soilmoist : soilmoisture content
        
    when soilmoist less than field capacity, no ht (water table set to depth)
       
    
    """
    
    ht = np.where(soilmoist < fc, 0.0, D)
    # where water content is between field capacity and porosity, water table height is determined linearly
    # the previous line accounts for anywhere water content is >= porosity
    ht = np.where((soilmoist < porosity) & (soilmoist >= fc), D*((soilmoist-fc)/(porosity-fc)), ht)
    return ht