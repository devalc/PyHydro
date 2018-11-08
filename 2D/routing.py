# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 18:02:22 2018

@author: Chinmay Deval
"""

import numpy as np
import richdem as rd
import gdal

def flow_from_neighcells(dem, nodata=-9999):
    """
    Computes flow from neighboring cells to the adjacent cell as a function of slope

    """
    
    contri_8cells = np.zeros((8, dem.shape[0], dem.shape[1]))
    # east
    contri_8cells[0, :, 0:-1] = (dem[:, 0:-1] - dem[:, 1:])
    # southeast
    contri_8cells[1, 0:-1, 0:-1] = (dem[0:-1, 0:-1] - dem[1:, 1:])/np.sqrt(2.0)
    # south
    contri_8cells[2, 0:-1, :] = (dem[0:-1, :] - dem[1:, :]) 
    # southwest
    contri_8cells[3, 0:-1, 1:] = (dem[0:-1, 1:] - dem[1:, 0:-1]) / np.sqrt(2.0) 
    # west
    contri_8cells[4, :, 1:] = (dem[:, 1:] - dem[:, 0:-1]) 
    # northwest
    contri_8cells[5, 1:, 1:] = (dem[1:, 1:] - dem[0:-1, 0:-1]) / np.sqrt(2.0) 
    # north
    contri_8cells[6, 1:, :] = (dem[1:, :] - dem[0:-1, :]) 
    # northeast
    contri_8cells[7, 1:, 0:-1] = (dem[1:,0:-1] - dem[0:-1,1:])/np.sqrt(2.0) 
    # Values smaller than zero are set to zero as that is contri from uphill cells 
    contri_8cells[contri_8cells < 0.0] = 0.0 
    # elevation drop
    totelev_drop = np.sum(contri_8cells, axis=0) 
    # contri from each cell
    contri_frac = np.where(totelev_drop > 0.0, np.divide(contri_8cells, totelev_drop), 0.0) 

    return contri_frac




def routeflow(flow_contri, flow):
    """
    Routes flow to adjacent cells based on flow contribution from each cell.

    flow_contri: flow contributions
    flow: amount of flow route

    """
    # flow routed
    routedf = np.zeros((flow_contri.shape[1], flow_contri.shape[2])) 
#    flowdec = flow.copy() #decrement the total flow, this is a mass balance check
    
     # flow from west
    routedf[:, 1:] = routedf[:, 1:] + flow_contri[0, :, 0:-1] * flow[:, 0:-1]
#    flowdec[:, 0:-1] = flowdec[:, 0:-1] - flow_contri[0, :, 0:-1] * flow[:, 0:-1]
    
     # flow from northwest
    routedf[1:, 1:] = routedf[1:, 1:] + flow_contri[1, 0:-1, 0:-1] * flow[0:-1, 0:-1] 
#    flowdec[0:-1, 0:-1] = flowdec[:-1, 0:-1] - flow_contri[1, 0:-1, 0:-1] * flow[0:-1, 0:-1]
    
     # flow from north
    routedf[1:, :] = routedf[1:, :] + flow_contri[2, 0:-1, :] * flow[0:-1, :] 
#    flowdec[0:-1, :] = flowdec[0:-1, :] - flow_contri[2, 0:-1, :] * flow[0:-1, :]
    
    # flow from northeast
    routedf[1:, 0:-1] = routedf[1:, 0:-1] + flow_contri[3, 0:-1, 1:] * flow[0:-1, 1:]  
#    flowdec[0:-1, 1:] = flowdec[0:-1, 1:] - flow_contri[3, 0:-1, 1:] * flow[0:-1, 1:]
    
     # flow from east
    routedf[:, 0:-1] = routedf[:, 0:-1] + flow_contri[4, :, 1:] * flow[:, 1:] 
#    flowdec[:, 1:] = flowdec[:, 1:] - flow_contri[4, :, 1:] * flow[:, 1:]
    
    # flow from southeast
    routedf[0:-1, 0:-1] = routedf[0:-1, 0:-1] + flow_contri[5, 1:, 1:] * flow[1:, 1:]  
#    flowdec[1:, 1:] = flowdec[1:, 1:] - flow_contri[5, 1:, 1:] * flow[1:, 1:]
    
     # flow from south
    routedf[0:-1, :] = routedf[0:-1, :] + flow_contri[6, 1:, :] * flow[1:, :] 
#    flowdec[1:, :] = flowdec[1:, :] - flow_contri[6, 1:, :] * flow[1:, :]
    
    # flow from southwest
    routedf[0:-1, 1:] = routedf[0:-1, 1:] + flow_contri[7, 1:, 0:-1] * flow[1:, 0:-1]  
#    flowdec[1:, 0:-1] = flowdec[1:, 0:-1] - flow_contri[7, 1:, 0:-1] * flow[1:, 0:-1]

    return routedf





#def routedf_RD(dempath, flow, method='Dinf'):
#    """
#    Uses richdem to route flow
#    
#        dempath: path to DEM (.tif)
#        flow: amount of flow to route
#        method: richdem routing method (default: 'Dinf')
#    """
#    rdprop = rd.FlowProportions(rd.LoadGDAL(dempath), method=method)



