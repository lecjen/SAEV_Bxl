import pandas as pd
import random

all_hh = pd.read_csv('all_hh_tot.csv')
print(all_hh)
e

young_couple_fe = all_hh[(all_hh.Age <20) & (all_hh.Age > 14) & (all_hh.WorkerID != 10) & (all_hh.ChildOrParent == "parent") & (all_hh.HouseholdTypeID == 2) & (all_hh.GenderID ==1)]
hh_concerned = young_couple_fe.HouseholdID.tolist()
nb = 0.9*len(hh_concerned)
hh_concerned = random.sample(hh_concerned, nb)

to_del = all_hh[all_hh.HouseholdID.isin(hh_concerned)]

index_to_del = to_del.index
all_hh_cleaned = all_hh.drop(index_to_del)
print(all_hh_cleaned)
all_hh_cleaned.to_csv('all_hh_child_Reallocated.csv')
