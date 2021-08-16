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


sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
print(sectors_names_correspondance)


all_hh = all_hh.merge(sectors_names_correspondance, left_on="SectorStatID", right_on="Code")
print(all_hh)


sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)
print(sectors)

communes = all_hh['Commune']
communes.drop_duplicates(inplace=True)
print(communes)

child_mat = all_hh[(all_hh.Age < 6) & (all_hh.Age > 2)]
print(child_mat)
"""
already done somewhere else

child_mat_collectif = child_mat[child_mat.HouseholdTypeID == 6]
print(child_mat_collectif)

child_mat_collectif['WorkerID']=10
child_mat_collectif['WorkerType']="Hospital"

print(child_mat_collectif)
print(len(child_mat_collectif)) #TODO check <= 401 (et difference avec 0-2 ans) ==> 42 ok
child_mat_collectif.to_csv("child_mat_collectif_workId.csv")
"""

child_mat_hh_types_1n4 = child_mat[(child_mat.HouseholdTypeID == 1) | (child_mat.HouseholdTypeID == 4)]
print(child_mat_hh_types_1n4)

child_mat_should_not = child_mat[(child_mat.HouseholdTypeID != 6) & (child_mat.HouseholdTypeID != 1) & (child_mat.HouseholdTypeID !=4)]
print(len(child_mat_should_not)) #= 0 ==> pft


avance_retard = pd.read_csv('avance_retard_5ans.csv', sep=";")
avance_retard.set_index('Commune', inplace=True, drop=True)
print(avance_retard)


#En avance : 5ans mais deja en primaires ==> at commune level because arrondi ==> tjr zero at ss level
colnames = child_mat_hh_types_1n4.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
en_avance = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for com in communes:
    print("com", com)
    possible = child_mat_hh_types_1n4[(child_mat_hh_types_1n4.GenderID == 0) & (child_mat_hh_types_1n4.Commune == com) &
                                      (child_mat_hh_types_1n4.Age == 5)]
    nb_avance_str = avance_retard.loc[com, "Garcons"]
    
    nb_avance = round(float(nb_avance_str)/6)
    
    while nb_avance > 0:
        print("i", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["2", "Primaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_mat_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

#Filles
for com in communes:
    print("com", com)
    possible = child_mat_hh_types_1n4[(child_mat_hh_types_1n4.GenderID == 1) & (child_mat_hh_types_1n4.Commune == com) &
                                      (child_mat_hh_types_1n4.Age == 5)]
    nb_avance_str = avance_retard.loc[com, "Filles"]
    
    nb_avance = round(float(nb_avance_str)/6)
    while nb_avance > 0:
        print("i files,", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["2", "Primaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_mat_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

print(en_avance)
en_avance.to_csv("child_mat_en_avance_so_prim_workId.csv")

"""
#School at home
colnames.extend(["WorkPlaceID", "WorkPlaceName"])
at_home = pd.DataFrame(columns=colnames)
nb_at_home = 275 #TODO adapt with 2018-2019 IBSA

i=0
while nb_at_home > 0:
    print("i at home", i)
    elu = random.randrange(0, len(child_mat_hh_types_1n4), 1)
    ind_elu = child_mat_hh_types_1n4.index[elu]
    el = child_mat_hh_types_1n4.loc[ind_elu].tolist()
    el.extend(["7", "StayHome", child_mat_hh_types_1n4.loc[ind_elu, "SectorStatID"],
               child_mat_hh_types_1n4.loc[ind_elu, "SectorStatName"]])
    at_home.loc[i] = el
    child_mat_hh_types_1n4.drop([ind_elu], inplace=True)
    nb_at_home-=1
    i+=1

print(at_home)
at_home.to_csv("child_mat_at_home_workId.csv")
"""

child_mat_hh_types_1n4['WorkerID']=1
child_mat_hh_types_1n4['WorkerType']="Maternelles"

print(child_mat_hh_types_1n4)
child_mat_hh_types_1n4.to_csv("child_mat_maternelles_workId.csv")