
import pandas as pd

baby = pd.read_csv('baby_creche_and_stay_home_workplace_v2.csv')
print(baby)
child = pd.read_csv('child_mat_at_home_workId.csv')
print(child)
jeune = pd.read_csv('jeune_at_home_workId_v2.csv')
print(jeune)
adulte = pd.read_csv('adultes_home_workid.csv')
print(adulte)
vieux = pd.read_csv('vieux_at_home.csv')
print(vieux)

print(baby.columns) #OK
print(child.columns)
child.drop(columns=['Code', 'Commune'], inplace=True)
child.rename(columns={'WorkPlaceID': 'WorkSectorStatID', 'WorkPlaceName' :'WorkSectorStatName'}, inplace=True)
print(jeune.columns)
jeune.drop(columns=['Code_x', 'Commune_x', 'Code_y', 'Name', 'Commune_y'], inplace=True)
jeune["WorkSectorStatID"]=jeune["SectorStatID"]
jeune["WorkSectorStatName"]=jeune["SectorStatName"]

print(adulte.columns)
adulte.drop(columns=['Code_x', 'Commune_x', 'Code_y', 'Name', 'Commune_y'], inplace=True)
adulte["WorkSectorStatID"]=adulte["SectorStatID"]
adulte["WorkSectorStatName"]=adulte["SectorStatName"]

print(vieux.columns)
vieux.drop(columns=['Unnamed: 0.1', 'Code', 'Commune'], inplace=True)
vieux.rename(columns={'WorkID': "WorkerID", 'WorkType':"WorkerType"}, inplace=True)
vieux["WorkSectorStatID"]=vieux["SectorStatID"]
vieux["WorkSectorStatName"]=vieux["SectorStatName"]

at_home = pd.concat([baby, child, jeune, adulte, vieux])
at_home.drop(columns=['Unnamed: 0'], inplace=True)
at_home.reset_index(inplace=True, drop=True)
print(at_home)
at_home = at_home[at_home.WorkerID == 7]
print(at_home)
at_home.to_csv('all_at_home_workplace.csv')