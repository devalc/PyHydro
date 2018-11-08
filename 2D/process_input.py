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
import osr
from pyproj import Proj, transform

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
    doy = doy[:-1]
    nvals = len(doy)
    P = clim[:nvals,3] * 0.0254
    tmax = clim[:nvals,7]
    tmin = clim[:nvals,8]
    
    return doy,nvals,P,tmax,tmin



def dem_row_col_info(fileloc):
    """
    extracts ncol and nrow info from dem
    """
    dem = gdal.Open(fileloc)
    nrow= dem.RasterYSize
    ncol= dem.RasterXSize
    dem = None
    return nrow, ncol


def getCoords(rasterpath):
    """
    extracts coordinates of each pixel in raster by
    iterating over each row and all columns in that row of the raster
    
    args:
        rasterpath: str of path to the raster file
        path_to_store_wgs84_raster: location where you'd like to store projected
        raster in case the projection of rasterpath is not equal to ESPG:4326
    
    returns: returns global coordinates from pixel x, y coords
    """
    file = gdal.Open(rasterpath)
#    #Check_coordinate system and if not wgs84 convert to wgs84
#    proj = osr.SpatialReference(wkt=file.GetProjection())
#    proj_in = proj.GetAttrValue('AUTHORITY',1)
    # if not ESPG:4326, project to it and get coordinates #Put this check
#    if proj_in != '4326':
#        filewgs84 = gdal.Warp('',file,dstSRS='EPSG:4326',format='VRT')
#        nrow= filewgs84.RasterYSize
#        ncol= filewgs84.RasterXSize    
#        xoff, a, b, yoff, d, e = file.GetGeoTransform()
#        lat = []
#        lon = []
#        for row in range(0,nrow):
#            for col in range (0,ncol):
#                xp = a * col + b * row + xoff
#                yp = d * col + e * row + yoff
#                lat.append(yp)
#                lon.append(xp)
#    #else get coordinates
#    else:
    nrow= file.RasterYSize
    ncol= file.RasterXSize    
    xoff, a, b, yoff, d, e = file.GetGeoTransform()
    lat = []
    lon = []
    for row in range(0,nrow):
        for col in range (0,ncol):
            xp = a * col + b * row + xoff
            yp = d * col + e * row + yoff
            lat.append(yp)
            lon.append(xp)
    return lat, lon


def UTM_to_DD(rasterpath, lat,lon):
   
    file = gdal.Open(rasterpath)
    proj = osr.SpatialReference(wkt=file.GetProjection())
    proj_in = proj.GetAttrValue('AUTHORITY',1)
    inProj = Proj(init='epsg:'+ proj_in)
    outProj = Proj(init='epsg:4326')
    lon_DD,lat_DD = transform(inProj,outProj,lon,lat)
    return lat_DD, lon_DD



def processDEM(fileloc):
    """
    computes hydrologically sound DEM by filling pits 
    and also computes flow accumulation 
    """
    pitremovedDEM = rd.FillDepressions(rd.LoadGDAL(fileloc))
    accumDEM = rd.FlowAccumulation(pitremovedDEM, method='Dinf')
    
    return pitremovedDEM, accumDEM



def clim_2d(P, tmax, tmin, nvals, nrow, ncol):
    """
    distributes variables (P, tmax, tmin) over the DEM clone
    and also in 2D
    """
#    doy= len(doy)-1
    P_2d = np.reshape(np.repeat(P, nrow*ncol), (nvals, nrow, ncol))
    tmin_2d = np.reshape(np.repeat(tmin, nrow*ncol), (nvals, nrow, ncol))
    tmax_2d = np.reshape(np.repeat(tmax, nrow*ncol), (nvals, nrow, ncol)) 
    tavg_2d = 0.5 * (tmin_2d + tmax_2d)
    
    return P_2d, tmax_2d, tmin_2d, tavg_2d
