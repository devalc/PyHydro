# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:33:14 2018

@author: Chinmay
"""

import os
import urllib
import zipfile
import numpy as np
import pcraster as pcr
import gdal
from gdalconst import *
import fiona

#def downloadDEM(url):
#    
#    """The function downloads the DEM from the given url 
#    (In this case National Elevation Dataset, USGS.) """
#    # Translate url into a filename
#    filename = url.rsplit('/', 1)[-1]
#    if not os.path.exists(filename):
#        outfile = urllib.URLopener()
#        print "..............downloading dem.............."
#        dem = outfile.retrieve(url, filename)
#        print "..............done downloading.............."
#        return dem
#        
#        
#
#def unzip(filepath, dest_path):
#    """Function extracts the downloaded zipped file to a folder named dem """
#    if os.path.isdir(dest_path):
#        print "..............data has been already extracted.............."
#    else:
#        print "..............extracting data.............."        
#        with zipfile.ZipFile(filepath) as zf:
#            extractedfiles = zf.extractall(dest_path)
#            print "..............done extraction....."
#    return extractedfiles 
#    
#
#url = 'https://dds.cr.usgs.gov/srtm/version2_1/SRTM1/Region_01/N47W117.hgt.zip'
#downloadDEM(url)
#unzip('D:/GitHub/PyHydro/sp/N47W117.hgt.zip' ,'D:/GitHub/PyHydro/sp/dem/')


shp = fiona.open('D:/OneDrive - University of Idaho/pyhydro_dat/shapefile/wsheds30mwgs84.shp')
bounds = shp.bounds

dem_path = 'D:/OneDrive - University of Idaho/pyhydro_dat/dem/n47_w117_1arc_v2.TIF'

#download and clip dem to the extent

dem = gdal.Open(dem_path)
dem= gdal.Translate('new.tif', dem, projWin = bounds)
dem.flus

