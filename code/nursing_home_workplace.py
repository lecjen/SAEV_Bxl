import pandas as pd

nursing_home = pd.read_csv('nursing_home.csv')
nursing_home.drop(columns=["Unnamed: 0", "Unnamed: 0.1"], inplace=True)
print(nursing_home)

nursing_home["WorkSectorStat"]=nursing_home["SectorStatID"]
nursing_home["WorkSectorStatName"]=nursing_home["SectorStatName"]
print(nursing_home)

nursing_home.to_csv('nursing_home_workplace.csv')