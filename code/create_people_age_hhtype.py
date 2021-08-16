

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

single_age_fe = pd.read_csv('Single_Age_Femmes.csv', sep=';')
single_age_fe= comma_to_dot(single_age_fe)
single_age_fe = clean_col_names(single_age_fe)
print(single_age_fe)

def create_people_single(people, ss, persid, ss_age_fe, ss_age_ho):
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
