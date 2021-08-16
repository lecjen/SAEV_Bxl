import pandas as pd

colnames = ["SectorStatID", "SectorStatName", "PersID", "Age", "GenderID", "GenderName", "HouseholdID", "HouseholdTypeID", "HouseholdTypeName", "WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"]

student = pd.DataFrame(columns=colnames)

unif_fr = pd.read_csv('unif_fr_hors_bxl_to_bxl_v2.csv', sep=";")
#unif_fr.set_index("Libellé commune de l'implantation", inplace = True, drop = True)
print(unif_fr)

closest_peri = pd.read_csv('closest_ss_peri_v2.csv')
closest_peri.set_index("SectorStatID", inplace=True, drop=True)
print(closest_peri)

ss_names = pd.read_csv('sector_stat.csv', sep=";")
ss_names.set_index("Code", inplace=True, drop=True)
print(ss_names)

#etudiant from bxl to bxl fr
ss = pd.read_csv('campus_fr_ss_commune.csv')
ss.drop(columns=["Unnamed: 0"], inplace=True)
#ss.set_index("SectorStat", inplace=True, drop=True)
print(ss)

communes = ss.Commune

dic = dict()
for com in communes:
    list_ss = ss[ss.Commune == com].SectorStat.tolist()
    dic[com]=list_ss #len(ss[ss.Commune==com])

print(dic)


i=0
for ind in unif_fr.index:
    print("ind", ind)
    if unif_fr.loc[ind, "Sexe"] == "Femme":
        sex = 1
    elif unif_fr.loc[ind, "Sexe"] == "Homme":
        sex = 0
    else:
        errorsex

    if sex == 0:
        gender_name = 'male'
    elif sex == 1:
        gender_name = 'female'
    else:
        errorSexName

    age = unif_fr.loc[ind, "Age"]
    nb = unif_fr.loc[ind, "Sum of Compte"]

    com_to = unif_fr.loc[ind, "Commune"]
    list_ss_to = dic[com_to]
    nb_per_ss = round(nb/len(list_ss_to))
    reste = nb%len(list_ss_to)
    first_ss = True

    for ss in list_ss_to:
        print("ss", ss)

        ss_from_id = closest_peri.loc[ss]
        if type(ss_from_id)!=str:
            ss_from_id = ss_from_id[0]
        
        ss_from_name = ss_names.loc[ss_from_id, "Name"]

        ss_to_name = ss_names.loc[ss, "Name"]

        if first_ss:
            nb_per_ss_tmp = nb_per_ss + reste
            first_ss = False
        else:
            nb_per_ss_tmp = nb_per_ss

        while nb_per_ss_tmp > 0:
            print("i", i)
            student.loc[i]=[ss_from_id, ss_from_name, i, "Useless for non resident but "+str(age), "Useless for non resident but "+str(gender_name), "Useless for non resident", "Useless for non resident", "Useless for non resident", "Useless for non resident", 5, "Unif off campus", ss, ss_to_name]

            nb_per_ss_tmp -=1
            i+=1

print(student)
student.to_csv("foreign_student_workplace.csv")