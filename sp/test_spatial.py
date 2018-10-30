# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 16:33:14 2018

@author: Chinmay
"""

import os
import urllib
import zipfile
import numpy as np
import pandas as pd
import pcraster as pcr
import gdal
from gdalconst import *
import fiona

from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg

import rasterio

from rasterio.plot import show

from rasterio.plot import show_hist

from rasterio.mask import mask



import pycrs



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



dem_path = r'D:/OneDrive - University of Idaho/pyhydro_dat/dem/n47_w117_1arc_v2.TIF'
out_tif = r"D:/OneDrive - University of Idaho/pyhydro_dat/dem/masked_DEM.TIF"
data = rasterio.open(dem_path)

shp = fiona.open('D:/OneDrive - University of Idaho/pyhydro_dat/shapefile/wsheds30mwgs84.shp')
minx, miny, maxx, maxy = shp.bounds

bbox = box(minx, miny, maxx, maxy)
geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))
geo = geo.to_crs(crs=data.crs.data)



def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

coords = getFeatures(geo)

out_img, out_transform = mask(raster=data, shapes=coords, crop=True)

out_meta = data.meta.copy()
epsg_code = int(data.crs.data['init'][5:])


out_meta.update({"driver": "GTiff","height": out_img.shape[1],\
                 "width": out_img.shape[2], "transform": out_transform, \
                 "crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()})


