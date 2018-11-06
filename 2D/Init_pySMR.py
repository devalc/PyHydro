# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 11:20:14 2018

@author: chinmay deval

This file initialized pyhydro model using inputs gathered from WEPP cloud

"""

import os
import shutil
import numpy as np
import unit_converter as uc ######## delete once everything working
import process_input as pi
import ET as ET
import snow as sn
import gdal
import height_wattable as watht
from latq import qlat_2d
from perc import perc_2d
import routing as RT
import richdem as rd
import matplotib.pylot as plt



#### Provide paths to the dem and climate##########################################################

dem_path = 'D:/Chinmay/storagetemp/data_from_WEPPcloud/dem/dem.tif'
climate_path = 'D:/Chinmay/storagetemp/data_from_WEPPcloud/climate/265191.cli'


#### provide directory to store outputs
#### creates new dir if the given dir doesnt exist 
#### Caution: Overwrites the existing dir

Outputdir = 'D:/Chinmay/storagetemp/Run_Outputs/'

if not os.path.exists(Outputdir):
    os.makedirs(Outputdir)
else:
    shutil.rmtree(Outputdir)          
    os.makedirs(Outputdir)


#### read climate data##########################################################

### USing this for test and not loging the entire data#####
########### DELETE THIS once model is funcitonal########
######## and use function from process_input.py to read data
"""eg: doy,P,tmax,tmin=process_wepp_cli(climate_path)"""
##############################################################



clim = np.loadtxt(climate_path, skiprows =15)

d = clim[:65,0]
m = clim[:65,1]
y = clim[:65,2]
doy = uc.ymd_to_doy(y,m,d)
P = clim[:65,3] * 0.0254
tmax = clim[:65,7]
tmin = clim[:65,8]



####### get DEM info, and calculate flow accum.  load slope and aspect#############################
nrow, ncol = pi.dem_row_col_info(dem_path)
slp = gdal.Open('D:/Chinmay/storagetemp/data_from_WEPPcloud/export/arcmap/gtiffs/FVSLOP.tif')
geot_info = slp.GetGeoTransform()
slope = slp.GetRasterBand(1).ReadAsArray()
pitremovedDEM , accumDEM = pi.processDEM(dem_path)


##### distribute same var values over DEM clone and also make it 2d#############################

P_2d,tmax_2d, tmin_2d, tavg_2d = pi.clim_2d(P,tmax,tmin,doy,nrow,ncol)


########### INIT Parameters####################################################
lat = 47.15
#optimized parameters for SWE
k = 1.16 #length/degree/day
tbase = 0.0 #degC
train = 3.0 #degC
tsnow = 0.0 #degC
# inti arrays to store var calcs
s = np.zeros(P_2d.shape) #array of storage
q = np.zeros(P_2d.shape) # array  runoff
qa = np.zeros(P_2d.shape) #accumulated runoff
hwt = np.zeros(P_2d.shape) #height of water table
qlat_out = np.zeros(P_2d.shape) # lateral flow
qlat_in = np.zeros(P_2d.shape) # lat flow in from upstream
percol = np.zeros(P_2d.shape) ## percolation
sb = np.zeros(P_2d.shape) ##baseflow storage
bf = np.zeros(P_2d.shape) ##baseflow
Q = np.zeros(P_2d.shape) #discharge
actET = np.zeros(P_2d.shape)
nr_qlat = np.zeros(doy)

##############################soil props#################
ksat = np.full((nrow, ncol), 1.0) # m/day
por_p = np.full((nrow, ncol), 0.45) #porosity in percent
fc_p = np.full((nrow, ncol), 0.36) #field capacity in percent
wp_p = np.full((nrow, ncol), 0.1) #wilting point in percent
kv = np.full((nrow, ncol), 0.001) # m/day # vertical condutivity
alpha = 0.02
soildepth = np.full((nrow, ncol), 1.2) #depth of soil profile m
por = np.muliply(por_p, soildepth) 
fc = np.muliply(fc_p, soildepth)
wp = np.muliply(wp_p, soildepth)
Smax = por 

############################### init values for vars#################
q[0,:,:] = 0 # set initial runoff m
qa[0,:,:] = 0
s[0,:,:] = 0.7 # set initial storage (i.e water content) m
sb[0,:,:] = 0 # set initial aquifer storage (baseflow source) m



#######################Precip to Psnow and Prain #############################

Psnow_2d, Prain_2d = sn.P_to_Snow_and_Rain_2d(P_2d, tavg_2d, train, tsnow)

###### call snow module#############################

meltflux_2d = np.apply_along_axis(sn.Snowmelt_DD_usace, 0, arr = k,temp = 'k, tavg_2d' )
simSWE_2d, act_melt_2d = sn.simSWE_2d(Psnow_2d, meltflux_2d)
Pin_2d = np.add(Prain_2d, act_melt_2d)

##### call ET module to estimate reference and potential ET#############################

extrarad_2d = ET.extrarad_2d(np.full((nrow, ncol),lat), doy)

RefET_2d = ET.RefET_Hargreaves(tmax_2d, tmin_2d, extrarad_2d)
PotET_2d = ET.ETpot(RefET_2d)
actET[0,:,:] = ET.simET_2d(PotET_2d[0,:,:], fc, wp, s[0,:,:])

neigh_contri = RT.flow_from_neighcells(pitremovedDEM)


for i in range(1,Pin_2d .shape[0]):
    s[i, :, :] = s[i - 1, :, :] + Pin_2d[i,:,:]
    hwt[i, :, :] = watht.ht_wattab(np.divide(s[i, :, :], soildepth), fc_p, por_p, soildepth)
    qlat_out[i, :, :] = qlat_2d(ksat, slope, hwt[i, :, :], geot_info[1], geot_info[1])
    qlat_in[i, :, :], nr_qlat[i] = RT.routeflow(neigh_contri, qlat_out[i, :, :])
    s[i, :, :] = s[i, :, :] + qlat_in[i,:,:] - qlat_out[i,:,:]
    actET[i, :, :] = ET.simET_2d(PotET_2d[i, :, :], fc, wp, s[i - 1, :, :])
    s[i,:,:] = s[i,:,:] - actET[i,:,:]
    percol[i, :, :] = perc_2d(kv, watht.ht_wattab(por, fc, np.divide(s[i, :, :], 1.0), soildepth))
    s[i, :, :] = s[i, :, :] - percol[i,:,:]
    q[i, :, :] = np.where(s[i, :, :] > (soildepth*por), (s[i, :, :] - (soildepth*por)), 0.0)
    qa[i, :, :] = rd.FlowAccumulation(rd.LoadGDAL(dem_path), method='Dinf', weights=q[i,:,:])
    s[i, :, :] = np.where(s[i, :, :] > (soildepth * por), (soildepth * por), s[i, :, :])


outrow = 12
outcol = 1
print(Pin_2d)
print('qlat', qlat_in[:, outrow, outcol]-qlat_out[:,outrow, outcol])
print('runoff accum', qa[:, outrow, outcol])
print('flow', qa[:, outrow,outcol]+(qlat_in[:, outrow, outcol]-qlat_out[:, outrow, outcol]))
plt.plot(doy, qlat_in[:, outrow, outcol]-qlat_out[:, outrow, outcol], 'g',
         doy, qa[:, outrow, outcol], 'c',
         doy, (qa[:, outrow, outcol]+(qlat_in[:, outrow, outcol]-qlat_out[:, outrow, outcol])), 'b')
plt.show()


