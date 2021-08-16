import pandas as pd
import math
import random
import bisect
import numpy as np

def replace_only_str_to_float(x, that, by):
    if type(x)==str:
        x = float(x.replace(that, by))

    return x

def comma_to_dot(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x : replace_only_str_to_float(x, ',', "."))

    return df

def clean_col_names(df):
    for col in df.columns:
        if 'Unnamed:' in col:
            new_col_name = col[9:]
            df[new_col_name]=df[col]
            df.drop(columns=[col], inplace=True)
    return df

work_distribution_time = pd.read_csv('distribution_start_time_work.csv', sep=';')
work_distribution_time = comma_to_dot(work_distribution_time)
work_distribution_time = work_distribution_time.proba.tolist()
print(work_distribution_time)

school_distribution_time = pd.read_csv('distribution_start_time_school.csv', sep=';')
school_distribution_time = comma_to_dot(school_distribution_time)
school_distribution_time = school_distribution_time.proba.tolist()
print(school_distribution_time)

home_distribution_time = pd.read_csv('distribution_start_time_home.csv', sep=';')
home_distribution_time = comma_to_dot(home_distribution_time)
home_distribution_time = home_distribution_time.proba.tolist()
print(home_distribution_time)

loisirs_distribution_time = pd.read_csv('distribution_start_time_loisirs.csv', sep=';')
loisirs_distribution_time = comma_to_dot(loisirs_distribution_time)
loisirs_distribution_time = loisirs_distribution_time.proba.tolist()
print(loisirs_distribution_time)

distances_distribution = [0.06, 0.08, 0.1, 0.11, 0.08, 0.14, 0.12, 0.08, 0.1, 0.06, 0.07]

people = pd.read_csv('all_pers_type_7.csv')# TODO LOAD pers and filter tripChainType 1
print(people)
e
"""
people = pd.DataFrame(columns=["Persid", "SectorStatID", "SectorStatName", "Age", "GenderID",
                               "GenderName", "ChildOrParent", "HouseholdID", "HouseholdTypeID",
                               "HouseholdTypeName", "WorkerTypeID", "WorkerName", "WorkSectorStat", "ChainType"])
people.loc[0]=[1, "21018A00-", "OSF", 21, 1, "female", "child", 2345, 1, "Couple with child", 5, 
               "Unif off campus", "21018A04-", 1]
people.loc[1]=[2, "21018A00-", "OSF1", 56, 0, "male", "parent", 2345, 1, "Couple with child", 6, 
               "Worker", "21018A30-", 1]

"""

sectors = pd.read_csv('ss_long_lat.csv')
sectors.set_index("SectorStatID", inplace=True, drop=True)
print(sectors) #TODO check format

trips = pd.DataFrame(columns=["PersID", "TripNumber", "TripTypeFrom", "TripTypeTo", "SS_Origin", "Long_Origin", 
                              "Lat_Origin", "SS_Destination", "Long_Destination", 
                              "Lat_Destination", "Distance", "Strat_Time_pos", "Strat_Time_h",
                              "Strat_Time_m", "End_Time_pos", "End_Time_h", "End_Time_m",
                              "Duration_Time"])


distances = pd.read_csv('distances_ss.csv')
distances.set_index("SectorStatID_1", inplace=True, drop=True)
distances.drop(columns=["SectorStatID_1.1"], inplace=True)
print(distances)

inf_250 = dict()
d_250_500 = dict()
d_500_1 = dict()
d_1_2 = dict()
d_2_3 = dict()
d_3_5 = dict()
d_5_7_5 = dict()
d_7_5_10 = dict()
d_10_15 = dict()
d_15_25 = dict()
d_25_40 = dict()
#sup_40 = dict()

for ss in distances.index:
    print('ss', ss)
    
    inf_250[ss] = list()
    d_250_500[ss] = list()
    d_500_1[ss] = list()
    d_1_2[ss] = list()
    d_2_3[ss] = list()
    d_3_5[ss] = list()
    d_5_7_5[ss] = list()
    d_7_5_10[ss] = list()
    d_10_15[ss] = list()
    d_15_25[ss] = list()
    d_25_40[ss] = list()
    #sup_40[ss] = list()
    
    
    for ss_to in distances.index:
        print("ss to", ss_to)
        dist = distances.loc[ss, ss_to]
        if dist <= 0.25:
            inf_250[ss].append(ss_to)
        elif dist > 0.25 and dist <= 0.5:
            d_250_500[ss].append(ss_to)
        elif dist > 0.5 and dist <= 1:
            d_500_1[ss].append(ss_to)            
        elif dist > 1 and dist <= 2:
            d_1_2[ss].append(ss_to)             
        elif dist > 2 and dist <= 3:
            d_2_3[ss].append(ss_to) 
        elif dist > 3 and dist <= 5:
            d_3_5[ss].append(ss_to) 
        elif dist > 5 and dist <= 7.5:
            d_5_7_5[ss].append(ss_to) 
        elif dist > 7.5 and dist <= 10:
            d_7_5_10[ss].append(ss_to) 
        elif dist > 10 and dist <= 15:
            d_10_15[ss].append(ss_to) 
        elif dist > 15 and dist <= 25:
            d_15_25[ss].append(ss_to) 
        elif dist > 25 and dist <= 40:
            d_25_40[ss].append(ss_to)  #Regroupe 25-40 et < 40 car both empty
        else:
            errorDistance
        """
        elif dist > 40:
            sup_40[ss].append(ss_to) 
        """
            
print(inf_250)
print(d_250_500)
print(d_500_1)
print(d_1_2)
print(d_2_3)
print(d_3_5)
print(d_5_7_5)
print(d_7_5_10)
print(d_10_15)
print(d_15_25)
print(d_25_40)
#print(sup_40)

list_distances = [inf_250, d_250_500, d_500_1, d_1_2, d_2_3, d_3_5, d_5_7_5, d_7_5_10, d_10_15, d_15_25, d_25_40]
"""
max_dist_ss = pd.DataFrame(columns=["SectorStatID", "Farest ss", "Max distance", "Distance category"])
max_dist_ss.set_index("SectorStatID", inplace=True, drop=True)

for ss in distances.index:
    max_d = max(distances.loc[ss])    
    max_ss = distances.loc[ss].idxmax()
    if max_d <= 0.25:
        dist_cat = 0
    elif max_d > 0.25 and max_d < 0.5:
        dist_cat = 1
    elif max_d > 0.5 and max_d < 1:
        dist_cat = 2
    elif max_d > 1 and max_d < 2:
        dist_cat = 3
    elif max_d > 2 and max_d < 3:
        dist_cat = 4
    elif max_d > 3 and max_d < 5:
        dist_cat = 5
    elif max_d > 5 and max_d < 7.5:
        dist_cat = 6
    elif max_d > 7.5 and max_d < 10:
        dist_cat = 7
    elif max_d > 10 and max_d < 15:
        dist_cat = 8
    elif max_d > 15 and max_d < 25:
        dist_cat = 9
    elif max_d > 25:
        dist_cat = 10
    else:
        errorMaxDist
    max_dist_ss.loc[ss]=[max_ss, max_d, dist_cat]
    

print(max_dist_ss)
"""
closest_peri = pd.read_csv('closest_ss_peri_v2.csv')
closest_peri.set_index("SectorStatID", inplace=True, drop=True)
print(closest_peri)
"""
def distance_two_points(lat1, long1, lat2, long2):
    #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    R = 6373.0 #km

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    long1 = math.radians(long1)
    long2 = math.radians(long2)

    delta_long = long2 - long1
    delta_lat = lat2 - lat1

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_long / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c #km

    return distance
"""
def get_distance(ss_origin, ss_destination):
    dist = distances.loc[ss_origin, ss_destination]
    return dist

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


def delta_time(distance):
    vitesse = 23.7 #km/h vitesse moyenne en voiture #mobilite-mobiliteit.brussels/sites/default/files/cahiers_mobilite-2_.pdf
    delta_t_h = distance / vitesse
    delta_t_min = delta_t_h*60
    
    return delta_t_min

def get_work_distribution(pers_worker_id):
    if pers_worker_id == 6:
            distribution = work_distribution_time
    elif pers_worker_id == 0 or pers_worker_id ==1 or pers_worker_id ==2 or pers_worker_id ==3 or pers_worker_id ==4 or pers_worker_id ==5:
        distribution = school_distribution_time
    else:
        errorStartTimeToWork
        
    return distribution

def trip_to_work(ss_from, ss_work, pers_worker_id, end_time_to_previous_pos, delta_t):
    #distance = distance_two_points(lat_from, long_from, lat_work, long_work)
    distance = get_distance(ss_from, ss_work)
    
    distribution = get_work_distribution(pers_worker_id)
        
    start_time_to_work_pos = end_time_to_previous_pos - 1
    
    count = 0
    while start_time_to_work_pos < end_time_to_previous_pos and count < 1442:
        print(count)
        count +=1
        start_time_to_work_pos = get_index(distribution)
    if count == 1442:
        start_time_to_work_pos = end_time_to_previous_pos + delta_t
        
    if start_time_to_work_pos >= 1440:
        start_time_to_work_pos = start_time_to_work_pos-1440
    
    start_time_to_work_hour = math.floor(start_time_to_work_pos/60)
    start_time_to_work_min = start_time_to_work_pos%60
    
    delta_t_to_work = delta_time(distance)
    end_time_to_work_pos = start_time_to_work_pos + delta_t_to_work
    
    if end_time_to_work_pos >= 1440:
        to_work_tomorrow = True #TODO usefull ?
        end_time_to_work_pos = end_time_to_work_pos-1440
    else:  #TODO usefull ?
        to_work_tomorrow = False  #TODO usefull ?
    
    end_time_to_work_hour = math.floor(end_time_to_work_pos/60)
    end_time_to_work_min = end_time_to_work_pos%60
    
    return distance, start_time_to_work_pos, start_time_to_work_hour, start_time_to_work_min, end_time_to_work_pos, end_time_to_work_hour, end_time_to_work_min, delta_t_to_work
    

def trip_to_loisir(ss_from, end_time_to_previous_pos, delta_t):
    distance_cat = get_index(distances_distribution)
        
    distance_range = list_distances[distance_cat]
    possible_ss_to = distance_range[ss_from]
    
    if len(possible_ss_to)==0:
        ss_loisir = closest_peri.loc[ss_from][0]
    else:
        elu = random.randrange(0, len(possible_ss_to), 1)
        ss_loisir = possible_ss_to[elu]

    long_loisir = sectors.loc[ss_loisir, "long"]
    #d
    lat_loisir = sectors.loc[ss_loisir, "lat"]
     
    #distance = distance_two_points(lat_from, long_from, lat_loisir, long_loisir)
    distance = get_distance(ss_from, ss_loisir)
    
    
    start_time_to_loisir_pos = end_time_to_previous_pos - 1
    
    count = 0
    while start_time_to_loisir_pos < end_time_to_previous_pos and count < 1442:
        print('c', count)
        count +=1
        start_time_to_loisir_pos = get_index(loisirs_distribution_time)
        
    if count == 1442:
        start_time_to_loisir_pos = end_time_to_previous_pos + delta_t
        
    if start_time_to_loisir_pos >= 1440:
        to_loisir_tomorrow = True #TODO usefull ?
        start_time_to_loisir_pos = start_time_to_loisir_pos-1440
    else:  #TODO usefull ?
        to_losir_tomorrow = False  #TODO usefull ?
    
    start_time_to_loisir_hour = math.floor(start_time_to_loisir_pos/60)
    start_time_to_loisir_min = start_time_to_loisir_pos%60
    
    delta_t_to_loisir = delta_time(distance)
    end_time_to_loisir_pos = start_time_to_loisir_pos + delta_t_to_loisir
    
    if end_time_to_loisir_pos >= 1440:
        to_loisir_tomorrow = True #TODO usefull ?
        end_time_to_loisir_pos = end_time_to_loisir_pos-1440
    else:  #TODO usefull ?
        to_loisir_tomorrow = False  #TODO usefull ?
    
    end_time_to_loisir_hour = math.floor(end_time_to_loisir_pos/60)
    end_time_to_loisir_min = end_time_to_loisir_pos%60
    
    return ss_loisir, long_loisir, lat_loisir, distance, start_time_to_loisir_pos, start_time_to_loisir_hour, start_time_to_loisir_min, end_time_to_loisir_pos, end_time_to_loisir_hour, end_time_to_loisir_min, delta_t_to_loisir

def trip_to_home(ss_from, end_time_to_previous_pos, delta_t):
    #distance = distance_two_points(lat_from, long_from, lat_home, long_home)
    distance = get_distance(ss_from, ss_home)
        
    start_time_to_home_pos = end_time_to_previous_pos - 1
    
    count = 0
    while start_time_to_home_pos < end_time_to_previous_pos and count < 1442:
        print('c', count)
        count +=1
        start_time_to_home_pos = get_index(home_distribution_time)
        
    if count == 1442:
        start_time_to_home_pos = end_time_to_previous_pos + delta_t
        
    if start_time_to_home_pos >= 1440:
        to_home_tomorrow = True #TODO usefull ?
        start_time_to_home_pos = start_time_to_home_pos-1440
    else:  #TODO usefull ?
        to_home_tomorrow = False  #TODO usefull ?
    
    start_time_to_home_hour = math.floor(start_time_to_home_pos/60)
    start_time_to_home_min = start_time_to_home_pos%60
    
    delta_t_to_home = delta_time(distance)
    end_time_to_home_pos = start_time_to_home_pos + delta_t_to_home
    
    if end_time_to_home_pos >= 1440:
        to_home_tomorrow = True #TODO usefull ?
        end_time_to_home_pos = end_time_to_home_pos-1440
    else:  #TODO usefull ?
        to_home_tomorrow = False  #TODO usefull ?
    
    end_time_to_home_hour = math.floor(end_time_to_home_pos/60)
    end_time_to_home_min = end_time_to_home_pos%60
    
    return distance, start_time_to_home_pos, start_time_to_home_hour, start_time_to_home_min, end_time_to_home_pos, end_time_to_home_hour, end_time_to_home_min, delta_t_to_home
        
i=0
for pers in people.index:
    print("i", i)
    """
    pers_id = #TODO
    a
    """
    pers_id = people.loc[pers, "PersID"]
    ss_home = people.loc[pers, "SectorStatID"] #TODO check format
    #b
    long_home = sectors.loc[ss_home, "long"]
    #d
    lat_home = sectors.loc[ss_home, "lat"]
    #e
    
    ss_work = people.loc[pers, "WorkSectorStatID"] #pers.WorkSectorStat #TODO check format
    #c
    long_work = sectors.loc[ss_work, "long"]
    #d
    lat_work = sectors.loc[ss_work, "lat"]
    #e
    
    if ss_home != ss_work:
        #ADD trip 1 Home - Work
        pers_worker_id = people.loc[pers, "WorkerID"] #pers.WorkerTypeID
        #f
        distance, start_time_to_work_pos, start_time_to_work_hour, start_time_to_work_min, end_time_to_work_pos, end_time_to_work_hour, end_time_to_work_min, delta_t_to_work = trip_to_work(ss_home, ss_work, pers_worker_id, -1, 0)
        
        trips.loc[i]=[pers_id, 1,"H", "W", ss_home, long_home, lat_home, ss_work, long_work, lat_work, distance,
                      start_time_to_work_pos, start_time_to_work_hour, start_time_to_work_min, 
                      end_time_to_work_pos, end_time_to_work_hour, end_time_to_work_min, delta_t_to_work]
        i+=1
        print("i", i)
        
        #ADD trip 2 Work - Loisir
        ss_loisir, long_loisir, lat_loisir, distance, start_time_to_loisir_pos, start_time_to_loisir_hour, start_time_to_loisir_min, end_time_to_loisir_pos, end_time_to_loisir_hour, end_time_to_loisir_min, delta_t_to_loisir = trip_to_loisir(ss_work, end_time_to_work_pos, 4*60)
        
        trips.loc[i]=[pers_id, 2, "W", "L", ss_work, long_work, lat_work, ss_loisir, long_loisir,
                      lat_loisir, distance, start_time_to_loisir_pos, start_time_to_loisir_hour,
                      start_time_to_loisir_min, end_time_to_loisir_pos, end_time_to_loisir_hour,
                      end_time_to_loisir_min, delta_t_to_loisir]
        i+=1
        print("i", i)

        
        #ADD trip 3 Loisir - Work    
        distance, start_time_to_work_pos, start_time_to_work_hour, start_time_to_work_min, end_time_to_work_pos, end_time_to_work_hour, end_time_to_work_min, delta_t_to_work = trip_to_work(ss_loisir, ss_work, pers_worker_id, end_time_to_loisir_pos, 60)
        
        trips.loc[i]=[pers_id, 3, "L", "W", ss_loisir, long_loisir, lat_loisir, ss_work, long_work, lat_work, distance,
                      start_time_to_work_pos, start_time_to_work_hour, start_time_to_work_min, 
                      end_time_to_work_pos, end_time_to_work_hour, end_time_to_work_min, delta_t_to_work]
        i+=1
        print("i", i)
        
        #ADD trip 4 Work - Loisir 2
        ss_loisir, long_loisir, lat_loisir, distance, start_time_to_loisir_pos, start_time_to_loisir_hour, start_time_to_loisir_min, end_time_to_loisir_pos, end_time_to_loisir_hour, end_time_to_loisir_min, delta_t_to_loisir = trip_to_loisir(ss_work, end_time_to_work_pos, 4*60)
        
        trips.loc[i]=[pers_id, 4, "W", "L", ss_work, long_work, lat_work, ss_loisir, long_loisir,
                      lat_loisir, distance, start_time_to_loisir_pos, start_time_to_loisir_hour,
                      start_time_to_loisir_min, end_time_to_loisir_pos, end_time_to_loisir_hour,
                      end_time_to_loisir_min, delta_t_to_loisir]
        i+=1
        print("i", i)
        
        #ADD trip 5 Loisir - Home        
        distance, start_time_to_home_pos, start_time_to_home_hour, start_time_to_home_min, end_time_to_home_pos, end_time_to_home_hour, end_time_to_home_min, delta_t_to_home = trip_to_home(ss_loisir, end_time_to_loisir_pos, 60)
        
        trips.loc[i]=[pers_id, 5, "L", "H", ss_loisir, long_loisir, lat_loisir, ss_home, long_home,
                      lat_home, distance, start_time_to_home_pos, start_time_to_home_hour,
                      start_time_to_home_min, end_time_to_home_pos, end_time_to_home_hour,
                      end_time_to_home_min, delta_t_to_home]
        i+=1
        print("i", i)
        
print(trips)
trips.to_csv("Trips_profile_7.csv")