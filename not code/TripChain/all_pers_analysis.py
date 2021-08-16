import pandas as pd

all_pers = pd.read_csv('all_pers_tripchaintype_in_and_out.csv') 
print(all_pers) #3 411 960

imo = all_pers[all_pers.TripChainType == 0]
print(imo)
