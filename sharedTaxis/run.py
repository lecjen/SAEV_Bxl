import pandas as pd
import random
import math

max_places = 6
max_waiting_time = 5

vitesse = 23.7

requests = pd.DataFrame() #read from trips files mais ordonnés par time departure croissant
#Tourner plus d'un jour
#add time dependance ?

sectors = pd.read_csv('ss_long_lat.csv')
sectors.set_index("SectorStatID", inplace=True, drop=True)
print(sectors) #TODO check format

class Taxi:
    def __init__(self, s, p):
        self.status = s
        self.nb_pers = 0
        self.pos = p        
        self.destination_book = None
        self.destination_working = None        
        
        self.destination_time = None
        self.book_time = None
        
        self.tot_waiting_time = 0
        self.tot_empty_km = 0
        self.tot_pers_km = 0
        self.pers_per_trip = 0
        self.nb_trips = 0
        self.km = 0
        
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

def time(ss_origin, ss_destination):
    dist = distance(ss_origin, ss_destination)
    t = (dist / vitesse )* 60 #min
    
    return t

taxis_list = []
#tot_waiting_time = 0
#tot_empty_km = 0
#tot_pers_km = 0
#pers_per_trip = 0
#nb_trips = 0
#avg_pers_per_trip = pers_per_trip / nb_trips

for t in range(0, 1442):
    for taxi in taxis_list:
        if taxi.status == "working" and taxi.destination_time == t:
                taxi.status = "free"
                d = distance(taxi.destination_book, taxi.destination_working)
                taxi.tot_pers_km += taxi.nb_pers * d
                taxi.km += d
                taxi.pers_per_trip += taxi.nb_pers
                taxi.nb_pers = 0
                taxi.pos = taxi.destination_working
                taxi.destination_working = None
                taxi.destination_book = None  
                taxi.nb_trips += 1
                
        elif taxi.status == "booked" and taxi.book_time == t:
            taxi.status = "waiting"
            taxi.pos = taxi.destination_book
            taxi.destination_book = None
        
        elif taxi.status == "waiting":
            if t < taxi.departure_time and taxi.nb_pers < max_places:
                for delta_t in range(0, max_waiting_time+1):

                    compagnons_request = requests[(requests.time + delta_t <=  taxi.departure_time) & 
                                             (requests.origin == taxi.pos) & 
                                             (requests.destination == taxi.destination_working)]
            
                            
                    while len(compagnons_request) > 0 and taxi.nb_pers < max_places:
                                elu = random.randrange(0, len(compagnons_request), 1)
                                ind_elu = compagnons_request.index[elu]
                                el = compagnons_request.loc[ind_elu]
                                
                                compagnons_request.drop([ind_elu], inplace=True)
                                requests.drop([ind_elu], inplace=True)
                                
                                if el.time > taxi.departure_time:
                                    taxi.tot_waiting_time += (taxi.nb_pers * (taxi.departure_time - el.time))
                                    taxi.departure_time = el.time
                                taxi.nb_pers+=1
                
                    taxi.destination_time = taxi.departure_time + time(taxi.destination_book, taxi.destination_working)
            
            elif t == taxi.departure_time:
                taxi.status == "working"
                #taxi.destination_book = None            
            
        
        elif taxi.status == "free":
            for r in requests:
                t_needed = time(taxi.pos, r.origin)
                if t_needed + t <= r.time + max_waiting_time:
                    taxi.status == "booked"
                    taxi.nb_pers +=1
                    taxi.destination_working = r.destination
                    taxi.destination_book = r.origin
                    
                    taxi.book_time = t_needed + t
                    taxi.tot_waiting_time += (t_needed + t -  r.time)
                    taxi.departure_time = t_needed + t
                    
                    taxi.tot_empty_km += distance(taxi.pos, r.origin)
                    
                    for delta_t in range(0, max_waiting_time+1):
                        compagnons_request = requests[(requests.time + delta_t == r.time)
                                                      & (r.origin == requests.origin)
                                                      & (r.destination == requests.destination)]
                        
                        while len(compagnons_request) > 0 and taxi.nb_pers < max_places:
                                    elu = random.randrange(0, len(compagnons_request), 1)
                                    ind_elu = compagnons_request.index[elu]
                                    el = compagnons_request.loc[ind_elu]
                                    
                                    compagnons_request.drop([ind_elu], inplace=True)
                                    requests.drop([ind_elu], inplace=True)
                                    
                                    if el.time > taxi.departure_time:
                                        taxi.tot_waiting_time += (taxi.nb_pers * (taxi.departure_time - el.time))
                                        taxi.departure_time = el.time
                                    taxi.nb_pers+=1
                    
                    taxi.destination_time = taxi.departure_time + time(taxi.destination_book, taxi.destination_working)
    
    min_t_request = min(requests.time)
    if min_t_request == t:
        t_requests = requests[requests.time == min_t_request]
        origins = t_requests.origin.drop_duplicates(inplace=True)
        
        for ori in origins:
            filtered_requests = t_requests[t_requests.origin == ori]
            
            r = filtered_requests.loc[filtered_requests.index[0]]
            
            new_taxi = Taxi("waiting", ori)
            
            new_taxi.nb_pers +=1
            new_taxi.destination_working = r.destination
            new_taxi.destination_book = ori
            new_taxi.book_time = t
            
            for delta_t in range(0, max_waiting_time+1):
                compagnons_request = requests[(requests.time + delta_t == r.time)
                                              & (r.origin == requests.origin)
                                              & (r.destination == requests.destination)]
                
                while len(compagnons_request) > 0 and taxi.nb_pers < max_places:
                            elu = random.randrange(0, len(compagnons_request), 1)
                            ind_elu = compagnons_request.index[elu]
                            el = compagnons_request.loc[ind_elu]
                            
                            compagnons_request.drop([ind_elu], inplace=True)
                            requests.drop([ind_elu], inplace=True)
                           
                            if el.time > taxi.departure_time:
                                taxi.tot_waiting_time += (taxi.nb_pers * (taxi.departure_time - el.time))
                                taxi.departure_time = el.time
                            taxi.nb_pers+=1
                        
            taxi.destination_time = taxi.departure_time + time(ori, taxi.destination_working)
            taxis_list.append(new_taxi)
 

results = pd.DataFram(columns=["WaitingTime", "Empty_km", "OnBoard_km", "Pers_km", "Tot_pers", "Nb_trips"])

i=0
for taxi in taxis_list:       
    results.loc[i]=taxi.get_results()

print(results)
results.to_csv("simulation_1.csv")
