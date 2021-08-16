import pandas as pd

all_hh = pd.read_csv('all_hh_child_Reallocated.csv')
print(all_hh)

not_coll = all_hh[all_hh.HouseholdTypeID != 6]
print(not_coll)

print(not_coll.HouseholdID.drop_duplicates())



