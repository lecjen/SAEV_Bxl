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

sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
print(sectors_names_correspondance)


all_hh = all_hh.merge(sectors_names_correspondance, left_on="SectorStatID", right_on="Code")
print(all_hh)

vieux = all_hh[all_hh.Age > 64]
vieux_not_collectif = vieux[vieux.HouseholdTypeID != 6]

#Vieux at Wrok
sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)

colnames = vieux_not_collectif.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
vieux_at_work = pd.DataFrame(columns=colnames)

#vieux_not_collectif_fe = vieux_not_collectif[vieux_not_collectif.GenderID == 1]

act_work_fe = pd.read_csv("activite_work_fe.csv", sep=";")
print(act_work_fe)

act_work_fe.set_index("Code", inplace=True, drop=True)
i = 0
for age in range(65, 105):
    print("age", age)
    age_str = str(age)+',00'
    act_work_fe_age= act_work_fe[age_str]

    for ss in sectors:
        print("ss", ss)
        
        nb_act_work_fe_str = act_work_fe_age.loc[ss]
        if type(nb_act_work_fe_str) == str:
            nb_act_work_fe_str = nb_act_work_fe_str.replace(",", ".")
        
        nb_act_work_fe = round(float(nb_act_work_fe_str))
        #nb_act_work_fe = round(act_work_fe_age.loc[ss])
        possible_fe = vieux_not_collectif[(vieux_not_collectif.SectorStatID == ss) & (vieux_not_collectif.GenderID == 1)]

        while nb_act_work_fe > 0 and len(possible_fe) > 0:
            print("i", i)
            elu = random.randrange(0, len(possible_fe), 1)
            ind_elu = possible_fe.index[elu]
            
            el = possible_fe.loc[ind_elu].tolist()
            el.extend([6, "Worker"])
            vieux_at_work.loc[i] = el

            possible_fe.drop([ind_elu], inplace=True)
            vieux_not_collectif.drop([ind_elu], inplace=True)

            nb_act_work_fe-=1
            i+=1

#vieux_not_collectif_ho = vieux_not_collectif[vieux_not_collectif.GenderID == 0]

act_work_ho = pd.read_csv("activite_work_ho.csv", sep=';')
print(act_work_ho)

act_work_ho.set_index("Code", inplace=True, drop=True)

for age in range(65, 95):
    print("age h", age)
    age_str = str(age)+',00'
    act_work_ho_age= act_work_ho[age_str]

    for ss in sectors:
        print("ss h", ss)
        
        nb_act_work_ho_str = act_work_ho_age.loc[ss]
        if type(nb_act_work_ho_str) == str:
            nb_act_work_ho_str = nb_act_work_ho_str.replace(",", ".")
        
        nb_act_work_ho = round(float(nb_act_work_ho_str))
        #nb_act_work_fe = round(act_work_fe_age.loc[ss])
        possible_ho = vieux_not_collectif[(vieux_not_collectif.SectorStatID == ss) & (vieux_not_collectif.GenderID == 0)]

        while nb_act_work_ho > 0 and len(possible_ho) > 0:
            print("i h", i)
            elu = random.randrange(0, len(possible_ho), 1)
            ind_elu = possible_ho.index[elu]
            
            el = possible_ho.loc[ind_elu].tolist()
            el.extend([6, "Worker"])
            vieux_at_work.loc[i] = el

            possible_ho.drop([ind_elu], inplace=True)
            vieux_not_collectif.drop([ind_elu], inplace=True)

            nb_act_work_ho-=1
            i+=1

"""
for age in range(65, 95):
    print("age", age)
    age_str = str(age)+',00'
    act_work_ho_age= act_work_fe[age_str]


    for ss in sectors:

        nb_act_work_ho = round(act_work_ho_age.loc[ss])
        possible_ho = vieux_not_collectif_ho[vieux_not_collectif_ho.SectorStatID == ss]

        while nb_act_work_ho > 0:
            elu = random.randrange(0, len(possible_ho), 1)
            ind_elu = possible_ho.index[elu]

            vieux_at_work.loc[i] = [vieux_not_collectif.loc[ind_elu], 6, "Worker"]

            possible_ho.drop([ind_elu], inplace=True)
            vieux_not_collectif.drop([ind_elu], inplace=True)

            nb_act_work_ho-=1
            i+=1
"""
print(vieux_at_work)
vieux_at_work.to_csv("vieux_worker_workid.csv")

vieux_not_collectif["WorkID"]=7
vieux_not_collectif["WorkType"]="Stay at home"
print(vieux_not_collectif)
vieux_not_collectif.to_csv('vieux_at_home.csv')


vieux_collectif = vieux[vieux.HouseholdTypeID == 6]

#Nursing home
colnames = vieux_collectif.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
nursing_home = pd.DataFrame(columns=colnames)

to_allocate = {"Anderlecht":2006, "Auderghem": 478, "Berchem Sainte-Agathe": 413, "Bruxelles":2495, 
               "Etterbeek":421, "Evere":1338, "Forest":572, "Ganshoren":210, "Ixelles":664, "Jette":1031,
               "Koekelberg": 271, "Saint-Gilles": 334, "Saint-Josse-ten-Noode":147, "Schaerbeek":989,
               "Uccle": 1752, "Watermael-Boitsfort": 574, "Molenbeek Saint-Jean":1387, 
               "Woluwe Saint-Lambert":882, "Woluwe Saint-Pierre": 412}
i=0
for com in to_allocate.keys():
    print("com nursing home", com)
    nb_to_allocate = to_allocate[com]
    possible = vieux_collectif[vieux_collectif.Commune == com]

    while nb_to_allocate > 0 and len(possible) > 0:
        print("i nursing", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        
        el = possible.loc[ind_elu].tolist()
        el.extend([8, "Nursing Home"])
        nursing_home.loc[i] = el

        possible.drop([ind_elu], inplace=True)
        vieux_collectif.drop([ind_elu], inplace=True)

        nb_to_allocate-=1
        i+=1
        
print(nursing_home)
nursing_home.to_csv('nursing_home.csv')

print(vieux_collectif)
vieux_collectif.to_csv("vieux_prison_hopital.csv")
#TODO hopital ou prison
