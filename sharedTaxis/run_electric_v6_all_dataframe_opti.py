import pandas as pd
import random
import math
import numpy as np
import datetime

start = datetime.datetime.now()
max_places = 5
max_waiting_time = 5

vitesse = 23.7

max_km_per_charge = 130
charge_vitesse =  130/(4*60) #km per min

pick_up_time = 1
drop_off_time = 1

cleaning_time = 15

sectors = pd.read_csv('ss_long_lat.csv')
sectors.set_index("SectorStatID", inplace=True, drop=True)
print(sectors) #TODO check format

distances = pd.read_csv('distances_ss.csv')
distances.set_index("SectorStatID_1", inplace=True, drop=True)
print(distances) #TODO check format

def distance(ss_origin, ss_destination):
    dist = distances.loc[ss_origin, ss_destination]
    #dist = dist.loc[ss_origin]
    #print("d", dist)
    return dist

            
def set_status_time(x, t):
    #print(x)
    stat = x.status
    status_t = x.status_time
    status_t[t] = stat
    return status_t
"""
requests = pd.DataFrame() #read from trips files mais ordonnés par time departure croissant
#Tourner plus d'un jour
#add time dependance ?
requests = pd.DataFrame(columns=["id", "time", "origin", "destination", "distance"])
"""
requests = pd.read_csv("all_drive_Ganshoren_in_and_out.csv") #read from trips files mais ordonnés par time departure croissant
requests.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'Unnamed: 0.1.1'], inplace=True)
requests.Strat_Time_pos = round(requests.Strat_Time_pos)
requests.sort_values(by='Strat_Time_pos', inplace = True)
print(requests)
"""
for i in range(0, 10000):
    t = random.randrange(0, 1440, 1)
    elu = random.randrange(0, len(sectors), 1)
    ori = sectors.index[elu]
    elu =  random.randrange(0, len(sectors), 1)
    desti = sectors.index[elu]
    dist = distance(ori, desti)
    requests.loc[i]=[i, t, ori, desti, dist]


requests.sort_values(by='time', inplace = True)
save_requests = requests.copy()
save_requests.to_csv('requests_test_7.csv')

requests = pd.read_csv('requests_test_6.csv')
requests.sort_values(by='time', inplace = True)
requests.drop(columns=['Unnamed: 0'], inplace=True)
print(requests)


for i in requests.index:
    requests.loc[i+10]=requests.loc[i]
    #requests.loc[2*i+10]=requests.loc[i]
requests.id = requests.index
requests.sort_values(by='time', inplace = True)
    
print(requests)


requests.loc[0]=[0, 1, '21001A552', '21002A11-', distance('21001A552', '21002A11-')]
requests.loc[1]=[0, 3, '21001A552', '21002A11-', distance('21001A552', '21002A11-')]
requests.loc[2]=[0, 100, '21002A11-', '21001A552', distance('21002A11-', '21001A552')]
#requests.loc[1]=[0, 3, '21001A552', '21002A11-', 5]
"""




clos_rank = pd.read_csv('ss_closeness_ranking_v2.csv')
clos_rank.set_index("SectorStatID", inplace=True, drop=True)
print(clos_rank) #TODO check format

taxis = pd.DataFrame(columns = ["status", "nb_pers", "pos", "destination_book", "destination_working", "destination_time", "book_time",
                                "departure_time", "max_departure_time", "km_battery", "charging_station", "tot_waiting_time", "tot_empty_km",
                                "tot_pers_km", "pers_per_trip", "nb_trips", "km", "tot_charging_time", "book_charge_desination_time", "d_tmp",
                                "status_time", "destination_charge", "cleaning_place", "time_cleaning_done", "tot_cleaning_time", "book_cleaning_destination_time",
                                "destination_cleaning"])
l = []
for i in range(0, 1441):
    l.append("")
"""
class Taxi: #TODO to dataframe
    def __init__(self, s, p):
        self.status = s
        self.nb_pers = 0
        self.pos = p        
        self.destination_book = None
        self.destination_working = None        
        
        self.destination_time = None
        self.book_time = None
        self.departure_time = None
        self.max_departure_time = None
        
        self.km_battery = max_km_per_charge
        self.charging_station = None
        
        self.tot_waiting_time = 0
        self.tot_empty_km = 0
        self.tot_pers_km = 0
        self.pers_per_trip = 0
        self.nb_trips = 0
        self.km = 0
        self.tot_charging_time = 0
    
class Station:
    def __init__(self, p):
        self.status = "free"
        self.pos = p
     
        
        
    def get_results(self):
        return [self.tot_waiting_time, self.tot_empty_km, self.km, self.tot_pers_km, self.pers_per_trip, self.nb_trips]

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


def distance(ss_origin, ss_destination):
    lat1 = sectors.loc[ss_origin, "lat"]
    long1 = sectors.loc[ss_origin, "long"]
    
    lat2 = sectors.loc[ss_destination, "lat"]
    long2 = sectors.loc[ss_destination, "long"]
    
    dist = distance_two_points(lat1, long1, lat2, long2)
    
    return dist
"""
def distance(ss_origin, ss_destination):
    dist = distances.loc[ss_origin, ss_destination]
    #dist = dist.loc[ss_origin]
    #print("d", dist)
    return dist
    
def distance_lambda(x, col1, col2):
    #print("x", x)
    ss_origin = x[col1]
    ss_destination = x[col2]
    dist = distances.loc[ss_origin, ss_destination]
    #dist = dist.loc[ss_origin]
    #print("d", dist)
    return dist

def time(ss_origin, ss_destination):
    dist = distance(ss_origin, ss_destination)
    t = (dist / vitesse )* 60 #min
    
    return t

#taxis_list = []
stations = pd.DataFrame(columns=["position", "status", "status_time"])
cleaning_place = pd.DataFrame(columns=["position", "status", "status_time", "tot_nb_cleaning"])
#stations_list = []
#tot_waiting_time = 0
#tot_empty_km = 0
#tot_pers_km = 0
#pers_per_trip = 0
#nb_trips = 0
#avg_pers_per_trip = pers_per_trip / nb_trips

for t in range(0, 1441): #TODO check max departure time de mes trips
    print("t", t)
    #if taxis.loc[taxi, "status"] == "working" and taxis.loc[taxi, "destination_time"] == t:
    mask_arrived_at_working_destination = ((taxis.status == "working") & (taxis.destination_time == t))
    taxis.loc[mask_arrived_at_working_destination, 'status'] = "free"
        
    taxis["d_tmp"]=0
    taxis_arrived_at_working_destination = taxis[mask_arrived_at_working_destination]
    if not taxis_arrived_at_working_destination.empty:        
        taxis_arrived_at_working_destination["d_tmp"] = taxis_arrived_at_working_destination.apply(lambda x: round(distance_lambda(x, "destination_book", "destination_working")), axis=1)
        taxis.loc[mask_arrived_at_working_destination, "tot_pers_km"] += taxis_arrived_at_working_destination["nb_pers"] * taxis_arrived_at_working_destination["d_tmp"]
        taxis.loc[mask_arrived_at_working_destination, "km"] += taxis_arrived_at_working_destination["d_tmp"]
        taxis.loc[mask_arrived_at_working_destination, "km_battery"] -= taxis_arrived_at_working_destination["d_tmp"]
        taxis.loc[mask_arrived_at_working_destination, "pers_per_trip"] += taxis_arrived_at_working_destination["nb_pers"]
        taxis.loc[mask_arrived_at_working_destination, "nb_pers"] = 0
        taxis.loc[mask_arrived_at_working_destination, "pos"] = taxis_arrived_at_working_destination["destination_working"]
        taxis.loc[mask_arrived_at_working_destination, "destination_working"] = None
        taxis.loc[mask_arrived_at_working_destination, "destination_book"] = None  
        taxis.loc[mask_arrived_at_working_destination, "nb_trips"] += 1
    print("working to free done")
    """
    for taxi in taxis.index:
        
        if taxis.loc[taxi, "status"] == "working" and taxis.loc[taxi, "destination_time"] == t:
                taxis.loc[taxi, "status"] = "free"
                d = distance(taxis.loc[taxi, "destination_book"], taxis.loc[taxi, "destination_working"])
                taxis.loc[taxi, "tot_pers_km"] += taxis.loc[taxi, "nb_pers"] * d
                taxis.loc[taxi, "km"] += d
                taxis.loc[taxi, "km_battery"] -= d
                taxis.loc[taxi, "pers_per_trip"] += taxis.loc[taxi, "nb_pers"]
                taxis.loc[taxi, "nb_pers"] = 0
                taxis.loc[taxi, "pos"] = taxis.loc[taxi, "destination_working"]
                taxis.loc[taxi, "destination_working"] = None
                taxis.loc[taxi, "destination_book"] = None  
                taxis.loc[taxi, "nb_trips"] += 1
    """
    # elif taxis.loc[taxi, "status"] == "booked" and taxis.loc[taxi, "book_time"] == t:
    mask_arrived_at_booked_destination = ((taxis.status == "booked") & (taxis.book_time == t))
    
    taxis_arrived_at_booked_destination = taxis[mask_arrived_at_booked_destination]
    if not taxis_arrived_at_booked_destination.empty:    
        taxis.loc[mask_arrived_at_booked_destination, 'status'] = "waiting"
        
                
        taxis_arrived_at_booked_destination["d_tmp"] = taxis_arrived_at_booked_destination.apply(lambda x: round(distance_lambda(x, "pos", "destination_book")), axis=1)
        #taxis.loc[mask_arrived_at_booked_destination, 'd_tmp'] = distance(taxis_arrived_at_booked_destination["pos"], taxis_arrived_at_booked_destination["destination_book"])
        taxis.loc[mask_arrived_at_booked_destination, "tot_empty_km"] += taxis_arrived_at_booked_destination["d_tmp"]
        #c
        taxis.loc[mask_arrived_at_booked_destination, "km_battery"] -= taxis_arrived_at_booked_destination["d_tmp"]
        taxis.loc[mask_arrived_at_booked_destination, "pos"] = taxis_arrived_at_booked_destination["destination_book"]
        #taxis.loc[mask_arrived_at_booked_destination, "destination_book"] = None
        
    print("booked to waiting done")
    """        
        elif taxis.loc[taxi, "status"] == "booked" and taxis.loc[taxi, "book_time"] == t:
            taxis.loc[taxi, "status"] = "waiting"
            
            dist_book = distance(taxis.loc[taxi, "pos"], taxis.loc[taxi, "destination_book"])
            taxis.loc[taxi, "tot_empty_km"] += dist_book
            taxis.loc[taxi, "km_battery"] -= dist_book
        
            taxis.loc[taxi, "pos"] = taxis.loc[taxi, "destination_book"]
            taxis.loc[taxi, "destination_book"] = None
    """
    """
    #Should be useless
    taxis_waiting_not_full = taxis[(taxis.status == "waiting") & (taxis.departure_time <= t) & (taxis.nb_pers < max_places)] 
    for taxi in taxis_waiting_not_full.index:
    """
    """
        elif taxis.loc[taxi, "status"] == "waiting":
            if t < taxis.loc[taxi, "departure_time"] and taxis.loc[taxi, "nb_pers"] < max_places: #Should be useless
    """
    """
        for delta_t in range(0, taxis.loc[taxi, "max_departure_time"] - t +1):

            compagnons_request = requests[(t + delta_t == requests.time) & (requests.origin == taxis.loc[taxi, "pos"]) & 
                                     (requests.destination == taxis.loc[taxi, "destination_working"])] #should always be null
    
                    
            while len(compagnons_request) > 0 and taxis.loc[taxi, "nb_pers"] < max_places:
                        elu = random.randrange(0, len(compagnons_request), 1)
                        ind_elu = compagnons_request.index[elu]
                        el = compagnons_request.loc[ind_elu]
                        
                        compagnons_request.drop([ind_elu], inplace=True)
                        requests.drop([ind_elu], inplace=True)
                        
                        if el.time > taxis.loc[taxi, "departure_time"]:
                            taxis.loc[taxi, "tot_waiting_time"] += (taxis.loc[taxi, "nb_pers"] * (el.time - taxis.loc[taxi, "departure_time"]))
                            if( (taxis.loc[taxi, "nb_pers"] * (el.time - taxis.loc[taxi, "departure_time"])))<0:
                                stop
                            taxis.loc[taxi, "departure_time"] = el.time
                        taxis.loc[taxi, "nb_pers"]+=1
        
            taxis.loc[taxi, "destination_time"] = round(taxis.loc[taxi, "departure_time"] + time(taxis.loc[taxi, "destination_book"], taxis.loc[taxi, "destination_working"]))
    """
    #elif taxis.loc[taxi, "status"] == "waiting": and elif t == taxis.loc[taxi, "departure_time"]:
    mask_departure = ((taxis.status == "waiting") & (taxis.departure_time == t))
    #taxis_departure = taxis[mask_departure]
    
    taxis.loc[mask_departure, 'status'] = "working"
    print("waiting to working done")
    """
            elif t == taxis.loc[taxi, "departure_time"]:
                taxis.loc[taxi, "status"] == "working"
                #taxi.destination_book = None 
    """            
    #elif taxis.loc[taxi, "status"] == "charging": and if taxis.loc[taxi, "km_battery"] == max_km_per_charge:
    mask_charging_done = ((taxis.status == "charging") & (taxis.km_battery >= max_km_per_charge))
    taxis_charging_done = taxis[mask_charging_done]
    
    taxis.loc[mask_charging_done, 'status'] = "free"
    index = taxis.loc[mask_charging_done, "charging_station"]
    if not index.empty:
        stations.loc[index, "status"] = "free"
        taxis.loc[mask_charging_done, 'charging_station'] = None
    print("charging to free done")
    
    #elif taxis.loc[taxi, "status"] == "charging": and if not taxis.loc[taxi, "km_battery"] < max_km_per_charge:
    mask_charging = ((taxis.status == "charging") & (taxis.km_battery < max_km_per_charge))
    #taxis_charging = taxis[mask_charging]
    taxis.loc[mask_charging, "km_battery"] += charge_vitesse
    taxis.loc[mask_charging, "tot_charging_time"] += 1
    print("charging battery done")
    """
        elif taxis.loc[taxi, "status"] == "charging":
            if taxis.loc[taxi, "km_battery"] == max_km_per_charge:
                taxis.loc[taxi, "status"] = "free"
                stations.loc[taxis.loc[taxi, "charging_station"], "Status"] = "free"
                taxis.loc[taxi, "charging_station"] = None
                
            else:
                taxis.loc[taxi, "km_battery"] += charge_vitesse
    """
    #elif taxis.loc[taxi, "status"] == "booked_for_charge" and t = taxis.loc[taxi, "book_cleaning_destination_time"]:
    mask_arrived_at_charge_destination = ((taxis.status == "booked_for_charge") & (taxis.book_cleaning_destination_time == t))
    #taxis_arrived_at_charge_destination = taxis[mask_arrived_at_charge_destination]
    print("booked for charging to charging done")

    #elif taxis.loc[taxi, "status"] == "cleaning": and if taxis.loc[taxi, "time_cleaning_done"] == t:
    mask_cleaning_done = ((taxis.status == "cleaning") & (taxis.time_cleaning_done == t))
    taxis_cleaning_done = taxis[mask_cleaning_done]

    taxis.loc[mask_cleaning_done, 'status'] = "free"
    index = taxis.loc[mask_cleaning_done, "cleaning_place"]
    if not index.empty:
        cleaning_place.loc[index, "status"] = "free"
        taxis.loc[mask_cleaning_done, 'cleaning_place'] = None
    print("cleaning to free done")

    #elif taxis.loc[taxi, "status"] == "booked_for_cleaning" and t = taxis.loc[taxi, "book_cleaning_desination_time"]:
    mask_arrived_at_cleaning_destination = ((taxis.status == "booked_for_cleaning") & (taxis.book_cleaning_destination_time == t))
    
    taxis.loc[mask_arrived_at_cleaning_destination, 'status'] = "cleaning"
    
    print("booked for cleaning to cleaning done")
    """
    elif taxis.loc[taxi, "status"] == "booked_for_charge" and t = taxis.loc[taxi, "book_charge_desination_time"]:
        taxis.loc[taxi, "status"] == "charging"
    """
    taxis_to_clean = taxis[(taxis.nb_trips%40 == 0) & (taxis.status == "free")]
    for taxi in taxis_to_clean.index:
        #if taxis.loc[taxi, "status"] == "free" and taxis.loc[taxi, "km_battery"] < max_km_per_charge:
        free_stations = cleaning_place[cleaning_place.status == "free"]
        if len(free_stations)>0:
            rank = 1
            ss_int = clos_rank.loc[taxis.loc[taxi, "pos"], str(rank)]
            possible_stations = free_stations[free_stations.position == ss_int]
            d = 0

            while len(possible_stations)<=0 and d <= taxis.loc[taxi, "km_battery"]:
                rank+=1
                ss_int = clos_rank.loc[taxis.loc[taxi, "pos"], str(rank)]
                possible_stations = free_stations[free_stations.position == ss_int]
                d = distance(taxis.loc[taxi, "pos"], ss_int)

            if len(possible_stations) == 0:
                #cree nouvelle station
                taxis.loc[taxi, "status"] = "cleaning"
                taxis.loc[taxi, "cleaning_place"] = len(cleaning_place)
                cleaning_place.loc[len(cleaning_place)] = [taxis.loc[taxi, "pos"], "busy", l.copy(), 1]
            else:
                elu = random.randrange(0, len(possible_stations), 1)
                ind_elu = possible_stations.index[elu]

                taxis.loc[taxi, "destination_cleaning"] = ss_int
                taxis.loc[taxi, "status"] = "booked_for_cleaning"
                taxis.loc[taxi, "book_cleaning_destination_time"] = round(t + time(taxis.loc[taxi, "pos"], ss_int))
                taxis.loc[taxi, "time_cleaning_done"] = taxis.loc[taxi, "book_cleaning_destination_time"] + cleaning_time
                cleaning_place.loc[ind_elu, "status"] = "busy"
                taxis.loc[taxi, "tot_empty_km"] += d
                taxis.loc[taxi, "km_battery"] -= d
                taxis.loc[taxi, "cleaning_place"] = ind_elu

        else:
            #cree nouvelle station
            taxis.loc[taxi, "status"] = "cleaning"
            taxis.loc[taxi, "cleaning_place"] = len(cleaning_place)
            cleaning_place.loc[len(cleaning_place)] = [taxis.loc[taxi, "pos"], "busy", l.copy(), 1]
    print('to cleaning done')

    taxis_available = taxis[(taxis.status == "free") | (taxis.status == "charging")]   
    if not taxis_available.empty:
        #for taxi in taxis_available.index:
            
            #elif taxis.loc[taxi, "status"] == "free" or taxis.loc[taxi, "status"] =="charging":
                #closest ? distance optimisation ...
        for ind in requests[requests.Strat_Time_pos <= t+40].index: #.index: #
            if ind in requests.index:
                #r = requests.loc[ind]
                rank = 1
                ss_int = clos_rank.loc[requests.loc[ind, "SS_Origin"], str(rank)]
                d = 0
                possible_taxis = taxis_available[(taxis_available.pos == ss_int) & (taxis_available.km_battery >= d + requests.loc[ind, "Distance"])] #+ distance to closest charging station
                t_needed = 0
                
                while len(possible_taxis)<=0 and rank < 724 and t_needed + t <= requests.loc[ind, "Strat_Time_pos"]:    
                    rank+=1   
                    ss_int = clos_rank.loc[requests.loc[ind, "SS_Origin"], str(rank)]
                    d = distance(requests.loc[ind, "SS_Origin"], ss_int)
                    t_needed = int((d / vitesse )* 60) #min
                    possible_taxis = taxis_available[(taxis_available.pos == ss_int) & (taxis_available.km_battery >= d + requests.loc[ind, "Distance"])] #+ distance to closest charging station
                
                if len(possible_taxis)!=0:
                    elu = random.randrange(0, len(possible_taxis), 1)
                    taxi = possible_taxis.index[elu]
                    
                    if taxis.loc[taxi, "status"]== "charging":
                        index = taxis.loc[taxi, "charging_station"]
                        stations.loc[index, "status"] = "free"
                        taxis.loc[taxi, 'charging_station'] = None
                        
                    taxis.loc[taxi, "status"] = "booked"
                    taxis.loc[taxi, "nb_pers"] +=1
                    taxis.loc[taxi, "destination_working"] = requests.loc[ind, "SS_Destination"]
                    taxis.loc[taxi, "destination_book"] = requests.loc[ind, "SS_Origin"]
                    #taxis.loc[taxi, "book_departure_time"]= max(requests.loc[ind, "time"] - t_needed, t)
                    taxis.loc[taxi, "book_time"] = max(t_needed + t, requests.loc[ind, "Strat_Time_pos"])
    
                    if t_needed + t > requests.loc[ind, "Strat_Time_pos"]:
                        
                        taxis.loc[taxi, "tot_waiting_time"] += (t_needed + t -  requests.loc[ind, "Strat_Time_pos"]) * taxis.loc[taxi, "nb_pers"]
                        if ((t_needed + t -  requests.loc[ind, "Strat_Time_pos"]) * taxis.loc[taxi, "nb_pers"]) <0:
                            stop
                    taxis.loc[taxi, "departure_time"] = max(t_needed + t, requests.loc[ind, "Strat_Time_pos"])
                    taxis.loc[taxi, "max_departure_time"] = requests.loc[ind, "Strat_Time_pos"] + max_waiting_time
                    
                    taxis_available.drop([taxi], inplace=True)
                
                    requests.drop([ind], inplace=True)            
            
                    for delta_t in range(0, int(taxis.loc[taxi, "max_departure_time"]) - t +1):
                        compagnons_request = requests[(t + delta_t == requests.Strat_Time_pos)
                                                      & (taxis.loc[taxi, "destination_book"] == requests.SS_Origin)
                                                      & (taxis.loc[taxi, "destination_working"] == requests.SS_Destination)]
                        
                        while len(compagnons_request) > 0 and taxis.loc[taxi, "nb_pers"] < max_places:
                            #i
                            elu = random.randrange(0, len(compagnons_request), 1)
                            ind_elu = compagnons_request.index[elu]
                            el = compagnons_request.loc[ind_elu]
                            
                            compagnons_request.drop([ind_elu], inplace=True)
                            requests.drop([ind_elu], inplace=True)
                            
                            if el.Strat_Time_pos > taxis.loc[taxi, "departure_time"]:
                                taxis.loc[taxi, "tot_waiting_time"] += (taxis.loc[taxi, "nb_pers"] * (el.Strat_Time_pos - taxis.loc[taxi, "departure_time"]))
                                if ((taxis.loc[taxi, "nb_pers"] * (el.Strat_Time_pos - taxis.loc[taxi, "departure_time"])))<0:
                                    stop
                                taxis.loc[taxi, "departure_time"] = el.Strat_Time_pos
                            taxis.loc[taxi, "nb_pers"]+=1
                    
                    taxis.loc[taxi, "destination_time"] = round(taxis.loc[taxi, "departure_time"] + time(taxis.loc[taxi, "destination_book"], taxis.loc[taxi, "destination_working"]))
                    if t_needed ==0:
                        if taxis.loc[taxi, "departure_time"]  == t:
                            taxis.loc[taxi, "status"] = "working"
                        else:
                            taxis.loc[taxi, "status"] = "waiting"
                    
     
        """
        t_needed = time(taxis.loc[taxi, "pos"], r.origin)
        tot_d = distance(taxis.loc[taxi, "pos"], r.origin) + distance(r.origin, r.destination)
        
        if t_needed + t <= r.time + max_waiting_time and taxis.loc[taxi, "km_battery"] > tot_d :
            taxis.loc[taxi, "status"] == "booked"
            taxis.loc[taxi, "nb_pers"] +=1
            taxis.loc[taxi, "destination_working"] = r.destination
            taxis.loc[taxi, "destination_book"] = r.origin
            
            taxis.loc[taxi, "book_time"] = t_needed + t
            taxis.loc[taxi, "tot_waiting_time"] += (t_needed + t -  r.time) * taxis.loc[taxi, "nb_pers"]
            taxis.loc[taxi, "departure_time"] = t_needed + t
            taxis.loc[taxi, "max_departure_time"] = r.time + max_waiting_time
                                
            requests.drop([ind], inplace=True)            
    
            for delta_t in range(taxis.loc[taxi, "departure_time"], taxis.loc[taxi, "max_departure_time"] - t +1):
                compagnons_request = requests[(t + delta_t == requests.time)
                                              & (taxis.loc[taxi, "destination_book"] == requests.origin)
                                              & (taxis.loc[taxi, "destination_working"] == requests.destination)]
                
                while len(compagnons_request) > 0 and taxis.loc[taxi, "nb_pers"] < max_places:
                            elu = random.randrange(0, len(compagnons_request), 1)
                            ind_elu = compagnons_request.index[elu]
                            el = compagnons_request.loc[ind_elu]
                            
                            compagnons_request.drop([ind_elu], inplace=True)
                            requests.drop([ind_elu], inplace=True)
                            
                            if el.time > taxis.loc[taxi, "departure_time"]:
                                taxis.loc[taxi, "tot_waiting_time"] += (taxis.loc[taxi, "nb_pers"] * (el.time - taxis.loc[taxi, "departure_time"]))
                                taxis.loc[taxi, "departure_time"] = el.time
                            taxis.loc[taxi, "nb_pers"]+=1
            
            taxis.loc[taxi, "destination_time"] = taxis.loc[taxi, "departure_time"] + time(taxis.loc[taxi, "destination_book"], taxis.loc[taxi, "destination_working"])
    
            """
    print("free to booked done")            
                
    if not requests.empty:
        min_t_request = min(requests.Strat_Time_pos)
        print(min_t_request)
        if min_t_request == t:
            t_requests = requests[requests.Strat_Time_pos == min_t_request]
            origins = t_requests.SS_Origin
            origins.drop_duplicates(inplace=True)
            
            for ori in origins:
                print("ori", ori)
                filtered_requests = t_requests[t_requests.SS_Origin == ori]
                
                while len(filtered_requests) > 0:
                
                    ind_0 = filtered_requests.index[0]
                    r = filtered_requests.loc[ind_0]
                    
                    new_taxi = ["waiting", 1, ori, ori, r.SS_Destination, None, t, t, t + max_waiting_time, max_km_per_charge, None, 0, 0, 0, 0, 0, 0, 0, None, 0, l.copy(), None, None, None, 0, None, None] #Taxi("waiting", ori)
                    #"status", "nb_pers", "pos", "destination_book", "destination_working", "destination_time", "book_time", 
                    #                "departure_time", "max_departure_time", "km_battery", "charging_station", "tot_waiting_time", "tot_empty_km",
                    #                "tot_pers_km", "pers_per_trip", "nb_trips", "km", "tot_charging_time"
                    

                    """
                    new_taxi.nb_pers +=1
                    new_taxi.destination_working = r.destination
                    new_taxi.destination_book = ori
                    new_taxi.book_time = t
                    new_taxi.departure_time = t
                    new_taxi.max_departure_time = t + max_waiting_time
                    """
                    t_requests.drop([ind_0], inplace=True)  
                    filtered_requests.drop([ind_0], inplace=True)   
                    requests.drop([ind_0], inplace=True)   
                    
                    for delta_t in range(0, max_waiting_time+1):
                        print("delta_t", delta_t)
                        compagnons_request = requests[(t + delta_t == requests.Strat_Time_pos)
                                                      & (ori == requests.SS_Origin)
                                                      & (r.SS_Destination == requests.SS_Destination)]
                        """
                        TODO test
                                added_pers = min(len(compagnons_request), max_places-taxis.loc[taxi, "nb_pers"])
                                if compagnons_request.time.any() > taxis.loc[taxi, "departure_time"]:
                                        taxis.loc[taxi, "tot_waiting_time"] += (taxis.loc[taxi, "nb_pers"] * (max(compagnons_request.time) - taxis.loc[taxi, "departure_time"]))
                                        if ((taxis.loc[taxi, "nb_pers"] * (max(compagnons_request.time) - taxis.loc[taxi, "departure_time"])))<0:
                                            stop
                                        taxis.loc[taxi, "departure_time"] =max(compagnons_request.time)
                                taxis.loc[taxi, "nb_pers"]+=added_pers
                                ind_to_del = compagnons_request.index().tolist()[:added_pers]
                                compagnons_request.drop(ind_to_del, inplace=True)
                                requests.drop(ind_to_del, inplace=True)
                                possibles_requests.drop(ind_to_del, inplace=True) 
                        """
                        while len(compagnons_request) > 0 and new_taxi[1] < max_places: #nb_pers
                            print(new_taxi[1])        
                            elu = random.randrange(0, len(compagnons_request), 1)
                            ind_elu = compagnons_request.index[elu]
                            el = compagnons_request.loc[ind_elu]
                            
                            compagnons_request.drop([ind_elu], inplace=True)
                            requests.drop([ind_elu], inplace=True)
                            #t_requests.drop([ind_elu], inplace=True)  
                            if ind_elu in filtered_requests.index:
                                filtered_requests.drop([ind_elu], inplace=True)   
                           
                            if el.Strat_Time_pos > new_taxi[7]: #.departure_time:
                                new_taxi[11] += (new_taxi[1] * (el.Strat_Time_pos - new_taxi[7])) #.tot_waiting_time, .nb_pers, departure_time
                                if (new_taxi[1] * (el.Strat_Time_pos - new_taxi[7]))<0:
                                    stop
                                new_taxi[7] = el.Strat_Time_pos #departure_time
                            new_taxi[1] +=1 #nb_pers
                            
                    new_taxi[5] = round(new_taxi[7] + time(ori, r.SS_Destination)) #destination_time, departure_time
                    taxis.loc[len(taxis)]=new_taxi
                    #taxis_list.append(new_taxi)
    
    #elif taxis.loc[taxi, "status"] == "waiting": and elif t == taxis.loc[taxi, "departure_time"]:
    mask_departure = ((taxis.status == "waiting") & (taxis.departure_time == t))
    #taxis_departure = taxis[mask_departure]
    
    taxis.loc[mask_departure, 'status'] = "working"
    print("waiting to working for new taxis done")            
    """
    free_stations_list = []
    for station in stations_list:
        if station.status = "free":
            free_stations_list.append(station)
    """
    taxis_to_charge = taxis[(taxis.status == "free") & (taxis.km_battery < max_km_per_charge)]
    for taxi in taxis_to_charge.index:
        #if taxis.loc[taxi, "status"] == "free" and taxis.loc[taxi, "km_battery"] < max_km_per_charge:
            free_stations = stations[stations.status == "free"]
            if len(free_stations)>0:
                rank = 1
                ss_int = clos_rank.loc[taxis.loc[taxi, "pos"], str(rank)]
                possible_stations = free_stations[free_stations.position == ss_int]
                d = 0
                
                while len(possible_stations)<=0 and d <= taxis.loc[taxi, "km_battery"]:    
                    rank+=1   
                    ss_int = clos_rank.loc[taxis.loc[taxi, "pos"], str(rank)]
                    possible_stations = free_stations[free_stations.position == ss_int]
                    d = distance(taxis.loc[taxi, "pos"], ss_int)
                    
                if len(possible_stations) == 0:
                    #cree nouvelle station
                    taxis.loc[taxi, "status"] = "charging"
                    taxis.loc[taxi, "charging_station"] = len(stations)
                    stations.loc[len(stations)] = [taxis.loc[taxi, "pos"], "busy", l.copy()]
                else:
                    elu = random.randrange(0, len(possible_stations), 1)
                    ind_elu = possible_stations.index[elu]
            
                    taxis.loc[taxi, "destination_charge"] = ss_int
                    taxis.loc[taxi, "status"] = "booked_for_charge"
                    taxis.loc[taxi, "book_charge_desination_time"] = round(t + time(taxis.loc[taxi, "pos"], ss_int))
                    stations.loc[ind_elu, "status"] = "busy"
                    taxis.loc[taxi, "tot_empty_km"] += d
                    taxis.loc[taxi, "km_battery"] -= d
                    taxis.loc[taxi, "charging_station"] = ind_elu
                    
            else:
                #cree nouvelle station
                taxis.loc[taxi, "status"] = "charging"
                taxis.loc[taxi, "charging_station"] = len(stations)
                stations.loc[len(stations)] = [taxis.loc[taxi, "pos"], "busy", l.copy()]
                    
                
            #TODO 1 cherche si station free
            #2 from matrice rank cherche si station free in closest
            #3 go to station (attention delta time and distance)
                
    if not taxis.empty:
        taxis.status_time = taxis.apply(lambda x : set_status_time(x, t), axis=1)
    if not stations.empty:
        stations.status_time = stations.apply(lambda x : set_status_time(x, t), axis=1)
    if not cleaning_place.empty:
        cleaning_place.status_time = cleaning_place.apply(lambda x : set_status_time(x, t), axis=1)
    #stations.status_time[t]=station.status

    taxis.to_csv('gans_simu_taxis_empty.csv')
    requests.to_csv('gans_simu_requests_empty.csv')
    stations.to_csv('gans_simu_stations_empty.csv')
    cleaning_place.to_csv('gans_simu_cleaning_empty.csv')
                    
print(requests) #should be null
print(taxis)
taxis.to_csv('gans_simu_taxis_empty.csv')
requests.to_csv('gans_simu_requests_empty.csv')
stations.to_csv('gans_simu_stations_empty.csv')
cleaning_place.to_csv('gans_simu_cleaning_empty.csv')
print(stations)
#stations.to_csv('stations_simulation_7b.csv')
print(cleaning_place)
end = datetime.datetime.now()
print(end-start, "time")
#refaire la simu sans creer de nouvelle station
#refaire la simu sans creer de nouveaux taxis      


""" 

results = pd.DataFram(columns=["WaitingTime", "Empty_km", "OnBoard_km", "Pers_km", "Tot_pers", "Nb_trips"])

i=0
for taxi in taxis_list:       
    results.loc[i]=taxi.get_results()

print(results)
results.to_csv("simulation_1.csv")
"""
