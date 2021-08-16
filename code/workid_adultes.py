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

all_hh = pd.read_csv('all_hh.csv')

adultes = all_hh[(all_hh.Age > 20) and (all_hh.Age < 65)]
adultes_not_collectif = adultes[adultes.HouseholdTypeID != 6]

#Etudiants from bxl to bxl nl
nb_student_nl = pd.read_csv("sup_nl_bxl_to_bxl.csv")
print(nb_student_nl)

colnames = adultes_not_collectif.columns
colnames = colnames.append(["WorkID", "WorkType"])
students_nl = pd.DataFrame(columns=colnames)
students_nl_off_or_on_campus_to_check = pd.DataFrame(columns=colnames)

i = 0
for age in range(21, 65):
    nb_student_nl_age = nb_student_nl[nb_student_nl.Age == age]

    nb_student_nl_age_fe = nb_student_nl_age.Fe
    nb_student_nl_age_ho = nb_student_nl_age.Ho

    possible_fe  = adultes_not_collectif[(adultes_not_collectif.Age == age) and (adultes_not_collectif.Gender == 1)]
    possible_ho  = adultes_not_collectif[(adultes_not_collectif.Age == age) and (adultes_not_collectif.Gender == 0)]

    while nb_student_nl_age_fe > 0:
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]

        hh_id = adultes_not_collectif.loc[ind_elu, "HouseholdTypeID"]

        if hh_id == 1 or hh_id == 2 or hh_id == 3 or hh_id == 4:
            students_nl.loc[i] = [adultes_not_collectif.loc[ind_elu], 5, "Unif off campus"]

        elif hh_id == 5:
            students_nl_off_or_on_campus_to_check.loc[i] = [adultes_not_collectif.loc[ind_elu],"4 or 5", "Unif on or off campus"]
            #TODO check whether same ss unif and logement
        else:
            error

        possible_fe.drop([ind_elu], inplace=True)
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_age_fe-=1
        i+=1

    while nb_student_nl_age_ho > 0:
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        hh_id = adultes_not_collectif.loc[ind_elu, "HouseholdTypeID"]

        if hh_id == 1 or hh_id == 2 or hh_id == 3 or hh_id == 4:
            students_nl.loc[i] = [adultes_not_collectif.loc[ind_elu], 5, "Unif off campus"]

        elif hh_id == 5:
            students_nl_off_or_on_campus_to_check.loc[i] = [adultes_not_collectif.loc[ind_elu],"4 or 5", "Unif on or off campus"]
            #TODO check whether same ss unif and logement
        else:
            error

        possible_ho.drop([ind_elu], inplace=True)
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_age_ho-=1
        i+=1

print(students_nl)
students_nl.to_csv("student_21+_nl_workid.csv")

print(students_nl_off_or_on_campus_to_check)
students_nl_off_or_on_campus_to_check.to_csv("student_21+_nl_workid_4_or_5_to_check.csv")


#Etudiants from bxl to out bxl nl
nb_student_nl_out = pd.read_csv("sup_nl_bxl_to_out_bxl.csv")
print(nb_student_nl_out)

closest_peri = pd.read_csv("closest_peri.csv")
print(closest_peri) #TODO check unnamed and index (should be ss id)

population = pd.read_csv('population.csv')
corres_commune_ss = pd.DataFrame()
corres_commune_ss['Code'] = population.Code
corres_commune_ss['Territoire'] = population.Territoire
corres_commune_ss['Commune'] = population.Commune

communes = corres_commune_ss.Commune
communes.drop_duplicates(inplace=True)
print(communes)

adultes_not_collectif = adultes_not_collectif.merge(corres_commune_ss, how='inner', left_on='SectorStatID', right_on='Code')
print(adultes_not_collectif)

corres_commune_ss.set_index("Code", inplace=True, drop=True)

students_nl_out = pd.DataFrame(columns=colnames)

i = 0
for age in range(21, 65):
    nb_student_nl_out_age = nb_student_nl_out[nb_student_nl_out.Age == age]

    nb_student_nl_out_age_fe = nb_student_nl_out_age.Fe
    nb_student_nl_out_age_ho = nb_student_nl_out_age.Ho

    possible_fe  = adultes_not_collectif[(adultes_not_collectif.Age == age) and (adultes_not_collectif.Gender == 1)]
    possible_ho  = adultes_not_collectif[(adultes_not_collectif.Age == age) and (adultes_not_collectif.Gender == 0)]

    while nb_student_nl_out_age_fe > 0:
        elu = random.randrange(0, len(possible_fe), 1)
        ind_elu = possible_fe.index[elu]

        work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]
        work_ss_name = corres_commune_ss.loc[work_ss_id, "Territoire"]
        students_nl_out.loc[i] = [adultes_not_collectif.loc[ind_elu], 5, "Unif off campus", work_ss_id, work_ss_name]

        possible_fe.drop([ind_elu], inplace=True)
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_out_age_fe-=1
        i+=1

    while nb_student_nl_out_age_ho > 0:
        elu = random.randrange(0, len(possible_ho), 1)
        ind_elu = possible_ho.index[elu]

        work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]
        work_ss_name = corres_commune_ss.loc[work_ss_id, "Territoire"]
        students_nl_out.loc[i] = [adultes_not_collectif.loc[ind_elu], 5, "Unif off campus", work_ss_id, work_ss_name]

        possible_ho.drop([ind_elu], inplace=True)
        adultes_not_collectif.drop([ind_elu], inplace=True)

        nb_student_nl_out_age_ho-=1
        i+=1

print(students_nl_out)
students_nl_out.to_csv("student_21+_nl_to_out_workplace.csv")


sup_fr_trajets = pd.read_csv('superieur_fr_trajets.csv')
sup_fr_trajets = sup_fr_trajets[(sup_fr_trajets["Bxl / hors bxl logement"]== "Brussels")]


colnames = adultes_not_collectif.columns
colnames = colnames.append(["WorkerID", "WorkerType", "WorkSectorStatID", "WorkSectorStatName"])
students = pd.DataFrame(columns=colnames)
i = 0

#etudiant from bxl to bxl fr TODO
for age in range(21, 65):
    sup_fr_trajets = sup_fr_trajets[sup_fr_trajets.Age == age]


    for com in communes:
        possible = sup_fr_trajets[sup_fr_trajets.Commune == com]

        hh_id = adultes_not_collectif.loc[ind_elu, "HouseholdTypeID"]
        if hh_id == 1 or hh_id == 2 or hh_id == 3:
            work_id = 5
            work_name = "Unif off campus"
        elif hh_id == 5:


#etudiants from bxl to out bxl fr
sup_fr_trajets_hors_bxl = pd.read_csv('sup_fr_trajet_hors_bxl.csv')

for age in range(21, 65):
    sup_fr_trajets_hors_bxl_age = sup_fr_trajets_hors_bxl[sup_fr_trajets_hors_bxl.Age == age]

    sup_fr_trajets_hors_bxl_age_fe = sup_fr_trajets_hors_bxl_age[sup_fr_trajets_hors_bxl_age.Sexe == "Femme"]
    sup_fr_trajets_hors_bxl_age_ho = sup_fr_trajets_hors_bxl_age[sup_fr_trajets_hors_bxl_age.Sexe == "Homme"]

    for com in communes:
        nb_to_allocate_fe = sup_fr_trajets_hors_bxl_age_fe[sup_fr_trajets_hors_bxl_age_fe["Libellé de la commune de domicile légal"]==com]
        print(nb_to_allocate_fe) #TODO verifier not null because of majuscules
        nb_to_allocate_ho = sup_fr_trajets_hors_bxl_age_ho[sup_fr_trajets_hors_bxl_age_ho["Libellé de la commune de domicile légal"]==com]

        possible_fe = adultes_not_collectif[(adultes_not_collectif.GenderID == 1) and (adultes_not_collectif.Commune == com) and
                                            (adultes_not_collectif.Age == age)]
        print(possible_fe)  #TODO verifier not null because of majuscules

        possible_ho = adultes_not_collectif[(adultes_not_collectif.GenderID == 0) and (adultes_not_collectif.Commune == com) and
                                            (adultes_not_collectif.Age == age)]

        while nb_to_allocate_fe > 0:
            elu = random.randrange(0, len(possible_fe), 1)
            ind_elu = possible_fe.index[elu]

            work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]
            work_ss_name = corres_commune_ss.loc[work_ss_id, "Territoire"]
            students.loc[i] = [adultes_not_collectif.loc[ind_elu], 5, "Unif off campus", work_ss_id, work_ss_name]

            possible_fe.drop([ind_elu], inplace=True)
            adultes_not_collectif.drop([ind_elu], inplace=True)

            nb_to_allocate_fe-=1
            i+=1

        while nb_to_allocate_ho > 0:
            elu = random.randrange(0, len(possible_ho), 1)
            ind_elu = possible_ho.index[elu]

            work_ss_id = closest_peri.loc[adultes_not_collectif.loc[ind_elu, "SectorStatID"]]
            work_ss_name = corres_commune_ss.loc[work_ss_id, "Territoire"]
            students.loc[i] = [adultes_not_collectif.loc[ind_elu], 5, "Unif off campus", work_ss_id, work_ss_name]

            possible_ho.drop([ind_elu], inplace=True)
            adultes_not_collectif.drop([ind_elu], inplace=True)

            nb_to_allocate_ho-=1
            i+=1

print(students)
students.to_csv("students_21+_unif_workplace.csv")

#Adultes at home
colnames = adultes_not_collectif.columns
colnames = colnames.append(["WorkerID", "WorkerType"])
adultes_at_home = pd.DataFrame(columns=colnames)

adultes_not_collectif_fe = adultes_not_collectif[adultes_not_collectif.Gender == 1]

act_home_fe = pd.read_csv("activite_home_fe.csv")
print(act_home_fe)

sectors = all_hh['SectorStatID']

act_home_fe.set_index("Code", inplace=True, drop=True)
i = 0
for age in range(21, 65):
    act_home_fe_age= act_home_fe[age]

    for ss in sectors:

        nb_act_home_fe = round(act_home_fe_age.loc[ss])
        possible_act_home_fe = adultes_not_collectif_fe[adultes_not_collectif_fe.SectorStatID == ss]

        while nb_act_home_fe > 0:
            elu = random.randrange(0, len(possible_act_home_fe), 1)
            ind_elu = possible_act_home_fe.index[elu]

            adultes_at_home.loc[i] = [adultes_not_collectif.loc[ind_elu], 7, "StayHome"]

            possible_act_home_fe.drop([ind_elu], inplace=True)
            adultes_not_collectif.drop([ind_elu], inplace=True)

            nb_act_home_fe-=1
            i+=1

adultes_not_collectif_ho = adultes_not_collectif[adultes_not_collectif.Gender == 0]

act_home_ho = pd.read_csv("activite_home_ho.csv")
print(act_home_ho)

act_home_ho.set_index("Code", inplace=True, drop=True)

for age in range(21, 65):
    act_home_ho_age= act_home_ho[age]

    for ss in sectors:

        nb_act_home_ho = round(act_home_ho_age.loc[ss])
        possible_act_home_ho = adultes_not_collectif_ho[adultes_not_collectif_ho.SectorStatID == ss]

        while nb_act_home_ho > 0:
            elu = random.randrange(0, len(possible_act_home_ho), 1)
            ind_elu = possible_act_home_ho.index[elu]

            adultes_at_home.loc[i] = [adultes_not_collectif.loc[ind_elu], 7, "StayHome"]

            possible_act_home_ho.drop([ind_elu], inplace=True)
            adultes_not_collectif.drop([ind_elu], inplace=True)

            nb_act_home_ho-=1
            i+=1

print(adultes_at_home)
adultes_at_home.to_csv("adultes_home_workid.csv")


#TODO hopital ou prison ?