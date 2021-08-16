import pandas as pd
import random

workers_1 = pd.read_csv('ado_worker_workId.csv')
workers_1.drop(columns=["Unnamed: 0.1", "Code"], inplace=True)
print(workers_1)
workers_2 = pd.read_csv('ado_worker_colloc_workId.csv')
workers_2.drop(columns=["Unnamed: 0.1", "Code"], inplace=True)
print(workers_2)
workers_3 = pd.read_csv('jeune_wroker_workId_v2.csv')
workers_3.drop(columns=["Code_x", "Code_y", "Name", "Commune_y"], inplace=True)
workers_3.rename(columns={"Commune_x":"Commune", "WorkID": "WorkerID", "WorkType": "WorkerType"}, inplace=True)
print(workers_3)
workers_4 = pd.read_csv('18_20_jeune_parent_worker_workId_v2.csv')
workers_4.drop(columns=["Code"], inplace=True)
print(workers_4)
workers_5 = pd.read_csv('adultes_worker.csv')
workers_5.drop(columns=["Code_x", "Code_y", "Name", "Commune_y"], inplace=True)
workers_5.rename(columns={"Commune_x":"Commune", "WorkID": "WorkerID", "WorkerName": "WorkerType"}, inplace=True)
print(workers_5)
workers_6 = pd.read_csv('vieux_worker_workid.csv')
workers_6.drop(columns=["Unnamed: 0.1", "Code"], inplace=True)
print(workers_6)

print(workers_1.columns)
print(workers_2.columns)
print(workers_3.columns)
print(workers_4.columns)
print(workers_5.columns)
print(workers_6.columns)
workers = pd.concat([workers_1, workers_2, workers_3, workers_4, workers_5, workers_6])
workers.drop(columns=["Unnamed: 0", ], inplace=True)
workers.reset_index(inplace=True, drop=True)
print(workers)
#workers = pd.read() #TODO

ss_names = pd.read_csv('sector_stat.csv', sep=";")
ss_names.set_index("Code", inplace=True, drop=True)
print(ss_names)

colnames = ["SectorStatID", "SectorStatName", "PersID", "Age", "GenderID", "GenderName", 'ChildOrParent', "HouseholdID", "HouseholdTypeID", "HouseholdTypeName",  'Commune', "WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"]
bxl_bxl_normal = pd.DataFrame(columns=colnames)


#From Bxl to Bxl
places = pd.read_csv('work_flow_from_bxl_to_bxl.csv', sep=";")
print(places)

Z_sectors_from_only = places[(places.SECTOR_From.str.contains("Z")) & 
                             (~places.SECTOR_To.str.contains("Z"))]
#Z_sectors_from_only.set_index("SECTOR_From", inplace=True, drop=True)
print(Z_sectors_from_only)

Z_sectors_from_and_to = places[(places.SECTOR_From.str.contains("Z")) & 
                             (places.SECTOR_To.str.contains("Z"))]
#Z_sectors_from_and_to.set_index("SECTOR_From", inplace=True, drop=True)
print(Z_sectors_from_and_to);

Z_sectors_to_only = places[(~places.SECTOR_From.str.contains("Z")) & 
                             (places.SECTOR_To.str.contains("Z"))]
#Z_sectors_to_only.set_index("SECTOR_From", inplace=True, drop=True)
print(Z_sectors_to_only)

normal_places = places[(~places.SECTOR_From.str.contains("Z")) & 
                       (~places.SECTOR_To.str.contains("Z"))]
#normal_places.set_index("SECTOR_From", inplace=True, drop=True)
print(normal_places)

corres = {"21001ZZZZ" : "Anderlecht", "21002ZZZZ" : "Auderghem", "21003ZZZZ" : "Berchem Sainte-Agathe",
          "21004ZZZZ" : "Bruxelles", "21005ZZZZ" :	"Etterbeek", "21006ZZZZ" : "Evere", "21007ZZZZ" : 
              "Forest", "21008ZZZZ" : "Ganshoren", "21009ZZZZ" : "Ixelles", "21010ZZZZ" : "Jette",
              "21011ZZZZ" : "Koekelberg", "21012ZZZZ" : "Molenbeek Saint-Jean", "21013ZZZZ" : 
                  "Saint-Gilles", "21014ZZZZ" : "Saint-Josse-ten-Noode", "21015ZZZZ" : "Schaerbeek",
                  "21016ZZZZ" : "Uccle", "21017ZZZZ" : "Watermael-Boitsfort", "21018ZZZZ" : 
                      "Woluwe Saint-Lambert", "21019ZZZZ" : "Woluwe Saint-Pierre", "ZZZZZZZZZ" : "all"}


i = 0
for ind in normal_places.index:
    print("ind", ind)
    ss_from = normal_places.loc[ind, "SECTOR_From"]
    
    ss_from_name = ss_names.loc[ss_from, "Name"]

    ss_to = normal_places.loc[ind, "SECTOR_To"]
    ss_to_name = ss_names.loc[ss_to, "Name"]    
   
    p= normal_places.loc[ind, "Corrected_val"]
    
    possibles = workers[workers.SectorStatID == ss_from]
    
    while p > 0 and len(possibles)>0:
        print("i", i)
        elu = random.randrange(0, len(possibles), 1)
        ind_elu = possibles.index[elu]
        
        el = workers.loc[ind_elu].tolist()
        el.extend([ss_to, ss_to_name])
        bxl_bxl_normal.loc[i] = el

        possibles.drop([ind_elu], inplace=True)
        workers.drop([ind_elu], inplace=True)

        p-=1
        i+=1
        
        
print(bxl_bxl_normal)
bxl_bxl_normal.to_csv('worker_workplace_bxl_bxl_normal.csv')

z_bxl = pd.DataFrame(columns=colnames)

i = 0
for ind in Z_sectors_from_only.index:
    print("ind", ind)
    commune = corres[Z_sectors_from_only.loc[ind, "SECTOR_From"]]
    
    if commune == "all":
        possible_ss = ss_names
    else:
        possible_ss = ss_names[ss_names.Commune==commune]

    ss_to = Z_sectors_from_only.loc[ind, "SECTOR_To"]
    ss_to_name = ss_names.loc[ss_to, "Name"]    
   
    p= Z_sectors_from_only.loc[ind, "Corrected_val"]
    
    while p > 0 and len(possible_ss)>0:
        print("i", i)
        possibles = pd.DataFrame()
        
        while len(possibles) <= 0 and len(possible_ss)>0:
            elu_ss = random.randrange(0, len(possible_ss), 1)
            ss_from = possible_ss.index[elu_ss]
            ss_from_name = ss_names.loc[ss_from, "Name"]
            
            possibles = workers[workers.SectorStatID == ss_from]
            if len(workers[workers.SectorStatID == ss_from]) <= 0:
                possible_ss.drop([ss_from], inplace=True)
        
        if len(possibles)==0:
            break
        
        elu = random.randrange(0, len(possibles), 1)
        ind_elu = possibles.index[elu]
        
        el = workers.loc[ind_elu].tolist()
        el.extend([ss_to, ss_to_name])
        z_bxl.loc[i] = el

        possibles.drop([ind_elu], inplace=True)
        workers.drop([ind_elu], inplace=True)
        
        if len(workers[workers.SectorStatID == ss_from]) <= 0:
            possible_ss.drop([ss_from], inplace=True)

        p-=1
        i+=1


print(z_bxl)
z_bxl.to_csv('worker_workplace_z_bxl.csv')
workers.to_csv('workers_id_save_tmp.csv')

bxl_z = pd.DataFrame(columns=colnames)
i = 0
for ind in Z_sectors_to_only.index:
    print("ind", ind)
    ss_from = Z_sectors_to_only.loc[ind, "SECTOR_From"]
    ss_from_name = ss_names.loc[ss_from, "Name"]

    p= Z_sectors_to_only.loc[ind, "Corrected_val"]
    
    commune = corres[Z_sectors_to_only.loc[ind, "SECTOR_To"]]
    
    if commune == "all":
        possible_ss = ss_names
    else:
        possible_ss = ss_names[ss_names.Commune==commune]
    
    possibles = workers[workers.SectorStatID == ss_from]
    
    
    
    while p > 0 and len(possibles)>0:
        print("i", i)
        elu_ss = random.randrange(0, len(possible_ss), 1)
        ss_to = possible_ss.index[elu_ss]
        ss_to_name = ss_names.loc[ss_to, "Name"]   
        
        elu = random.randrange(0, len(possibles), 1)
        ind_elu = possibles.index[elu]
        
        el = workers.loc[ind_elu].tolist()
        el.extend([ss_to, ss_to_name])
        bxl_z.loc[i] = el

        possibles.drop([ind_elu], inplace=True)
        workers.drop([ind_elu], inplace=True)

        p-=1
        i+=1
        

print(bxl_z)
bxl_z.to_csv('worker_workplace_bxl_z.csv')
workers.to_csv('workers_id_save_tmp.csv')

z_z = pd.DataFrame(columns=colnames)

i = 0
for ind in Z_sectors_from_and_to.index:
    print("ind", ind)
    commune_from = corres[Z_sectors_from_and_to.loc[ind, "SECTOR_From"]]
    
    if commune_from == "all":
        possible_ss_from = ss_names
    else:
        possible_ss_from = ss_names[ss_names.Commune==commune_from]

    p= Z_sectors_from_and_to.loc[ind, "Corrected_val"]
    
    commune_to = corres[Z_sectors_from_and_to.loc[ind, "SECTOR_To"]]
    
    if commune_to == "all":
        possible_ss_to = ss_names
    else:
        possible_ss_to = ss_names[ss_names.Commune==commune_to]
    
    while p > 0 and len(possible_ss_from)>0:
        print("i", i)
        possibles = pd.DataFrame()
        
        while len(possibles) <= 0 and len(possible_ss_from)>0:
            elu_ss = random.randrange(0, len(possible_ss_from), 1)
            ss_from = possible_ss_from.index[elu_ss]
            ss_from_name = ss_names.loc[ss_from, "Name"]
            
            possibles = workers[workers.SectorStatID == ss_from]
            if len(workers[workers.SectorStatID == ss_from]) <= 0:
                possible_ss_from.drop([ss_from], inplace=True)
        
        if len(possibles)==0:
            break
        
        elu_ss_to = random.randrange(0, len(possible_ss_to), 1)
        ss_to = possible_ss_to.index[elu_ss_to]
        ss_to_name = ss_names.loc[ss_to, "Name"]   
        
        elu = random.randrange(0, len(possibles), 1)
        ind_elu = possibles.index[elu]
        
        el = workers.loc[ind_elu].tolist()
        el.extend([ss_to, ss_to_name])
        z_z.loc[i] = el

        possibles.drop([ind_elu], inplace=True)
        workers.drop([ind_elu], inplace=True)
        
        if len(workers[workers.SectorStatID == ss_from]) <= 0:
            possible_ss_from.drop([ss_from], inplace=True)

        p-=1
        i+=1
        
print(z_z)
z_z.to_csv('worker_workplace_z_z.csv')
workers.to_csv('workers_id_save_tmp.csv')

#From Bxl to out
places_out = pd.read_csv('work_flow_from_bxl_to_out.csv', sep=";")
print(places_out)

Z_sectors = places_out[places_out.SECTOR.str.contains("Z")]
#Z_sectors_from_only.set_index("SECTOR_From", inplace=True, drop=True)
print(Z_sectors)

out_normal = places_out[~places_out.SECTOR.str.contains("Z")]
print(out_normal)

closest_peri = pd.read_csv('closest_ss_peri_v2.csv')
closest_peri.set_index("SectorStatID", inplace=True, drop=True)
print(closest_peri)

bxl_out = pd.DataFrame(columns=colnames)

i = 0
for ind in out_normal.index:
    print("ind", ind)
    ss_from = out_normal.loc[ind, "SECTOR"]
    
    ss_from_name = ss_names.loc[ss_from, "Name"]

    ss_to = closest_peri.loc[ss_from, "Closest_Peri"]
    ss_to_name = ss_names.loc[ss_to, "Name"]   
   
    p= out_normal.loc[ind, "Corrected_val"]
    
    possibles = workers[workers.SectorStatID == ss_from]
    
    while p > 0 and len(possibles)>0:
        print("i", i)
        elu = random.randrange(0, len(possibles), 1)
        ind_elu = possibles.index[elu]
        
        el = workers.loc[ind_elu].tolist()
        el.extend([ss_to, ss_to_name])
        bxl_out.loc[i] = el

        possibles.drop([ind_elu], inplace=True)
        workers.drop([ind_elu], inplace=True)

        p-=1
        i+=1
        
        
print(bxl_out)
bxl_out.to_csv('worker_workplace_bxl_out_normal.csv')
workers.to_csv('workers_id_save_tmp.csv')

z_out = pd.DataFrame(columns=colnames)

i = 0
for ind in Z_sectors.index:
    print("ind", ind)
    
    commune = corres[Z_sectors.loc[ind, "SECTOR"]]
    
    if commune == "all":
        possible_ss = ss_names
    else:
        possible_ss = ss_names[ss_names.Commune==commune]  
   
    p= Z_sectors.loc[ind, "Corrected_val"]
    
    while p > 0 and len(possible_ss)>0:
        print("i", i)
        possibles = pd.DataFrame()
        
        while len(possibles) <= 0 and len(possible_ss)>0:
            elu_ss = random.randrange(0, len(possible_ss), 1)
            ss_from = possible_ss.index[elu_ss]
            ss_from_name = ss_names.loc[ss_from, "Name"]
            
            possibles = workers[workers.SectorStatID == ss_from]
            if len(workers[workers.SectorStatID == ss_from]) <= 0:
                possible_ss.drop([ss_from], inplace=True)
        
        if len(possibles)==0:
            break
        
        ss_to = closest_peri.loc[ss_from, "Closest_Peri"]
        ss_to_name = ss_names.loc[ss_to, "Name"] 
    
        elu = random.randrange(0, len(possibles), 1)
        ind_elu = possibles.index[elu]
        
        el = workers.loc[ind_elu].tolist()
        el.extend([ss_to, ss_to_name])
        z_out.loc[i] = el
        
        if len(workers[workers.SectorStatID == ss_from]) <= 0:
            possible_ss.drop([ss_from], inplace=True)

        possibles.drop([ind_elu], inplace=True)
        workers.drop([ind_elu], inplace=True)

        p-=1
        i+=1
        
        
print(z_out)
z_out.to_csv('worker_workplace_z_out.csv')
workers.to_csv('workers_id_save_tmp.csv')

#reste 61000
work = pd.DataFrame(columns=colnames)
i=0
for ind in workers.index:
    print("i", i)
    elu = random.randrange(0, len(ss_names), 1)
    ss = ss_names.index[elu]
    
    ss_to_name = ss_names.loc[ss, "Name"]
    
    el = workers.loc[ind].tolist()
    el.extend([ss, ss_to_name])
    work.loc[i]=el
    
    i+=1
    
print(work)
work.to_csv("to_much_worker.csv")

    

