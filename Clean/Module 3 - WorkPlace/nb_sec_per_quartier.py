import pandas as pd

maternelles_1 = pd.read_csv('child_prim_en_avance_so_sec_workId.csv') #TODO add nema off correct file maybe needs merge
maternelles_2 = pd.read_csv('child_sec_secondaires_workId.csv')
prim_3 = pd.read_csv('ado_sec_workId.csv')
prim_4 = pd.read_csv('jeune_sec_en_retard_1_workId_v2.csv')
sec_5 = pd.read_csv('jeune_sec_en_retard_2_workId_v2.csv')

maternelles_1.drop(columns=['Code', "Commune"], inplace = True)
prim_3.drop(columns=['Unnamed: 0.1', "Commune", "Code"], inplace = True)
prim_4.drop(columns=['Code', "Commune"], inplace = True)
sec_5.drop(columns=['Code', "Commune"], inplace = True)
print(maternelles_1)
print(maternelles_2)
print(prim_3)
print(prim_4)
print(sec_5)

sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
#sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
print(sectors_names_correspondance)

maternelles = pd.concat([maternelles_1, maternelles_2, prim_3, prim_4, sec_5], ignore_index = True)
maternelles.drop(columns=["Unnamed: 0"], inplace=True)
maternelles = maternelles.merge(sectors_names_correspondance, left_on = "SectorStatID", right_index=True)
print(maternelles)

corr_ss_quart = pd.read_csv("correspondance_ss_quartiers.csv", sep=";")
print(corr_ss_quart)

maternelles = maternelles.merge(corr_ss_quart, left_on='SectorStatID', right_on="Code")
maternelles.to_csv('sec_workid_quartier.csv')

quartiers = maternelles.Quartier
quartiers.drop_duplicates(inplace=True)
print(quartiers)

nb_mat_quart = pd.DataFrame(columns=["Quartier", "Nb d'enfants inscrits en secondaires habitant le quartier"])
i=0
for quar in quartiers:
    print("quar", quar)
    mat_quart = maternelles[maternelles.Quartier == quar]
    nb_mat = len(mat_quart)
    nb_mat_quart.loc[i]=[quar, nb_mat]
    i+=1

print(nb_mat_quart)
nb_mat_quart.to_csv("nb_inscrits_sec_habitant_le_quartier.csv")

sectors = maternelles.SectorStatID
sectors.drop_duplicates(inplace=True)
print(sectors)

maternelles.set_index("SectorStatID", inplace=True, drop=True)

nb_mat_ss = pd.DataFrame(columns=["SectorStatID", "Nb d'enfants inscrits en secondaires habitant le ss"])
i=0
for ss in sectors:
    print("ss", ss)
    mat_ss = maternelles.loc[ss]
    nb_mat = len(mat_ss)
    nb_mat_ss.loc[i]=[ss, nb_mat]
    i+=1

print(nb_mat_ss)
nb_mat_ss.to_csv("nb_inscrits_sec_habitant_le_ss.csv")

communes = sectors_names_correspondance.Commune
communes.drop_duplicates(inplace=True)
print(communes)

nb_mat_com = pd.DataFrame(columns=["SectorStatID", "Nb d'enfants inscrits en secondaires habitant la com"])
i=0
for com in communes:
    print("com", com)
    mat_com = maternelles[maternelles.Commune_x == com]
    nb_mat = len(mat_com)
    nb_mat_com.loc[i]=[com, nb_mat]
    i+=1

print(nb_mat_com)
nb_mat_com.to_csv("nb_inscrits_sec_habitant_la_com.csv")
"""
maternelles_f = maternelles[maternelles.GenderID == 1]
maternelles_h = maternelles[maternelles.GenderID==0]
nb_mat_ss_f = pd.DataFrame(columns=["SectorStatID", "Nb de filles inscrites en secondaires habitant le ss"])
i=0
for ss in sectors:
    print("ss", ss)
    mat_ss = maternelles_f.loc[ss]
    nb_mat = len(mat_ss)
    nb_mat_ss_f.loc[i]=[ss, nb_mat]
    i+=1

print(nb_mat_ss_f)
nb_mat_ss_f.to_csv("nb_inscrites_f_sec_habitant_le_ss.csv")

nb_mat_ss_h = pd.DataFrame(columns=["SectorStatID", "Nb de garcons inscrits en secondaires habitant le ss"])
i=0
for ss in sectors:
    print("ss", ss)
    mat_ss = maternelles_h.loc[ss]
    nb_mat = len(mat_ss)
    nb_mat_ss_h.loc[i]=[ss, nb_mat]
    i+=1

print(nb_mat_ss_h)
nb_mat_ss_h.to_csv("nb_inscrits_h_sec_habitant_le_ss.csv")
"""
#TODO dans excel ==> rapport entre nb_mat_ss et nb_mat_quart
