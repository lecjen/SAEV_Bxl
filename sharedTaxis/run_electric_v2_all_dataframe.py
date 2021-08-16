import pandas as pd
import random
import math

max_places = 6
max_waiting_time = 5

vitesse = 23.7

max_km_per_charge = 500 #https://beev.co/voitures-electriques/voiture-electrique-autonomie/
charge_vitesse =  #km per min

requests = pd.DataFrame() #read from trips files mais ordonnés par time departure croissant
#Tourner plus d'un jour
#add time dependance ?

sectors = pd.read_csv('ss_long_lat.csv')
sectors.set_index("SectorStatID", inplace=True, drop=True)
print(sectors) #TODO check format

distances = pd.read_csv('distances_ss.csv')
print(distances) #TODO check format

clos_rank = pd.read_csv('ss_closeness_ranking.csv')
print(clos_rank) #TODO check format

taxis = pd.DataFrame(columns = ["status", "nb_pers", "pos", "destination_book", "destination_working", "destination_time", "book_time", 
                                "departure_time", "max_departure_time", "km_battery", "charging_station", "tot_waiting_time", "tot_empty_km",
                                "tot_pers_km", "pers_per_trip", "nb_trips", "km", "tot_charging_time"])
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
    return dist
    
def time(ss_origin, ss_destination):
    dist = distance(ss_origin, ss_destination)
    t = (dist / vitesse )* 60 #min
    
    return t

#taxis_list = []
stations = pd.DataFrame(columns=["position", "status"])
#stations_list = []
#tot_waiting_time = 0
#tot_empty_km = 0
#tot_pers_km = 0
#pers_per_trip = 0
#nb_trips = 0
#avg_pers_per_trip = pers_per_trip / nb_trips

for t in range(0, 1442):
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
                
        elif taxis.loc[taxi, "status"] == "booked" and taxis.loc[taxi, "book_time"] == t:
            taxis.loc[taxi, "status"] = "waiting"
            
            dist_book = distance(taxis.loc[taxi, "pos"], taxis.loc[taxi, "destination_book"])
            taxis.loc[taxi, "tot_empty_km"] += dist_book
            taxis.loc[taxi, "km_battery"] -= dist_book
        
            taxis.loc[taxi, "pos"] = taxis.loc[taxi, "destination_book"]
            taxis.loc[taxi, "destination_book"] = None
            
        elif taxis.loc[taxi, "status"] == "waiting":
            if t < taxis.loc[taxi, "departure_time"] and taxis.loc[taxi, "nb_pers"] < max_places: #Should be useless
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
                                    taxis.loc[taxi, "departure_time"] = el.time
                                taxis.loc[taxi, "nb_pers"]+=1
                
                    taxis.loc[taxi, "destination_time"] = taxis.loc[taxi, "departure_time"] + time(taxis.loc[taxi, "destination_book"], taxis.loc[taxi, "destination_working"])
            
            elif t == taxis.loc[taxi, "departure_time"]:
                taxis.loc[taxi, "status"] == "working"
                #taxi.destination_book = None            
            
        
        elif taxis.loc[taxi, "status"] == "booked_for_charge" and t = taxis.loc[taxi, "book_charge_desination_time"]:
            taxis.loc[taxi, "status"] == "charging"
            
        elif taxis.loc[taxi, "status"] == "free" or taxis.loc[taxi, "status"] =="charging":
            #closest ? distance optimisation ...
            for ind in requests.index:
                r = requests.loc[ind]
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
            
        elif taxis.loc[taxi, "status"] == "charging":
            if taxis.loc[taxi, "km_battery"] == max_km_per_charge:
                taxis.loc[taxi, "status"] = "free"
                stations.loc[taxis.loc[taxi, "charging_station"], "Status"] = "free"
                taxis.loc[taxi, "charging_station"] = None
                
            else:
                taxis.loc[taxi, "km_battery"] += charge_vitesse
                
                
    min_t_request = min(requests.time)
    if min_t_request == t:
        t_requests = requests[requests.time == min_t_request]
        origins = t_requests.origin.drop_duplicates(inplace=True)
        
        for ori in origins:
            filtered_requests = t_requests[t_requests.origin == ori]
            
            ind_0 = filtered_requests.index[0]
            r = filtered_requests.loc[ind_0]
            
            new_taxi = Taxi("waiting", ori)
            
            new_taxi.nb_pers +=1
            new_taxi.destination_working = r.destination
            new_taxi.destination_book = ori
            new_taxi.book_time = t
            new_taxi.departure_time = t
            new_taxi.max_departure_time = t + max_waiting_time
            
            t_requests.drop([ind_0], inplace=True)  
            filtered_requests.drop([ind_0], inplace=True)   
            requests.drop([ind_0], inplace=True)   
            
            for delta_t in range(0, max_waiting_time+1):
                compagnons_request = requests[(t + delta_t == requests.time)
                                              & (new_taxi.destination_book == requests.origin)
                                              & (new_taxi.destination_working == requests.destination)]
                
                while len(compagnons_request) > 0 and new_taxi.nb_pers < max_places:
                            elu = random.randrange(0, len(compagnons_request), 1)
                            ind_elu = compagnons_request.index[elu]
                            el = compagnons_request.loc[ind_elu]
                            
                            compagnons_request.drop([ind_elu], inplace=True)
                            requests.drop([ind_elu], inplace=True)
                            t_requests.drop([ind_0], inplace=True)  
                            filtered_requests.drop([ind_0], inplace=True)   
                           
                            if el.time > new_taxi.departure_time:
                                new_taxi.tot_waiting_time += (new_taxi.nb_pers * (new_taxi.departure_time - el.time))
                                new_taxi.departure_time = el.time
                            new_taxi.nb_pers+=1
                        
            new_taxi.destination_time = new_taxi.departure_time + time(ori, new_taxi.destination_working)
            taxis_list.append(new_taxi)
            
    """
    free_stations_list = []
    for station in stations_list:
        if station.status = "free":
            free_stations_list.append(station)
    """
    for taxi in taxis.index:
        if taxis.loc[taxi, "status"] == "free" and taxis.loc[taxi, "km_battery"] < max_km_per_charge:
            free_stations = stations[stations.status == "free"]
            if len(free_stations)>0:
                rank = 0
                ss_int = clos_rank.loc[taxis.loc[taxi, "pos"], rank]
                possible_stations = free_stations[free_stations.position == ss_int]
                d = 0
                
                while len(possible_stations)<=0 and d <= taxis.loc[taxi, "km_battery"]:    
                    rank+=1   
                    ss_int = clos_rank.loc[taxis.loc[taxi, "pos"], rank]
                    possible_stations = free_stations[free_stations.position == ss_int]
                    d = distance(taxis.loc[taxi, "pos"], ss_int)
                    
                if len(possible_stations) == 0:
                    stations.loc[len(stations)] = [taxis.loc[taxi, "pos"], "busy"]
                    taxis.loc[taxi, "status"] = "charging"
                else:
                    elu = random.randrange(0, len(possible_stations), 1)
                    ind_elu = possible_stations.index[elu]
            
                    taxis.loc[taxi, "destination_charge"] = ss_int
                    taxis.loc[taxi, "status"] = "booked_for_charge"
                    taxis.loc[taxi, "book_charge_desination_time"] = t + time(taxis.loc[taxi, "pos"], ss_int)
                    stations.loc[ind_elu, "status"] = "busy"
                    
                
            #TODO 1 cherche si station free
            #2 from matrice rank cherche si station free in closest
            #3 go to station (attention delta time and distance)
            
            
            
            
            

 

results = pd.DataFram(columns=["WaitingTime", "Empty_km", "OnBoard_km", "Pers_km", "Tot_pers", "Nb_trips"])

i=0
for taxi in taxis_list:       
    results.loc[i]=taxi.get_results()

print(results)
results.to_csv("simulation_1.csv")
