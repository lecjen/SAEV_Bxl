import pandas as pd

bxl_cleaning = pd.read_csv('big_simu_putty_cleaning.csv') #0
#bxl_requests = pd.read_csv('big_simu_putty_requests.csv') 
bxl_stations = pd.read_csv('big_simu_putty_stations.csv') #1 392
bxl_taxis = pd.read_csv('big_simu_putty_taxis.csv') #1 532

gans_cleaning = pd.read_csv('gans_simu_cleaning_lim.csv') #0
gans_requests = pd.read_csv('gans_simu_request_lim.csv')
gans_stations = pd.read_csv('gans_simu_stations_lim.csv') #222
gans_taxis = pd.read_csv('gans_simu_taxis_lim.csv') #1 165
"""
all_gans = pd.read_csv('all_drive_Ganshoren_in_and_out.csv') #21 135

all_drive = pd.read_csv('all_drive.csv') #2 416 074

km_gans_taxis_empty = gans_taxis_empty.km
km_gans_taxis_empty.mean(axis=0)

empty_km_gans_taxis_empty = gans_taxis_empty.tot_empty_km
empty_km_gans_taxis_empty.mean(axis=0)

km_gans_taxis = gans_taxis.km
km_gans_taxis.mean(axis=0)

empty_km_gans_taxis = gans_taxis.tot_empty_km
empty_km_gans_taxis.mean(axis=0)

gans_taxis['avg_waiting_time_per_pers']=gans_taxis.tot_waiting_time/gans_taxis.pers_per_trip
gans_taxis.avg_waiting_time_per_pers.mean(axis=0)

gans_taxis_empty['avg_waiting_time_per_pers']=gans_taxis_empty.tot_waiting_time/gans_taxis_empty.pers_per_trip
gans_taxis_empty.avg_waiting_time_per_pers.mean(axis=0)

gans_taxis_empty['avg_pers_per_trip']=gans_taxis_empty.pers_per_trip/gans_taxis_empty.nb_trips
gans_taxis_empty.avg_pers_per_trip.mean(axis=0)

gans_taxis['avg_pers_per_trip']=gans_taxis.pers_per_trip/gans_taxis.nb_trips
gans_taxis.avg_pers_per_trip.mean(axis=0)

st = gans_taxis.status_time
st = st.apply(lambda x : list(x.split(",")))

def get_el(x, place):
    return x[t]

status_time_taxi = pd.DataFrame()
#status_time_taxi[]
for t in range(0, 1441):
    status_time_taxi[t]=st.apply(lambda x: get_el(x, t))
    
print(status_time_taxi)

l = list()
for i in range(0,1441):
    l.append(i)

status = pd.DataFrame(columns=l)
for t in range(0, 1441):
    status.loc["working", t]=len(status_time_taxi[status_time_taxi[t].str.contains("working")])
    status.loc["free", t]=len(status_time_taxi[status_time_taxi[t].str.contains("free")])
    status.loc["charging", t]=len(status_time_taxi[status_time_taxi[t].str.contains("charging")])
    status.loc["cleaning", t]=len(status_time_taxi[status_time_taxi[t].str.contains("cleaning")])
    status.loc["waiting", t]=len(status_time_taxi[status_time_taxi[t].str.contains("waiting")])
    
print(status)
status.to_csv('gans_status_taxi.csv')

st = gans_taxis_empty.status_time
st = st.apply(lambda x : list(x.split(",")))

def get_el(x, place):
    return x[t]

status_time_taxi = pd.DataFrame()
#status_time_taxi[]
for t in range(0, 1441):
    status_time_taxi[t]=st.apply(lambda x: get_el(x, t))
    
print(status_time_taxi)

l = list()
for i in range(0,1441):
    l.append(i)

status = pd.DataFrame(columns=l)
for t in range(0, 1441):
    print(t)
    status.loc["working", t]=len(status_time_taxi[status_time_taxi[t].str.contains("working")])
    status.loc["free", t]=len(status_time_taxi[status_time_taxi[t].str.contains("free")])
    status.loc["charging", t]=len(status_time_taxi[status_time_taxi[t].str.contains("charging")])
    status.loc["cleaning", t]=len(status_time_taxi[status_time_taxi[t].str.contains("cleaning")])
    status.loc["waiting", t]=len(status_time_taxi[status_time_taxi[t].str.contains("waiting")])
    status.loc["booked for cleaning", t]=len(status_time_taxi[status_time_taxi[t].str.contains("booked_for_cleaning")])
    status.loc["booked for charging", t]=len(status_time_taxi[status_time_taxi[t].str.contains("booked_for_charge")])
    status.loc["booked", t]=len(status_time_taxi[status_time_taxi[t] == (" 'booked'")])
print(status)
status.to_csv('gans_status_taxi_empty.csv')

st = gans_stations_empty.status_time
st = st.apply(lambda x : list(x.split(",")))

def get_el(x, place):
    return x[t]

status_time_taxi = pd.DataFrame()
#status_time_taxi[]
for t in range(0, 1441):
    status_time_taxi[t]=st.apply(lambda x: get_el(x, t))
    
print(status_time_taxi)

l = list()
for i in range(0,1441):
    l.append(i)

status = pd.DataFrame(columns=l)
for t in range(0, 1441):
    print(t)
    status.loc["busy", t]=len(status_time_taxi[status_time_taxi[t].str.contains("busy")])
    status.loc["free", t]=len(status_time_taxi[status_time_taxi[t].str.contains("free")])
print(status)
status.to_csv('gans_status_stations_empty.csv')


st = gans_stations.status_time
st = st.apply(lambda x : list(x.split(",")))

def get_el(x, place):
    return x[t]

status_time_taxi = pd.DataFrame()
#status_time_taxi[]
for t in range(0, 1441):
    status_time_taxi[t]=st.apply(lambda x: get_el(x, t))
    
print(status_time_taxi)

l = list()
for i in range(0,1441):
    l.append(i)

status = pd.DataFrame(columns=l)
for t in range(0, 1441):
    print(t)
    status.loc["busy", t]=len(status_time_taxi[status_time_taxi[t].str.contains("busy")])
    status.loc["free", t]=len(status_time_taxi[status_time_taxi[t].str.contains("free")])
print(status)
status.to_csv('gans_status_stations.csv')
"""