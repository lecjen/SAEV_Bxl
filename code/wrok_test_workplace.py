import pyodbc
import pandas as pd

print("coucou")
co = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=C:/Users/MediMonster/Downloads/workplace/TU_GEO_LPW_SECTOR.mdb')
cursor = co.cursor()
cursor.execute("SELECT * FROM resultat")
colnames = ['CD_RGN_RESIDENCE', 'TX_RGN_RESIDENCE_DESCR_NL',
            'TX_RGN_RESIDENCE_DESCR_FR', 'CD_PROV_RESIDENCE',
            'TX_PROV_RESIDENCE_DESCR_NL', 'TX_PROV_RESIDENCE_DESCR_FR',
            'CD_DSTR_RESIDENCE', 'TX_ADM_DSTR_RESIDENCE_DESCR_NL',
            'TX_ADM_DSTR_RESIDENCE_DESCR_FR', 'CD_MUNTY_RESIDENCE',
            'TX_MUNTY_RESIDENCE_DESCR_NL', 'TX_MUNTY_RESIDENCE_DESCR_FR',
            'CD_SECTOR_RESIDENCE', 'TX_SECTOR_RESIDENCE_DESCR_NL',
            'TX_SECTOR_RESIDENCE_DESCR_FR', 'XY_X_LB_72_RESIDENCE',
            'XY_Y_LB_72_RESIDENCE', 'CD_CNTRY_WORK', 'TX_CNTRY_WORK_DESCR_NL',
            'TX_CNTRY_WORK_DESCR_FR', 'CD_RGN_WORK', 'TX_RGN_WORK_DESCR_NL',
            'TX_RGN_WORK_DESCR_FR', 'CD_PROV_WORK', 'TX_PROV_WORK_DESCR_NL',
            'TX_PROV_WORK_DESCR_FR', 'CD_DSTR_WORK', 'TX_ADM_DSTR_WORK_DESCR_NL',
            'TX_ADM_DSTR_WORK_DESCR_FR', 'CD_MUNTY_WORK', 'TX_MUNTY_WORK_DESCR_NL',
            'TX_MUNTY_WORK_DESCR_FR', 'CD_SECTOR_WORK', 'TX_SECTOR_WORK_DESCR_NL',
            'TX_SECTOR_WORK_DESCR_FR', 'XY_X_LB_72_WORK', 'XY_Y_LB_72_WORK',
            'OBS_VALUE']

data = pd.DataFrame(cursor.fetchall())
clean = pd.DataFrame(columns=colnames)
print(data)
i = 0
for ind in data.index:
    print(i)
    clean.loc[i] = data.loc[ind, 0]
    i +=1

print(data)
print(clean)

clean.to_csv("work_flow.csv")