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

p = 0.37 #% in bxl from bxl / in bxl from every where

all_hh = pd.read_csv('all_hh_child_Reallocated.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace=True)
print(all_hh)

sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
print(sectors_names_correspondance)


all_hh = all_hh.merge(sectors_names_correspondance, left_on="SectorStatID", right_on="Code")
print(all_hh)

communes = all_hh['Commune']
communes.drop_duplicates(inplace=True)
print(communes)


sectors = all_hh['SectorStatID']
sectors.drop_duplicates(inplace=True)
print(sectors)

adultes = all_hh[(all_hh.Age > 20) & (all_hh.Age < 65)]
adultes_not_collectif = adultes[adultes.HouseholdTypeID != 6]


#etudiant from bxl to bxl fr
campus = pd.read_csv("sup_campus_bxl_fr_with_ss_v2.csv")

print(campus.columns)

ss = pd.DataFrame()
ss['SectorStat'] = campus.sector_stat
#ss.drop_duplicates(inplace=True)
print(ss)

sectors_names_correspondance = pd.read_csv('sector_stat.csv', sep=';')
#sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
print(sectors_names_correspondance)


ss = ss.merge(sectors_names_correspondance, left_on="SectorStat", right_on="Code", how='inner')
ss.drop(columns=["Code"], inplace=True)
print(ss)
ss.to_csv('campus_fr_ss_commune.csv')
communes = ss.Commune
communes.drop_duplicates(inplace=True)
sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
dic = dict()
for com in communes:
    list_ss = ss[ss.Commune == com].SectorStat.tolist()
    dic[com]=list_ss #len(ss[ss.Commune==com])
    
print(dic)

colnames = adultes_not_collectif.columns.tolist()
colnames.extend(["WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"])
adulte_students = pd.DataFrame(columns=colnames)

age_min = 21
age_max = 64
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
        possible = adultes_not_collectif[(adultes_not_collectif.GenderID == sex) & (adultes_not_collectif.Age == age) &
                                 (adultes_not_collectif.Commune == unif_fr.loc[ind, "Commune_from"])]
        nb = unif_fr.loc[ind, "Sum of Compte"]
        
        com_to = unif_fr.loc[ind, "Commune_to"]
        list_ss_to = dic[com_to]

        if com_to == "Bruxelles":
            nb_per_ss = max(round(nb/len(list_ss_to)), 0)
            nb_per_ss = max(round((nb*(1-650*p/8634-200*p/8634-2783*p/8634-16407*p/8634))/len(list_ss_to-4)), 0)
            reste = (nb*(1-650*p/8634-200*p/8634-2783*p/8634-16407*p/8634))%len(list_ss_to-4)
        elif com_to == 'Anderlecht':
            nb_per_ss = max(round((nb*(1-200*p/3520-4707*p/3520))/len(list_ss_to-2)), 0)
            reste = (nb*(1-200*p/3520-4707*p/3520))%len(list_ss_to-2)
        elif com_to == 'Ixelles':
            nb_per_ss = max(round((nb*(1-1050*p/2022-2476*p/2022))/len(list_ss_to-2)), 0)
            reste = (nb*(1-1050*p/2022-2476*p/2022))%len(list_ss_to-2)
        elif com_to == 'Woluwe Saint-Pierre':
            nb_per_ss = max(round((nb(1-2000*p/2453))/len(list_ss_to-1)), 0)
            reste = (nb(1-2000*p/2453))%len(list_ss_to-1)
        elif com_to == 'Woluwe Saint-Lambert':
            nb_per_ss = max(round((nb*(1-7006*p/9213))/len(list_ss_to-1)), 0)
            reste = (nb*(1-7006*p/9213))%len(list_ss_to-1)
        else:
            nb_per_ss = max(round(nb/len(list_ss_to)), 0)
            reste = (nb)%len(list_ss_to)

        first_ss = True
        
        for ss in list_ss_to:
            print("ss", ss)
            if ss == '21004C642':
                nb_per_ss_tmp = round(nb*650*p/8634)
            elif ss == '21004A3MJ':
                nb_per_ss_tmp = round(nb*200*p/8634)
            elif ss == '21001B25-':
                nb_per_ss_tmp = round(nb*200*p/3520)
            elif ss == "21004A32-":
                nb_per_ss_tmp = round(nb*2783*p/8634)
            elif ss == '21004C61-':
                nb_per_ss_tmp = round(nb*16407*p/8634)
            elif ss == '21001C522':
                nb_per_ss_tmp = round(nb*(4707*p + 2*nb_per_ss))/3
            elif ss == '21009A602':
                nb_per_ss_tmp = round(nb*1050*p/2022)
            elif ss == '21009A2MJ':
                nb_per_ss_tmp = round(nb*2476*p/2022)
            elif ss == '21019A52-':
                nb_per_ss_tmp = round(nb*2000*p/2453)
            elif ss == '21018A87-':
                nb_per_ss_tmp = round(nb*7006*p/9213 + 7+nb_per_ss)/8


            elif first_ss:
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
                adulte_students.loc[i]=el
                
                possible.drop([ind_elu], inplace=True)
                adultes_not_collectif.drop([ind_elu], inplace = True)
                
                nb_per_ss_tmp -=1
                i+=1

print(adulte_students)
adulte_students.to_csv("student_fr_bxl_bxl_adultes_workplace_v2.csv")                     
    
closest_peri = pd.read_csv("closest_ss_peri_v2.csv")
closest_peri.set_index('SectorStatID', inplace=True, drop=True)
print(closest_peri) #TODO check unnamed and index (should be ss id)


#etudiants from bxl to out bxl fr
sup_fr_trajets_hors_bxl = pd.read_csv('sup_fr_trajets_to_hors_bxl.csv', sep=';')

for age in range(21, 65):
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
            possible_fe = adultes_not_collectif[(adultes_not_collectif.GenderID == 1) & (adultes_not_collectif.Commune == com) & (adultes_not_collectif.Age == age)]
            print(possible_fe)  #TODO verifier not null because of majuscules
            
            
            while nb_to_allocate_fe > 0 and len(possible_fe)>0:
                print("i com bxl out bxl fr", i)
                elu = random.randrange(0, len(possible_fe), 1)
                ind_elu = possible_fe.index[elu]
    
                work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
                work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
                
                el = possible_fe.loc[ind_elu].tolist()
                el.extend([5, "Unif off campus", work_ss_id, work_ss_name])
                adulte_students.loc[i] = el
    
                possible_fe.drop([ind_elu], inplace=True)
                adultes_not_collectif.drop([ind_elu], inplace=True)
    
                nb_to_allocate_fe-=1
                i+=1

        nb_to_allocate_ho = sup_fr_trajets_hors_bxl_age_ho[sup_fr_trajets_hors_bxl_age_ho["Commune_from"]==com]
        nb_to_allocate_ho.reset_index(inplace=True)
        if not nb_to_allocate_ho.empty:
        
            nb_to_allocate_ho= nb_to_allocate_ho.loc[0,"Sum of Compte"]
            print(nb_to_allocate_ho) #TODO verifier not null because of majuscules
            possible_ho = adultes_not_collectif[(adultes_not_collectif.GenderID == 0) & (adultes_not_collectif.Commune == com) & (adultes_not_collectif.Age == age)]
    
            while nb_to_allocate_ho > 0 and len(possible_ho)>0:
                print("i com bxl out bxl fr g", i)
                elu = random.randrange(0, len(possible_ho), 1)
                ind_elu = possible_ho.index[elu]
    
                work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
                work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
                
                el = possible_ho.loc[ind_elu].tolist()
                el.extend([5, "Unif off campus", work_ss_id, work_ss_name])
                adulte_students.loc[i] = el
    
                possible_ho.drop([ind_elu], inplace=True)
                adultes_not_collectif.drop([ind_elu], inplace=True)
    
                nb_to_allocate_ho-=1
                i+=1

print(adulte_students)
adulte_students.to_csv("students_adultes_unif_workplace_v2.csv")

#Etudiants from bxl to bxl nl
nb_student_nl = pd.read_csv("sup_nl_bxl_to_bxl.csv", sep=";")
print(nb_student_nl)

colnames = ["SectorStatID", "SectorStatName", "PersID", "Age", "GenderID", "GenderName", "ChildOrParent",
            "HouseholdID", "HouseholdTypeID", "HouseholdTypeName", "Code", "Commune", "WorkerID", 
            "WorkerType"]
students_nl = pd.DataFrame(columns=colnames)
students_nl_off_or_on_campus_to_check = pd.DataFrame(columns=colnames)

i = 0
for age in range(18, 21):
    print("age", age)
    nb_student_nl_age = nb_student_nl[nb_student_nl.Age == age]

    nb_student_nl_age_fe = int(nb_student_nl_age.loc[:, "Fe"])
    nb_student_nl_age_ho = int(nb_student_nl_age.loc[:, "Ho"])

    possible_fe  = adultes_not_collectif[(adultes_not_collectif.Age == age) & (adultes_not_collectif.GenderID == 1)]
    possible_ho  = adultes_not_collectif[(adultes_not_collectif.Age == age) & (adultes_not_collectif.GenderID == 0)]

    while nb_student_nl_age_fe > 0 and len(possible_fe) > 0:
        print("age i", i)
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]

        hh_id = adultes_not_collectif.loc[ind_elu, "HouseholdTypeID"]
        
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
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_age_fe-=1
        i+=1

    while nb_student_nl_age_ho > 0 and len(possible_fe) > 0:
        print("age i g", i)
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        hh_id = adultes_not_collectif.loc[ind_elu, "HouseholdTypeID"]
        
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
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_age_ho-=1
        i+=1

print(students_nl)
students_nl.to_csv("student_adultes_nl_workid_v2.csv")

print(students_nl_off_or_on_campus_to_check)
students_nl_off_or_on_campus_to_check.to_csv("student_adultes_nl_workid_4_or_5_to_check_v2.csv")


#Etudiants from bxl to out bxl nl
nb_student_nl_out = pd.read_csv("sup_nl_bxl_to_out_bxl.csv", sep=";")
print(nb_student_nl_out)


sectors_names_correspondance = pd.read_csv("sector_stat.csv", sep=";")
#sectors_names_correspondance.drop(columns=["Name"], inplace=True)
sectors_names_correspondance.drop_duplicates(inplace=True)
print(sectors_names_correspondance)

communes = sectors_names_correspondance.Commune
communes.drop_duplicates(inplace=True)
print(communes)

adultes_not_collectif = adultes_not_collectif.merge(sectors_names_correspondance, how='inner', left_on='SectorStatID', right_on='Code')
print(adultes_not_collectif)

sectors_names_correspondance.set_index("Code", inplace=True, drop=True)

colnames = adultes_not_collectif.columns.tolist()
colnames.extend(["WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"])
students_nl_out = pd.DataFrame(columns=colnames)

i = 0
for age in range(21, 65):
    print("age g bxl out bxl", age)
    nb_student_nl_out_age = nb_student_nl_out[nb_student_nl_out.Age == age]

    nb_student_nl_out_age_fe = int(nb_student_nl_out_age.loc[:, "Fe"])
    nb_student_nl_out_age_ho = int(nb_student_nl_out_age.loc[:, "Ho"])

    possible_fe  = adultes_not_collectif[(adultes_not_collectif.Age == age) & (adultes_not_collectif.GenderID == 1)]
    possible_ho  = adultes_not_collectif[(adultes_not_collectif.Age == age) & (adultes_not_collectif.GenderID == 0)]

    while nb_student_nl_out_age_fe > 0 and len(possible_fe) > 0:
        print("i g bxl out bxl", i)
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]
        
        el = possible_fe.loc[ind_elu].tolist()

        work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
        work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
        
        el.extend([ 5, "Unif off campus", work_ss_id, work_ss_name])
        students_nl_out.loc[i] = el

        possible_fe.drop([ind_elu], inplace=True)
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_out_age_fe-=1
        i+=1

    while nb_student_nl_out_age_ho > 0 and len(possible_ho) > 0:
        print("i g bxl out bxl g", i)
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        el = possible_ho.loc[ind_elu].tolist()
        
        work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]["Closest_Peri"]
        work_ss_name = sectors_names_correspondance.loc[work_ss_id, "Name"]
        
        el.extend([ 5, "Unif off campus", work_ss_id, work_ss_name])
        students_nl_out.loc[i] = el

        possible_ho.drop([ind_elu], inplace=True)
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_out_age_ho-=1
        i+=1

print(students_nl_out)
students_nl_out.to_csv("student_adultes_nl_to_out_workplace_v2.csv")



#Adultes at home
colnames = adultes_not_collectif.columns.tolist()
colnames.extend(["WorkerID", "WorkerType"])
adultes_at_home = pd.DataFrame(columns=colnames)

adultes_not_collectif_fe = adultes_not_collectif[adultes_not_collectif.GenderID == 1]

act_home_fe = pd.read_csv("activite_home_fe.csv", sep=';')
print(act_home_fe)

sectors = all_hh['SectorStatID']

act_home_fe.set_index("Code", inplace=True, drop=True)
i = 0
for age in range(21, 65):
    print("age fin", age)
    act_home_fe_age= act_home_fe[str(age)+",00"]

    for ss in sectors:
        print("ss fin", ss)
        nb_act_home_fe = act_home_fe_age.loc[ss]
        if type(nb_act_home_fe)==str:
            nb_act_home_fe = nb_act_home_fe.replace(",", ".")
            nb_act_home_fe = float(nb_act_home_fe)
        nb_act_home_fe = round(nb_act_home_fe)
        
        possible_act_home_fe = adultes_not_collectif_fe[adultes_not_collectif_fe.SectorStatID == ss]

        while nb_act_home_fe > 0:
            print("i fin", i)
            elu = random.randrange(0, len(possible_act_home_fe), 1)
            ind_elu = possible_act_home_fe.index[elu]
        
            el = possible_act_home_fe.loc[ind_elu].tolist()
            el.extend([7, "StayHome"])
        
            adultes_at_home.loc[i] = el

            possible_act_home_fe.drop([ind_elu], inplace=True)
            adultes_not_collectif.drop([ind_elu], inplace=True)

            nb_act_home_fe-=1
            i+=1

adultes_not_collectif_ho = adultes_not_collectif[adultes_not_collectif.GenderID == 0]

act_home_ho = pd.read_csv("activite_home_ho.csv", sep=';')
print(act_home_ho)

act_home_ho.set_index("Code", inplace=True, drop=True)

for age in range(21, 65):
    print("age fin g", age)
    act_home_ho_age= act_home_ho[str(age)+",00"]

    for ss in sectors:
        print("ss fin g", ss)
        nb_act_home_ho = act_home_ho_age.loc[ss]
        if type(nb_act_home_ho)==str:
            nb_act_home_ho = nb_act_home_ho.replace(",", ".")
            nb_act_home_ho = float(nb_act_home_ho)
        nb_act_home_ho= round(nb_act_home_ho)
        
        possible_act_home_ho = adultes_not_collectif_ho[adultes_not_collectif_ho.SectorStatID == ss]

        while nb_act_home_ho > 0:
            print("i fin g", i)
            elu = random.randrange(0, len(possible_act_home_ho), 1)
            ind_elu = possible_act_home_ho.index[elu]

            el = possible_act_home_ho.loc[ind_elu].tolist()
            el.extend([7, "StayHome"])
        
            adultes_at_home.loc[i] = el
            
            possible_act_home_ho.drop([ind_elu], inplace=True)
            adultes_not_collectif.drop([ind_elu], inplace=True)

            nb_act_home_ho-=1
            i+=1


print(adultes_at_home)
adultes_at_home.to_csv("adultes_home_workid.csv")

adultes_not_collectif["WorkerID"]=6
adultes_not_collectif["WorkerName"]="Worker"

print(adultes_not_collectif)
adultes_not_collectif.to_csv("adultes_worker.csv")

adultes_collectif = adultes[adultes.HouseholdTypeID == 6]
print(adultes_collectif)
adultes_collectif.to_csv("adultes_collectif.csv")

#TODO hopital ou prison ?