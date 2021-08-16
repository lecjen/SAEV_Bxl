


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

#df = pandas.read_csv(filepath, sep='delimiter', header=None)
ss_age_fe = pd.read_csv('SectorStat_Age_Femme.csv', sep=';')
ss_age_fe= comma_to_dot(ss_age_fe)
ss_age_fe = clean_col_names(ss_age_fe)
print(ss_age_fe)

ss_age_ho = pd.read_csv('SectorStat_Age_Hommes.csv', sep=';')
ss_age_ho= comma_to_dot(ss_age_ho)
ss_age_ho = clean_col_names(ss_age_ho)
ss_age_ho.drop(columns=['98', '99', '100', '101', '102', '103', '104', '105', '106', '107'], inplace=True)
print(ss_age_ho.columns)
print(ss_age_ho)

SectorStats = ss_age_fe['Code']
print(SectorStats)

def add_pers(all_hh, nb, sector_stat, ss_name, persid, age, gender_id):
    
    gender = get_gender(gender_id)
    
    all_hh.loc[persid]=[sector_stat, ss_name, persid, age, gender_id, gender]
    persid +=1
    nb -=1
    
    return all_hh, persid, nb

def get_gender(gender_id):
    if gender_id == 1:
        gender = 'female'
    elif gender_id == 0 :
        gender = 'male'
    else:
        print('Error: Gender Id unknow. Should be 1 or 0')
    
    return gender

def get_nbre_fe(sector_stat, age, ss_age_fe):
    fe_ss = ss_age_fe[ss_age_fe.Code==sector_stat]
    nbre = fe_ss[str(age)]
    
    
    index = ss_age_fe.index
    ind = index[ss_age_fe['Code']== sector_stat][0]
    
    return round(float(nbre.loc[ind]))


def get_ss_name(ss, ss_age_fe):
    ss_row = ss_age_fe[ss_age_fe.Code==ss]
    name = ss_row['Territoire']
    
    index = ss_age_fe.index
    ind = index[ss_age_fe['Code']== ss][0]
    
    #print(name)
    #print(ind)
    return name.loc[ind]

def create_people(people, ss, persid, ss_age_fe, ss_age_ho):
    ss_name = get_ss_name(ss, ss_age_fe)
    
    for age in range(0, 104):
        nbre_fe = get_nbre_fe(ss, age, ss_age_fe)
                
        while nbre_fe > 0:
            
            people, persid, nbre_fe = add_pers(people, nbre_fe, ss, ss_name, persid, age, 1) 
        
            print("fe added")    
    
    for age in range(0, 94):
        nbre_ho = get_nbre_fe(ss, age, ss_age_ho)
                
        while nbre_ho > 0:
            
            people, persid, nbre_ho = add_pers(people, nbre_ho, ss, ss_name, persid, age, 0) 
        
            print("ho added")  
            
    return people, persid

def create_people_for_all_ss(people, SectorStats, ss_age_fe, single_age_fe):

    persid = 0

    for ss in SectorStats:
        people, persid = create_people(people, ss, persid, ss_age_fe, ss_age_ho)
        
        
    return people

#print(get_nbre_fe('21001A472', 103, ss_age_fe))
people = pd.DataFrame(columns=['SectorStatID', 'SectorStatName', 'PersID', 'Age', 'GenderID', 'GenderName']) #ssLat, ssLong

people = create_people_for_all_ss(people, ['21001A041','21001A472'], ss_age_fe, ss_age_ho)
print(people)
people.to_csv('people.csv')
