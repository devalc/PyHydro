# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:41:02 2018

@author: Chinmay
"""

import numpy as np

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