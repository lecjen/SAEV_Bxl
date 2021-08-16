import pandas as pd
import random

places = pd.read_csv('work_flow_from_out_to_bxl.csv', sep=";")
print(places)

Z_sectors = places[places.SECTOR.str.contains("Z")]
Z_sectors.set_index("SECTOR", inplace=True, drop=True)
print(Z_sectors)

normal_places = places[~places.SECTOR.str.contains("Z")]
normal_places.set_index("SECTOR", inplace=True, drop=True)
print(normal_places)


closest_peri = pd.read_csv('closest_ss_peri_v2.csv')
closest_peri.set_index("SectorStatID", inplace=True, drop=True)
print(closest_peri)

ss_names = pd.read_csv('sector_stat.csv', sep=";")
ss_names.set_index("Code", inplace=True, drop=True)
print(ss_names)

colnames = ["SectorStatID", "SectorStatName", "PersID", "Age", "GenderID", "GenderName", "HouseholdID", "HouseholdTypeID", "HouseholdTypeName", "WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"]
workers = pd.DataFrame(columns=colnames)

corres = {"21001ZZZZ" : "Anderlecht", "21002ZZZZ" : "Auderghem", "21003ZZZZ" : "Berchem Sainte-Agathe",
          "21004ZZZZ" : "Bruxelles", "21005ZZZZ" :	"Etterbeek", "21006ZZZZ" : "Evere", "21007ZZZZ" : 
              "Forest", "21008ZZZZ" : "Ganshoren", "21009ZZZZ" : "Ixelles", "21010ZZZZ" : "Jette",
              "21011ZZZZ" : "Koekelberg", "21012ZZZZ" : "Molenbeek Saint-Jean", "21013ZZZZ" : 
                  "Saint-Gilles", "21014ZZZZ" : "Saint-Josse-ten-Noode", "21015ZZZZ" : "Schaerbeek",
                  "21016ZZZZ" : "Uccle", "21017ZZZZ" : "Watermael-Boitsfort", "21018ZZZZ" : 
                      "Woluwe Saint-Lambert", "21019ZZZZ" : "Woluwe Saint-Pierre", "ZZZZZZZZZ" : "all"}

i=0
for ss in Z_sectors.index:
    print("ss", ss)
    commune = corres[ss]
    
    if commune == "all":
        possibles = ss_names
    else:
        possibles = ss_names[ss_names.Commune==commune]
        
    p= Z_sectors.loc[ss, "Sum of OBS_VALUE"]
    while p > 0:
        print("i", i)
        
        elu = random.randrange(0, len(possibles), 1)
        ss_to = possibles.index[elu]
        #ss_to = possibles.loc[ind_elu, "Code"]
        ss_to_name = ss_names.loc[ss_to, "Name"]
            
        ss_from_id = closest_peri.loc[ss_to]
        ss_from_name = ss_names.loc[ss_from_id, "Name"]

        workers.loc[i]=[ss_from_id, ss_from_name, i, "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", 6, "Worker", ss_to, ss_to_name]
        p-=1
        i+=1


for ss in normal_places.index:
    print("ss", ss)
    ss_from_id = closest_peri.loc[ss]
    ss_from_name = ss_names.loc[ss_from_id, "Name"]


    ss_to_name = ss_names.loc[ss, "Name"]
    p= normal_places.loc[ss, "Sum of OBS_VALUE"]
    while p > 0:
        print("p", p)
        workers.loc[i]=[ss_from_id, ss_from_name, i, "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", 6, "Worker", ss, ss_to_name]
        p-=1
        i+=1

print(workers)
workers.to_csv("foreign_worker_workplace.csv")


