import pandas as pd

colnames = ["SectorStatID", "SectorStatName", "PersID", "Age", "GenderID", "GenderName", "HouseholdID", "HouseholdTypeID", "HouseholdTypeName", "WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"]

tourists = pd.DataFrame(columns=colnames)

places = pd.read_csv('touristes_v2.csv', sep=";")
places.set_index("Code", inplace = True, drop = True)
print(places)

i=0
for ss in places.index:
    print("ss", ss)
    ss_name = places.loc[ss, "Territoire"]

    p= places.loc[ss, "Nb_touristes_ss"]
    if type(p) == str:
        p = p.replace(",", ".")
    
    p = round(float(p))
    while p > 0:
        print("i", i)
        tourists.loc[i]=[ss, ss_name, i, "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", 11, "Tourist", ss, ss_name]
        p-=1
        i+=1

print(tourists)
tourists.to_csv("foreign_tourists_workplace.csv")