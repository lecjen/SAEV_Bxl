import pandas as pd
import numpy as np

ranking = pd.read_csv('ss_closeness_ranking_v2.csv')
print(ranking)
print(ranking.columns, "col")
print(ranking.index, 'ind')
ranking.set_index('SectorStatID', inplace=True, drop=True)


peri = pd.read_csv('ss_peripherie.csv', sep=";")
print(peri)

peri = peri[peri.Peripherie == "Périphérie"]
peri = peri.Code

closest_peri = pd.DataFrame()
closest_peri["SectorStatID"]=ranking.index
closest_peri.set_index('SectorStatID', inplace=True, drop=True)
closest_peri["Closest_Peri"]=np.zeros(len(closest_peri))

for ind in closest_peri.index:
    for i in range(1, 725):
        ss_best_ranked = ranking[str(i)][ind]
        if ss_best_ranked in peri:
            break

    closest_peri.loc[ind, "Closest_Peri"]= ss_best_ranked

print(closest_peri)
closest_peri.to_csv('closest_ss_peri_v2.csv')
