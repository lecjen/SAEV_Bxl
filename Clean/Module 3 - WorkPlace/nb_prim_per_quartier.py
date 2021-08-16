import pandas as pd

maternelles_1 = pd.read_csv('child_mat_en_avance_so_prim_workId.csv') #TODO add nema off correct file maybe needs merge
maternelles_2 = pd.read_csv('child_prim_primaires_workId.csv')
prim_3 = pd.read_csv('child_sec_en_retard_1_workId.csv')
prim_4 = pd.read_csv('child_sec_en_retard_2_workId.csv')

maternelles_1.drop(columns=['Code', "Commune"], inplace = True)
maternelles_2.drop(columns=['Code', "Commune"], inplace = True)
print(maternelles_1)
print(maternelles_2)
print(prim_3)
print(prim_4)
maternelles = pd.concat([maternelles_1, maternelles_2, prim_3, prim_4], ignore_index = True)
maternelles.drop(columns=["Unnamed: 0"], inplace=True)
print(maternelles)

corr_ss_quart = pd.read_csv("correspondance_ss_quartiers.csv", sep=";")
print(corr_ss_quart)

maternelles = maternelles.merge(corr_ss_quart, left_on='SectorStatID', right_on="Code")
maternelles.to_csv('prim_workid_quartier.csv')

quartiers = maternelles.Quartier
quartiers.drop_duplicates(inplace=True)
print(quartiers)

nb_mat_quart = pd.DataFrame(columns=["Quartier", "Nb d'enfants inscrits en primaires habitant le quartier"])
i=0
for quar in quartiers:
    print("quar", quar)
    mat_quart = maternelles[maternelles.Quartier == quar]
    nb_mat = len(mat_quart)
    nb_mat_quart.loc[i]=[quar, nb_mat]
    i+=1

print(nb_mat_quart)
nb_mat_quart.to_csv("nb_inscrits_prim_habitant_le_quartier.csv")

sectors = maternelles.SectorStatID
sectors.drop_duplicates(inplace=True)
print(sectors)

maternelles.set_index("SectorStatID", inplace=True, drop=True)

nb_mat_ss = pd.DataFrame(columns=["SectorStatID", "Nb d'enfants inscrits en primaires habitant le ss"])
i=0
for ss in sectors:
    print("ss", ss)
    mat_ss = maternelles.loc[ss]
    nb_mat = len(mat_ss)
    nb_mat_ss.loc[i]=[ss, nb_mat]
    i+=1

print(nb_mat_ss)
nb_mat_ss.to_csv("nb_inscrits_prim_habitant_le_ss.csv")

#TODO dans excel ==> rapport entre nb_mat_ss et nb_mat_quart
