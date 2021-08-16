import pandas as pd
import random
import datetime

start = datetime.datetime.now()

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

avance_retard = pd.read_csv('avance_retard_scolaire.csv', sep=";")
avance_retard.set_index('Code', inplace=True, drop=True)
print(avance_retard) 

avance = pd.read_csv('avance_retard_11ans.csv', sep=";")
avance.set_index('Commune', inplace=True, drop=True)
avance = comma_to_dot(avance)
print(avance) 

sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
print(sectors_names_correspondance)

all_hh = all_hh.merge(sectors_names_correspondance, left_on="SectorStatID", right_on="Code")
print(all_hh)

child_prim = all_hh[(all_hh.Age < 12) & (all_hh.Age > 5)]
print(child_prim)
"""
#already done
child_prim_collectif = child_prim[child_prim.HouseholdTypeID == 6]

child_prim_collectif['WorkerID']=10
child_prim_collectif['WorkerType']="Hospital"

print(child_prim_collectif)
print(len(child_prim_collectif)) #TODO check <= 401 and somme avec 0-2 et 3-5 ==> 76


child_prim_collectif.to_csv("child_prim_collectif_workId.csv")
"""

child_prim_hh_types_1n4 = child_prim[(child_prim.HouseholdTypeID == 1) | (child_prim.HouseholdTypeID == 4)]
print(child_prim_hh_types_1n4)

child_prim_should_not = child_prim[(child_prim.HouseholdTypeID != 6) & (child_prim.HouseholdTypeID != 1) & (child_prim.HouseholdTypeID !=4)]
print(len(child_prim_should_not)) #= 0 ==> pft

sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)

communes = all_hh['Commune']
communes.drop_duplicates(inplace=True)
print(communes)

#En avance : 11ans mais deja en secondaires
colnames = child_prim_hh_types_1n4.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
en_avance = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for com in communes:
    print("com", com)
    possible = child_prim_hh_types_1n4[(child_prim_hh_types_1n4.GenderID == 0) & (child_prim_hh_types_1n4.Commune == com) &
                                      (child_prim_hh_types_1n4.Age == 11)]
    nb_avance_str = avance.loc[com, "Garcons"]
    
    nb_avance = round(float(nb_avance_str)/6)
    
    while nb_avance > 0:
        print("i", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["3", "Secondaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_prim_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

#Filles
for com in communes:
    print("com", com)
    possible = child_prim_hh_types_1n4[(child_prim_hh_types_1n4.GenderID == 1) & (child_prim_hh_types_1n4.Commune == com) &
                                      (child_prim_hh_types_1n4.Age == 11)]
    nb_avance_str = avance.loc[com, "Filles"]
    
    nb_avance = round(float(nb_avance_str)/6)
    
    while nb_avance > 0:
        print("i", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["3", "Secondaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_prim_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

print(en_avance)
en_avance.to_csv("child_prim_en_avance_so_sec_workId.csv")

"""
#En retard : 6ans mais deja encore en maternelles
en_retard = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for s in sectors:
    print("s retard g", s)
    possible = child_prim_hh_types_1n4[(child_prim_hh_types_1n4.GenderID == 0) & (child_prim_hh_types_1n4.SectorStatID == s) &
                                       (child_prim_hh_types_1n4.Age == 6)]
    
    nb_retard_str = avance_retard.loc[s, "#6 ans en maternelles garçon"]
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    
    while nb_retard > 0 and len(possible) > 0:
        print("i retard g", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["1", "Maternelles"])
        en_retard.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_prim_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

#Filles
for s in sectors:
    print("s retard f", s)
    possible = child_prim_hh_types_1n4[(child_prim_hh_types_1n4.GenderID == 1) & (child_prim_hh_types_1n4.SectorStatID == s) &
                                       (child_prim_hh_types_1n4.Age == 6)]
    nb_retard_str = avance_retard.loc[s, "#6 ans en maternelles filles"]
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0:
        print("i retard f", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["1", "Maternelles"])
        en_retard.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_prim_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1


print(en_retard)
en_retard.to_csv("child_prim_en_retard_workId.csv")
"""

child_prim_hh_types_1n4['WorkerID']=2
child_prim_hh_types_1n4['WorkerType']="Primaires"

print(child_prim_hh_types_1n4)
child_prim_hh_types_1n4.to_csv("child_prim_primaires_workId.csv")


end = datetime.datetime.now()

print(end-start)