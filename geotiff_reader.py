#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 10:54:21 2020

@author: nagypeter
"""

    

import rasterio
import rasterio.features
import rasterio.warp



def find_elevation(lon, lat, data, bounds):
    data_size = data.shape[0];
    y = data_size-(lon - bounds.bottom) / (bounds.top-bounds.bottom )* data_size;
    x = (lat - bounds.left) / (bounds.right-bounds.left )* data_size;
    print(x, y)
    return data[round(y), round(x)];


with rasterio.open('srtm_40_03.tif') as raster:
    
    bounds = raster.bounds;
    data = raster.read(1);
    elevation = find_elevation(46.803654, 17.495757 , data, bounds)
    H = np.array(data)





    
   