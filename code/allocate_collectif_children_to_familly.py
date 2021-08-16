import pandas as pd
import random

all_hh = pd.read_csv('all_hh_final.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace=True)
all_hh.rename(columns={"HouseHorldTypeName": "HouseholdTypeName"}, inplace=True)
print(all_hh, "all_hh")

coll_child = all_hh[(all_hh.HouseholdTypeID == 6) & (all_hh.Age > 0) & (all_hh.Age < 18)]
print(coll_child)

#age = 0 ==> 104 enfants ==> tous en néonat à l'hopital

#IBSA 4213 401 lits en pédiatrie
colnames = coll_child.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
hospi = pd.DataFrame(columns=colnames)

nb_hospi = 401 #IBSA 4213 401 lits en pédiatrie

i = 0

    
while len(coll_child) > 0 and nb_hospi > 0:
    print("i", i)
    elu = random.randrange(0, len(coll_child), 1)
    ind_elu = coll_child.index[elu]
    el = coll_child.loc[ind_elu].tolist()
    el.extend([10, "Hospital"])
    hospi.loc[i] = el
    coll_child.drop([ind_elu], inplace=True)
    all_hh.drop([ind_elu], inplace=True)
    nb_hospi-=1
    i+=1

#Reallouer enfants collectifs à des familles
sectors = coll_child.SectorStatID
sectors.drop_duplicates(inplace=True)
print(sectors)

realloue = pd.DataFrame(columns=colnames)
i =0
for s in sectors:
    #print(s)

    possible_fam = all_hh[(all_hh.HouseholdTypeID == 1) | (all_hh.HouseholdTypeID == 4)]
    possible_fam = possible_fam[possible_fam.SectorStatID == s]
    
    print(possible_fam)
    
    coll_child_s = coll_child[coll_child.SectorStatID == s]
    if s != '21001C522' and s != '21009A2MJ' and s != '21009A922' and s!= '21004B2NJ' and s!= '21009A602' and s!= '21009A512' and s != '21016A331': #Hopital ==> aucune famille, campus unif ==> aucune famille, casern ==> aucune famille, cite de la chaussée, belvedere, wiertz et CHAUSSEE DE WATERLOO-OUESTpas de famille ?
    
        for child in coll_child_s.index:
            if len(possible_fam) > 0:
                print("i", i)
                elu = random.randrange(0, len(possible_fam), 1)
                ind_elu = possible_fam.index[elu]
                el = possible_fam.loc[ind_elu]
                
                hh_id = el.HouseholdID
                hh_type_id = el.HouseholdTypeID
                hh_type_name = el.HouseholdTypeName
    
                all_hh.loc[child, "HouseholdID"]= hh_id
                all_hh.loc[child, "HouseholdTypeID"]= hh_type_id
                all_hh.loc[child, "HouseholdTypeName"]= hh_type_name
                
                realloue.loc[i] = el
    
                i+=1
            else:
                error
            
print(all_hh)
all_hh.to_csv('all_hh_child_Reallocated.csv')
child_co = all_hh[(all_hh.HouseholdTypeID == 6) & (all_hh.Age > 0) & (all_hh.Age < 18)]
print(child_co)
    

    