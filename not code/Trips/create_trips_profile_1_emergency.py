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


people = pd.read_csv('all_pers_type_1.csv')# TODO LOAD pers and filter tripChainType 1
print(len(people))


sectors = pd.read_csv('ss_long_lat.csv')
sectors.set_index("SectorStatID", inplace=True, drop=True)
print(sectors) #TODO check format

trips = pd.DataFrame(columns=["PersID", "TripNumber", "TripTypeFrom", "TripTypeTo", "SS_Origin", "Long_Origin", 
                              "Lat_Origin", "SS_Destination", "Long_Destination", "Lat_Destination", "Distance", "Strat_Time_pos", "Strat_Time_h", "Strat_Time_m", "End_Time_pos", "End_Time_h", "End_Time_m", "Duration_Time"])


distances = pd.read_csv('distances_ss.csv')
distances.set_index('SectorStatID_1', inplace=True, drop=True)
print(distances) #TODO check format
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
def get_time(distribution):
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
   
h_w_trips  = pd.DataFrame(columns=["PersID_1", "WorkerID_1", "TripNumber_1", "TripTypeFrom_1", "TripTypeTo_1", "SS_Origin_1",
                                   "Long_Origin_1", "Lat_Origin_1", "SS_Destination_1", "Long_Destination_1", "Lat_Destination_1",
                                   "Distance_1", "Strat_Time_pos_1", "Strat_Time_h_1", "Strat_Time_m_1", "End_Time_pos_1",
                                   "End_Time_h_1", "End_Time_m_1", "Duration_Time_1", "PersID_2", "WorkerID_2", "TripNumber_2",
                                   "TripTypeFrom_2", "TripTypeTo_2", "SS_Origin_2", "Long_Origin_2", "Lat_Origin_2", 
                                   "SS_Destination_2", "Long_Destination_2", "Lat_Destination_2", "Distance_2", "Strat_Time_pos_2",
                                   "Strat_Time_h_2", "Strat_Time_m_2", "End_Time_pos_2", "End_Time_h_2", "End_Time_m_2", 
                                   "Duration_Time_2"])


h_w_trips.PersID_1 = people.PersID
h_w_trips.WorkerID_1 = people.WorkerID
h_w_trips.TripNumber_1 = 1
h_w_trips.TripTypeFrom_1 = "H"
h_w_trips.TripTypeTo_1 = "W"
h_w_trips.SS_Origin_1 = people.SectorStatID

h_w_trips.Long_Origin_1 = h_w_trips.SS_Origin_1.apply(lambda x: sectors.loc[x, "long"])
h_w_trips.Lat_Origin_1 = h_w_trips.SS_Origin_1.apply(lambda x: sectors.loc[x, "lat"])

h_w_trips.SS_Destination_1 = people.WorkSectorStatID

h_w_trips.Long_Destination_1 = h_w_trips.SS_Destination_1.apply(lambda x: sectors.loc[x, "long"])
h_w_trips.Lat_Destination_1 = h_w_trips.SS_Destination_1.apply(lambda x: sectors.loc[x, "lat"])

h_w_trips.Distance_1 = h_w_trips.apply(lambda x: get_distance(x.SS_Origin_1, x.SS_Destination_1), axis=1)

def get_trip_to_work_time(pers_worker_id):
    if pers_worker_id == 6:
            distribution = work_distribution_time
    elif pers_worker_id == 0 or pers_worker_id ==1 or pers_worker_id ==2 or pers_worker_id ==3 or pers_worker_id ==4 or pers_worker_id ==5:
        distribution = school_distribution_time
    else:
        errorStartTimeToWork
        
    start_time_to_work_pos = get_time(distribution)
    if start_time_to_work_pos >= 1440:
        to_work_tomorrow = True #TODO usefull ?
        start_time_to_work_pos = start_time_to_work_pos-1440
    else:  #TODO usefull ?
        to_work_tomorrow = False  #TODO usefull ?
        
    return start_time_to_work_pos


h_w_trips.Strat_Time_pos_1 = h_w_trips.WorkerID_1.apply(lambda x: get_trip_to_work_time(x))
h_w_trips.Strat_Time_h_1 = h_w_trips.Strat_Time_pos_1.apply(lambda x : math.floor(x/60))
h_w_trips.Strat_Time_m_1 = h_w_trips.Strat_Time_pos_1.apply(lambda x : x%60)

h_w_trips.Duration_Time_1 = h_w_trips.Distance_1 / 23.7 * 60

h_w_trips.End_Time_pos_1 = round(h_w_trips.Strat_Time_pos_1 + h_w_trips.Duration_Time_1)
h_w_trips.End_Time_h_1 = h_w_trips.End_Time_pos_1.apply(lambda x : math.floor(x/60))
h_w_trips.End_Time_m_1 = h_w_trips.End_Time_pos_1.apply(lambda x : x%60)

print(h_w_trips)

print("2")

h_w_trips.PersID_2 = h_w_trips.PersID_1
h_w_trips.WorkerID_2 = h_w_trips.WorkerID_1
h_w_trips.TripNumber_2 = 2
h_w_trips.TripTypeFrom_2 = "W"
h_w_trips.TripTypeTo_2 = "H"
h_w_trips.SS_Origin_2 = h_w_trips.Long_Destination_1

h_w_trips.Long_Origin_2 = h_w_trips.SS_Destination_1
h_w_trips.Lat_Origin_2 = h_w_trips.Lat_Destination_1

h_w_trips.SS_Destination_2 = h_w_trips.SS_Origin_1

h_w_trips.Long_Destination_2 = h_w_trips.Long_Origin_1
h_w_trips.Lat_Destination_2 = h_w_trips.Lat_Origin_1

h_w_trips.Distance_2 = h_w_trips.Distance_1


def get_trip_to_home_time(end_time_to_work_pos):
    start_time_to_home_pos = end_time_to_work_pos - 1
        
    while start_time_to_home_pos < end_time_to_work_pos:
        start_time_to_home_pos = get_time(home_distribution_time)
        
    if start_time_to_home_pos >= 1440:
        to_work_tomorrow = True #TODO usefull ?
        start_time_to_home_pos = start_time_to_home_pos-1440
    else:  #TODO usefull ?
        to_work_tomorrow = False  #TODO usefull ?
    return start_time_to_home_pos


h_w_trips.Strat_Time_pos_2 = h_w_trips.End_Time_pos_1.apply(lambda x: get_trip_to_home_time(x))
h_w_trips.Strat_Time_h_2 = h_w_trips.Strat_Time_pos_2.apply(lambda x : math.floor(x/60))
h_w_trips.Strat_Time_m_2 = h_w_trips.Strat_Time_pos_2.apply(lambda x : x%60)

h_w_trips.Duration_Time_2 = h_w_trips.Duration_Time_1

h_w_trips.End_Time_pos_2 = round(h_w_trips.Strat_Time_pos_2 + h_w_trips.Duration_Time_2)
h_w_trips.End_Time_h_2 = h_w_trips.End_Time_pos_2.apply(lambda x : math.floor(x/60))
h_w_trips.End_Time_m_2 = h_w_trips.End_Time_pos_2.apply(lambda x : x%60)

print(h_w_trips)
h_w_trips.to_csv('big_profile_1.csv')

h_w_trips_1 = pd.DataFrame()

for col in ["PersID_1", "WorkerID_1", "TripNumber_1", "TripTypeFrom_1", "TripTypeTo_1", "SS_Origin_1",
                                   "Long_Origin_1", "Lat_Origin_1", "SS_Destination_1", "Long_Destination_1", "Lat_Destination_1",
                                   "Distance_1", "Strat_Time_pos_1", "Strat_Time_h_1", "Strat_Time_m_1", "End_Time_pos_1",
                                   "End_Time_h_1", "End_Time_m_1", "Duration_Time_1"]:
    short_col = col[:-2]
    h_w_trips_1[short_col] = h_w_trips[col]
    
h_w_trips_2 = pd.DataFrame()

for col in ["PersID_2", "WorkerID_2", "TripNumber_2",
                                   "TripTypeFrom_2", "TripTypeTo_2", "SS_Origin_2", "Long_Origin_2", "Lat_Origin_2", 
                                   "SS_Destination_2", "Long_Destination_2", "Lat_Destination_2", "Distance_2", "Strat_Time_pos_2",
                                   "Strat_Time_h_2", "Strat_Time_m_2", "End_Time_pos_2", "End_Time_h_2", "End_Time_m_2", 
                                   "Duration_Time_2"]:
    short_col = col[:-2]
    h_w_trips_2[short_col] = h_w_trips[col]

all_trips = pd.concat([h_w_trips_1, h_w_trips_2])

print(all_trips)
all_trips.to_csv('profile_1_emergency.csv')

"""

i=0
for pers in people.index:
    print("i", i)

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
        #distance = distance_two_points(lat_home, long_home, lat_work, long_work)
        distance = get_distance(ss_home, ss_work)
        
        pers_worker_id = people.loc[pers, "WorkerID"] #pers.WorkerTypeID
        #f
        
        if pers_worker_id == 6:
            distribution = work_distribution_time
        elif pers_worker_id == 0 or pers_worker_id ==1 or pers_worker_id ==2 or pers_worker_id ==3 or pers_worker_id ==4 or pers_worker_id ==5:
            distribution = school_distribution_time
        else:
            errorStartTimeToWork
            
        start_time_to_work_pos = get_time(distribution)
        if start_time_to_work_pos >= 1440:
            to_work_tomorrow = True #TODO usefull ?
            start_time_to_work_pos = start_time_to_work_pos-1440
        else:  #TODO usefull ?
            to_work_tomorrow = False  #TODO usefull ?
        
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
        
        
        trips.loc[i]=[pers_id, 1, "H", "W", ss_home, long_home, lat_home, ss_work, long_work, lat_work, distance,
                      start_time_to_work_pos, start_time_to_work_hour, start_time_to_work_min, 
                      end_time_to_work_pos, end_time_to_work_hour, end_time_to_work_min, delta_t_to_work]
        i+=1
        
        #ADD trip 2 Work - Home
        start_time_to_home_pos = end_time_to_work_pos - 1
        
        while start_time_to_home_pos < end_time_to_work_pos:
            start_time_to_home_pos = get_time(home_distribution_time)
            
        if start_time_to_home_pos >= 1440:
            to_work_tomorrow = True #TODO usefull ?
            start_time_to_home_pos = start_time_to_home_pos-1440
        else:  #TODO usefull ?
            to_work_tomorrow = False  #TODO usefull ?
        
        start_time_to_home_hour = math.floor(start_time_to_home_pos/60)
        start_time_to_home_min = start_time_to_home_pos%60
        
        delta_t_to_home = delta_t_to_work
        end_time_to_home_pos = start_time_to_home_pos + delta_t_to_home
        
        if end_time_to_home_pos >= 1440:
            to_home_tomorrow = True #TODO usefull ?
            end_time_to_home_pos = end_time_to_home_pos-1440
        else:  #TODO usefull ?
            to_home_tomorrow = False  #TODO usefull ?
        
        end_time_to_home_hour = math.floor(end_time_to_home_pos/60)
        end_time_to_home_min = end_time_to_home_pos%60
        
        
        trips.loc[i]=[pers_id, 2, "W", "H", ss_work, long_work, lat_work, ss_home, long_home, lat_home, distance,
                      start_time_to_home_pos, start_time_to_home_hour, start_time_to_home_min, 
                      end_time_to_home_pos, end_time_to_home_hour, end_time_to_home_min, delta_t_to_home]
        i+=1
        
print(trips)
trips.to_csv("Trips_profile_1.csv")
"""