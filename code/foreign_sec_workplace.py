import pandas as pd

colnames = ["SectorStatID", "SectorStatName", "PersID", "Age", "GenderID", "GenderName", "HouseholdID", "HouseholdTypeID", "HouseholdTypeName", "WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"]

baby = pd.DataFrame(columns=colnames)

places = pd.read_csv('sec_places_restantes_for_foreigners.csv')
places.set_index("SectorStatID", inplace = True, drop = True)
places = places[places["places_ss"]> 0]
print(places)

closest_peri = pd.read_csv('closest_ss_peri_v2.csv')
closest_peri.set_index("SectorStatID", inplace=True, drop=True)
print(closest_peri)

ss_names = pd.read_csv('sector_stat.csv', sep=";")
ss_names.set_index("Code", inplace=True, drop=True)
print(ss_names)

i=0
for ss in places.index:
    print("ss", ss)
    ss_from_id = closest_peri.loc[ss][0]
    ss_from_name = ss_names.loc[ss_from_id, "Name"]


    ss_to_name = ss_names.loc[ss, "Name"]
    p= places.loc[ss, "places_ss"]
    while p > 0:
        print("p", p)
        baby.loc[i]=[ss_from_id, ss_from_name, i, "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", 3, "Secondaires", ss, ss_to_name]
        p-=1
        i+=1

print(baby)
baby.to_csv("foreign_sec_workplace.csv")