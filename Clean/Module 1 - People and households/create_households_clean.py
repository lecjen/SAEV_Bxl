# -*- coding: utf-8 -*-
"""
@author: Jennifer Leclipteur
"""
########################################################################################################################
#       Imports                                                                                                        #
########################################################################################################################
import pandas as pd
import random
import bisect

########################################################################################################################
#       Define constants' value                                                                                        #
########################################################################################################################
delta_age_husband_wife = 3

distribution_age_child = [0.012, 0.087, 0.252, 0.35, 0.229, 0.064, 0.006]
min_delta_ages = [15, 20, 25, 30, 35, 40, 45]

distribution_nb_children = [0.466, 0.3265, 0.1405, 0.0496, 0.0131, 0.0032, 0.0008, 0.0003]

########################################################################################################################
#       Usefull functions for data cleaning                                                                            #
########################################################################################################################
def replace_only_str(x, that, by):
    """
    Check whether x is a string and replace that by by if it is the case
    Otherwise do nothing

    :param x: an element
    :param that: string to be replaced
    :param by: string to replace with

    :return: x : initial string with the desired replacements
    """
    if type(x)==str:
        x = x.replace(that, by)

    return x

def comma_to_dot(df):
    """
    Change all commas by dots (french numbers convention to english one)

    :param df: pd.DataFrame to clean

    :return: df with the desired changes
    """
    for col in df.columns:
        df[col] = df[col].apply(lambda x : replace_only_str(x, ',', "."))

    return df

def clean_col_names(df):
    """
    Remove all columns starting by 'Unnamed:' (resulting from the saving of a dataframe and then load again)

    :param df: pd.DataFrame to clean

    :return: df without the columns containing 'Unnamed: '
    """
    for col in df.columns:
        if 'Unnamed:' in col:
            new_col_name = col[9:]
            df[new_col_name]=df[col]
            df.drop(columns=[col], inplace=True)
    return df

########################################################################################################################
#       Load and clean data (from excel module 1)                                                                      #
########################################################################################################################
ss_age_fe = pd.read_csv('SectorStat_Age_Femmes.csv', sep=';')
ss_age_fe= comma_to_dot(ss_age_fe)
ss_age_fe = clean_col_names(ss_age_fe)
print(ss_age_fe)

ss_age_ho = pd.read_csv('SectorStat_Age_Hommes.csv', sep=';')
ss_age_ho= comma_to_dot(ss_age_ho)
ss_age_ho = clean_col_names(ss_age_ho)
ss_age_ho.drop(columns=['98', '99', '100', '101', '102', '103', '104', '105', '106', '107'],
               inplace=True)                                                                    #empty columns
print(ss_age_ho.columns)                                                                        #check
print(ss_age_ho)

couple_child_age_mom = pd.read_csv('Couple_enfant_age_mere.csv', sep=';')
couple_child_age_mom= comma_to_dot(couple_child_age_mom)
couple_child_age_mom = clean_col_names(couple_child_age_mom)
print(couple_child_age_mom)

couple_age_fe = pd.read_csv('Couple_age_femme.csv', sep=';')
couple_age_fe= comma_to_dot(couple_age_fe)
couple_age_fe = clean_col_names(couple_age_fe)
print(couple_age_fe)

single_age_fe = pd.read_csv('Single_Age_Femme.csv', sep=';')
single_age_fe= comma_to_dot(single_age_fe)
single_age_fe = clean_col_names(single_age_fe)
print(single_age_fe)

single_age_ho = pd.read_csv('Single_Age_Homme.csv', sep=';')
single_age_ho= comma_to_dot(single_age_ho)
single_age_ho = clean_col_names(single_age_ho)
print(single_age_ho)

single_mom_age = pd.read_csv('Single_Parent_Age_Fe.csv', sep=';')
single_mom_age= comma_to_dot(single_mom_age)
single_mom_age = clean_col_names(single_mom_age)
print(single_mom_age)

single_dad = pd.read_csv('Single_Parent_enfant_ho.csv', sep=';')
single_dad= comma_to_dot(single_dad)
single_dad = clean_col_names(single_dad)
print(single_dad)

colloc_fe = pd.read_csv('Femme_colloc_ind_age.csv', sep=';')
colloc_fe= comma_to_dot(colloc_fe)
colloc_fe = clean_col_names(colloc_fe)
print(colloc_fe)

colloc_ho = pd.read_csv('Homme_colloc_ind_age.csv', sep=';')
colloc_ho= comma_to_dot(colloc_ho)
colloc_ho = clean_col_names(colloc_ho)
print(colloc_ho)

SectorStats = ss_age_fe['Code']
print(SectorStats)

########################################################################################################################
#       Functions definition                                                                                           #
########################################################################################################################

def get_nbre_fe(sector_stat, age, ss_age_fe):
    """
    Return the number of women according to a given age and a given sector statistics

    :param sector_stat: string; sector statistics
    :param age: int; age
    :param ss_age_fe: pd.DataFrame; table with the data

    :return:int; number of women of age age living in the sector statistics sector_stat
    """
    fe_ss = ss_age_fe[ss_age_fe.Code==sector_stat]
    nbre = fe_ss[str(age)]

    index = ss_age_fe.index
    ind = index[ss_age_fe['Code']== sector_stat][0]

    return round(float(nbre.loc[ind]))

def get_nbre_ho_colloc(sector_stat, colloc_ho):
    """
    Return the number of men living in colocation in a given sector statistics

    :param sector_stat: string; sector statistics
    :param colloc_ho: pd.DataFrame; table with the data

    :return: int; number of men living in a colocation in the sector statistics sector_stat
    """
    ho_ss = colloc_ho[colloc_ho.Code==sector_stat]
    nbre = ho_ss['#hommes colloc dans secteur stat']

    index = colloc_ho.index
    ind = index[colloc_ho['Code']== sector_stat][0]

    return round(float(nbre.loc[ind]))

def get_nbre_fe_colloc(sector_stat, colloc_fe):
    """
    Return the number of women living in colocation in a given sector statistics

    :param sector_stat: string; sector statistics
    :param colloc_fe: pd.DataFrame; table with the data

    :return: int; number of women living in a colocation in the sector statistics sector_stat
    """
    fe_ss = colloc_fe[colloc_fe.Code==sector_stat]
    nbre = fe_ss['#femmes colloc dans secteur stat']

    index = colloc_fe.index
    ind = index[colloc_fe['Code']== sector_stat][0]

    return round(float(nbre.loc[ind]))

def get_nbre_single_dad(sector_stat, single_dad):
    """
    Return the number of single dad living in a given sector statistics

    :param sector_stat: string; sector statistics
    :param single_dad: pd.DataFrame; table with the data

    :return: int; number of dad living in the sector statistics sector_stat
    """
    dad_ss = single_dad[single_dad.Code==sector_stat]
    nbre = dad_ss['single dad']

    index = single_dad.index
    ind = index[single_dad['Code']== sector_stat][0]

    return round(float(nbre.loc[ind]))

def get_hh_id(hh_type):
    """
    Return the household id corresponding to the household name

    :param hh_type: string; household name

    :return: int; household id
    """
    if hh_type == 'couple_with_child':
        hh_id = 1
    elif hh_type == 'couple_no_child':
        hh_id = 2
    elif hh_type == 'single':
        hh_id = 3
    elif hh_type == 'single_with_child':
        hh_id = 4
    elif hh_type == 'colloc':
        hh_id = 5
    elif hh_type == 'collectif':
        hh_id = 6
    else :
        print("Error: Household Type unknown. It should be 'couple_with_child', 'couple_no_child', 'single', 'single_with_child', 'colloc' or 'collectif'")

    return hh_id

def get_ss_name(ss, ss_age_fe):
    """
    Return the name of the sector statistics corresponding to the code ss

    :param ss: string; code of the desired sector statistics
    :param ss_age_fe: pd.DataFrame; table used as correspondance table

    :return: string; name of the sector statistics
    """
    ss_row = ss_age_fe[ss_age_fe.Code==ss]
    name = ss_row['Territoire']

    index = ss_age_fe.index
    ind = index[ss_age_fe['Code']== ss][0]

    return name.loc[ind]

def get_gender(gender_id):
    """
    Return the name of the gender corresponding to the gender id

    :param gender_id: int; gender id

    :return: string; name of the gender
    """
    if gender_id == 1:
        gender = 'female'
    elif gender_id == 0 :
        gender = 'male'
    else:
        print('Error: Gender Id unknow. Should be 1 or 0')

    return gender

def add_pers(all_hh, nb, sector_stat, ss_name, persid, age, gender_id, hhid, hh_type_id, hh_type, same_hh,
             child_or_parent):
    """
    Add a person in the all_hh table with all his caracteristics

    :param all_hh: pd.DataFrame; all people already created
    :param nb: int; remaining places in the concerned category
    :param sector_stat: int; id of the sector statistics where the person to be added lives
    :param ss_name: string; name of the sector statistics where the person to be added lives
    :param persid: int; id of the person to be added
    :param age: int; age of the person to be added
    :param gender_id: int; gender id of the person to be added
    :param hhid: int; household id of the person to be added
    :param hh_type_id: int; id of the household type of the person to be added
    :param hh_type: string; name of the household type of the person to be added
    :param same_hh: boolean; True if the next person to be added has to be in the same household
    :param child_or_parent: string; status of the person to be added

    :return: all_hh with the new person added
    """
    gender = get_gender(gender_id)

    all_hh.loc[persid]=[sector_stat, ss_name, persid, age, gender_id, gender, child_or_parent, hhid, hh_type_id, hh_type]
    persid +=1
    if not same_hh:
        hhid +=1
    nb -=1

    return all_hh, persid, hhid, nb

def get_age_mari(age):
    """
    Return the age of the husband according to the age of the wife

    :param age: int; age of the wife

    :return: age_mari; int; age of the husband
    """
    age_mari = age + delta_age_husband_wife

    return age_mari

def check_age_mari(ss, ss_age_ho, age_mari):
    """
    Check whether it is still possible to create a man of age age_mari living in the sector statistics ss

    :param ss: string; code of the sector statistics
    :param ss_age_ho: pd.DataFrame; data table
    :param age_mari: int; age of the man

    :return: boolean; True if it is not possible to add a man of age age_mari living in the sector statistics ss
    """
    ss_row = ss_age_ho[ss_age_ho.Code==ss]
    nb = ss_row[str(age_mari)]

    index = ss_age_ho.index
    ind = index[ss_age_ho['Code']== ss][0]

    clean_nb = round(float(nb.loc[ind]))
    if clean_nb == 0 or clean_nb < 0:
        nok = True
    elif clean_nb > 0:
        nok = False

    return nok

def adapt_nb(sector_stat, ss_age_ho, age_mari):
    """
    Update the data table after having created a person (so there is one place less in the sector statistics sector_stat
     for people of age age_mari)

    :param sector_stat: string; sector statistics where the person added lives
    :param ss_age_ho: pd.DataFrame; data table to be updated
    :param age_mari: int; age of the person added

    :return:ss_age_ho; the updated data table
    """
    index = ss_age_ho.index
    ind = index[ss_age_ho['Code']== sector_stat][0]
    places = ss_age_ho.loc[ind, str(age_mari)]

    places = round(float(places))

    ss_age_ho.loc[ind, str(age_mari)] = places - 1

    return ss_age_ho

def adapt_nb_single_dad(sector_stat, single_dad):
    """
    Update the data table after having created a single dad (so there is one place less in the sector statistics
    sector_stat for a single dad)

    :param sector_stat: string; sector statistics where the single dad added lives
    :param single_dad: pd.DataFrame; data table

    :return:single_dad; the updated data table
    """
    index = single_dad.index
    ind = index[single_dad['Code']== sector_stat][0]
    places = single_dad.loc[ind, 'single dad']

    places = round(float(places))

    single_dad.loc[ind, 'single dad'] = places - 1

    return single_dad

def adapt_nb_colloc_fe(sector_stat, colloc_fe):
    """
    Update the data table after having created a woman living in colocation in the sector statistics sector_stat
    (so there is one place less in the sector statistics sector_stat for a woman in colocation)

    :param sector_stat: string; sector statistics where the woman added lives
    :param colloc_fe: pd.DataFrame; data table

    :return:colloc_fe; the updated data table
    """
    index = colloc_fe.index
    ind = index[colloc_fe['Code']== sector_stat][0]
    places = colloc_fe.loc[ind, '#femmes colloc dans secteur stat']

    places = round(float(places))

    colloc_fe.loc[ind, '#femmes colloc dans secteur stat'] = places - 1

    return colloc_fe

def adapt_nb_colloc_ho(sector_stat, colloc_fe):
    """
    Update the data table after having created a man living in colocation in the sector statistics sector_stat
    (so there is one place less in the sector statistics sector_stat for a man in colocation)

    :param sector_stat: string; sector statistics where the man added lives
    :param colloc_fe: pd.DataFrame; data table

    :return:colloc_fe; the updated data table
    """
    index = colloc_fe.index
    ind = index[colloc_fe['Code']== sector_stat][0]

    places = colloc_fe.loc[ind, '#hommes colloc dans secteur stat']

    places = round(float(places))

    colloc_fe.loc[ind, '#hommes colloc dans secteur stat'] = places - 1

    return colloc_fe

def cdf(weights):
    """
    Create Cumulative Distribution
    TODO SOURCING FROM THESIS

    :param weights: list of probabilities for each index to happen

    :return: result; list; the cumulative distribution
    """
    total=sum(weights); result=[]; cumsum=0

    for w in weights:
        cumsum+=w
        result.append(cumsum/total)

    return result

def get_index(distribution):
    """
    Return the index randomly pick according to the probabilities distribution distribution
    TODO SOURCING FROM THESIS

    :param distribution: list; probabilities distribution

    :return: int; index picked
    """
    dist = distribution #allDistributions[travelerType]
    weights = cdf(dist)
    split = random.random()
    idx = bisect.bisect(weights, split)

    return idx

def get_age_child(age):
    """
    Return the age of a child according to the age of his mother (age) following a given probabilities distribution

    :param age: int; mother's age

    :return: int; child's age
    """
    age_child = -1
    while age_child < 0:
        dist = distribution_age_child
        idx = get_index(dist)
        delta_age_plus = random.randrange(0, 5,1)

        delta_age = min_delta_ages[idx]+delta_age_plus
        if delta_age == 15:
            delta_age = 16

        age_child = age - delta_age

    return age_child

def get_sex_child():
    """
    Return the gender id of a child

    :return: int; gender id
    """
    sex_child = random.randrange(0, 2,1)

    return sex_child

def get_nb_children():
    """
    Return the number of children in a household according to the probabilities distribution

    :return: int; number of children in a household
    """
    dist = distribution_nb_children
    nb_child = get_index(dist) + 1

    return nb_child

def get_nb_colloc():
    """
    Return the number of roommates in a household randomly chosen between 3 and 9

    :return: int; number of roommates in a household
    """
    nb_colloc = random.randrange(3, 9, 1)

    return nb_colloc

def get_age_dad():
    """
    Return the age of a single father randomly chosen between 16 and 71

    :return: age; int; age of the father
    """
    age = random.randrange(16, 71,1)

    return age

def get_age_colloc():
    """
    Return the age of a roommate randomly chosen between 16 and 71

    :return: age; int; age of the roommate
    """
    age = random.randrange(16, 71,1)

    return age

def get_closest_not_empty(age, ss_age_ho, ss, age_mom = 121):
    """
    Return the closest age to age for which we can still create a person living in the sector statistics ss

    :param age: int; age we want to be the closest to
    :param ss_age_ho: pd.DataFrame; data table with the remaining places
    :param ss: string; code of the sector statistics where the person lives
    :param age_mom: int; age of the mother if we create a child; 121 otherwise
    :param first_child: boolean; True if we are creating the a necessary person of an household (otherwise the household
    type changes)

    :return: int; closest age to age for which we can still create a person living in the sector statistics ss
    """
    #Check whether we are creating a child
    if age_mom == 121:
        child = False
    else:
        child = True

    ss_row = ss_age_ho[ss_age_ho.Code==ss]

    index = ss_age_ho.index
    ind = index[ss_age_ho['Code']== ss][0]

    ss_row.drop(columns=['Code', 'Territoire'], inplace=True)

    for col in ss_row.columns:
        #Remove the useless column "Commune"
        if col == 'Commune':
            ss_row.drop(columns=[col], inplace = True)

        #Remove all columns for which the age difference between the mother and the child would be too small to be
        # realistic or for which there is no more places
        elif child:
            if round(float(ss_row.loc[ind, col])) <= 0 or int(col)> age_mom-16:
                ss_row.drop(columns=[col], inplace = True)

        #Remove all columns for which there is no more places
        else:
            if round(float(ss_row.loc[ind, col])) <= 0:
                ss_row.drop(columns=[col], inplace = True)

    for i in range(0, 104):                                         #Iterates through possible difference ages
        if str(age-i) in ss_row.columns:
            new_age = age-i
            too_many = False
            if child:
                break                                               #Closest age found
            elif new_age < 95:
                break                                               #Closest age found
        elif str(age+i) in ss_row.columns and age+i+16 < age_mom:
            new_age = age+i
            too_many = False
            if child:
                break                                               #Closest age found
            elif new_age < 95:
                break                                               #Closest age found

    if len(ss_row.columns) == 0:                    #No more places possible but first child is True
                                                                    #so we have to create a person
        new_age = age
        too_many = True
        if not child and new_age > 94:                              #if the person of age age is a woman but we are
            new_age = 94                                            #creating a man
    """
    TODO del
    elif len(ss_row.columns) == 0 and not first_child:
        new_age = age
        too_many = True
        if not child and new_age > 94:
            new_age = 94
    else:
        new_age = age
        too_many = False
        if not child and new_age > 94:
            new_age = 94
    """

    return new_age, too_many

def check_age_child(ss, ss_age_fe, ss_age_ho, age_child, sex_child):
    """
    Check whether the person of age age_child and sex sex_child living in the sector statistics ss can be added (there
    is enough place remaining)

    :param ss: string; code of the sector statistics where the person to be added lives
    :param ss_age_fe: pd.DataFrame; data table with the remaining places for women
    :param ss_age_ho: pd.DataFrame; data table with the remaining places for men
    :param age_child: int; age of the the person to be added
    :param sex_child: int; gender id of the person to be added

    :return: boolean; False if there is enough places and the person can be added
    """
    if age_child < 0:                                                                  #ERROR should not happen
        nok = True
    else:
        if sex_child == 0:                                                             #It is a man
            ss_row = ss_age_ho[ss_age_ho.Code==ss]
            index = ss_age_ho.index
            ind = index[ss_age_ho['Code']== ss][0]

        elif sex_child == 1:                                                          #It is a woman
            ss_row = ss_age_fe[ss_age_fe.Code==ss]
            index = ss_age_fe.index
            ind = index[ss_age_fe['Code']== ss][0]

        nb = ss_row[str(age_child)]

        clean_nb = round(float(nb.loc[ind]))

        if clean_nb <= 0:
            nok = True
        elif clean_nb > 0:
            nok = False

    return nok

def create_households(all_hh, sector_stat, persid, hhid, ss_age_fe, single_age_fe, couple_age_fe, ss_age_ho,
                      single_mom_age, couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, single_dad):
    """
    Append households of people living in the sector statitstics sector_stat to the table all_hh

    :param all_hh: pd.DataFrame; table where to add the new households
    :param sector_stat: string; code of the sector statistics
    :param persid: int; next id for the next person to be created
    :param hhid: int; next household id for the next household to be created
    :param ss_age_fe: pd.DataFrame; table with places per sector statistics and per age for women
    :param single_age_fe: pd.DataFrame; table with places per sector statistics and per age for women living alone
    :param couple_age_fe: pd.DataFrame; table with places per sector statistics and per age of women for couples without
     child
    :param ss_age_ho: pd.DataFrame; table with places per sector statistics and per age for men
    :param single_mom_age: pd.DataFrame; table with places per sector statistics and per age for single mothers
    :param couple_child_age_mom: pd.DataFrame; table with places per sector statistics and per age of women for couples
    with child
    :param colloc_fe: pd.DataFrame; table with places per sector statistics and per age for women living in colocation
    :param colloc_ho: pd.DataFrame; table with places per sector statistics and per age for men living in colocation
    :param single_age_ho: pd.DataFrame; table with places per sector statistics and per age for men living alone
    :param single_dad: pd.DataFrame; table with places per sector statistics and per age for single fathers

    :return: all_hh with the people added, updated persid and hhid
    """
    hh_list = ['couple_with_child', 'couple_no_child', 'single', 'single_with_child', 'colloc', 'collectif']

    ss_name = get_ss_name(sector_stat, ss_age_fe)

    for age in range(104, 15, -1):

        for hh_type in hh_list:
            hh_type_id = get_hh_id(hh_type)

            #Create single women
            if hh_type == 'single':

                nbre_fe_single = get_nbre_fe(sector_stat, age, single_age_fe)

                while nbre_fe_single > 0:

                    all_hh, persid, hhid, nbre_fe_single = add_pers(all_hh, nbre_fe_single, sector_stat, ss_name,
                                                                    persid, age, 1, hhid, hh_type_id, hh_type, False,
                                                                    'parent')

                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    single_age_fe = adapt_nb(sector_stat, single_age_fe, age)

                print("single fe added")

            #Create couples without child
            elif hh_type == 'couple_no_child':

                nbre_fe_couple = get_nbre_fe(sector_stat, age, couple_age_fe)

                while nbre_fe_couple > 0 :

                    all_hh, persid, hhid, nbre_fe_couple = add_pers(all_hh, nbre_fe_couple, sector_stat, ss_name,
                                                                    persid, age, 1, hhid, hh_type_id, hh_type, True,
                                                                    'parent')

                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    couple_age_fe = adapt_nb(sector_stat, couple_age_fe, age)

                    print("couple fe added")

                    age_mari_nok = True
                    triche_age_mari_nok = True
                    i = 0
                    while age_mari_nok:
                        i += 1
                        age_mari = get_age_mari(age)

                        age_mari_nok = check_age_mari(sector_stat, ss_age_ho, age_mari)

                        if i >= 95:
                            age_mari, too_many = get_closest_not_empty(age, ss_age_ho, sector_stat)
                            age_mari_nok = False

                    if triche_age_mari_nok:
                        ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_mari)

                    osf = 0
                    all_hh, persid, hhid, osf = add_pers(all_hh, osf, sector_stat, ss_name, persid, age_mari, 0, hhid,
                                                         hh_type_id, hh_type, False, 'parent')

                    print("couple ho added")

            #Create single mothers
            elif hh_type == 'single_with_child':

                nbre_single_mom = get_nbre_fe(sector_stat, age, single_mom_age)

                while nbre_single_mom > 0 :

                    all_hh, persid, hhid, nbre_single_mom = add_pers(all_hh, nbre_single_mom, sector_stat, ss_name,
                                                                     persid, age, 1, hhid, hh_type_id, hh_type, True,
                                                                     'parent')

                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    single_mom_age = adapt_nb(sector_stat, single_mom_age, age)

                    print("single mom added of age", age)

                    nbr_children = get_nb_children()
                    too_many_children = False

                    while nbr_children > 0 :

                        age_child_nok = True
                        i = 0

                        while age_child_nok:
                            i += 1
                            age_child = get_age_child(age)
                            sex_child = get_sex_child()
                            age_child_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)


                            if i >= 105:
                                if sex_child == 0:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32, 0), ss_age_ho,
                                                                                         sector_stat, age)
                                elif sex_child == 1:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32,0), ss_age_fe,
                                                                                         sector_stat, age)
                                age_child_nok = False

                        if not too_many_children:
                            if sex_child == 0 :
                                ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_child)
                            elif sex_child == 1:
                                ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_child)

                            all_hh, persid, hhid, nbr_children = add_pers(all_hh, nbr_children, sector_stat, ss_name,
                                                                          persid, age_child, sex_child, hhid,
                                                                          hh_type_id, hh_type, True, 'child')

                            print("child of single mom added")
                        else :
                            nbr_children = 0

                    hhid += 1

            #Create couples with child
            elif hh_type == 'couple_with_child':

                nbre_couple_mom = get_nbre_fe(sector_stat, age, couple_child_age_mom)

                while nbre_couple_mom > 0 :

                    all_hh, persid, hhid, nbre_couple_mom = add_pers(all_hh, nbre_couple_mom, sector_stat, ss_name,
                                                                     persid, age, 1, hhid, hh_type_id, hh_type, True,
                                                                     'parent')
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    couple_child_age_mom = adapt_nb(sector_stat, couple_child_age_mom, age)
                    print("mom added of age", age)

                    age_mari_nok = True
                    triche_age_mari_nok = True
                    i = 0
                    while age_mari_nok:
                        i += 1
                        age_mari = get_age_mari(age)
                        age_mari_nok = check_age_mari(sector_stat, ss_age_ho, age_mari)
                        if i >= 105:
                            age_mari, too_many = get_closest_not_empty(age, ss_age_ho, sector_stat)
                            age_mari_nok = False

                    if triche_age_mari_nok:
                        ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_mari)

                    osf = 0
                    all_hh, persid, hhid, osf = add_pers(all_hh, osf, sector_stat, ss_name, persid, age_mari, 0, hhid,
                                                         hh_type_id, hh_type, True, 'parent')

                    print("dad added of age", age_mari)

                    nbr_children = get_nb_children()
                    print(nbr_children, 'nbr children')
                    first_child = True
                    too_many_children = False

                    while nbr_children > 0 :

                        age_child_nok = True
                        i = 0
                        while age_child_nok:
                            i += 1
                            age_child = get_age_child(age)
                            print(age_child)
                            sex_child = get_sex_child()
                            age_child_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)
                            if i >= 105:
                                if sex_child == 0:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32, 0), ss_age_ho,
                                                                                         sector_stat, age)
                                elif sex_child == 1:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32,0), ss_age_fe,
                                                                                         sector_stat, age)
                                age_child_nok = False

                        if not too_many_children:
                            if sex_child == 0 :
                                ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_child)
                            elif sex_child == 1:
                                ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_child)

                            all_hh, persid, hhid, nbr_children = add_pers(all_hh, nbr_children, sector_stat, ss_name,
                                                                          persid, age_child, sex_child, hhid,
                                                                          hh_type_id, hh_type, True, 'child')

                            print("child of couple added")
                        else :
                            nbr_children = 0
                    hhid += 1

    #Create single men
    for age in range(94, 15, -1):

        hh_type = 'single'
        hh_type_id = get_hh_id(hh_type)

        nbre_ho_single = get_nbre_fe(sector_stat, age, single_age_ho)

        while nbre_ho_single >  0:

            all_hh, persid, hhid, nbre_ho_single = add_pers(all_hh, nbre_ho_single, sector_stat, ss_name, persid, age,
                                                            0, hhid, hh_type_id, hh_type, False, 'parent')

            ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age)
            single_age_ho = adapt_nb(sector_stat, single_age_ho, age)
            print("single ho added")
            print(nbre_ho_single, '#single ho to add of age', age)

    #Create single fathers
    hh_type = 'single_with_child'
    hh_type_id = get_hh_id(hh_type)

    nbre_single_dad = get_nbre_single_dad(sector_stat, single_dad)

    while nbre_single_dad > 0:

        age_dad_nok = True
        i = 0
        while age_dad_nok :
            i += 1

            age_dad = get_age_dad()
            age_dad_nok = check_age_mari(sector_stat, ss_age_ho, age_dad)

            if i >= 95:
                age_dad, too_many = get_closest_not_empty(43, ss_age_ho, sector_stat)


        all_hh, persid, hhid, nbre_single_dad = add_pers(all_hh, nbre_single_dad, sector_stat, ss_name, persid, age_dad,
                                                         0, hhid, hh_type_id, hh_type, True, 'parent')

        ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_dad)
        single_dad = adapt_nb_single_dad(sector_stat, single_dad)

        print("single dad added")

        nbr_children = get_nb_children()
        too_many_children = False

        while nbr_children > 0 :

            age_child_nok = True
            i = 0
            while age_child_nok:
                i += 1
                age_child = get_age_child(age_dad-3)
                sex_child = get_sex_child()
                age_child_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)

                if i >= 105:
                    if sex_child == 0:
                        age_child, too_many_children = get_closest_not_empty(max(age-36, 0), ss_age_ho, sector_stat,
                                                                             age_dad)
                    elif sex_child == 1:
                        age_child, too_many_children = get_closest_not_empty(max(age-36,0), ss_age_fe, sector_stat,
                                                                             age_dad)
                    age_child_nok = False

            if not too_many_children:
                if sex_child == 0 :
                    ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_child)
                elif sex_child == 1:
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_child)

                all_hh, persid, hhid, nbr_children = add_pers(all_hh, nbr_children, sector_stat, ss_name, persid, age_child, sex_child, hhid, hh_type_id, hh_type, True, 'child')

                print("child of single dad added")
            else :
                nbr_children = 0

        hhid += 1

    #Create colocations
    hh_type = 'colloc'
    hh_type_id = get_hh_id(hh_type)

    nbre_colloc_fe = get_nbre_fe_colloc(sector_stat, colloc_fe)

    while nbre_colloc_fe  > 0 :

        age_fe_nok = True
        triche_age_fe_nok = True
        i = 0
        while age_fe_nok:
            i += 1
            age_fe = get_age_colloc()
            age_fe_nok = check_age_mari(sector_stat, ss_age_fe, age_fe)

            if i >= 105:
                age_fe, too_many = get_closest_not_empty(52, ss_age_fe, sector_stat)
                age_fe_nok = False

        if triche_age_fe_nok:
            ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_fe)
            colloc_fe = adapt_nb_colloc_fe(sector_stat, colloc_fe)

        all_hh, persid, hhid, nbre_colloc_fe = add_pers(all_hh, nbre_colloc_fe, sector_stat, ss_name, persid, age_fe, 1,
                                                        hhid, hh_type_id, hh_type, True, 'parent')

        print("colloc 1 added")

        nbr_colloc = get_nb_colloc()
        too_many_colloc = False

        while nbr_colloc > 0 :

            age_colloc_nok = True
            i = 0
            while age_colloc_nok:
                i += 1
                age_colloc = get_age_mari(age_fe)
                sex_colloc = get_sex_child()
                age_colloc_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_colloc, sex_colloc)

                if i >= 105:
                    if sex_colloc == 0:
                        age_colloc, too_many_colloc = get_closest_not_empty(age_fe, ss_age_ho, sector_stat, 121)
                    elif sex_colloc == 1:
                        age_colloc, too_many_colloc = get_closest_not_empty(age_fe, ss_age_fe, sector_stat, 121)
                    age_colloc_nok = False

            if not too_many_colloc:
                if sex_colloc == 0 :
                    ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_colloc)
                    colloc_ho = adapt_nb_colloc_ho(sector_stat, colloc_ho)
                elif sex_colloc == 1:
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_colloc)
                    colloc_fe = adapt_nb_colloc_fe(sector_stat, colloc_fe)
                    nbre_colloc_fe -= 1

                all_hh, persid, hhid, nbr_colloc = add_pers(all_hh, nbr_colloc, sector_stat, ss_name, persid,
                                                            age_colloc, sex_colloc, hhid, hh_type_id, hh_type, True,
                                                            'parent')

                print("colloc added")
            else :
                nbr_colloc = 0

        hhid += 1

    nbre_colloc_ho = get_nbre_ho_colloc(sector_stat, colloc_ho)

    while nbre_colloc_ho  > 0 :

        age_ho_nok = True
        triche_age_ho_nok = True
        i = 0
        while age_ho_nok:
            i += 1
            age_ho = get_age_colloc()
            age_ho_nok = check_age_mari(sector_stat, ss_age_ho, age_ho)

            if i >= 95:
                age_ho, too_many = get_closest_not_empty(52, ss_age_ho, sector_stat)
                age_ho_nok = False

        if triche_age_ho_nok:
            ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_ho)
            colloc_ho = adapt_nb_colloc_ho(sector_stat, colloc_ho)

        all_hh, persid, hhid, nbre_colloc_ho = add_pers(all_hh, nbre_colloc_ho, sector_stat, ss_name, persid, age_ho, 0,
                                                        hhid, hh_type_id, hh_type, True, 'parent')

        print("colloc 1 added")

        nbr_colloc = get_nb_colloc()
        too_many_colloc = False

        while nbr_colloc > 0 :

            age_colloc_nok = True
            i = 0
            while age_colloc_nok:
                i += 1
                age_colloc = get_age_mari(age_ho)
                sex_colloc = 0
                age_colloc_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_colloc, sex_colloc)

                if i >= 95:
                    age_colloc, too_many_colloc = get_closest_not_empty(age_ho, ss_age_ho, sector_stat, 121)
                    age_colloc_nok = False

            if not too_many_colloc:
                ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_colloc)
                colloc_ho = adapt_nb_colloc_ho(sector_stat, colloc_ho)
                nbre_colloc_ho -= 1

                all_hh, persid, hhid, nbr_colloc = add_pers(all_hh, nbr_colloc, sector_stat, ss_name, persid,
                                                            age_colloc, sex_colloc, hhid, hh_type_id, hh_type, True,
                                                            'parent')

                print("colloc added")
            else :
                nbr_colloc = 0

        hhid += 1

    #Create collectif
    hh_type = 'collectif'
    hh_type_id = get_hh_id(hh_type)

    for age in range(104, -1, -1):

        nbre_fe = get_nbre_fe(sector_stat, age, ss_age_fe)
        i = 0
        while nbre_fe > 0:
            i +=1
            all_hh, persid, hhid, nbre_fe = add_pers(all_hh, nbre_fe, sector_stat, ss_name, persid, age, 1, hhid,
                                                     hh_type_id, hh_type, False, 'parent')

            ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
            if i > 1400:
                all_hh.to_csv('error collectif femmes_v2.csv')
                nbre_fe = 0

            print("collectif fe added")

    for age in range(94, -1, -1):

        nbre_ho = get_nbre_fe(sector_stat, age, ss_age_ho)
        i = 0
        while nbre_ho > 0:
            i +=1
            all_hh, persid, hhid, nbre_ho = add_pers(all_hh, nbre_ho, sector_stat, ss_name, persid, age, 0, hhid,
                                                     hh_type_id, hh_type, False, 'parent')

            ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age)
            if i > 1400:
                all_hh.to_csv('error collectif hommes_v2.csv')
                nbre_ho = 0
            print("collectif ho added")

    print('all_hh', all_hh)
    all_hh.to_csv('./hh_'+str(ss_name)+'.csv')

    return all_hh, persid, hhid

def create_households_for_all_ss(all_hh, SectorStats, ss_age_fe, single_age_fe, couple_age_fe, ss_age_ho,
                                 single_mom_age, couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, single_dad):
    """
    Create all people

    :param all_hh: pd.DataFrame; table where to add the new households
    :param SectorStats: list of all sector statistics
    :param ss_age_fe: pd.DataFrame; table with places per sector statistics and per age for women
    :param single_age_fe: pd.DataFrame; table with places per sector statistics and per age for women living alone
    :param couple_age_fe: pd.DataFrame; table with places per sector statistics and per age of women for couples without
    child
    :param ss_age_ho: pd.DataFrame; table with places per sector statistics and per age for men
    :param single_mom_age: pd.DataFrame; table with places per sector statistics and per age for single mothers
    :param couple_child_age_mom: pd.DataFrame; table with places per sector statistics and per age of women for couples
    with child
    :param colloc_fe: pd.DataFrame; table with places per sector statistics and per age for women living in colocation
    :param colloc_ho: pd.DataFrame; table with places per sector statistics and per age for men living in colocation
    :param single_age_ho: pd.DataFrame; table with places per sector statistics and per age for men living alone
    :param single_dad: pd.DataFrame; table with places per sector statistics and per age for single fathers

    :return: all_hh with the people added
    """
    persid = 0
    hhid = 0

    for ss in SectorStats:
    #for i in range(356, 725):
        #ss = SectorStats.loc[i]
        print(ss, 'ss')
        all_hh, persid, hhid = create_households(all_hh, ss, persid, hhid, ss_age_fe, single_age_fe, couple_age_fe,
                                                 ss_age_ho, single_mom_age, couple_child_age_mom, colloc_fe, colloc_ho,
                                                 single_age_ho, single_dad)

    return all_hh


########################################################################################################################
#       Run                                                                                                            #
########################################################################################################################
#all_hh = pd.read_csv('all_hh_last_2.csv')
#all_hh.drop(columns=["Unnamed: 0"], inplace=True)
#print(all_hh)
all_hh = pd.DataFrame(columns=["SectorStatID", "SectorStatName", "PersID", "Age", "GenderID", "GenderName",
                               "ChildOrParent", "HouseholdID", "HouseholdTypeID", "HouseHorldTypeName"])

all_hh = create_households_for_all_ss(all_hh, SectorStats, ss_age_fe, single_age_fe, couple_age_fe, ss_age_ho, single_mom_age,
                                      couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, single_dad)
all_hh.to_csv('./hh/all_hh_enooorme.csv')
