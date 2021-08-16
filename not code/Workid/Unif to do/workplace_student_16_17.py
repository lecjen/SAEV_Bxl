import pandas as pd
import random

sec = pd.read_csv('child_sec_en_avance_so_unif_workId.csv')
sec.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)
print(sec)

closest_peri = pd.read_csv("closest_ss_peri_v2.csv")
closest_peri.set_index('SectorStatID', inplace=True, drop=True)
print(closest_peri) #TODO check unnamed and index (should be ss id)

sectors_names_correspondance = pd.read_csv('sector_stat.csv', sep=';')
#sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
print(sectors_names_correspondance)


communes = sectors_names_correspondance.Commune
communes.drop_duplicates(inplace=True)
print(communes)
campus = pd.read_csv("sup_campus_bxl_fr_with_ss_v2.csv")

print(campus.columns)

ss = pd.DataFrame()
ss['SectorStat'] = campus.sector_stat
ss.drop_duplicates(inplace=True)
print(ss)

ss = ss.merge(sectors_names_correspondance, left_on="SectorStat", right_on="Code", how='inner')
ss.drop(columns=["Code"], inplace=True)
print(ss)
ss.to_csv('campus_fr_ss_commune.csv')
communes = ss.Commune
sectors_names_correspondance.set_index("Code", inplace=True, drop=True)

colnames = sec.columns.tolist()
colnames.extend(["WorkSectorStatID", "WorkSectorStatName"])
students = pd.DataFrame(columns=colnames)

#etudiants from bxl to out bxl fr
sup_fr_trajets_hors_bxl = pd.read_csv('sup_fr_trajets_to_hors_bxl.csv', sep=';')
i = 0
for age in range(16, 18):
    print("age bxl out bxl fr", age)
    sup_fr_trajets_hors_bxl_age = sup_fr_trajets_hors_bxl[sup_fr_trajets_hors_bxl.Age == age]

    sup_fr_trajets_hors_bxl_age_fe = sup_fr_trajets_hors_bxl_age[sup_fr_trajets_hors_bxl_age.Sexe == "Femme"]
    sup_fr_trajets_hors_bxl_age_ho = sup_fr_trajets_hors_bxl_age[sup_fr_trajets_hors_bxl_age.Sexe == "Homme"]

    for com in communes:
        if com == 'Saint-Josse-ten-Noode':
            com = 'Saint-Josse-Ten-Noode'
        print("com", com)
        nb_to_allocate_fe = sup_fr_trajets_hors_bxl_age_fe[sup_fr_trajets_hors_bxl_age_fe["Commune_from"]==com]
        nb_to_allocate_fe.reset_index(inplace=True)
        
        if not nb_to_allocate_fe.empty:
            
            nb_to_allocate_fe= nb_to_allocate_fe.loc[0,"Sum of Compte"]
            print(nb_to_allocate_fe) #TODO verifier not null because of majuscules
            possible_fe = sec[(sec.GenderID == 1) & (sec.Commune == com) & (sec.Age == age) & (sec.WorkerID != 4)]
            print(possible_fe)  #TODO verifier not null because of majuscules
            
            
            while nb_to_allocate_fe > 0 and len(possible_fe)>0:
                print("i com bxl out bxl fr", i)
                elu = random.randrange(0, len(possible_fe), 1)
                ind_elu = possible_fe.index[elu]
    
                work_ss_id = closest_peri.loc[sec.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
                work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
                
                el = possible_fe.loc[ind_elu].tolist()
                el.extend([work_ss_id, work_ss_name])
                students.loc[i] = el
                students.loc[i, "WorkerID"]=5
                students.loc[i, "WorkerType"]="Unif off campus"
    
                possible_fe.drop([ind_elu], inplace=True)
                sec.drop([ind_elu], inplace=True)
    
                nb_to_allocate_fe-=1
                i+=1

        nb_to_allocate_ho = sup_fr_trajets_hors_bxl_age_ho[sup_fr_trajets_hors_bxl_age_ho["Commune_from"]==com]
        nb_to_allocate_ho.reset_index(inplace=True)
        if not nb_to_allocate_ho.empty:
        
            nb_to_allocate_ho= nb_to_allocate_ho.loc[0,"Sum of Compte"]
            print(nb_to_allocate_ho) #TODO verifier not null because of majuscules
            possible_ho = sec[(sec.GenderID == 0) & (sec.Commune == com) & (sec.Age == age) & (sec.WorkerID != 4)]
    
            while nb_to_allocate_ho > 0 and len(possible_ho)>0:
                print("i com bxl out bxl fr g", i)
                elu = random.randrange(0, len(possible_ho), 1)
                ind_elu = possible_ho.index[elu]
    
                work_ss_id = closest_peri.loc[sec.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
                work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
                
                el = possible_ho.loc[ind_elu].tolist()
                el.extend([work_ss_id, work_ss_name])
                students.loc[i] = el
                students.loc[i, "WorkerID"]=5
                students.loc[i, "WorkerType"]="Unif off campus"
                
                possible_ho.drop([ind_elu], inplace=True)
                sec.drop([ind_elu], inplace=True)
    
                nb_to_allocate_ho-=1
                i+=1


#etudiant from bxl to bxl fr
dic = dict()
for com in communes:
    list_ss = ss[ss.Commune == com].SectorStat.tolist()
    dic[com]=list_ss #len(ss[ss.Commune==com])
    
print(dic)

age_min = 16
age_max = 17
unif_fr = pd.read_csv("unif_fr_bxl_to_bxl.csv", sep=';')
print(unif_fr)

for ind in unif_fr.index:
    print("ind", ind)
    if unif_fr.loc[ind, "Sexe"] == "Femme":
        sex = 1
    elif unif_fr.loc[ind, "Sexe"] == "Homme":
        sex = 0
    else:
        errorsex
    
    age = unif_fr.loc[ind, "Age"]
    if age >= age_min and age<= age_max:
        possible = sec[(sec.GenderID == sex) & (sec.Age == age) &
                                 (sec.Commune == unif_fr.loc[ind, "Commune_from"])]
        
        nb = unif_fr.loc[ind, "Sum of Compte"]
        
        com_to = unif_fr.loc[ind, "Commune_to"]
        list_ss_to = dic[com_to]
        nb_per_ss = round(nb/len(list_ss_to))
        reste = nb%len(list_ss_to)
        first_ss = True
        
        for ss in list_ss_to:
            print("ss", ss)
            if first_ss:
                nb_per_ss_tmp = nb_per_ss + reste
                first_ss = False
            else:
                nb_per_ss_tmp = nb_per_ss
                
            while nb_per_ss_tmp > 0 and len(possible) > 0:
                print("i ss", i)
                elu = random.randrange(0, len(possible), 1)
                ind_elu = possible.index[elu]
                
                el = possible.loc[ind_elu].tolist()
                
                hh_type_id = possible.loc[ind_elu, "HouseholdTypeID"]
                
                if hh_type_id == 3 or hh_type_id == 5:
                    ss_home = possible.loc[ind_elu, "SectorStatID"]
                    
                    if ss_home == ss:
                        work_id = 4
                        work_type = "Unif on campus"
                    else:
                        work_id = 5
                        work_type = "Unif off campus"
                else:
                    work_id = 5
                    work_type = "Unif off campus"                    
                
                work_ss_name = sectors_names_correspondance.loc[ss, "Name"]
                el.extend([ss, work_ss_name])
                students.loc[i]=el
                students.loc[i, "WorkerID"]=work_id
                students.loc[i, "WorkerType"]= work_type
                
                possible.drop([ind_elu], inplace=True)
                sec.drop([ind_elu], inplace = True)
                
                nb_per_ss_tmp -=1
                i+=1

print(students)
#students.to_csv("student_fr_bxl_bxl_18_20_workplace_v2.csv")     


#error 28 places while 243 pers
#alloue les autres randomly
for pers in sec.index:
    elu = random.randrange(0, len(sectors_names_correspondance), 1)
    ss = sectors_names_correspondance.index[elu]
    work_ss_name = sectors_names_correspondance.loc[ss, "Name"]
    
    el = sec.loc[pers].tolist()
    el.extend([ss, work_ss_name])
    students.loc[i]=el
    students.loc[i, "WorkerID"]=work_id
    students.loc[i, "WorkerType"]= work_type
                
    i+=1
    
print(students)
students.to_csv("students_16_17_unif_workplace_v2.csv")