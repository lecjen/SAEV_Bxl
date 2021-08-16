import pandas as pd

trips_1 = pd.read_csv('profile_1_emergency.csv')
print(trips_1)

trips_2 = pd.read_csv('Trips_profile_2.csv')
print(trips_2)

trips_3 = pd.read_csv('Trips_profile_3.csv')
print(trips_3)

trips_4 = pd.read_csv('Trips_profile_4.csv')
print(trips_4)

trips_5 = pd.read_csv('Trips_profile_5.csv')
print(trips_5)

trips_6 = pd.read_csv('Trips_profile_6.csv')
print(trips_6)

trips_7 = pd.read_csv('Trips_profile_7.csv')
print(trips_7)

trips_8 = pd.read_csv('Trips_profile_8.csv')
print(trips_8)

trips_9 = pd.read_csv('Trips_profile_9.csv')
print(trips_9)

trips_10 = pd.read_csv('Trips_profile_10.csv')
print(trips_10)

trips_11 = pd.read_csv('Trips_profile_11.csv')
print(trips_11)

trips_12 = pd.read_csv('Trips_profile_12.csv')
print(trips_12)

trips_13 = pd.read_csv('Trips_profile_13.csv')
print(trips_13)

trips_14 = pd.read_csv('Trips_profile_14.csv')
print(trips_14)

trips_15 = pd.read_csv('Trips_profile_15.csv')
print(trips_15)

trips_16 = pd.read_csv('Trips_profile_16.csv')
print(trips_16)

trips_17 = pd.read_csv('Trips_profile_17.csv')
print(trips_17)

trips_18 = pd.read_csv('Trips_profile_18.csv')
print(trips_18)

trips_19 = pd.read_csv('Trips_profile_19.csv')
print(trips_19)

trips_20 = pd.read_csv('Trips_profile_20.csv')
print(trips_20)

trips_21 = pd.read_csv('Trips_profile_21.csv')
print(trips_21)

trips_22 = pd.read_csv('Trips_profile_22.csv')
print(trips_22)

trips_23 = pd.read_csv('Trips_profile_23.csv')
print(trips_23)

trips_24 = pd.read_csv('Trips_profile_24.csv')
print(trips_24)

trips_25 = pd.read_csv('Trips_profile_25.csv')
print(trips_25)

trips_26 = pd.read_csv('Trips_profile_26.csv')
print(trips_26)

trips_27 = pd.read_csv('Trips_profile_27.csv')
print(trips_27)

trips_28 = pd.read_csv('Trips_profile_28.csv')
print(trips_28)

trips_30 = pd.read_csv('Trips_profile_30.csv')
print(trips_30)

trips_31 = pd.read_csv('Trips_profile_31.csv')
print(trips_31)

print(trips_1.columns)
print(trips_2.columns)
print(trips_3.columns)
print(trips_4.columns)
print(trips_5.columns)
print(trips_6.columns)
print(trips_7.columns)
print(trips_8.columns)
print(trips_9.columns)
print(trips_10.columns)
print(trips_11.columns)
print(trips_12.columns)
print(trips_13.columns)
print(trips_14.columns)
print(trips_15.columns)
print(trips_16.columns)
print(trips_17.columns)
print(trips_18.columns)
print(trips_19.columns)
print(trips_20.columns)
print(trips_21.columns)
print(trips_22.columns)
print(trips_23.columns)
print(trips_24.columns)
print(trips_25.columns)
print(trips_26.columns)
print(trips_27.columns)
print(trips_28.columns)
print(trips_30.columns)
print(trips_31.columns)

all_trips = pd.concat([trips_1, trips_2, trips_3, trips_4, trips_5, trips_6, trips_7, trips_8, trips_9, trips_10, trips_11, trips_12, trips_13, trips_14,
                       trips_15, trips_16, trips_17, trips_18, trips_19, trips_20, trips_21, trips_22, trips_23, trips_24, trips_25, trips_26,
                       trips_27, trips_28, trips_30, trips_31])

print("all_trips", all_trips)

all_trips.to_csv('all_trips.csv')

zero_distance_trips = all_trips[all_trips.SS_Origin == all_trips.SS_Destination]
print("zero_distance_trips", zero_distance_trips)
zero_distance_trips.to_csv("zero_distance_trips.csv")

non_zero_distance_trips = all_trips[all_trips.SS_Origin != all_trips.SS_Destination]
print("non_zero_distance_trips", non_zero_distance_trips)
zero_distance_trips.to_csv("non_zero_distance_trips.csv")

inf_1 = non_zero_distance_trips[non_zero_distance_trips.Distance <= 1]
print("inf_1", inf_1)
inf_1.to_csv("trips_dist_inf_1km.csv")

dist_1_2 = non_zero_distance_trips[(non_zero_distance_trips.Distance > 1) & (non_zero_distance_trips.Distance <=2)]
print("dist_1_2", dist_1_2)
dist_1_2.to_csv("trips_dist_1_2_km.csv")

dist_2_5 = non_zero_distance_trips[(non_zero_distance_trips.Distance > 2) & (non_zero_distance_trips.Distance <=5)]
print("dist_2_5", dist_2_5)
dist_2_5.to_csv("trips_dist_2_5_km.csv")

dist_5_10 = non_zero_distance_trips[(non_zero_distance_trips.Distance > 5) & (non_zero_distance_trips.Distance <=10)]
print("dist_5_10", dist_5_10)
dist_5_10.to_csv("trips_dist_5_10_km.csv")

dist_sup_10 = non_zero_distance_trips[(non_zero_distance_trips.Distance > 10)]
print("dist_sup_10", dist_sup_10)
dist_sup_10.to_csv("trips_dist_sup_10_km.csv")


