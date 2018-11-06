# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:34:30 2018

@author: Chinmay
"""
import pandas as pd
import numpy as np
import unit_converter as uc
import gdal
import richdem as rd

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


def process_wepp_cli(filepath):
    """
    reads in typical climate file as obtained from WEPPcloud
    and extracts day of year (doy), Precipitation (P), maximum temperature (tmax)
    and min temp (tmin)
    """
    clim = np.loadtxt(filepath, skiprows =15)
    d = clim[:,0]
    m = clim[:,1]
    y = clim[:,2]
    doy = uc.ymd_to_doy(y,m,d)
    P = clim[:,3] * 0.0254
    tmax = clim[:,7]
    tmin = clim[:,8]
    
    return doy,P,tmax,tmin



def dem_row_col_info(fileloc):
    """
    extracts ncol and nrow info from dem
    """
    dem = gdal.Open(fileloc)
    nrow= dem.RasterYSize
    ncol= dem.RasterXSize
    dem = None
    return nrow, ncol


def processDEM(fileloc):
    """
    computes hydrologically sound DEM by filling pits 
    and also computes flow accumulation 
    """
    pitremovedDEM = rd.FillDepressions(rd.LoadGDAL(fileloc))
    accumDEM = rd.FlowAccumulation(pitremovedDEM, method='Dinf')
    
    return pitremovedDEM, accumDEM



def clim_2d(P, tmax, tmin, doy, nrow, ncol):
    """
    distributes variables (P, tmax, tmin) over the DEM clone
    and also in 2D
    """
    #doy= len(doy)-1
    P_2d = np.reshape(np.repeat(P, nrow*ncol), (len(doy), nrow, ncol))
    tmin_2d = np.reshape(np.repeat(tmin, nrow*ncol), (len(doy), nrow, ncol))
    tmax_2d = np.reshape(np.repeat(tmax, nrow*ncol), (len(doy), nrow, ncol)) 
    tavg_2d = 0.5 * (tmin_2d + tmax_2d)
    
    return P_2d, tmax_2d, tmin_2d, tavg_2d
