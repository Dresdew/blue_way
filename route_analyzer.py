#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:02:59 2020

@author: nagypeter
"""

import rasterio
import rasterio.features
import rasterio.warp

import requests
import numpy as np 
import matplotlib.pyplot as plt
import math 

def convertToXY(lon, lat):
    x = 110.574 * lat;
    y = 111.320 * lon * math.cos(lat /180*math.pi);
    return x, y

class RouteAnalyzer:
    
    def __init__(self, name_of_route):
        self.name_of_route = name_of_route;
        self.route = [];
        
    def calculate_elevation(self, lon, lat):
        bounds = self.bounds;
        data_size = self.data.shape[0];
        y = data_size-(lat - bounds.bottom) / (bounds.top-bounds.bottom )* data_size;
        x = (lon - bounds.left) / (bounds.right-bounds.left )* data_size;
        return self.data[round(y), round(x)];
        
    def read_elevation_data(self):
        with rasterio.open('srtm_40_03.tif') as raster:
            self.bounds = raster.bounds;
            self.data = raster.read(1);
            
    def load_osm_data(self):
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = """
            [out:json];
                area["ISO3166-1"="HU"][admin_level=2];
                    (
                        rel["name"="Országos Kéktúra 5. - Tapolca - Badacsonytördemic"](area);
                        );
                    out body;
                    >;
                    out skel qt;
                    """
        response = requests.get(overpass_url, params={'data': overpass_query});
        self.osm_data = response.json();  
        
    def calculate_osm_route(self):
        for element in self.osm_data['elements']:
            if element['type'] == 'way':
               nodeIds =  element['nodes'];
               nodes = list(map(self.find_node_by_id, nodeIds));
               for node in nodes:
                   self.route.append([node['lon'], node['lat']]);
                
                
    def find_node_by_id(self, id):
        for element in self.osm_data['elements']:
            if element['id'] == id:
                return element;      
        
    def calculate_elevation_profile(self):
        mapper = map(lambda point : self.calculate_elevation(point[0], point[1]), self.route)
        self.elevation_profile = list(mapper);
        
  
        
    
analyzer = RouteAnalyzer("hy");
analyzer.read_elevation_data();
analyzer.load_osm_data();
analyzer.calculate_osm_route();
analyzer.calculate_elevation_profile();
