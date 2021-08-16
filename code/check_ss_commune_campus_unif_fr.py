
import pandas as pd

campus = pd.read_csv("sup_campus_bxl_fr_with_ss_v2.csv")

print(campus.columns)

ss = pd.DataFrame()
ss['SectorStat'] = campus.sector_stat
#ss.drop_duplicates(inplace=True)
print(ss)

sectors_names_correspondance = pd.read_csv('sector_stat.csv', sep=';')
#sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
print(sectors_names_correspondance)

ss = ss.merge(sectors_names_correspondance, left_on="SectorStat", right_on="Code", how='inner')
ss.drop(columns=["Code"], inplace=True)
print(ss)
ss.to_csv('campus_fr_ss_commune.csv')
communes = ss.Commune
dic = dict()
for com in communes:
    list_ss = ss[ss.Commune == com].SectorStat.tolist()
    dic[com]=list_ss #len(ss[ss.Commune==com])
    
print(dic)