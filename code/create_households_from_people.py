
import pandas as pd
import random

#hh_list = ['couple_with_child', 'couple_no_child', 'single', 'single_with_child', 'colloc', 'collectif']

people = pd.read_csv('people.csv')
people.drop(columns=['Unnamed: 0'], inplace = True)
print(people)


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



single_age_fe = pd.read_csv('Single_Age_Femmes.csv', sep=';')
single_age_fe= comma_to_dot(single_age_fe)
single_age_fe = clean_col_names(single_age_fe)
print(single_age_fe)

single_age_ho = pd.read_csv('Single_Age_Hommes.csv', sep=';')
single_age_ho= comma_to_dot(single_age_ho)
single_age_ho = clean_col_names(single_age_ho)
print(single_age_ho)

couple_age_fe = pd.read_csv('Couple_Age_Femme.csv', sep=';')
couple_age_fe= comma_to_dot(couple_age_fe)
couple_age_fe = clean_col_names(couple_age_fe)
print(couple_age_fe)

colloc_fe = pd.read_csv('Colloc_Femmes.csv', sep=';')
colloc_fe= comma_to_dot(colloc_fe)
colloc_fe = clean_col_names(colloc_fe)
print(colloc_fe)

colloc_ho = pd.read_csv('Colloc_Hommes.csv', sep=';')
colloc_ho= comma_to_dot(colloc_ho)
colloc_ho = clean_col_names(colloc_ho)
print(colloc_ho)

def get_hh_id(hh_type):
    
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

def check_pers_possible(people, ss, age, sex):
    possible_pers = people[(people.Age==age) & (people.GenderID == sex) & (people.SectorStatID == ss)]
    
    if len(possible_pers) == 0:
        poss = False
    
    else:
        poss = True
    
    return poss

def add_pers_to_hh(all_hh, people, nbre_pers, ss, age, sex, hhid, hh_type_id, hh_type):
    
    possible_pers = people[(people.Age==age) & (people.GenderID == sex) & (people.SectorStatID == ss)]
    
    if len(possible_pers) == 0:
        nbre_pers -=1
        imposs = True
    
    else:
        ind =  possible_pers.index[0]
        ss_name = possible_pers.loc[ind, "SectorStatName"]
        persid = possible_pers.loc[ind, "PersID"]
        gender = possible_pers.loc[ind, "GenderName"]
        all_hh.loc[ind]=[ss, ss_name, persid, age, sex, gender, hhid, hh_type_id, hh_type]
        people.drop([ind], inplace=True)
        nbre_pers -=1
        imposs = False
    
    return all_hh, nbre_pers, people, imposs
            
def get_nbre_pers(sector_stat, age, ss_age_fe):
    fe_ss = ss_age_fe[ss_age_fe.Code==sector_stat]
    nbre = fe_ss[str(age)]
    
    
    index = ss_age_fe.index
    ind = index[ss_age_fe['Code']== sector_stat][0]
    
    return round(float(nbre.loc[ind]))

def create_single(hhid, all_hh, single_age, people, sex, ss):
    hh_type = 'single'
    hh_type_id = get_hh_id(hh_type)
    
    if sex == 0:
        max_age = 95
        name = 'fe'
    elif sex == 1:
        max_age = 105
        name = 'ho'
    
    for age in range(0, max_age):
                
        nbre_single = get_nbre_pers(ss, age, single_age)
                
        while nbre_single > 0:
            
            
            all_hh, nbre_single, people, imposs = add_pers_to_hh(all_hh, people, nbre_single, ss, age, sex, hhid, hh_type_id, hh_type)
            #TODO gerer imposs
            
            print("single added", name)
            
            hhid +=1
    return all_hh, hhid, people

def get_closest_mari(people, age, ss):
    
    for i in range(0, 95):
        
        age_tmp = age-i
        
        exist = check_pers_possible(people, ss, age_tmp, 0)
        
        if exist:
            age_mari = age_tmp
            break
        
        else:
            age_tmp = age+i
            exist = check_pers_possible(people, ss, age_tmp, 0)
        
            if exist:
                age_mari = age_tmp
                break
    
    return age_mari

def get_closest_child(people, age, ss, sex):
    age_ideal = age - 30
    
    age_child = -1
    for i in range(0, 105):
        
        age_tmp = age_ideal-i
        
        exist = check_pers_possible(people, ss, age_tmp, sex)
        
        if exist:
            age_child = age_tmp
            break
        
        else:
            age_tmp = age_ideal+i
            if age_tmp < age:
                
                exist = check_pers_possible(people, ss, age_tmp, sex)
            
                if exist:
                    age_child = age_tmp
                    break
    
    if age_child == -1:
        imposs = True
    else :
        imposs = False
        
    return age_child, imposs
        

def create_couple(hhid, hh_type, all_hh, file, people, ss, with_child = False):

    hh_type_id = get_hh_id(hh_type)
    
    for age in range(0, 105):
                
        nbre_fe = get_nbre_pers(ss, age, file)
                
        while nbre_fe > 0:
            
            all_hh, nbre_fe, people, imposs = add_pers_to_hh(all_hh, people, nbre_fe, ss, age, 1, hhid, hh_type_id, hh_type)
            
            if imposs:
                nbre_fe == 0
            else:
                print("fe added")
                
                age_mari = get_closest_mari(people, ss, age)
                
                osf = 0
                
                all_hh, osf, people, imposs = add_pers_to_hh(all_hh, people, osf, ss, age_mari, 0, hhid, hh_type_id, hh_type)
            
                if imposs:
                    error
                else:
                    print("mari added")
            
            #TODO with child
            hhid +=1
            
    return all_hh, hhid, people


def get_nb_children():
    #TODO ameliorer
    
    nb_child = random.randrange(1, 4,1)
    
    return nb_child

def get_sex():
    #TODO ameliorer
    
    sex = random.randrange(1, 3,1)
    
    return sex

def create_children(hhid, hh_type, all_hh, people, ss, age_parent):

    hh_type_id = get_hh_id(hh_type)
    
    nb_children = get_nb_children()
                
    first_child = True
    too_many_children = False
    
    while nb_children > 0:
        
            sex = get_sex()
            age_child, imposs = get_closest_child(people, age_parent, ss, sex)
            
            if imposs and not first_child :
                nb_children = 0
            elif not imposs:
                all_hh, nb_children, people, imposs = add_pers_to_hh(all_hh, people, nb_children, ss, age_child, sex, hhid, hh_type_id, hh_type)
                print('child added')
    return all_hh, people

def create_single_mom(hhid, all_hh, single_mom, people, ss):
    hh_type = 'single_with_child'
    hh_type_id = get_hh_id(hh_type)
    
    for age in range(0, 105):
                
        nbre_single = get_nbre_pers(ss, age, single_mom)
                
        while nbre_single > 0:
            
            
            all_hh, nbre_single, people, imposs = add_pers_to_hh(all_hh, people, nbre_single, ss, age, 1, hhid, hh_type_id, hh_type)
            #TODO gerer imposs
            
            print("single mom added")
            all_hh, people = create_children(hhid, hh_type, all_hh, people, ss, age)
            hhid +=1
    return all_hh, hhid, people

def create_couple_with_child(hhid, hh_type, all_hh, file, people, ss, with_child = False):

    hh_type_id = get_hh_id(hh_type)
    
    for age in range(0, 105):
                
        nbre_fe = get_nbre_pers(ss, age, file)
                
        while nbre_fe > 0:
            
            all_hh, nbre_fe, people, imposs = add_pers_to_hh(all_hh, people, nbre_fe, ss, age, 1, hhid, hh_type_id, hh_type)
            
            if imposs:
                nbre_fe == 0
            else:
                print("fe added")
                
                age_mari = get_closest_mari(people, ss, age)
                
                osf = 0
                
                all_hh, osf, people, imposs = add_pers_to_hh(all_hh, people, osf, ss, age_mari, 0, hhid, hh_type_id, hh_type)
            
                if imposs:
                    error
                else:
                    print("mari added")
                    all_hh, people = create_children(hhid, hh_type, all_hh, people, ss, age)
                    
            
            #TODO with child
            hhid +=1
            
    return all_hh, hhid, people

#TODO single dad
def get_nbre_ho_colloc(sector_stat, colloc_ho):
    ho_ss = colloc_ho[colloc_ho.Code==sector_stat]
    nbre = ho_ss['#hommes colloc dans secteur stat']
    
    
    index = colloc_ho.index
    ind = index[colloc_ho['Code']== sector_stat][0]
    
    return round(float(nbre.loc[ind]))

def get_nbre_fe_colloc(sector_stat, colloc_fe):
    fe_ss = colloc_fe[colloc_fe.Code==sector_stat]
    nbre = fe_ss['#femmes colloc dans secteur stat']
    
    
    index = colloc_fe.index
    ind = index[colloc_fe['Code']== sector_stat][0]
    
    return round(float(nbre.loc[ind]))
    
    
def create_colloc(hhid, all_hh, people, ss, colloc_fe, colloc_ho):
    hh_type = 'colloc'
    
    nbre_fe_colloc= get_nbre_fe_colloc(ss, colloc_fe)
    nbre_ho_colloc= get_nbre_ho_colloc(ss, colloc_ho)

    hh_type_id = get_hh_id(hh_type)
    
    nb_children = get_nb_children()
                INCIPIT
    while nb_children > 0:
        
            sex = get_sex()
            age_child, imposs = get_closest_child(people, age_parent, ss, sex)
            
            if imposs and not first_child :
                nb_children = 0
            elif not imposs:
                all_hh, nb_children, people, imposs = add_pers_to_hh(all_hh, people, nb_children, ss, age_child, sex, hhid, hh_type_id, hh_type)
                print('child added')
    return all_hh, people

all_hh = pd.DataFrame(columns=['SectorStatID', 'SectorStatName', 'PersID', 'Age', 'GenderID', 'GenderName', 'HouseholdID',
                                   'HouseholdTypeID', 'HouseHorldTypeName']) #ssLat, ssLong

#all_hh, hhid, people = create_single(0, all_hh, single_age_ho, people, 0, '21001A041')
all_hh, hhid, people = create_couple(0, 'couple', all_hh, couple_age_fe, people, '21001A041')

print(all_hh)