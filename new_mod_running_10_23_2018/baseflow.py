# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:45:13 2018

@author: Chinmay
"""

#import numpy as np

#def baseflow(storage, perc, alpha = 0.2):
#    bflo = np.zeros(storage.shape)
#    
#    for i in range (1, len(storage)):
#        bflo[i] = storage[i] * alpha
#        storage[i]= storage[i-1] - bflo[i] + perc[i] 
#    return bflo, storage


def baseflow(storage, alpha, beta=1):
    return alpha*storage**beta
    