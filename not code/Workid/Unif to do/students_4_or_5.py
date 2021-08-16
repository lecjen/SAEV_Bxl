import pandas as pd
import random

jeune = pd.read_csv('student_18_20_nl_workid_4_or_5_to_check_v2.csv')
print(jeune)
adultes = pd.read_csv('student_adultes_nl_workid_4_or_5_to_check_v2.csv')
print(adultes)

j = pd.read_csv('student_18_20_nl_workid_v2.csv')
print(j)
a = pd.read_csv('student_adultes_nl_workid_v2.csv')
print(a)

all_students = pd.concat([jeune, adultes, j, a])
all_students.reset_index(inplace=True, drop=True)
print(all_students)

sectors_names_correspondance = pd.read_csv('sector_stat.csv', sep=';')
#sectors_names_correspondance.set_index("Code", inplace=True, drop=True)
print(sectors_names_correspondance)
sectors_names_correspondance.set_index("Code", inplace=True, drop=True)

ss_campus = ['21001A3MJ', '21001B17-', "21004A13-", '21004A22-', '21004A23-', '21004A23-', '21004A23-', '21004A32-', '21004A32-', '21007A79-', '21009A2MJ', '21010A4MJ', '21014A3MJ', '21015A12-',
             '21015A612']

colnames = all_students.columns.tolist()
colnames.extend(["WorkSectorStatID", "WorkSectorStatName"])
students = pd.DataFrame(columns=colnames)
#p = 0.37 #% in bxl from bxl / in bxl from every where

i=0
for camp in ss_campus:
    avg_nb_student = max(len(all_students)-1500-417-8977-2033-4482, 0)/len(ss_campus-5)
    if camp == '21004A22-':
        avg_nb_student = 1500
    elif camp == '21004A32-':
        avg_nb_student = (417 + avg_nb_student) / 2
    elif camp == '21009A2MJ':
        avg_nb_student = 9877
    elif camp == '21010A4MJ':
        avg_nb_student= 2033
    elif camp == '21015A612':
        avg_nb_student = 4482
    
    while avg_nb_student > 0 and len(all_students) > 0:
        print(i)
        elu = random.randrange(0, len(all_students), 1)
        ind_elu = all_students.index[elu]
    
        work_ss_name = sectors_names_correspondance.loc[camp, "Name"]
        
        if all_students.loc[ind_elu, "SectorStatID"]== camp and all_students.loc[ind_elu, "WorkerID"] != 5:
            work_id = 4
            work_type = "Unif on campus"
        else:
            work_id = 5
            work_type = "Unif off campus"
                
        el = all_students.loc[ind_elu].tolist()
        el.extend([camp, work_ss_name])
        students.loc[i] = el
        
        students.loc[i, "WorkerID"] = work_id
        students.loc[i, "WorkerType"] = work_type
    
        all_students.drop([ind_elu], inplace=True)
    
        avg_nb_student-=1
        i+=1
        
print(students)
students.to_csv('unif_nl_workplace.csv')
"""
sec = pd.read_csv('child_sec_en_avance_so_unif_workId.csv')
print(sec)
"""
