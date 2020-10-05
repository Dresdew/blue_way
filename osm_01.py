import numpy as np
import matplotlib.pyplot as plt# Collect coords into list
import requests
import json
import math 

def convertToXY(lon, lat):
    x = 110.574 * lat;
    y = 111.320 * lon * math.cos(lat /180*math.pi);
    return x, y

def calculateXYOfNode(node):
    return convertToXY(node['lon'], node['lat']);

def calculateDistance(x1, x0, y1, y0):
    return math.sqrt(math.pow(x1-x0, 2) + math.pow(y1-y0, 2));

def calculateDistanceOfNodes(node0, node1):
    x0, y0 = calculateXYOfNode(node0);
    x1, y1 = calculateXYOfNode(node1);
    return calculateDistance(x1, x0, y1, y0);

def calculateTotalDistanceOfNodeList(nodes):
    if(len(nodes) == 0):
        return 0;
    distance = 0;
    node0 = nodes[0];
    for node in nodes:
        distance += calculateDistanceOfNodes(node0, node);
        node0 = node;
    return distance;

def findNodeById(data, id):
    for element in data['elements']:
        if element['type'] == 'node':
            if element['id'] == id:
                return element;        

def calculateRouteDistance(data):
    distance = 0;
    for element in data['elements']:
        if element['type'] == 'way':
            nodeIds =  element['nodes'];
            nodes = list(map(lambda nodeId : findNodeById(data, nodeId), nodeIds));
            dis = calculateTotalDistanceOfNodeList(nodes);
            distance += dis;
    return distance;


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
data = response.json();
ddddd = calculateRouteDistance(data)



    
