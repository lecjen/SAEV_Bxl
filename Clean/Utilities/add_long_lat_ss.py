import pandas as pd
from shapely.geometry import Point, Polygon
import numpy as np
import pyproj


bxl = pd.read_csv("bruxelles_parsed_lat_long.csv")
bxl.drop(columns='Unnamed: 0', inplace=True)

centroids = pd.DataFrame(columns=['SectorStatID', 'Centroid'])
print(centroids)
zones = dict()

i =0

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

    centroid=poly.centroid

    centroids.loc[i] = [bxl.CD_SECTOR[ind], str(centroid)]

    zones[bxl.CD_SECTOR[ind]]=poly
    i +=1
print(zones)

print(centroids)

centroids['long'] = centroids['Centroid'].map(lambda x: x.split()[1][1:])
centroids['lat'] = centroids['Centroid'].map(lambda x: x.split()[2][:-1])

centroids.drop(columns=['Centroid'], inplace=True)

print(centroids)
print(centroids.long)
print(centroids.lat)

centroids.to_csv('ss_long_lat.csv')
"""
#TODO put the right all_hh
all_hh = pd.read_csv('hh_VEEWEYDE-SUD.csv')
print(all_hh)
#all_hh = pd.read_csv('all_hh.csv')
all_hh = all_hh.merge(centroids, how='left', left_on='SectorStatID', right_on='SectorStatID')
print(all_hh)
print(all_hh.long)
print(all_hh.lat)

all_hh.to_csv("all_hh_long_lat.csv")
"""