import pandas as pd
import math as m

def distance_two_points(lat1, long1, lat2, long2):
    #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    R = 6373.0 #km

    lat1 = m.radians(lat1)
    lat2 = m.radians(lat2)
    long1 = m.radians(long1)
    long2 = m.radians(long2)

    delta_long = long2 - long1
    delta_lat = lat2 - lat1

    a = m.sin(delta_lat / 2)**2 + m.cos(lat1) * m.cos(lat2) * m.sin(delta_long / 2)**2
    c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))

    distance = R * c #km

    return distance

def compute_distance(x, ss, df):
    lat_x = df.loc[x, 'lat']
    long_x = df.loc[x, 'long']

    lat_ss = df.loc[ss, 'lat']
    long_ss = df.loc[ss, 'long']

    distance = distance_two_points(lat_x, long_x, lat_ss, long_ss)

    return distance

sectors = pd.read_csv('ss_long_lat.csv')

distances = pd.DataFrame()
distances['SectorStatID_1']=sectors['SectorStatID']

sectors.set_index('SectorStatID', inplace=True, drop=True)
distances.set_index('SectorStatID_1', inplace=True, drop=True)
distances['SectorStatID_1']=sectors.index

for ss in sectors.index:
    code = ss
    distances[code]=distances['SectorStatID_1'].apply(lambda x:compute_distance(x, code, sectors))

print(distances)

distances.to_csv("distances_ss.csv")