
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

couple_child_age_mom = pd.read_csv('Couple_enfants_age_mere.csv', sep=';')
couple_child_age_mom= comma_to_dot(couple_child_age_mom)
couple_child_age_mom = clean_col_names(couple_child_age_mom)
print(couple_child_age_mom)

couple_age_fe = pd.read_csv('Couple_Age_Femme.csv', sep=';')
couple_age_fe= comma_to_dot(couple_age_fe)
couple_age_fe = clean_col_names(couple_age_fe)
print(couple_age_fe)

single_age_fe = pd.read_csv('Single_Age_Femmes.csv', sep=';')
single_age_fe= comma_to_dot(single_age_fe)
single_age_fe = clean_col_names(single_age_fe)
print(single_age_fe)

single_age_ho = pd.read_csv('Single_Age_Hommes.csv', sep=';')
single_age_ho= comma_to_dot(single_age_ho)
single_age_ho = clean_col_names(single_age_ho)
print(single_age_ho)

single_mom_age = pd.read_csv('Single_parent_Age_Femmes.csv', sep=';')
single_mom_age= comma_to_dot(single_mom_age)
single_mom_age = clean_col_names(single_mom_age)
print(single_mom_age)

single_dad = pd.read_csv('Single_parent_Hommes.csv', sep=';')
single_dad= comma_to_dot(single_dad)
single_dad = clean_col_names(single_dad)
print(single_dad)

colloc_fe = pd.read_csv('Colloc_Femmes.csv', sep=';')
colloc_fe= comma_to_dot(colloc_fe)
colloc_fe = clean_col_names(colloc_fe)
print(colloc_fe)

colloc_ho = pd.read_csv('Colloc_Hommes.csv', sep=';')
colloc_ho= comma_to_dot(colloc_ho)
colloc_ho = clean_col_names(colloc_ho)
print(colloc_ho)
"""
place_child = pd.read_csv('Place_enfants.csv', sep=';')
print(place_child)
"""
SectorStats = ss_age_fe['Code']
print(SectorStats)


def get_nbre_fe(sector_stat, age, ss_age_fe):
    fe_ss = ss_age_fe[ss_age_fe.Code==sector_stat]
    nbre = fe_ss[str(age)]
    
    
    index = ss_age_fe.index
    ind = index[ss_age_fe['Code']== sector_stat][0]
    
    return round(float(nbre.loc[ind]))

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

def get_nbre_single_dad(sector_stat, single_dad):
    fe_ss = single_dad[single_dad.Code==sector_stat]
    nbre = fe_ss['single dad']
    
    
    index = single_dad.index
    ind = index[single_dad['Code']== sector_stat][0]
    
    return round(float(nbre.loc[ind]))

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

def get_ss_name(ss, ss_age_fe):
    ss_row = ss_age_fe[ss_age_fe.Code==ss]
    name = ss_row['Territoire']
    
    index = ss_age_fe.index
    ind = index[ss_age_fe['Code']== ss][0]
    
    #print(name)
    #print(ind)
    return name.loc[ind]

def get_gender(gender_id):
    if gender_id == 1:
        gender = 'female'
    elif gender_id == 0 :
        gender = 'male'
    else:
        print('Error: Gender Id unknow. Should be 1 or 0')
    
    return gender

def add_pers(all_hh, nb, sector_stat, ss_name, persid, age, gender_id, hhid, hh_type_id, hh_type, same_hh, child_or_parent):
    
    gender = get_gender(gender_id)
    
    all_hh.loc[persid]=[sector_stat, ss_name, persid, age, gender_id, gender, child_or_parent, hhid, hh_type_id, hh_type]
    persid +=1
    if not same_hh:
        hhid +=1
    nb -=1
    
    return all_hh, persid, hhid, nb
    
def get_age_mari(age):
    
    age_mari = age + 3 #random.randrange(min(max(16,age-7), 94), min(age+8, 95),1)
    
    return age_mari
    
def check_age_mari(ss, ss_age_ho, age_mari):
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
    index = ss_age_ho.index
    ind = index[ss_age_ho['Code']== sector_stat][0]
    act = ss_age_ho.loc[ind, str(age_mari)]
    print(act, 'act 1')
    act = round(float(act))
    #print(act, 'act 2')
    ss_age_ho.loc[ind, str(age_mari)] = act - 1
    print(ss_age_ho.loc[ind, str(age_mari)], 'act 3')
    
    return ss_age_ho

def adapt_nb_single_dad(sector_stat, single_dad):
    index = single_dad.index
    ind = index[single_dad['Code']== sector_stat][0]
    act = single_dad.loc[ind, 'single dad']
    print(act, 'act 1')
    act = round(float(act)) 
    #print(act, 'act 2')
    single_dad.loc[ind, 'single dad'] = act - 1
    print(single_dad.loc[ind, 'single dad'], 'act 3')
    return single_dad

def adapt_nb_colloc_fe(sector_stat, colloc_fe):
    index = colloc_fe.index
    ind = index[colloc_fe['Code']== sector_stat][0]
    act = colloc_fe.loc[ind, '#femmes colloc dans secteur stat']
    print(act, 'act 1')
    act = round(float(act)) 
    #print(act, 'act 2')
    colloc_fe.loc[ind, '#femmes colloc dans secteur stat'] = act - 1
    print(colloc_fe.loc[ind, '#femmes colloc dans secteur stat'], 'act 3')
    return colloc_fe


def adapt_nb_colloc_ho(sector_stat, colloc_fe):
    index = colloc_fe.index
    ind = index[colloc_fe['Code']== sector_stat][0]
    
    act = colloc_fe.loc[ind, '#hommes colloc dans secteur stat']
    print(act, 'act 1')
    act = round(float(act))
    #print(act, 'act 2')
    colloc_fe.loc[ind, '#hommes colloc dans secteur stat'] = act - 1
    print( colloc_fe.loc[ind, '#hommes colloc dans secteur stat'], 'act 1')
    return colloc_fe

#FROM THESIS
#'Create Cumulative Distribution'
def cdf(weights):
    total=sum(weights); result=[]; cumsum=0
    for w in weights:
        cumsum+=w
        result.append(cumsum/total)
    return result

#FROM THESIS
def get_index(distribution):
    'Revise Traveler Type, In the event of no school assigned (incredibly fringe population < 0.001%)'
    """
    if person[len(person) - 3] == 'NA' and (travelerType == 3 or travelerType == 4 or travelerType == 2 or travelerType == 1):
        travelerType = 6
    """
    dist = distribution #allDistributions[travelerType]
    weights = cdf(dist)
    split = random.random()
    idx = bisect.bisect(weights, split)
    return idx

def get_age_child(age):
    age_child = -1
    while age_child < 0:
        dist = [0.012, 0.087, 0.252, 0.35, 0.229, 0.064, 0.006]
        idx = get_index(dist)
        min_delta_ages = [15, 20, 25, 30, 35, 40, 45]
        delta_age_plus = random.randrange(0, 5,1)
        
        delta_age = min_delta_ages[idx]+delta_age_plus
        if delta_age == 15:
            delta_age = 16
        
        age_child = age - delta_age#random.randrange(max(age-50, 0), max(age-15,0),1)
        
    return age_child

def get_sex_child():
    #TODO ameliorer
    
    sex_child = random.randrange(0, 2,1)
    
    return sex_child


def get_nb_children():
    dist = [0.466, 0.3265, 0.1405, 0.0496, 0.0131, 0.0032, 0.0008, 0.0003]
    nb_child = get_index(dist) + 1#random.randrange(1, 4,1)
    
    return nb_child

def get_nb_colloc():
    #TODO ameliorer
    
    nb_colloc = random.randrange(2, 9, 1)
    
    return nb_colloc

def get_age_dad():
    #TODO ameliorer
    
    age = random.randrange(16, 71,1)
    
    return age

def get_age_colloc():
    #TODO ameliorer
    
    age = random.randrange(16, 71,1)
    
    return age

def get_closest_not_empty(age, ss_age_ho, ss, age_mom = 121, first_child = True):
    if age_mom == 121:
        child = False
    else:
        child = True
        
    ss_row = ss_age_ho[ss_age_ho.Code==ss]
    
    index = ss_age_ho.index
    ind = index[ss_age_ho['Code']== ss][0]
    
    ss_row.drop(columns=['Code', 'Territoire'], inplace=True)
    
    for col in ss_row.columns:
        if col == 'Commune':
            ss_row.drop(columns=[col], inplace = True)
        elif child:
            
            if round(float(ss_row.loc[ind, col])) <= 0 or int(col)> age_mom-16:
                ss_row.drop(columns=[col], inplace = True)
        else: 
            if round(float(ss_row.loc[ind, col])) <= 0:
                ss_row.drop(columns=[col], inplace = True)
                
    for i in range(0, 104):
        if str(age-i) in ss_row.columns:
            new_age = age-i
            too_many = False
            if child:
                break
            elif new_age < 95:
                break
        elif str(age+i) in ss_row.columns and age+i+16 < age_mom:
            new_age = age+i
            too_many = False
            if child:
                break
            elif new_age < 95:
                break
    if len(ss_row.columns) == 0 and first_child:
        new_age = age
        too_many = True
        if not child and new_age > 94:
            new_age = 94
    elif not first_child:
        new_age = age
        too_many = True
        if not child and new_age > 94:
            new_age = 94
    
    else:
        print(age, 'age')
        print(ss_row)
        print(first_child, 'First child')
        new_age = age
        too_many = False
        if not child and new_age > 94:
            new_age = 94
    
    return new_age, too_many
        
    

def check_age_child(ss, ss_age_fe, ss_age_ho, age_child, sex_child):
    
    
    if age_child < 0:
        nok = True
    else:
        if sex_child == 0:
            ss_row = ss_age_ho[ss_age_ho.Code==ss]
            index = ss_age_ho.index
            ind = index[ss_age_ho['Code']== ss][0]
            
        elif sex_child == 1:
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
    
def create_households(all_hh, sector_stat, persid, hhid, ss_age_fe, single_age_fe, couple_age_fe, ss_age_ho, single_mom_age, 
                      couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, single_dad):
    """
    all_hh = pd.DataFrame(columns=['SectorStatID', 'SectorStatName', 'PersID', 'Age', 'GenderID', 'GenderName', 'HouseholdID',
                                   'HouseholdTypeID', 'HouseHorldTypeName']) #ssLat, ssLong
    """    
    hh_list = ['couple_with_child', 'couple_no_child', 'single', 'single_with_child', 'colloc', 'collectif']
    
    ss_name = get_ss_name(sector_stat, ss_age_fe)
    
    for age in range(104, 15, -1):
    
        for hh_type in hh_list:
            hh_type_id = get_hh_id(hh_type)
            
            if hh_type == 'single':
                
                nbre_fe_single = get_nbre_fe(sector_stat, age, single_age_fe)
                
                while nbre_fe_single > 0:
                    
                    all_hh, persid, hhid, nbre_fe_single = add_pers(all_hh, nbre_fe_single, sector_stat, ss_name, persid, age, 1, hhid, hh_type_id, hh_type, False, 'parent')
                    
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    single_age_fe = adapt_nb(sector_stat, single_age_fe, age)
                
                print("single fe added")
            
            elif hh_type == 'couple_no_child':
                
                nbre_fe_couple = get_nbre_fe(sector_stat, age, couple_age_fe)
                
                while nbre_fe_couple > 0 :
                    
                    all_hh, persid, hhid, nbre_fe_couple = add_pers(all_hh, nbre_fe_couple, sector_stat, ss_name, persid, age, 1, hhid, hh_type_id, hh_type, True, 'parent')
                    
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    couple_age_fe = adapt_nb(sector_stat, couple_age_fe, age)
                    
                    print("couple fe added")
                    age_mari_nok = True
                    triche_age_mari_nok = True
                    i = 0
                    while age_mari_nok: #and triche_age_mari_nok:
                        i += 1
                        #print(age)
                        age_mari = get_age_mari(age)
                        #print(age_mari)
                        
                        age_mari_nok = check_age_mari(sector_stat, ss_age_ho, age_mari)
                        
                        if i >= 95:
                            #triche_age_mari_nok = False
                            age_mari, too_many = get_closest_not_empty(age, ss_age_ho, sector_stat)
                            age_mari_nok = False #check_age_mari(sector_stat, ss_age_ho, age_mari)
                            
                    if triche_age_mari_nok:
                        ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_mari)
                    
                    osf = 0
                    all_hh, persid, hhid, osf = add_pers(all_hh, osf, sector_stat, ss_name, persid, age_mari, 0, hhid, hh_type_id, hh_type, False, 'parent')
                    
                    print("couple ho added")
                    
            elif hh_type == 'single_with_child':
             
                nbre_single_mom = get_nbre_fe(sector_stat, age, single_mom_age)
             
                while nbre_single_mom > 0 :
                     
                    all_hh, persid, hhid, nbre_single_mom = add_pers(all_hh, nbre_single_mom, sector_stat, ss_name, persid, age, 1, hhid, hh_type_id, hh_type, True, 'parent')
                    
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    single_mom_age = adapt_nb(sector_stat, single_mom_age, age)
                    
                    print("single mom added of age", age)
                     
                    nbr_children = get_nb_children()
                    first_child = True
                    too_many_children = False
                    
                    while nbr_children > 0 :
                         
                        age_child_nok = True
                        triche_age_child_nok = True
                        i = 0
                         
                        while age_child_nok:  #and triche_age_child_nok :
                            i += 1
                            age_child = get_age_child(age)
                            sex_child = get_sex_child()
                            age_child_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)
                             
                            
                            if i >= 105:
                                #triche_age_child_nok = False
                                if sex_child == 0:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32, 0), ss_age_ho, sector_stat, age, first_child)
                                elif sex_child == 1:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32,0), ss_age_fe, sector_stat, age, first_child)
                                age_child_nok = False #check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)
                            
                        if not too_many_children:
                            if sex_child == 0 :
                                ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_child)
                            elif sex_child == 1:
                                ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_child)
                             
                            all_hh, persid, hhid, nbr_children = add_pers(all_hh, nbr_children, sector_stat, ss_name, persid, age_child, sex_child, hhid, hh_type_id, hh_type, True, 'child')
                    
                            print("child of single mom added")
                            first_child = False
                        else :
                            nbr_children = 0
                            
                        
                        
                        
                    
                    hhid += 1
                  
            elif hh_type == 'couple_with_child':
             
                nbre_couple_mom = get_nbre_fe(sector_stat, age, couple_child_age_mom)
             
                while nbre_couple_mom > 0 :
                     
                    all_hh, persid, hhid, nbre_couple_mom = add_pers(all_hh, nbre_couple_mom, sector_stat, ss_name, persid, age, 1, hhid, hh_type_id, hh_type, True, 'parent')
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
                    couple_child_age_mom = adapt_nb(sector_stat, couple_child_age_mom, age)
                    print("mom added of age", age)
                       
                    age_mari_nok = True
                    triche_age_mari_nok = True
                    i = 0
                    while age_mari_nok: #and triche_age_mari_nok:
                        i += 1
                        age_mari = get_age_mari(age)
                        age_mari_nok = check_age_mari(sector_stat, ss_age_ho, age_mari)
                        if i >= 105:
                            #triche_age_mari_nok = False
                            age_mari, too_many = get_closest_not_empty(age, ss_age_ho, sector_stat)
                            age_mari_nok = False #check_age_mari(sector_stat, ss_age_ho, age_mari)
                            
                    if triche_age_mari_nok:
                        ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_mari)
                    
                    osf = 0
                    all_hh, persid, hhid, osf = add_pers(all_hh, osf, sector_stat, ss_name, persid, age_mari, 0, hhid, hh_type_id, hh_type, True, 'parent')
            
                    print("dad added of age", age_mari)
                    
                    nbr_children = get_nb_children()
                    print(nbr_children, 'nbr children')
                    first_child = True
                    too_many_children = False
                    
                    while nbr_children > 0 :
                    
                        age_child_nok = True
                        triche_age_child_nok = True
                        i = 0
                        while age_child_nok: #and triche_age_child_nok:
                            i += 1 
                            #print(age)
                            age_child = get_age_child(age)
                            print(age_child)
                            sex_child = get_sex_child()
                            age_child_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)
                            if i >= 105:
                                print("depassé")
                                #triche_age_child_nok = False
                                if sex_child == 0:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32, 0), ss_age_ho, sector_stat, age, first_child)
                                elif sex_child == 1:
                                    age_child, too_many_children = get_closest_not_empty(max(age-32,0), ss_age_fe, sector_stat, age, first_child)
                                age_child_nok = False
                                #age_child_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)
                            
                        if not too_many_children:
                            if sex_child == 0 :
                                ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_child)
                            elif sex_child == 1:
                                ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_child)
                             
                            all_hh, persid, hhid, nbr_children = add_pers(all_hh, nbr_children, sector_stat, ss_name, persid, age_child, sex_child, hhid, hh_type_id, hh_type, True, 'child')
                    
                            print("child of couple added")
                            first_child = False
                        else :
                            nbr_children = 0
                            
                        
                            
                    
                    hhid += 1
    #singe man                    
    for age in range(94, 15, -1):
    
            hh_type = 'single'
            hh_type_id = get_hh_id(hh_type)
            
                
            nbre_ho_single = get_nbre_fe(sector_stat, age, single_age_ho)
            
            while nbre_ho_single >  0:
                
                all_hh, persid, hhid, nbre_ho_single = add_pers(all_hh, nbre_ho_single, sector_stat, ss_name, persid, age, 0, hhid, hh_type_id, hh_type, False, 'parent')
                
                ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age)     
                single_age_ho = adapt_nb(sector_stat, single_age_ho, age)  
                print("single ho added")
                print(nbre_ho_single, '#single ho to add of age', age)
                
    #'single_with_child' dad
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
                age_mari_nok = False
                #age_mari_nok = check_age_mari(sector_stat, ss_age_ho, age_dad)
                                    
        
        all_hh, persid, hhid, nbre_single_dad = add_pers(all_hh, nbre_single_dad, sector_stat, ss_name, persid, age_dad, 0, hhid, hh_type_id, hh_type, True, 'parent')
            
        ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_dad)
        single_dad = adapt_nb_single_dad(sector_stat, single_dad)
            
        print("single dad added")
             
        nbr_children = get_nb_children()
        first_child = True
        too_many_children = False
        
        while nbr_children > 0 :
             
            age_child_nok = True

            triche_age_child_nok = True
            i = 0
            while age_child_nok: # and triche_age_child_nok:
                i += 1         
                age_child = get_age_child(age_dad-3)
                sex_child = get_sex_child()
                age_child_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)
                
                if i >= 105:
                    #triche_age_child_nok = False
                    if sex_child == 0:
                        age_child, too_many_children = get_closest_not_empty(max(age-36, 0), ss_age_ho, sector_stat, age_dad, first_child)
                    elif sex_child == 1:
                        age_child, too_many_children = get_closest_not_empty(max(age-36,0), ss_age_fe, sector_stat, age_dad, first_child)
                    age_child_nok = False # check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_child, sex_child)
                
            if not too_many_children:
                if sex_child == 0 :
                    ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_child)
                elif sex_child == 1:
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_child)
                 
                all_hh, persid, hhid, nbr_children = add_pers(all_hh, nbr_children, sector_stat, ss_name, persid, age_child, sex_child, hhid, hh_type_id, hh_type, True, 'child')
        
                print("child of single dad added")
                first_child = False
            else :
                nbr_children = 0
                
            
                        
        
        hhid += 1
      

    hh_type = 'colloc'            
    hh_type_id = get_hh_id(hh_type)
                     
    nbre_colloc_fe = get_nbre_fe_colloc(sector_stat, colloc_fe)
                     
    while nbre_colloc_fe  > 0 :
        
        age_fe_nok = True
        triche_age_fe_nok = True
        i = 0
        while age_fe_nok: # and triche_age_fe_nok:
            i += 1             
        #while age_fe_nok :
            age_fe = get_age_colloc()
            age_fe_nok = check_age_mari(sector_stat, ss_age_fe, age_fe)
            
            
            if i >= 105:
                #triche_age_fe_nok = False
                age_fe, too_many = get_closest_not_empty(52, ss_age_fe, sector_stat)
                age_fe_nok = False #check_age_mari(sector_stat, ss_age_fe, age_fe)
            
        if triche_age_fe_nok:
            ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_fe)
            colloc_fe = adapt_nb_colloc_fe(sector_stat, colloc_fe)

        all_hh, persid, hhid, nbre_colloc_fe = add_pers(all_hh, nbre_colloc_fe, sector_stat, ss_name, persid, age_fe, 1, hhid, hh_type_id, hh_type, True, 'parent')
        
        print("colloc 1 added")
        
        nbr_colloc = get_nb_colloc()
        first_added_colloc = True
        too_many_colloc = False
         
        while nbr_colloc > 0 :
             
            age_colloc_nok = True

            triche_age_colloc_nok = True
            i = 0
            while age_colloc_nok: # and triche_age_colloc_nok:
                i += 1
                age_colloc = get_age_mari(age_fe)
                sex_colloc = get_sex_child()
                age_colloc_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_colloc, sex_colloc)
                
                if i >= 105:
                    #triche_age_child_nok = False
                    if sex_colloc == 0:
                        age_colloc, too_many_colloc = get_closest_not_empty(age_fe, ss_age_ho, sector_stat, 121, first_added_colloc)
                    elif sex_colloc == 1:
                        age_colloc, too_many_colloc = get_closest_not_empty(age_fe, ss_age_fe, sector_stat, 121, first_added_colloc)
                    age_colloc_nok = False #check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_colloc, sex_colloc)
                
            if not too_many_colloc:
                if sex_colloc == 0 :
                    ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_colloc)
                    colloc_ho = adapt_nb_colloc_ho(sector_stat, colloc_ho)
                elif sex_colloc == 1:
                    ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age_colloc)
                    colloc_fe = adapt_nb_colloc_fe(sector_stat, colloc_fe)
                    nbre_colloc_fe -= 1
                 
                all_hh, persid, hhid, nbr_colloc = add_pers(all_hh, nbr_colloc, sector_stat, ss_name, persid, age_colloc, sex_colloc, hhid, hh_type_id, hh_type, True, 'parent')
            
                print("colloc added")
            else :
                nbr_colloc = 0
                
            first_added_colloc = False
            
               
        
        hhid += 1
        
    nbre_colloc_ho = get_nbre_ho_colloc(sector_stat, colloc_ho) 
                     
    while nbre_colloc_ho  > 0 :
        
        age_ho_nok = True
        triche_age_ho_nok = True
        i = 0
        while age_ho_nok: # and triche_age_fe_nok:
            i += 1             
        #while age_fe_nok :
            age_ho = get_age_colloc() 
            age_ho_nok = check_age_mari(sector_stat, ss_age_ho, age_ho)
            
            
            if i >= 95:
                #triche_age_fe_nok = False
                age_ho, too_many = get_closest_not_empty(52, ss_age_ho, sector_stat)
                age_ho_nok = False #check_age_mari(sector_stat, ss_age_fe, age_fe)
            
        if triche_age_ho_nok:
            ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_ho)
            colloc_ho = adapt_nb_colloc_ho(sector_stat, colloc_ho)

        all_hh, persid, hhid, nbre_colloc_ho = add_pers(all_hh, nbre_colloc_ho, sector_stat, ss_name, persid, age_ho, 0, hhid, hh_type_id, hh_type, True, 'parent')
        
        print("colloc 1 added")
        
        nbr_colloc = get_nb_colloc()
        first_added_colloc = True
        too_many_colloc = False
         
        while nbr_colloc > 0 :
             
            age_colloc_nok = True

            triche_age_colloc_nok = True
            i = 0
            while age_colloc_nok: # and triche_age_colloc_nok:
                i += 1
                age_colloc = get_age_mari(age_ho)
                sex_colloc = 0
                age_colloc_nok = check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_colloc, sex_colloc)
                
                if i >= 95:
                    #triche_age_child_nok = False
                    age_colloc, too_many_colloc = get_closest_not_empty(age_ho, ss_age_ho, sector_stat, 121, first_added_colloc)
                    age_colloc_nok = False #check_age_child(sector_stat, ss_age_fe, ss_age_ho, age_colloc, sex_colloc)
                
            if not too_many_colloc:
                ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age_colloc)
                colloc_ho = adapt_nb_colloc_ho(sector_stat, colloc_ho)
                nbre_colloc_ho -= 1
                 
                all_hh, persid, hhid, nbr_colloc = add_pers(all_hh, nbr_colloc, sector_stat, ss_name, persid, age_colloc, sex_colloc, hhid, hh_type_id, hh_type, True, 'parent')
            
                print("colloc added")
            else :
                nbr_colloc = 0
                
            first_added_colloc = False
            
               
        
        hhid += 1
     
    hh_type = 'collectif'            
    hh_type_id = get_hh_id(hh_type)
    
    for age in range(104, -1, -1):
        
        nbre_fe = get_nbre_fe(sector_stat, age, ss_age_fe)
        i = 0                    
        while nbre_fe > 0:
            i +=1
            all_hh, persid, hhid, nbre_fe = add_pers(all_hh, nbre_fe, sector_stat, ss_name, persid, age, 1, hhid, hh_type_id, hh_type, False, 'parent')
            
            ss_age_fe = adapt_nb(sector_stat, ss_age_fe, age)
            if i > 1400:
                all_hh.to_csv('error collectif femmes_v2.csv')
                nbre_fe = 0
                
            print("collectif fe added")
        #hhid += 1
    
    for age in range(94, -1, -1):
        
        nbre_ho = get_nbre_fe(sector_stat, age, ss_age_ho)
        i = 0            
        while nbre_ho > 0:
            i +=1
            all_hh, persid, hhid, nbre_ho = add_pers(all_hh, nbre_ho, sector_stat, ss_name, persid, age, 0, hhid, hh_type_id, hh_type, False, 'parent')
            
            ss_age_ho = adapt_nb(sector_stat, ss_age_ho, age)
            if i > 1400:
                all_hh.to_csv('error collectif hommes_v2.csv')
                nbre_ho = 0
            print("collectif ho added")
            
    print('all_hh', all_hh)
    all_hh.to_csv('./hh_'+str(ss_name)+'.csv')
    
    return all_hh, persid, hhid
    

def create_households_for_all_ss(all_hh, SectorStats, ss_age_fe, single_age_fe, couple_age_fe, ss_age_ho, single_mom_age, 
                                 couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, single_dad):
    """
    all_hh = pd.DataFrame(columns=['SectorStatID', 'SectorStatName', 'PersID', 'Age', 'GenderID', 'GenderName', 'HouseholdID',
                                   'HouseholdTypeID', 'HouseHorldTypeName']) #ssLat, ssLong
    """
    persid = 521279 #0
    hhid = 284852 #0
    #for ss in SectorStats:
    for i in range(356, 725):
        ss = SectorStats.loc[i]
        print(ss, 'ss')
        all_hh, persid, hhid = create_households(all_hh, ss, persid, hhid, ss_age_fe, single_age_fe, couple_age_fe, ss_age_ho, 
                                                 single_mom_age, couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, 
                                                 single_dad)
        #all_hh = pd.concat([all_hh, to_add], ignore_index=True)
        
    return all_hh

#print(get_nbre_fe('21001A472', 103, ss_age_fe))
"""
all_hh = pd.DataFrame(columns=['SectorStatID', 'SectorStatName', 'PersID', 'Age', 'GenderID', 'GenderName', 'ChildOrParent', 'HouseholdID',
                                   'HouseholdTypeID', 'HouseHorldTypeName']) #ssLat, ssLong
"""
all_hh = pd.read_csv('all_hh_last_2.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace=True)
print(all_hh)
#all_hh = create_households_for_all_ss(all_hh, ['21001A472'], ss_age_fe, single_age_fe,  couple_age_fe, ss_age_ho,
#                            single_mom_age, couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, single_dad)
#print(all_hh)
#all_hh.to_csv('all_hh_vtot.csv')
#name, ind = get_ss_name('21001A472', ss_age_fe)

#adapt_nb_colloc_ho('21001A472', colloc_ho)

all_hh = create_households_for_all_ss(all_hh, SectorStats, ss_age_fe, single_age_fe, couple_age_fe, ss_age_ho, single_mom_age, 
                                 couple_child_age_mom, colloc_fe, colloc_ho, single_age_ho, single_dad)
all_hh.to_csv('./hh/all_hh_enooorme.csv')
