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

campus = pd.read_csv("sup_campus_bxl_fr.csv", sep=';')

#campus.drop(columns='Unnamed: 0', inplace=True) #TODO check if needed
print(campus)

campus_points = []

for ind in campus.index:
    long = campus["Longitude du campus"][ind]
    if type(long) == str:
        long = long.replace(",", ".")

    lat = campus["Latitude du campus"][ind]
    if type(lat) == str:
        lat = lat.replace(",", ".")

    campus_points.append(Point(float(long),float(lat)))

print(campus_points)

liste = []
for i in range(0, len(campus_points)):
    liste.append("")

sectors = liste

for el in zones.keys():
    for i in range(len(campus_points)):
        point = campus_points[i]
        if point.within(zones[el]):
            if sectors[i]=="":
                sectors[i]=el
            else:
                print(sectors[i], "sec i")
                print(i, "i")
                print(el, 'el')
                error
    #print(zones[el].contains(point))

campus["sector_stat"]=sectors

print(campus)
print(campus.sector_stat)

campus.to_csv("sup_campus_bxl_fr_with_ss_v2.csv")

#TODO Checker si differents ss au sein d'une meme commune