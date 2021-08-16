import pandas as pd

simu = pd.read_csv('all_hh_tot.csv')
print(simu)

th_fe = pd.read_csv('SectorStat_Age_Femmes.csv', sep=';')
print(th_fe)

th_ho = pd.read_csv('SectorStat_Age_Hommes.csv', sep=';')
print(th_ho)

sectors = th_fe.Code

colnames = ["SectorStatID"]

for  i in range(0, 100):
    colnames.append(i)
    
pivot_fe = pd.DataFrame(columns=colnames)
pivot_fe.set_index("SectorStatID", inplace=True)

for s in sectors:
    for age in range(0,100):
        simu_fe = simu[(simu.GenderID == 1) & (simu.Age == age) & (simu.SectorStatID == s)]
        pivot_fe.loc[s, age] = len(simu_fe)
print(pivot_fe)
pivot_fe.to_csv('pivot_hh_fe.csv')


colnames = ["SectorStatID"]

for  i in range(0, 95):
    colnames.append(i)
    
pivot_ho = pd.DataFrame(columns(=colnames)
pivot_ho.set_index("SectorStatID", inplace=True)

for s in sectors:
    for age in range(0,95):
        simu_ho = simu[(simu.GenderID == 0) & (simu.Age == age) & (simu.SectorStatID == s)]
        pivot_ho.loc[s, age] = len(simu_ho)
print(pivot_ho)
pivot_ho.to_csv('pivot_hh_ho.csv')
    