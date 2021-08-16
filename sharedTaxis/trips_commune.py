import pandas as pd

trips = pd.read_csv('all_drive.csv')
print(trips)

sectors = pd.read_csv('sector_stat.csv', sep=";")
#sectors.set_index("SectorStatID", inplace=True, drop=True)
print(sectors) #TODO check format

trips = trips.merge(sectors, left_on = "SS_Origin", right_on = "Code", how='left')
trips = trips.merge(sectors, left_on = "SS_Destination", right_on = "Code", how='left')
print(trips)


commune = sectors.Commune
commune.drop_duplicates(inplace=True)

in_and_out = dict()
in_only = dict()
out_only = dict()

for com in commune:
    a = len(trips[(trips.Commune_x == com) | (trips.Commune_y == com)])
    in_and_out[com]= a
    
    b = len(trips[(trips.Commune_x == com)])
    in_only[com]=b
    
    c = len(trips[(trips.Commune_y == com)])
    out_only[com]=c
    
print(in_and_out)
print(in_only)
print(out_only)
"""
Ganshoren = trips[(trips.Commune_x == "Ganshoren") | (trips.Commune_y == "Ganshoren")]
Ganshoren.to_csv('all_drive_Ganshoren_in_and_out.csv')
"""

Koekelberg = trips[(trips.Commune_x == "Koekelberg") | (trips.Commune_y == "Koekelberg")]
Koekelberg.to_csv('all_drive_Koekelberg_in_and_out.csv')