import pandas as pd

all_hh = pd.read_csv('all_hh_final.csv')
all_hh.drop(columns=["Unnamed: 0"], inplace=True)
print(all_hh, "all_hh")