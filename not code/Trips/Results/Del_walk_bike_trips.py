import pandas as pd

inf_1 = pd.read_csv("trips_dist_inf_1km.csv")
dist_1_2 = pd.read_csv("trips_dist_1_2_km.csv")
dist_2_5 = pd.read_csv("trips_dist_2_5_km.csv")
dist_5_10 = pd.read_csv("trips_dist_5_10_km.csv")
dist_sup_10 = pd.read_csv("trips_dist_sup_10_km.csv")

def separate_walk_bike_trips(df, perc):
    df.sort_values(by='Distance', inplace = True)
    l = len(df)
    nb = round(perc*l)
    walk_bike = df.head(nb)
    drive = df.tail(l-nb)
    return walk_bike, drive

walk_bike_inf_1, drive_inf_1 = separate_walk_bike_trips(inf_1, 0.76)
print(inf_1)
print(walk_bike_inf_1)
print(drive_inf_1)

walk_bike_inf_1.to_csv('walk_bike_inf_1.csv')
drive_inf_1.to_csv('drive_inf_1.csv')


walk_bike_dist_1_2, drive_dist_1_2 = separate_walk_bike_trips(dist_1_2, 0.55)
print(dist_1_2)
print(walk_bike_dist_1_2)
print(drive_dist_1_2)

walk_bike_dist_1_2.to_csv('walk_bike_dist_1_2.csv')
drive_dist_1_2.to_csv('drive_dist_1_2.csv')


walk_bike_dist_2_5, drive_dist_2_5 = separate_walk_bike_trips(dist_2_5, 0.31)
print(dist_2_5)
print(walk_bike_dist_2_5)
print(drive_dist_2_5)

walk_bike_dist_2_5.to_csv('walk_bike_dist_2_5.csv')
drive_dist_2_5.to_csv('drive_dist_2_5.csv')


walk_bike_dist_5_10, drive_dist_5_10 = separate_walk_bike_trips(dist_5_10, 0.15)
print(dist_5_10)
print(walk_bike_dist_5_10)
print(drive_dist_5_10)

walk_bike_dist_5_10.to_csv('walk_bike_dist_5_10.csv')
drive_dist_5_10.to_csv('drive_dist_5_10.csv')


walk_bike_dist_sup_10, drive_dist_sup_10 = separate_walk_bike_trips(dist_sup_10, 0.07)
print(dist_sup_10)
print(walk_bike_dist_sup_10)
print(drive_dist_sup_10)

walk_bike_dist_sup_10.to_csv('walk_bike_dist_sup_10.csv')
drive_dist_sup_10.to_csv('drive_dist_sup_10.csv')

all_walk_bike = pd.concat([walk_bike_inf_1, walk_bike_dist_1_2, walk_bike_dist_2_5, walk_bike_dist_5_10, walk_bike_dist_sup_10])
print(all_walk_bike)
all_walk_bike.to_csv('all_walk_bike.csv')

all_drive = pd.concat([drive_inf_1, drive_dist_1_2, drive_dist_2_5, drive_dist_5_10, drive_dist_sup_10])
print(all_drive)
all_drive.to_csv("all_drive.csv")