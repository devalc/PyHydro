# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 21:18:27 2018

@author: Chinmay
"""
import os
import pcraster as pcr




dem = 'D:/Chinmay/Hydro_modeling_erin_fall_2018/sp_model/dem.map'
output_path = 'D:/Chinmay/Hydro_modeling_erin_fall_2018/sp_model/'

pcr.setclone(dem)

slope = pcr.slope(dem)
pcr.report(slope, output_path +"gradient.map")

ldd = pcr.lddcreate(dem, 1e31, 1e31, 1e31, 1e31)
pcr.report(ldd, output_path +"ldd.map")

os.system('augila ldd.map')

