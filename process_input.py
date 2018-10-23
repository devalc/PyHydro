# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:34:30 2018

@author: Chinmay
"""
import pandas as pd

def process_data(filepath):
    data = pd.read_csv(filepath, nrows = 6954,parse_dates=['Date'], skiprows=1,\
                       names= ['Date', 'SWE_obs','P_accum','T_max','T_min',\
                               'T_avg','P_incremental']).dropna()
    data['Jday'] = data['Date'].apply(lambda x: x.strftime('%j'))
    J = data['Jday']
    P = data['P_incremental'].values
    T_avg = data['T_avg'].values
    T_max = data['T_max'].values
    T_min = data['T_min'].values
    SWE_obs= data['SWE_obs'].values
    return data, P, T_avg, SWE_obs, J, T_max, T_min
