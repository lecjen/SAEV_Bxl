import pandas as pd
import random

def replace_only_str(x, that, by):
    if type(x)==str:
        x = x.replace(that, by)

    return x

def comma_to_dot(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x : replace_only_str(x, ',', "."))

    return df

def clean_col_names(df):
    for col in df.columns:
        if 'Unnamed:' in col:
            new_col_name = col[9:]
            df[new_col_name]=df[col]
            df.drop(columns=[col], inplace=True)
    return df

all_hh = pd.read_csv('all_hh.csv') #TODO to change
print(all_hh)

ado = all_hh[(all_hh.Age == 16) or (all_hh.Age == 17)]

ado_parents = ado[(ado.ChildOrParent == "Parent")]
ado_parents = ado_parents[(ado_parents.HouseHoldTypeID == 1) | (ado_parents.HouseHoldTypeID == 2) | (ado_parents.HouseHoldTypeID == 3) |
                          (ado_parents.HouseHoldTypeID == 4)]

ado_parents['WorkerID']=6
ado_parents['WorkerType']="Worker"

print(ado_parents)
ado_parents.to_csv("ado_worker_workId.csv")

ado_not_collectif = ado[(ado.HouseholdTypeID == 5) | ((ado.ChildOrParent == "Child") & (ado.HouseholdTypeID == 1)) |
                        ((ado.ChildOrParent == "Child") & (ado.HouseholdTypeID == 4))]

avance_retard = pd.read_csv('avance_retard_scolaire.csv')
avance_retard.set_index('Code', inplace=True, drop=True)
print(avance_retard) #TODO check unnamed, index etc

sectors = all_hh['SectorStatID']

#En avance: 17 ans mais deja à l'unif ==> TODO at another level
colnames = ado_not_collectif.columns
colnames = colnames.append(["WorkerID", "WorkerType"])
en_avance = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for s in sectors:
    possible = ado_not_collectif[(ado_not_collectif.GenderID == 0) & (ado_not_collectif.SectorStatID == s) &
                                 (ado_not_collectif.Age == 17)]
    nb_avance = round(avance_retard.loc[s, "#17 ans a l'unif garçon"])
    while nb_avance > 0:
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        hh_type_id = ado_not_collectif.loc[ind_elu, "HouseholdTypeID"]

        if hh_type_id == 5:
            en_avance.loc[i] = [possible.loc[ind_elu], "4", "Unif on campus"]
        elif hh_type_id == 1 or hh_type_id == 4 :
            en_avance.loc[i] = [possible.loc[ind_elu], "5", "Unif off campus"]
        else:
            error

        possible.drop([ind_elu], inplace=True)
        ado_not_collectif.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

#Filles
for s in sectors:
    possible = ado_not_collectif[(ado_not_collectif.GenderID == 1) & (ado_not_collectif.SectorStatID == s) &
                                 (ado_not_collectif.Age == 17)]
    nb_avance = round(avance_retard.loc[s, "#17 ans a l'unif filles"])
    while nb_avance > 0:
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        hh_type_id = ado_not_collectif.loc[ind_elu, "HouseholdTypeID"]

        if hh_type_id == 5:
            en_avance.loc[i] = [possible.loc[ind_elu], "4", "Unif on campus"]
        elif hh_type_id == 1 or hh_type_id == 4 :
            en_avance.loc[i] = [possible.loc[ind_elu], "5", "Unif off campus"]
        else:
            error

        possible.drop([ind_elu], inplace=True)
        ado_not_collectif.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

print(en_avance)
en_avance.to_csv("ado_unif_en_avance_workId.csv")

ado_sec = ado_not_collectif[(ado_not_collectif.HouseholdTypeID == 1) | (ado_not_collectif.HouseholdTypeID == 4)]

ado_sec['WorkerID']=3
ado_sec['WorkerType']="Secondaires"

print(ado_sec)
ado_sec.to_csv("ado_sec_workId.csv")

ado_colloc_worker = ado_not_collectif[ado_not_collectif.HouseholdTypeID == 5]

ado_colloc_worker['WorkerID']=6
ado_colloc_worker['WorkerType']="Worker"

print(ado_colloc_worker)
ado_colloc_worker.to_csv("ado_worker_colloc_workId.csv")

#TODO clarifier hopital prison
ado_hopital = pd.DataFrame(columns=colnames)

place_hopital = 401 #- somme des places pediatrie utilisées

ado_collectif = ado[ado.HouseholdTypeID == 10]
i = 0
while len(ado_collectif) > 0 and place_hopital > 0 :
    elu = random.randrange(0, len(ado_collectif), 1)
    ind_elu = ado_collectif.index[elu]

    ado_hopital.loc[i] = [ado_collectif.loc[ind_elu], "10", "Hospital"]

    ado_collectif.drop([ind_elu], inplace=True)
    place_hopital-=1
    i+=1

print(ado_hopital)
ado_hopital.to_csv("ado_16_17_hopital_workid.csv")
"""
ado_collectif["WorkID"]=9
ado_collectif["WorkType"]="Prison"

print(ado_collectif)
ado_collectif.to_csv("ado_16_17_prison_workid.csv")
"""