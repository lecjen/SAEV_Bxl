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

all_hh = pd.read_csv('all_hh_collectif_cleaned_v2.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace = True)
print(all_hh)



child_mat = all_hh[(all_hh.Age < 6) & (all_hh.Age > 2)]

child_mat_collectif = child_mat[child_mat.HouseholdTypeID == 6]

child_mat_collectif['WorkerID']=10
child_mat_collectif['WorkerType']="Hospital"

print(child_mat_collectif)
print(len(child_mat_collectif)) #TODO check <= 401 (et difference avec 0-2 ans)
child_mat_collectif.to_csv("child_mat_collectif_workId.csv")

child_mat_hh_types_1n4 = child_mat[(child_mat.HouseholdTypeID == 1) | (child_mat.HouseholdTypeID == 4)]

child_mat_should_not = child_mat[(child_mat.HouseholdTypeID != 6) & (child_mat.HouseholdTypeID != 1) & (child_mat.HouseholdTypeID !=4)]
print(len(child_mat_should_not)) #TODO check it is 0



avance_retard = pd.read_csv('avance_retard_scolaire.csv', sep=";")
avance_retard.set_index('Code', inplace=True, drop=True)
print(avance_retard) 

sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)


#En avance : 5ans mais deja en primaires ==> TODO at another level because arrondi ==> tjr zero
colnames = child_mat_hh_types_1n4.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
en_avance = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for s in sectors:
    print("s", s)
    possible = child_mat_hh_types_1n4[(child_mat_hh_types_1n4.GenderID == 0) & (child_mat_hh_types_1n4.SectorStatID == s) &
                                      (child_mat_hh_types_1n4.Age == 5)]
    nb_avance_str = avance_retard.loc[s, "#5 ans en primaire garçon"]
    if type(nb_avance_str) == str:
        nb_avance_str = nb_avance_str.replace(",", ".")
    
    nb_avance = round(float(nb_avance_str))
    
    while nb_avance > 0:
        print("i", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu]
        el.extend(["2", "Primaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_mat_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

#Filles
for s in sectors:
    print("s filles", s)
    possible = child_mat_hh_types_1n4[(child_mat_hh_types_1n4.GenderID == 1) & (child_mat_hh_types_1n4.SectorStatID == s) &
                                      (child_mat_hh_types_1n4.Age == 5)]
    nb_avance_str = avance_retard.loc[s, "#5 ans en primaire filles"]
    if type(nb_avance_str) == str:
        nb_avance_str = nb_avance_str.replace(",", ".")
    
    nb_avance = round(float(nb_avance_str))
    while nb_avance > 0:
        print("i files,", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu]
        el.extend(["2", "Primaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_mat_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

print(en_avance)
en_avance.to_csv("child_mat_en_avance_workId.csv")

#School at home
at_home = pd.DataFrame(columns=colnames)
nb_at_home = 275 #TODO adapt with 2018-2019 IBSA

i=0
while nb_at_home > 0:
    print("i at home", i)
    elu = random.randrange(0, len(child_mat_hh_types_1n4), 1)
    ind_elu = child_mat_hh_types_1n4.index[elu]
    el = child_mat_hh_types_1n4.loc[ind_elu].tolist()
    el.extend(["7", "StayHome"])
    at_home.loc[i] = el
    child_mat_hh_types_1n4.drop([ind_elu], inplace=True)
    nb_at_home-=1
    i+=1

print(at_home)
at_home.to_csv("child_mat_at_home_workId.csv")


child_mat_hh_types_1n4['WorkerID']=1
child_mat_hh_types_1n4['WorkerType']="Maternelles"

print(child_mat_hh_types_1n4)
child_mat_hh_types_1n4.to_csv("child_mat_maternelles_workId.csv")