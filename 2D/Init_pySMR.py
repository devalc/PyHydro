# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 11:20:14 2018

@author: chinmay deval

This file initialized pyhydro model using inputs gathered from WEPP cloud

"""

import os
#import gdal
import numpy as np

#### Provide paths to the dem and climate

dem_path = 'C:/Chinmay/storagetemp/data_from_WEPPcloud/dem/dem.tif'
climate_path = 'C:/Chinmay/storagetemp/data_from_WEPPcloud/climate/'

#### read data 
#dem = gdal.Open(dem_path)

clim = np.loadtxt(climate_path, skiprows =15)
#### provide paths to store outputs and create dir if necessary

Outputdir = 'C:/Chinmay/storagetemp/data_from_WEPPcloud/Run_Outputs/'

if not os.path.exists(Outputdir):
    os.makedirs(Outputdir)
    
