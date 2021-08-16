import pandas as pd

coll_1 = pd.read_csv('baby_collectif_workId_v2.csv')
print(coll_1)

coll_2 = pd.read_csv('jeune_collectif_hopi_or_prison_v2.csv')
print(coll_2)

coll_3 = pd.read_csv('adultes_collectif.csv')
print(coll_3)

coll_4 = pd.read_csv('vieux_prison_hopital.csv')
print(coll_4)

print(373+len(coll_1)+len(coll_2)+len(coll_3)+len(coll_4)) #82843

all_hh = pd.read_csv('all_hh_final.csv')
print(all_hh) #1223937