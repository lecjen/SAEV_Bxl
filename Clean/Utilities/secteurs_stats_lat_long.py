import pandas as pd
import numpy as np
import pyproj


bxl = pd.read_csv("bruxelles_parsed.csv")
bxl.drop(columns='Unnamed: 0', inplace=True)

coord_lat_long=[]
for ind in bxl.index:
    coords = bxl.Coord[ind]
    
    tmp_coord = coords.split(" ")
    clean_coord = []
    
    for pt in tmp_coord:
        tmp_pt = pt.split(',')
        x = float(tmp_pt[0])
        y = float(tmp_pt[1])
        coord = pyproj.transform(pyproj.Proj(init='EPSG:31370'), pyproj.Proj(init='EPSG:4326'), x, y)
        #lat.append(coord[0])
        #long.append(coord[1])
        clean_coord.append((coord[0],coord[1]))
    
    coord_lat_long.append(clean_coord)
    

bxl['coord_lat_long']=coord_lat_long
#bxl['long']=long

print(bxl)
print(bxl.coord_lat_long)
#print(bxl.long)

bxl.to_csv("bruxelles_parsed_lat_long.csv")