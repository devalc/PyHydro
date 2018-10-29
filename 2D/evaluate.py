# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:33:24 2018

@author: Chinmay
"""

import numpy as np


def md(sim, obs):
    """
    Mean difference 

    """
    return(np.mean(np.subtract(sim, obs)))

def nse(sim, obs):
    """
    Nash-Sutcliffe Efficiency

    """
    obs_mod2 = np.sum(np.square(np.subtract(obs, sim)))
    obs_mean2 = np.sum(np.square(np.subtract(obs, np.mean(obs))))
    nse = 1-(obs_mod2/obs_mean2)
    return nse

def rmse(sim, obs):
    """
    
    """
    return(np.nanmean(np.sqrt(np.square(np.subtract(sim, obs)))))
