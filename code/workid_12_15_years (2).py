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

all_hh = pd.read_csv('all_hh_child_Reallocated.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace = True)
print(all_hh)


child_sec = all_hh[(all_hh.Age < 16) & (all_hh.Age > 11)]
print(child_sec)
"""
#already done
child_sec_collectif = child_sec[child_sec.HouseholdTypeID == 6]

child_sec_collectif['WorkerID']=10
child_sec_collectif['WorkerType']="Hospital"

print(child_sec_collectif)
print(len(child_sec_collectif)) #TODO check <= 401 de pediatrie and check somme avec 0-2 and 3-5 and 6-11 ==> 52 ok
child_sec_collectif.to_csv("child_sec_collectif_workId.csv")
"""

child_sec_hh_types_1n4 = child_sec[(child_sec.HouseholdTypeID == 1) | (child_sec.HouseholdTypeID == 4)]
print(child_sec_hh_types_1n4)

child_sec_should_not = child_sec[(child_sec.HouseholdTypeID != 6) & (child_sec.HouseholdTypeID != 1) & (child_sec.HouseholdTypeID !=4)]
print(len(child_sec_should_not)) #=0 ==> pft

avance_retard = pd.read_csv('avance_retard_scolaire.csv', sep=";")
avance_retard.set_index('Code', inplace=True, drop=True)
print(avance_retard) 

sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)
print(sectors)

#En retard d'un an: 12ans mais encore en primaires
colnames = child_sec_hh_types_1n4.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
en_retard_1 = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for s in sectors:
    possible = child_sec_hh_types_1n4[(child_sec_hh_types_1n4.GenderID == 0) & (child_sec_hh_types_1n4.SectorStatID == s) &
                                      (child_sec_hh_types_1n4.Age == 12)]
    
    nb_retard_str = avance_retard.loc[s, "#12 ans en primaires garçon"]
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0 and len(possible)>0:
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["2", "Primaires"])
        en_retard_1.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_sec_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

#Filles
for s in sectors:
    possible = child_sec_hh_types_1n4[(child_sec_hh_types_1n4.GenderID == 1) & (child_sec_hh_types_1n4.SectorStatID == s) &
                                      (child_sec_hh_types_1n4.Age == 12)]
    
    
    nb_retard_str = avance_retard.loc[s, "#12 ans en primaires filles"]
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0 and len(possible) > 0:
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["2", "Primaires"])
        en_retard_1.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_sec_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

print(en_retard_1)
en_retard_1.to_csv("child_sec_en_retard_1_workId.csv")

#En retard de 2 ans: 13ans mais encore en primaires
en_retard_2 = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for s in sectors:
    possible = child_sec_hh_types_1n4[(child_sec_hh_types_1n4.GenderID == 0) & (child_sec_hh_types_1n4.SectorStatID == s) &
                                      (child_sec_hh_types_1n4.Age == 13)]
        
    nb_retard_str = avance_retard.loc[s, "#13 ans en primaires garçon"]
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0:
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["2", "Primaires"])
        en_retard_2.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_sec_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

#Filles
for s in sectors:
    possible = child_sec_hh_types_1n4[(child_sec_hh_types_1n4.GenderID == 1) & (child_sec_hh_types_1n4.SectorStatID == s) &
                                      (child_sec_hh_types_1n4.Age == 11)]
        
    nb_retard_str = avance_retard.loc[s, "#13 ans en primaires filles"]
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0 and len(possible)>0:
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["2", "Primaires"])
        en_retard_2.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_sec_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

print(en_retard_2)
en_retard_2.to_csv("child_sec_en_retard_2_workId.csv")


child_sec_hh_types_1n4['WorkerID']=3
child_sec_hh_types_1n4['WorkerType']="Secondaires"

print(child_sec_hh_types_1n4)
child_sec_hh_types_1n4.to_csv("child_sec_secondaires_workId.csv")
