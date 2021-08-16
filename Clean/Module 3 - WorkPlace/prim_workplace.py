import pandas as pd
import numpy as np
import random

maternelles = pd.read_csv('prim_workid_quartier.csv')
maternelles.drop(columns=["Code", "Territoire", "Unnamed: 0"], inplace=True)
#maternelles.rename(columns={"Commune_x":"Commune"}, inplace=True)
print(maternelles)
e
perc_out = pd.read_csv('prim_from_quart_to_out_bxl_perc.csv', sep=';')
perc_out.drop(columns=["Code"], inplace=True)
perc_out.set_index("Territoire", inplace=True, drop=True)
print(perc_out)

nb_mat_quart = pd.read_csv("nb_inscrits_prim_habitant_le_quartier.csv")
nb_mat_quart.drop(columns=["Unnamed: 0"], inplace=True)
nb_mat_quart.set_index("Quartier", inplace=True, drop=True)
print(nb_mat_quart)

nb_mat_quart_out = pd.DataFrame()
nb_mat_quart_out["Quartiers"]=nb_mat_quart.index
nb_mat_quart_out.set_index('Quartiers', inplace=True, drop=True)
nb_mat_quart_out["Nb_out"]=np.zeros(len(nb_mat_quart_out))

for quart in nb_mat_quart_out.index:
    print("quart", quart)
    p = perc_out.loc[quart, "Part des enfants du territoire (quartier ou commune) inscrits dans une école primaire située en dehors de la Région (%)"]
    if type(p)==str:
         p = p.replace(",", ".")
    p = float(p)/100
    
    if quart in nb_mat_quart.index:
        n = nb_mat_quart.loc[quart, "Nb d'enfants inscrits en primaires habitant le quartier"]
        if type(n)==str:
            n = n.replace(",", ".")
        n = float(n)
    else:
        n =0
    
    nb =  p*n 
    nb_mat_quart_out.loc[quart] = nb

print(nb_mat_quart_out)
nb_mat_quart_out.to_csv('nb_prim_quart_out.csv')

colnames = maternelles.columns.tolist()
colnames.extend(["WorkSectorStatID", "WorkSectorStatName", "WorkCommuneName"])
mat_out = pd.DataFrame(columns=colnames)

closest_peri = pd.read_csv("closest_ss_peri_v2.csv")
closest_peri.set_index("SectorStatID", inplace=True, drop=True)
print(closest_peri)

population = pd.read_csv('correspondance_ss_quartiers.csv', sep=';')
corres_quartier_ss = pd.DataFrame()
corres_quartier_ss['Code'] = population.Code
corres_quartier_ss['Territoire'] = population.Territoire
corres_quartier_ss['Quartier'] = population.Quartier
corres_quartier_ss.dropna(inplace=True)
corres_quartier_ss.set_index("Code", inplace=True, drop=True)
print(corres_quartier_ss)

sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
#sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
print(sectors_names_correspondance)

#from bxl to out bxl
i=0
for quart in nb_mat_quart_out.index:
    print("quart add", quart)
    nb = nb_mat_quart_out.loc[quart, "Nb_out"]

    possible = maternelles[maternelles.Quartier == quart]

    while len(possible) > 0 and nb > 0:
        print("i", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]

        work_ss_id = closest_peri.loc[maternelles.loc[ind_elu, "SectorStatID"]]
        if type(work_ss_id)!= str:
            work_ss_id = work_ss_id[0]
        work_ss_name = corres_quartier_ss.loc[work_ss_id, "Territoire"]
        work_commune = sectors_names_correspondance.loc[work_ss_id, "Commune"]
        
        el = maternelles.loc[ind_elu].tolist()
        el.extend([work_ss_id, work_ss_name, work_commune])
        mat_out.loc[i] = el

        possible.drop([ind_elu], inplace=True)
        maternelles.drop([ind_elu], inplace=True)

        nb-=1
        i+=1

print(mat_out)
mat_out.to_csv('prim_out.csv')

places_mat_per_child = pd.read_csv('places_prim.csv', sep=";") #places par quart
places_mat_per_child.set_index("Territoire", inplace=True, drop=True)
places_mat_per_child.drop(columns=["Code"], inplace=True)
print(places_mat_per_child)


nb_mat_quart_in = pd.DataFrame()
nb_mat_quart_in["Quartiers"]=nb_mat_quart.index
nb_mat_quart_in.set_index('Quartiers', inplace=True, drop=True)
nb_mat_quart_in["Capacité d’accueil scolaire du quartier (nb d'élèves)"]=np.zeros(len(nb_mat_quart_out))

for quart in nb_mat_quart_out.index:
    print("quart", quart)
    p = places_mat_per_child.loc[quart, "Capacité d’accueil scolaire relative du territoire (primaire) (nb d'élèves/nb enfants)"]
    if type(p)==str:
         p = p.replace(",", ".")
    p = float(p)
    
    if quart in nb_mat_quart.index:
        n = nb_mat_quart.loc[quart, "Nb d'enfants inscrits en primaires habitant le quartier"]
        if type(n)==str:
            n = n.replace(",", ".")
        n = float(n)
    else:
        n =0
    
    nb =  p*n 
    nb_mat_quart_in.loc[quart] = nb

print(nb_mat_quart_in)
nb_mat_quart_in.to_csv('nb_prim_quart_in.csv')


ratio = pd.read_csv("ratio_inscrits_prim_ss_quart.csv", sep=";")

print(ratio)

capa_per_ss = pd.DataFrame()
capa_per_ss["SectorStatID"]=ratio.SectorStatID
capa_per_ss["Quartier"]=ratio.Quartier
capa_per_ss["Places Mat ss"]=np.zeros(len(ratio.index))
capa_per_ss.set_index("SectorStatID", inplace=True, drop=True)

ratio.set_index("SectorStatID", inplace=True, drop=True)
print(capa_per_ss)


for ss in capa_per_ss.index:
    print("ss", ss)    
    quart = capa_per_ss.loc[ss, "Quartier"]

    p = nb_mat_quart_in.loc[quart,"Capacité d’accueil scolaire du quartier (nb d'élèves)"]
    if type(p)==str:
         p = p.replace(",", ".")
    p = float(p)
    
    r = ratio.loc[ss, "ratio"]
    if type(r)==str:
         r = r.replace(",", ".")
    r = float(r)
    
    nb =  round(p*r)
    capa_per_ss.loc[ss, "Places Prim ss"] = nb

print(capa_per_ss)
capa_per_ss.to_csv('capa_per_ss_prim.csv')
capa_per_ss["SectorStatID2"]=capa_per_ss.index
#capa_per_ss.reset_index(inplace=True)

quart_limitrophes = pd.read_csv('limitrophe_quartiers.csv', sep=";")
quart_limitrophes.set_index("Territoire", inplace=True, drop=True)
print(quart_limitrophes) #Probleme d'accents


mat_limitrophes = pd.read_csv('prim_limitrophe_quartier.csv', sep=";") #TODO create file
mat_limitrophes.set_index("Territoire", inplace=True, drop=True)
print(mat_limitrophes)


communes = sectors_names_correspondance.Commune
communes.drop_duplicates(inplace=True)
print(communes)

#sectors_names_correspondance.set_index('Code', inplace=True, drop=True)
"""
sectors = places_mat.Code
places_mat.set_index('Code', inplace=True, drop=True)
"""
corres_quartier_ss = ratio
corres_quartier_ss.drop(columns=['nb_inscrits_ss', 'nb_inscrits_quart', 'ratio'], inplace=True)
#corres_quartier_ss.set_index('Quartier', inplace=True, drop=True)
print(corres_quartier_ss)

mat_lim =  pd.DataFrame(columns=colnames)

i = 0
for quart in nb_mat_quart_out.index:
    print(quart, "quart")
    nb_to_limitrophe = mat_limitrophes.loc[quart, "nb_child_vivant_quart_prim_lim"]
    if type(nb_to_limitrophe)==str:
        nb_to_limitrophe = nb_to_limitrophe.replace(",", ".")
    
    nb_to_limitrophe = round(float(nb_to_limitrophe))
    
    from_ss = corres_quartier_ss[corres_quartier_ss.Quartier == quart].index.tolist()

    possible_child = maternelles[maternelles.SectorStatID.isin(from_ss)]

    row_lim = quart_limitrophes.loc[quart]
    quart_to = []
    for r in row_lim.index:
        if row_lim.loc[r] == 1:
            quart_to.append(r)

    possible_ss_to = corres_quartier_ss[corres_quartier_ss.Quartier.isin(quart_to)]

    places_mat_poss = capa_per_ss.merge(possible_ss_to, how='inner')
    places_mat_poss = places_mat_poss[places_mat_poss["Places Prim ss"] > 0]
    places_mat_poss.drop_duplicates(inplace=True)

    possible_ss_to = places_mat_poss.SectorStatID2 #TODO check index has to be ss id
    places_mat_poss.set_index("SectorStatID2", inplace=True, drop=True)
    
    while nb_to_limitrophe > 0 and len(possible_child) > 0 and len(possible_ss_to) > 0:
        print(i, "i")
        elu = random.randrange(0, len(possible_child), 1)
        ind_elu = possible_child.index[elu]

        elu_ss = random.randrange(0, len(possible_ss_to), 1)
        ind_elu_ss = possible_ss_to.index[elu_ss]

        work_ss_id =  possible_ss_to.loc[ind_elu_ss] #closest_peri.loc[maternelles.loc[ind_elu, "SectorStatID"]]
        work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
        work_commune = sectors_names_correspondance.loc[work_ss_id, "Commune"]
        
        el = maternelles.loc[ind_elu].tolist()
        el.extend([work_ss_id, work_ss_name, work_commune])
        mat_lim.loc[i] = el

        possible_child.drop([ind_elu], inplace=True)
        maternelles.drop([ind_elu], inplace=True)

        places_mat_poss.loc[work_ss_id, "Places Prim ss"] = places_mat_poss.loc[work_ss_id, "Places Prim ss"] - 1
        places = places_mat_poss.loc[work_ss_id, "Places Prim ss"]
        if type(places)!= np.float64:
            places = places[0]
        capa_per_ss.loc[work_ss_id, "Places Prim ss"] = places

        if  places <=0:
            possible_ss_to.drop([ind_elu_ss], inplace=True)

        nb_to_limitrophe -=1
        i+=1



print(mat_lim)
mat_lim.to_csv('prim_limitrophe.csv')
print(capa_per_ss)
mat_workplace = pd.concat([mat_out, mat_lim], ignore_index = True)

from_to_commune = pd.read_csv("prim_com_flow.csv", sep=';')
from_to_commune.set_index('Origine (lieu de résidence)', inplace= True, drop=True)
print(from_to_commune) #TODO to check

colnames = maternelles.columns.tolist()
colnames.extend(["WorkSectorStatID", "WorkSectorStatName", "WorkCommuneName"])
mat_com =  pd.DataFrame(columns=colnames)
i = 0
for com in communes:
    print("com", com)
    for co in communes:
        nb_already = len(mat_workplace[(mat_workplace.Commune == com) & (mat_workplace.WorkCommuneName == co)])

        should = str(from_to_commune.loc[com, co])
        if "." in should: 
            should = should.replace(".", "")
        should = int(should)
        
        possible = maternelles[maternelles.Commune == com]

        if len(possible) >0:
            possible_ss_to = sectors_names_correspondance[sectors_names_correspondance.Commune == co]
            possible_ss_to.drop_duplicates(inplace=True)
            places_mat_poss = capa_per_ss.merge(possible_ss_to, how='inner', left_index = True, right_index=True)
            places_mat_poss.set_index("SectorStatID2", inplace=True, drop=True)
            places_mat_poss = places_mat_poss[places_mat_poss["Places Prim ss"] > 0]
            places_mat_poss.drop_duplicates(inplace=True)
            possible_ss = places_mat_poss.index #TODO check index has to be ss id

        else:
            possible_ss = pd.DataFrame()


        while nb_already < should and len(possible) > 0 and len(possible_ss) > 0:
            print("i", i)
            elu = random.randrange(0, len(possible), 1)
            ind_elu = possible.index[elu]

            elu_ss = random.randrange(0, len(possible_ss), 1)
            work_ss_id = possible_ss[elu_ss]

            #work_ss_id =  possible_ss.loc[ind_elu_ss] #closest_peri.loc[maternelles.loc[ind_elu, "SectorStatID"]]
            work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
            work_commune = sectors_names_correspondance.loc[work_ss_id, "Commune"]
            
            el = maternelles.loc[ind_elu].tolist()
            el.extend([work_ss_id, work_ss_name, work_commune])
            mat_com.loc[i] = el

            possible.drop([ind_elu], inplace=True)
            maternelles.drop([ind_elu], inplace=True)

            places_mat_poss.loc[work_ss_id, "Places Prim ss"] = places_mat_poss.loc[work_ss_id, "Places Prim ss"] - 1
            places = places_mat_poss.loc[work_ss_id, "Places Prim ss"]
            
            if type(places)!= np.float64:
                places = places[0]
            capa_per_ss.loc[work_ss_id, "Places Prim ss"] = places
            
            if places <=0:
                #possible_ss_to.drop([ind_elu_ss])
                possible_ss = possible_ss.drop([work_ss_id])
                if places < 0:
                    stop

            nb_already +=1
            i+=1

print(mat_com)
mat_com.to_csv("prim_commune.csv")

mat_plus = pd.DataFrame(columns=colnames)
"""
for ss in capa_per_ss.index:
    
    while len(maternelles) > 0 and 
"""
print(maternelles) #TODO check if empty ==> not empty donc alloue random

capa_per_ss = capa_per_ss[capa_per_ss["Places Prim ss"] > 0]
mat_random =  pd.DataFrame(columns=colnames)
i = 0
if not maternelles.empty and not capa_per_ss.empty:
    possibles_ss = capa_per_ss[capa_per_ss["Places Prim ss"] > 0]
    possibles_ss = possibles_ss.index
    
    while len(possibles_ss) > 0 and len(maternelles) > 0:
        
        ind = maternelles.index[0]
        elu_ss = random.randrange(0, len(possibles_ss), 1)
        work_ss_id = possibles_ss[elu_ss]
    
        work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
        work_commune = sectors_names_correspondance.loc[work_ss_id, "Commune"]
        
        el = maternelles.loc[ind].tolist()
        el.extend([work_ss_id, work_ss_name, work_commune])
        mat_random.loc[i] = el

        maternelles.drop([ind], inplace=True)

        capa_per_ss.loc[work_ss_id, "Places Prim ss"] = capa_per_ss.loc[work_ss_id, "Places Prim ss"] - 1
        places = capa_per_ss.loc[work_ss_id, "Places Prim ss"]
        
        if type(places)!= np.float64:
            places = places[0]
        capa_per_ss.loc[work_ss_id, "Places Prim ss"] = places
        
        possibles_ss = capa_per_ss[capa_per_ss["Places Prim ss"] > 0]
        possibles_ss = possibles_ss.index
        """
        if places <=0:
            #possible_ss_to.drop([ind_elu_ss])
            possible_ss = possible_ss.drop([work_ss_id])
            if places < 0:
                stop

        nb_already +=1
        """
        i+=1
        
print(mat_random)
print(maternelles) #TODO check empty

mat_workplace = pd.concat([mat_com, mat_workplace, mat_random], ignore_index=True)
print(mat_workplace)
mat_workplace.to_csv("primaires_workplace.csv")
        
print(capa_per_ss)
capa_per_ss.to_csv("prim_places_restantes_for_foreigners.csv")

#TODO use the same code for primaires and secondaires ==> sous forme de fonction avec fichiers en input