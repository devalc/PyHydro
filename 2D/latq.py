# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:44:40 2018

@author: Chinmay
"""
#
#import numpy as np
#
#def qlat(ht,SM, fc, Ksat=10, D = 100, w=20):
#    
#    """
#    w: width of soil over which we have ht
#    """
#    qlat = np.zeros(ht.shape)
#    
#    for i in range(1, len(ht)):
##        if SM[i] > fc:
##            k = 
##            
#        qlat[i] =  ht[i] * Ksat 
#    return qlat

def qlat(Ksat,slope,hwt,l=1, w=1):
    """
    Ksat: saturated conductivity
    hwt: height of watertable
    l, w: length and width respectively
    """
    
    qlat = ((Ksat*slope*hwt*w)/(w*l))
    
    return qlat