import pandas as pd

trips = pd.read_csv('all_trips.csv') 
print(trips) #3 411 960

trips_1 = pd.read_csv('trips_dist_inf_1km.csv') 
print(trips_1) #399,212

trips_2 = pd.read_csv('trips_dist_1_2_km.csv') 
print(trips_2) #307,498

trips_3 = pd.read_csv('trips_dist_2_5_km.csv') 
print(trips_3) #644,808

trips_4 = pd.read_csv('trips_dist_5_10_km.csv') 
print(trips_4) #1,130,420

trips_5 = pd.read_csv('trips_dist_sup_10_km.csv') 
print(trips_5) #834,531

dist = trips.Distance
avg = dist.mean(axis=0)

w = trips[(trips.TripTypeFrom == 'W') | (trips.TripTypeTo == 'W')]
print(w)