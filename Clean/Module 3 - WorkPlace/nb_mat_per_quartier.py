import pandas as pd

maternelles = pd.read_csv('child_mat_maternelles_workId.csv') #TODO add nema off correct file maybe needs merge
#maternelles_2 = pd.read_csv('child_prim_en_retard_workId.csv')
#print(maternelles_1)
#print(maternelles_2)
#maternelles = pd.concat([maternelles_1, maternelles_2], ignore_index = True)
maternelles.drop(columns=["Unnamed: 0"], inplace=True)
print(maternelles)

corr_ss_quart = pd.read_csv("correspondance_ss_quartiers.csv", sep=";")
print(corr_ss_quart)

maternelles = maternelles.merge(corr_ss_quart, left_on='SectorStatID', right_on="Code")
maternelles.to_csv('mat_workid_quartier.csv')

quartiers = maternelles.Quartier
quartiers.drop_duplicates(inplace=True)
print(quartiers)

nb_mat_quart = pd.DataFrame(columns=["Quartier", "Nb d'enfants inscrits en maternelles habitant le quartier"])
i=0
for quar in quartiers:
    print("quar", quar)
    mat_quart = maternelles[maternelles.Quartier == quar]
    nb_mat = len(mat_quart)
    nb_mat_quart.loc[i]=[quar, nb_mat]
    i+=1

print(nb_mat_quart)
nb_mat_quart.to_csv("nb_inscrits_mat_habitant_le_quartier.csv")


sectors = maternelles.SectorStatID
sectors.drop_duplicates(inplace=True)
print(sectors)

maternelles.set_index("SectorStatID", inplace=True, drop=True)

nb_mat_ss = pd.DataFrame(columns=["SectorStatID", "Nb d'enfants inscrits en maternelles habitant le ss"])
i=0
for ss in sectors:
    print("ss", ss)
    mat_ss = maternelles.loc[ss]
    nb_mat = len(mat_ss)
    nb_mat_ss.loc[i]=[ss, nb_mat]
    i+=1

print(nb_mat_ss)
nb_mat_ss.to_csv("nb_inscrits_mat_habitant_le_ss.csv")

#TODO dans excel ==> rapport entre nb_mat_ss et nb_mat_quart
