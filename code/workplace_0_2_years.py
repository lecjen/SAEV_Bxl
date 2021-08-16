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

all_hh = pd.read_csv('all_hh_final.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace=True)
print(all_hh, "all_hh")
closeness = pd.read_csv('ss_closeness_ranking_v2.csv')
closeness.set_index("SectorStatID", inplace=True, drop=True)
print(closeness, "closeness")

baby = all_hh[all_hh.Age < 3]

baby_collectif = baby[baby.HouseholdTypeID == 6]

baby_collectif['WorkerID']=10
baby_collectif['WorkerType']="Hospital"

print(baby_collectif, "baby co")
print(len(baby_collectif)) #TODO check <= 958 = 448 de maternité + 401 de pediatrie + 109 de néo nat

baby_collectif.to_csv("baby_collectif_workId.csv")

baby_hh_types_1n4 = baby[(baby.HouseholdTypeID == 1) | (baby.HouseholdTypeID == 4)]

baby_should_not = baby[(baby.HouseholdTypeID != 6) & (baby.HouseholdTypeID != 1) & (baby.HouseholdTypeID !=4)]
print(len(baby_should_not), "zero ?") #TODO check it is 0 ==> pft

places_creches = pd.read_csv('places_creches.csv', sep=';')
places_creches= comma_to_dot(places_creches)
places_creches.set_index('Code', inplace=True, drop=True)
print(places_creches, "place creches")

sectors = all_hh.SectorStatID
colnames = baby.columns.tolist()
print(colnames)
colnames.extend(["WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"])
baby_hh_types_1n4_workplace = pd.DataFrame(columns=colnames)
sectors_names_correspondance = pd.DataFrame()
sectors_names_correspondance['SectorStatID']=all_hh['SectorStatID']
sectors_names_correspondance['SectorStatName']=all_hh['SectorStatName']
sectors_names_correspondance.set_index('SectorStatID', inplace=True, drop=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
i = 0
for rank in range(1, 725): #TODO check in closeness 724 ou 25 ou 26 ?
    print("rank", rank)
    for s in sectors:
        print("sector,", s)
        ranking = closeness.loc[s]
        ss_creche = ranking[rank]

        baby_in_s = baby_hh_types_1n4[baby_hh_types_1n4.SectorStatID == s]
        
        nbr_places = round(float(places_creches.loc[ss_creche, '#places en creche']))

        #j = 0
        while len(baby_in_s) > 0 and nbr_places > 0:
            print("i", i)
            bb = baby_in_s.index.tolist()[0]
            ss_creche_name = sectors_names_correspondance.loc[ss_creche]
            #bb = bbs[j]
            baby_hh_types_1n4_workplace.loc[i]=baby_in_s.loc[bb].tolist().extend([0, "Creche", ss_creche, ss_creche_name])

            baby_in_s.drop([bb], inplace=True)
            baby_hh_types_1n4.drop([bb], inplace=True)
            i +=1
            nbr_places -=1

for ind in baby_hh_types_1n4.index:
    print("ind", ind)
    baby_hh_types_1n4_workplace.loc[i]=[baby_hh_types_1n4.loc[ind], 7, "StayHome", baby_hh_types_1n4.loc[ind, "SectorStatId"],
                                        baby_hh_types_1n4.loc[ind, "SectorStatName"]]

print(baby_hh_types_1n4_workplace)
baby_hh_types_1n4_workplace.to_csv("baby_creche_and_stay_home_workplace.csv")

"""
for s in sectors:
    ranking = closeness.loc[s]
    baby_in_s = baby_hh_types_1n4[baby_hh_types_1n4.SectorStatID == s]
    #nbr_babys_in_s = len(baby_in_s)
    bbs = baby_in_s.index

    i = 0

    while len(baby_in_s) > 0:
        nbr_places = 0
        rank = 1
        while nbr_places <= 0 and rank < 724: #TODO check in closeness 724 ou 25 ou 23 ?
            ss_creche = ranking[rank]
            nbr_places = round(places_creches.loc[ss_creches, '#places en crèche'])
            rank+=1
        
        if rank == 724: #TODO lié au 724 du dessus
            
        
        else:
            ss_creche_name = sectors_names_correspondance.loc[ss_creche]
            bb = bbs[i]
            baby_hh_types_1n4_workplace.loc[i]=[baby_in_s.loc[bb], 0, "Creche", ss_creche, ss_creche_name]
            
            baby_in_s.drop([bb], inplace=True)
            
"""