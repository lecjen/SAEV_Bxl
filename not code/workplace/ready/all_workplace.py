import pandas as pd


workers_1 = pd.read_csv('to_much_worker.csv')
workers_1.drop(columns=["Commune"], inplace=True)
print(workers_1)

workers_2 = pd.read_csv('worker_workplace_z_out.csv')
workers_2.drop(columns=["Commune"], inplace=True)
print(workers_2)

workers_3 = pd.read_csv('worker_workplace_bxl_out_normal.csv')
workers_3.drop(columns=["Commune"], inplace=True)
print(workers_3)

workers_4 =pd.read_csv('worker_workplace_z_z.csv')
workers_4.drop(columns=["Commune"], inplace=True)
print(workers_4)

workers_5 = pd.read_csv('worker_workplace_bxl_z.csv')
workers_5.drop(columns=["Commune"], inplace=True)
print(workers_5)

workers_6 = pd.read_csv('worker_workplace_z_bxl.csv')
workers_6.drop(columns=["Commune"], inplace=True)
print(workers_6)

workers_7 = pd.read_csv('worker_workplace_bxl_bxl_normal.csv')
workers_7.drop(columns=["Commune"], inplace=True)
print(workers_7)

unif_1 = pd.read_csv('unif_nl_workplace.csv')
unif_1.drop(columns=["Unnamed: 0.1", "Code", "Commune"], inplace=True)
print(unif_1)

unif_2 = pd.read_csv('students_16_17_unif_workplace_v2.csv')
unif_2.drop(columns=["Code", "Commune"], inplace=True)
print(unif_2)

unif_3 = pd.read_csv('student_adultes_nl_to_out_workplace_v2.csv')
unif_3.drop(columns=["Commune_y", "Code_x", "Code_y", "Name", "Commune_x"], inplace=True)
print(unif_3)

unif_4 = pd.read_csv('students_adultes_unif_workplace_v2.csv')
unif_4.drop(columns=["Code", "Commune"], inplace=True)
print(unif_4)

unif_5 = pd.read_csv('student_18_20_nl_to_out_workplace_v2.csv')
unif_5.drop(columns=["Commune_y", "Code_x", "Code_y", "Name", "Commune_x"], inplace=True)
print(unif_5)

unif_6 = pd.read_csv('students_18_20_unif_workplace_v2.csv')
unif_6.drop(columns=["Code", "Commune"], inplace=True)
print(unif_6)

home = pd.read_csv('all_at_home_workplace.csv')
print(home)

sec = pd.read_csv('secondaires_workplace.csv')
sec.drop(columns=["Commune_y", "Quartier", "WorkCommuneName", "Name", "Commune_x"], inplace=True)
print(sec)

prim = pd.read_csv('primaires_workplace.csv')
prim.drop(columns=["Quartier", "WorkCommuneName", "Commune"], inplace=True)
print(prim)

mat = pd.read_csv('maternelles_workplace.csv')
mat.drop(columns=["Quartier", "WorkCommuneName", "Commune"], inplace=True)
print(mat)

creche = pd.read_csv('baby_creche_and_stay_home_workplace.csv')
print(creche)

workplace = pd.concat([workers_1, workers_2, workers_3, workers_4, workers_5, workers_6, workers_7, unif_1, unif_2, unif_3, unif_4, unif_5, unif_6, 
                   home, sec, prim, mat, creche])
print(workplace)
workplace.to_csv('all_workplace.csv')