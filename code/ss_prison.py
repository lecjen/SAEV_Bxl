import pandas as pd
from shapely.geometry import Point, Polygon
import numpy as np
import pyproj

bxl = pd.read_csv("bruxelles_parsed_lat_long.csv")
bxl.drop(columns='Unnamed: 0', inplace=True)

zones = dict()

for ind in bxl.index:
    coord = bxl.coord_lat_long[ind]

    tmp_coord = coord[2:-2].split("), (")
    #print(tmp_coord)

    clean_coord = []

    for pt in tmp_coord:
        tmp_pt = pt.split(',')
        clean_coord.append((float(tmp_pt[0]),float(tmp_pt[1])))

    #print(coord)
    #print(clean_coord)
    #print(type(clean_coord[0][1]))


    #coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
    poly = Polygon(clean_coord)
    print(poly)

    zones[bxl.CD_SECTOR[ind]]=poly

print(zones)


#point = Point(169289.82809999958, 156203.8125)
"""
coord_forest = pyproj.transform(pyproj.Proj(init='EPSG:31370'), pyproj.Proj(init='EPSG:4326'), 148686.3, 167795.87)
print(coord_forest)
prison_forest = Point(coord_forest[0], coord_forest[1])

coord_st_gilles = pyproj.transform(pyproj.Proj(init='EPSG:31370'), pyproj.Proj(init='EPSG:4326'), 148452.58, 167985.81)
prison_st_gilles = Point(coord_st_gilles[0], coord_st_gilles[1])

for el in zones.keys():
    if prison_forest.within(zones[el]):
        prison_forest_ss = el
    if prison_st_gilles.within(zones[el]):
        prison_st_gilles_ss = el
    if zones[el].contains(prison_forest):
        prison_forest_ss = el
    if zones[el].contains(prison_st_gilles):
        prison_st_gilles_ss = el
        


print(prison_forest_ss, "forest")
print(prison_st_gilles_ss, "gilles")
"""
pt = Point(4.35778759999994, 50.8558488)
for el in zones.keys():
    if pt.within(zones[el]):
        pt_ss = el
print(pt_ss)
        
