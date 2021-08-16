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

all_hh = pd.read_csv('all_hh_child_Reallocated.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace=True)
print(all_hh)

sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
print(sectors_names_correspondance)


all_hh = all_hh.merge(sectors_names_correspondance, left_on="SectorStatID", right_on="Code")
print(all_hh)

sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)

communes = all_hh['Commune']
communes.drop_duplicates(inplace=True)
print(communes)


jeune = all_hh[(all_hh.Age > 17) & (all_hh.Age < 21)]
print(jeune.ChildOrParent)
jeune_parents = jeune[(jeune.ChildOrParent == "parent")]
jeune_parents = jeune_parents[(jeune_parents.HouseholdTypeID == 4)]
print(jeune_parents)


jeune_parents['WorkerID']=6
jeune_parents['WorkerType']="Worker"

print(jeune_parents)
jeune_parents.to_csv("18_20_jeune_parent_worker_workId.csv")

jeune_student = jeune[(jeune.ChildOrParent == "child")]
jeune_student = jeune_student[(jeune.HouseholdTypeID == 1) | (jeune.HouseholdTypeID == 4)]
print(jeune_student)

avance_retard = pd.read_csv('avance_retard_scolaire.csv', sep=";")
avance_retard.set_index('Code', inplace=True, drop=True)
print(avance_retard)

sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)
print(sectors)


#En retard d'un an: 18ans mais encore en secondaires
colnames = jeune_student.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
en_retard_1 = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for s in sectors:
    print('s', s)
    possible = jeune_student[(jeune_student.GenderID == 0) & (jeune_student.SectorStatID == s) & (jeune_student.Age == 18)]

    nb_retard_str = avance_retard.loc[s, "#18 ans en secondaires garçon"]
    
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))

    while nb_retard > 0 and len(possible) > 0:
        print('i', i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        
        el = possible.loc[ind_elu].tolist()
        el.extend(["3", "Secondaires"])
        en_retard_1.loc[i] = el
        
        possible.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

#Filles
for s in sectors:
    print("s f", s)
    possible = jeune_student[(jeune_student.GenderID == 1) & (jeune_student.SectorStatID == s) & (jeune_student.Age == 18)]
    nb_retard_str = avance_retard.loc[s, "#18 ans en secondaires filles"]
    
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0 and len(possible) > 0:
        print("i f", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["3", "Secondaires"])
        en_retard_1.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

print(en_retard_1)
en_retard_1.to_csv("jeune_sec_en_retard_1_workId.csv")

#En retard de 2 ans: 19ans mais encore en secondaires
en_retard_2 = pd.DataFrame(columns=colnames)

#Garcons
i = 0
for s in sectors:
    print("s r", s)
    possible = jeune_student[(jeune_student.GenderID == 0) & (jeune_student.SectorStatID == s) & (jeune_student.Age == 19)]
    
    nb_retard_str = avance_retard.loc[s, "#19 ans en secondaires garçon"]
    
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0 and len(possible) > 0:
        print("i r", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["3", "Secondaires"])
        en_retard_2.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

#Filles
for s in sectors:
    print("s r f", s)
    possible = jeune_student[(jeune_student.GenderID == 1) & (jeune_student.SectorStatID == s) & (jeune_student.Age == 19)]
    nb_retard_str = avance_retard.loc[s, "#19 ans en secondaires filles"]
    
    if type(nb_retard_str) == str:
        nb_retard_str = nb_retard_str.replace(",", ".")
    
    nb_retard = round(float(nb_retard_str))
    while nb_retard > 0 and len(possible) > 0:
        print("i r f", i)
        elu = random.randrange(0, len(possible), 1)
        ind_elu = possible.index[elu]
        el = possible.loc[ind_elu].tolist()
        el.extend(["3", "Secondaires"])
        en_retard_2.loc[i] = el
        possible.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)
        nb_retard-=1
        i+=1

print(en_retard_2)
en_retard_2.to_csv("jeune_sec_en_retard_2_workId.csv")

"""
jeune_student['WorkerID']=5
jeune_student['WorkerType']="Unif off campus"
"""
jeune_student_alone = jeune[(jeune.ChildOrParent == "parent")]
jeune_student_alone = jeune_student_alone[(jeune_student_alone.HouseholdTypeID == 1) | (jeune_student_alone.HouseholdTypeID == 2) |
                                          (jeune_student_alone.HouseholdTypeID == 3) | (jeune_student_alone.HouseholdTypeID == 5)]

jeune_student = pd.concat([jeune_student_alone, jeune_student], ignore_index = True)


#Etudiants from bxl to bxl nl
nb_student_nl = pd.read_csv("sup_nl_bxl_to_bxl.csv", sep=";")
print(nb_student_nl)

students_nl = pd.DataFrame(columns=colnames)
students_nl_off_or_on_campus_to_check = pd.DataFrame(columns=colnames)

i = 0
for age in range(18, 21):
    print("age", age)
    nb_student_nl_age = nb_student_nl[nb_student_nl.Age == age]

    nb_student_nl_age_fe = int(nb_student_nl_age.loc[:, "Fe"])
    nb_student_nl_age_ho = int(nb_student_nl_age.loc[:, "Ho"])

    possible_fe  = jeune_student[(jeune_student.Age == age) & (jeune_student.GenderID == 1)]
    possible_ho  = jeune_student[(jeune_student.Age == age) & (jeune_student.GenderID == 0)]

    while nb_student_nl_age_fe > 0:
        print("age i", i)
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]

        hh_id = jeune_student.loc[ind_elu, "HouseholdTypeID"]
        
        el = possible_fe.loc[ind_elu].tolist()

        if hh_id == 1 or hh_id == 2 or hh_id == 3 or hh_id == 4:
            el.extend([5, "Unif off campus"])
            students_nl.loc[i] = el

        elif hh_id == 5:
            el.extend(["4 or 5", "Unif on or off campus"])
            students_nl_off_or_on_campus_to_check.loc[i] = el #jeune_student.loc[ind_elu],"4 or 5", "Unif on or off campus"]
            #TODO check whether same ss unif and logement
        else:
            error

        possible_fe.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_student_nl_age_fe-=1
        i+=1

    while nb_student_nl_age_ho > 0:
        print("age i g", i)
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        hh_id = jeune_student.loc[ind_elu, "HouseholdTypeID"]
        
        el = possible_ho.loc[ind_elu].tolist()

        if hh_id == 1 or hh_id == 2 or hh_id == 3 or hh_id == 4:
            el.extend([5, "Unif off campus"])
            students_nl.loc[i] = el

        elif hh_id == 5:
            el.extend(["4 or 5", "Unif on or off campus"])
            students_nl_off_or_on_campus_to_check.loc[i] = el
            #TODO check whether same ss unif and logement
        else:
            error

        possible_ho.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_student_nl_age_ho-=1
        i+=1

print(students_nl)
students_nl.to_csv("student_18_20_nl_workid.csv")

print(students_nl_off_or_on_campus_to_check)
students_nl_off_or_on_campus_to_check.to_csv("student_18_20_nl_workid_4_or_5_to_check.csv")


#Etudiants from bxl to out bxl nl
nb_student_nl_out = pd.read_csv("sup_nl_bxl_to_out_bxl.csv", sep=";")
print(nb_student_nl_out)

closest_peri = pd.read_csv("closest_ss_peri_v2.csv")
closest_peri.set_index('SectorStatID', inplace=True, drop=True)
print(closest_peri) #TODO check unnamed and index (should be ss id)


sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
#sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
print(sectors_names_correspondance)

communes = sectors_names_correspondance.Commune
communes.drop_duplicates(inplace=True)
print(communes)

jeune_student = jeune_student.merge(sectors_names_correspondance, how='inner', left_on='SectorStatID', right_on='Code')
print(jeune_student)

sectors_names_correspondance.set_index("Code", inplace=True, drop=True)

colnames = jeune_student.columns.tolist()
colnames.extend(["WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"])
students_nl_out = pd.DataFrame(columns=colnames)

i = 0
for age in range(18, 21):
    print("age g bxl out bxl", age)
    nb_student_nl_out_age = nb_student_nl_out[nb_student_nl_out.Age == age]

    nb_student_nl_out_age_fe = int(nb_student_nl_out_age.loc[:, "Fe"])
    nb_student_nl_out_age_ho = int(nb_student_nl_out_age.loc[:, "Ho"])

    possible_fe  = jeune_student[(jeune_student.Age == age) & (jeune_student.GenderID == 1)]
    possible_ho  = jeune_student[(jeune_student.Age == age) & (jeune_student.GenderID == 0)]

    while nb_student_nl_out_age_fe > 0 and len(possible_fe) > 0:
        print("i g bxl out bxl", i)
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]
        
        el = possible_fe.loc[ind_elu].tolist()

        work_ss_id = closest_peri.loc[jeune_student.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
        work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
        
        el.extend([ 5, "Unif off campus", work_ss_id, work_ss_name])
        students_nl_out.loc[i] = el

        possible_fe.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_student_nl_out_age_fe-=1
        i+=1

    while nb_student_nl_out_age_ho > 0 and len(possible_ho) > 0:
        print("i g bxl out bxl g", i)
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        el = possible_ho.loc[ind_elu].tolist()
        
        work_ss_id = closest_peri.loc[jeune_student.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
        work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
        
        el.extend([ 5, "Unif off campus", work_ss_id, work_ss_name])
        students_nl_out.loc[i] = el

        possible_ho.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_student_nl_out_age_ho-=1
        i+=1

print(students_nl_out)
students_nl_out.to_csv("student_18_20_nl_to_out_workplace.csv")



#etudiant from bxl to bxl fr
campus = pd.read_csv("sup_campus_bxl_fr_with_ss_v2.csv")

print(campus.columns)

ss = pd.DataFrame()
ss['SectorStat'] = campus.sector_stat
ss.drop_duplicates(inplace=True)
print(ss)

sectors_names_correspondance = pd.read_csv('sector_stat.csv', sep=';')
#sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
print(sectors_names_correspondance)


ss = ss.merge(sectors_names_correspondance, left_on="SectorStat", right_on="Code", how='inner')
ss.drop(columns=["Code"], inplace=True)
print(ss)
ss.to_csv('campus_fr_ss_commune.csv')
communes = ss.Commune
sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
dic = dict()
for com in communes:
    list_ss = ss[ss.Commune == com].SectorStat.tolist()
    dic[com]=list_ss #len(ss[ss.Commune==com])
    
print(dic)

colnames = jeune_student.columns.tolist()
colnames.extend(["WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"])
students = pd.DataFrame(columns=colnames)

age_min = 18
age_max = 20
unif_fr = pd.read_csv("unif_fr_bxl_to_bxl.csv", sep=';')
print(unif_fr)
i=0
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
        possible = jeune_student[(jeune_student.GenderID == sex) & (jeune_student.Age == age) &
                                 (jeune_student.Commune_x == unif_fr.loc[ind, "Commune_from"])]
        
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
                
                work_ss_name = sectors_names_correspondance.loc[ss]
                el.extend([work_id, work_type, ss, work_ss_name])
                students.loc[i]=el
                
                possible.drop([ind_elu], inplace=True)
                jeune_student.drop([ind_elu], inplace = True)
                
                nb_per_ss_tmp -=1
                i+=1

print(students)
students.to_csv("student_fr_bxl_bxl_18_20_workplace.csv")                     
    
"""
sup_fr_trajets = pd.read_csv('superieur_fr_trajets.csv', sep=';')
sup_fr_trajets = sup_fr_trajets[(sup_fr_trajets["Bxl / hors bxl logement"]== "Brussels")]

for age in range(18, 21):
    sup_fr_trajets = sup_fr_trajets[sup_fr_trajets.Age == age]


    for com in communes:
        possible = sup_fr_trajets[sup_fr_trajets.Commune == com]

        hh_id = jeune_student.loc[ind_elu, "HouseholdTypeID"]
        if hh_id == 1 or hh_id == 2 or hh_id == 3:
            work_id = 5
            work_name = "Unif off campus"
        elif hh_id == 5:
"""

#etudiants from bxl to out bxl fr
sup_fr_trajets_hors_bxl = pd.read_csv('sup_fr_trajets_to_hors_bxl.csv', sep=';')

for age in range(18, 21):
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
            possible_fe = jeune_student[(jeune_student.GenderID == 1) & (jeune_student.Commune_y == com) & (jeune_student.Age == age)]
            print(possible_fe)  #TODO verifier not null because of majuscules
            
            
            while nb_to_allocate_fe > 0 and len(possible_fe)>0:
                print("i com bxl out bxl fr", i)
                elu = random.randrange(0, len(possible_fe), 1)
                ind_elu = possible_fe.index[elu]
    
                work_ss_id = closest_peri.loc[jeune_student.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
                work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
                
                el = possible_fe.loc[ind_elu].tolist()
                el.extend([5, "Unif off campus", work_ss_id, work_ss_name])
                students.loc[i] = el
    
                possible_fe.drop([ind_elu], inplace=True)
                jeune_student.drop([ind_elu], inplace=True)
    
                nb_to_allocate_fe-=1
                i+=1

        nb_to_allocate_ho = sup_fr_trajets_hors_bxl_age_ho[sup_fr_trajets_hors_bxl_age_ho["Commune_from"]==com]
        nb_to_allocate_ho.reset_index(inplace=True)
        if not nb_to_allocate_ho.empty:
        
            nb_to_allocate_ho= nb_to_allocate_ho.loc[0,"Sum of Compte"]
            print(nb_to_allocate_ho) #TODO verifier not null because of majuscules
            possible_ho = jeune_student[(jeune_student.GenderID == 0) & (jeune_student.Commune_y == com) & (jeune_student.Age == age)]
    
            while nb_to_allocate_ho > 0 and len(possible_ho)>0:
                print("i com bxl out bxl fr g", i)
                elu = random.randrange(0, len(possible_ho), 1)
                ind_elu = possible_ho.index[elu]
    
                work_ss_id = closest_peri.loc[jeune_student.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
                work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
                
                el = possible_ho.loc[ind_elu].tolist()
                el.extend([5, "Unif off campus", work_ss_id, work_ss_name])
                students.loc[i] = el
    
                possible_ho.drop([ind_elu], inplace=True)
                jeune_student.drop([ind_elu], inplace=True)
    
                nb_to_allocate_ho-=1
                i+=1

print(students)
students.to_csv("students_18_20_unif_workplace.csv")

#Jeune at home
colnames = jeune_student.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
jeune_at_home = pd.DataFrame(columns=colnames)

jeune_student_fe = jeune_student[jeune_student.GenderID == 1]
jeune_student_fe_18_19 = jeune_student_fe[(jeune_student_fe.Age == 18) | (jeune_student_fe.Age == 19)]

to_allocate_fe = {"Anderlecht":2, "Evere":1, "Forest":1, "Ganshoren":1, "Jette":1, "Uccle":1} #From activites home fe pivot

i=0
for com in to_allocate_fe.keys():
    print("com home", com)
    nb_to_allocate_fe = to_allocate_fe[com]
    possible_fe = jeune_student_fe_18_19[jeune_student_fe_18_19.Commune_y == com]

    while nb_to_allocate_fe > 0 and len(possible_fe) > 0:
        print("com home i", i)
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]

        el = possible_fe.loc[ind_elu].tolist()
        el.extend([7, "StayHome"])
        jeune_at_home.loc[i] = el

        possible_fe.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_to_allocate_fe-=1
        i+=1

jeune_student_ho = jeune_student[jeune_student.GenderID == 0]
jeune_student_ho_18_19 = jeune_student_ho[(jeune_student_ho.Age == 18) | (jeune_student_ho.Age == 19)]

to_allocate_ho = {"Anderlecht":53, "Bruxelles":4, "Forest":1, "Ganshoren":1, "Saint-Josse-ten-Noode":3, "Schaerbeek":3, "Molenbeek Saint-Jean":4}

for com in to_allocate_ho.keys():
    print("com home g", com)
    nb_to_allocate_ho = to_allocate_ho[com]
    possible_ho = jeune_student_ho_18_19[jeune_student_ho_18_19.Commune_y == com]

    while nb_to_allocate_ho > 0 and len(possible_ho) > 0:
        print("com home g i", i)
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        el = possible_ho.loc[ind_elu].tolist()
        el.extend([7, "StayHome"])
        jeune_at_home.loc[i] = el

        possible_ho.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_to_allocate_ho-=1
        i+=1


jeune_student_fe = jeune_student[jeune_student.GenderID == 1]
jeune_student_fe_20 = jeune_student_fe[(jeune_student_fe.Age == 20)]

to_allocate_fe = {"Anderlecht":30, "Auderghem": 3, "Bruxelles":44, "Etterbeek":4, "Evere":15, "Forest":11, "Ganshoren":7, "Ixelles":10, "Jette":11,
                  "Koekelberg": 5, "Saint-Gilles": 7, "Saint-Josse-ten-Noode":10, "Schaerbeek":31, "Uccle": 7, "Watermael-Boitsfort": 4,
                  "Berchem Sainte-Agathe": 4, "Molenbeek Saint-Jean":32, "Woluwe Saint-Lambert":4, "Woluwe Saint-Pierre": 3}

for com in to_allocate_fe.keys():
    print("com home 20:", com)
    nb_to_allocate_fe = to_allocate_fe[com]
    possible_fe = jeune_student_fe_20[jeune_student_fe_20.Commune_y == com]

    while nb_to_allocate_fe > 0 and len(possible_fe) > 0:
        print("com home 20 i", i)
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]
        
        el = possible_fe.loc[ind_elu].tolist()
        el.extend([7, "StayHome"])
        jeune_at_home.loc[i] = el

        possible_fe.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_to_allocate_fe-=1
        i+=1

jeune_student_ho = jeune_student[jeune_student.GenderID == 0]
jeune_student_ho_20 = jeune_student_ho[(jeune_student_ho.Age == 20)]

to_allocate_ho = {"Anderlecht":36, "Auderghem": 4, "Bruxelles":62, "Etterbeek":5, "Evere":9, "Forest":11, "Ganshoren":6, "Ixelles":14, "Jette":18,
                  "Koekelberg": 8, "Saint-Gilles": 14, "Saint-Josse-ten-Noode":10, "Schaerbeek":40, "Uccle": 11, "Watermael-Boitsfort": 4,
                  "Berchem Sainte-Agathe": 6, "Molenbeek Saint-Jean":30, "Woluwe Saint-Lambert":6, "Woluwe Saint-Pierre": 3}


for com in to_allocate_ho.keys():
    print("com home 20 g :", com)
    nb_to_allocate_ho = to_allocate_ho[com]
    possible_ho = jeune_student_ho_20[jeune_student_ho_20.Commune_y == com]

    while nb_to_allocate_ho > 0 and len(possible_ho) > 0:
        print("com home 20 i g", i)
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        el = possible_ho.loc[ind_elu].tolist()
        el.extend([7, "StayHome"])
        jeune_at_home.loc[i] = el

        possible_ho.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_to_allocate_ho-=1
        i+=1

print(jeune_at_home)
jeune_at_home.to_csv("jeune_at_home_workId.csv")

jeune_student["WorkID"]=6
jeune_student["WorkType"]="Worker"

print(jeune_student)
jeune_student.to_csv("jeune_wroker_workId.csv")


"""
ado_hopital = pd.DataFrame(columns=colnames)

place_hopital = 401 #- somme des places pediatrie utilisées
"""
jeune_collectif = jeune[jeune.HouseholdTypeID == 6]
print(jeune_collectif)
jeune_collectif.to_csv("jeune_collectif_hopi_or_prison.csv")
"""
i = 0
while len(ado_collectif) > 0 and place_hopital > 0 :
    elu = random.randrange(0, len(ado_collectif), 1)
    ind_elu = ado_collectif.index[elu]

    ado_hopital.loc[i] = [ado_collectif.loc[ind_elu], "10", "Hospital"]

    ado_collectif.drop([ind_elu], inplace=True)
    place_hopital-=1
    i+=1

print(ado_hopital)
ado_hopital.to_csv("ado_16_17_hopital_workid.csv")

ado_collectif["WorkID"]=9
ado_collectif["WorkType"]="Prison"

print(ado_collectif)
ado_collectif.to_csv("ado_16_17_prison_workid.csv")
#TODO hh_id 9 prison or hopital

for others years

act_home_fe = pd.read_csv("activite_home_fe.csv")
print(act_home_fe)

act_home_fe= act_home_fe["20"]
act_home_fe.set_index("Code", inplace=True, drop=True)

for ss in sectors:

    nb_act_home_fe = round(act_home_fe.loc[ss])
    possible_act_home_fe = jeune_student_fe_20[jeune_student_fe_20.SectorStatID == ss]

    while nb_act_home_fe > 0:
        elu = random.randrange(0, len(possible_act_home_fe), 1)
        ind_elu = possible_fe.index[elu]

        jeune_at_home.loc[i] = [jeune_student.loc[ind_elu], 7, "StayHome"]

        possible_act_home_fe.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_act_home_fe-=1
        i+=1

act_home_fe = pd.read_csv("activite_home_fe.csv")
print(act_home_fe)

act_home_fe= act_home_fe["20"]
act_home_fe.set_index("Code", inplace=True, drop=True)

for ss in sectors:

    nb_act_home_fe = round(act_home_fe.loc[ss])
    possible_act_home_fe = jeune_student_fe_20[jeune_student_fe_20.SectorStatID == ss]

    while nb_act_home_fe > 0:
        elu = random.randrange(0, len(possible_act_home_fe), 1)
        ind_elu = possible_fe.index[elu]

        jeune_at_home.loc[i] = [jeune_student.loc[ind_elu], 7, "StayHome"]

        possible_act_home_fe.drop([ind_elu], inplace=True)
        jeune_student.drop([ind_elu], inplace=True)

        nb_act_home_fe-=1
        i+=1
"""
"""
ado_sec = ado_not_collectif[(ado_not_collectif.HouseholdTypeID == 1) or (ado_not_collectif.HouseholdTypeID == 4)]

ado_sec['WorkerID']=3
ado_sec['WorkerType']="Secondaires"

print(ado_sec)
ado_sec.to_csv("ado_sec_workId.csv")

ado_colloc_worker = ado_not_collectif[ado_not_collectif.HouseholdTypeID == 5]

ado_colloc_worker['WorkerID']=6
ado_colloc_worker['WorkerType']="Worker"

print(ado_colloc_worker)
ado_colloc_worker.to_csv("ado_worker_colloc_workId.csv")

#TODO hopital ou prison ?
"""

