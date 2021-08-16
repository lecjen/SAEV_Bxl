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

all_hh = pd.read_csv('all_hh_collectif_cleaned_v2.csv') #TODO to change
all_hh.drop(columns=["Unnamed: 0"], inplace = True)
print(all_hh)

child_prim = all_hh[(all_hh.Age < 12) & (all_hh.Age > 5)]

child_prim_collectif = child_prim[child_prim.HouseholdTypeID == 6]

child_prim_collectif['WorkerID']=10
child_prim_collectif['WorkerType']="Hospital"

print(child_prim_collectif)
print(len(child_prim_collectif)) #TODO check <= 401 and somme avec 0-2 et 3-5


child_prim_collectif.to_csv("child_prim_collectif_workId.csv")

child_prim_hh_types_1n4 = child_prim[(child_prim.HouseholdTypeID == 1) | (child_prim.HouseholdTypeID == 4)]

child_prim_should_not = child_prim[(child_prim.HouseholdTypeID != 6) & (child_prim.HouseholdTypeID != 1) & (child_prim.HouseholdTypeID !=4)]
print(len(child_prim_should_not)) #TODO check it is 0


avance_retard = pd.read_csv('avance_retard_scolaire.csv', sep=";")
avance_retard.set_index('Code', inplace=True, drop=True)
print(avance_retard) 

avance = pd.read_csv('avance_retard_11ans.csv', sep=";")
avance.set_index('Code', inplace=True, drop=True)
print(avance) 

sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)

#En avance : 11ans mais deja en secondaires ==> TODO at commune level
colnames = child_prim_hh_types_1n4.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
en_avance = pd.DataFrame(columns=colnames)


#Garcons
i = 0
for s in sectors:
    print("s", s)
    possible = child_prim_hh_types_1n4[(child_prim_hh_types_1n4.GenderID == 0) & (child_prim_hh_types_1n4.SectorStatID == s) &
                                       (child_prim_hh_types_1n4.Age == 11)]
    
    nb_avance_str = avance_retard.loc[s, "#11 ans en secondaires garçon"]
    if type(nb_avance_str) == str:
        nb_avance_str = nb_avance_str.replace(",", ".")
    
    nb_avance = round(float(nb_avance_str))
   
    while nb_avance > 0:
        print("i", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu]
        el.extend(["3", "Secondaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_prim_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1

#Filles
for s in sectors:
    print("s filles", s)
    possible = child_prim_hh_types_1n4[(child_prim_hh_types_1n4.GenderID == 1) & (child_prim_hh_types_1n4.SectorStatID == s) &
                                       (child_prim_hh_types_1n4.Age == 11)]
    nb_avance_str = avance_retard.loc[s, "#11 ans en secondaires filles"]
    if type(nb_avance_str) == str:
        nb_avance_str = nb_avance_str.replace(",", ".")
    
    nb_avance = round(float(nb_avance_str))
    while nb_avance > 0:
        print("i filles", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu]
        el.extend(["3", "Secondaires"])
        en_avance.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        child_prim_hh_types_1n4.drop([ind_elu], inplace=True)
        nb_avance-=1
        i+=1


print(en_avance)
en_avance.to_csv("child_prim_en_avance_workId.csv")


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

child_prim_hh_types_1n4['WorkerID']=2
child_prim_hh_types_1n4['WorkerType']="Primaires"

print(child_prim_hh_types_1n4)
child_prim_hh_types_1n4.to_csv("child_prim_primaires_workId.csv")