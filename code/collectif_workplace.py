import pandas as pd
import random

all_hh = pd.read_csv('all_hh_child_Reallocated.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace=True)
print(all_hh, "all_hh")
a

collectif = all_hh[all_hh.HouseholdType==6]
print(collectif) #TODO number used as x in chainType allocation
b

collectif_child = collectif[collectif.Age < 14]
print(collectif_child) #TODO check < nbr de places en hopital
c

collectif_jeune = collectif[(collectif.Age > 13) & (collectif.Age < 19)]
print(collectif_jeune) #TODO check if < nbr places hopital sinon certain en prison
d

collectif_adulte = collectif[collectif.Age > 18]
print(collectif_adulte)
e

places_nursing = pd.read_csv('nursing_home_ss.csv', sep=";")
#places_nursing.drop(columns=["Unnamed: 0"], inplace=True)
placeS_nursing.set_index("Code", inplace=True, drop=True)
print(places_nursing)
f

colnames = collectif_adulte.columns.tolist()
print(colnames) #TODO check quelles col doivent etre ajoutees
g
colnames.extend() #TODO
nursing_people = pd.DataFrame(colunms=colnames)

i= 0
for ss in places_nursing.index:
    places = places_nursing.loc[ss, "Nb_lits_ss"]
    
    if type(places)==str:
        places = places.replace(",", ".")
    
    places = round(float(places))
    
    for age in range(104, 18, -1):
        possible = collectif_adulte[(collectif_adulte.Age == age) & (collectif_adulte.SectorStatID == ss)]
        
        while len(possible) > 0 and places > 0:
            elu = random.randrange(0, len(possible), 1)
            ind_elu = possible.index[elu]
            el = possible.loc[ind_elu].tolist()
            el.extend([8, "Nursing Home"])
            nursing_people.loc[i] = el
            possible.drop([ind_elu], inplace=True)
            collectif_adulte.drop([ind_elu], inplace=True)
            places-=1
            i+=1

print(nursing_people)
nursing_people.to_csv("nursing_workplace.csv")
h

prisoneers = pd.DataFrame(colunms=colnames)
ss_st_gilles_prison = '21013A04-'
ss_forest_prison = '21007A73-'

prisonneers_forest = collectif_adulte[(collectif_adulte.GenderID == 0) & (collectif_adulte.SectorStatID == ss_forest_prison)]
print(prisonneers_forest) #TODO check nb < 180 ?
i

prisonneers_st_gilles = collectif_adulte[(collectif_adulte.GenderID == 0) & (collectif_adulte.SectorStatID == ss_st_gilles_prison)]
print(prisonneers_st_gilles) #TODO check nb < 850 ?
j

hopi = collectif_adulte[(collectif_adulte.GenderID != 0) | (collectif_adulte.SectorStatID != ss_forest_prison)]
hopi = hopi[(hopi.GenderID !0) | (hopi.SectorStatID != ss_st_gilles_prison)]
print(hopi) #TODO check size
k

hopi_geria = hopi[hopi.Age > 64]
print(hopi_geria) #TODO check < 1083
l

hopi_adultes = hopi[hopi.Age < 65]
print(hopi_adultes) #TODO check < 6912

#TODO save les bonhommes    