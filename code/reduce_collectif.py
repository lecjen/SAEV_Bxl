import pandas as pd

pop = pd.read_csv('all_hh_final.csv')
print(pop.columns)
pop.drop(columns=["Unnamed: 0"], inplace = True)

repart = pd.read_csv('ages_tranches_5ans_par_sex.csv', sep=';')
print(repart.columns)

sectors = pop.SectorStatID
sectors.drop_duplicates(inplace=True)

repart.set_index('Code', inplace=True, drop=True)
print(repart)

age_min = 0
age_max = 4
for ss in sectors:
    print("ss", ss)
    for k in range(0,20):
        print("k", k)
        if k == 19:
            name_col_fe = "95+ ans femmes"
        else:
            name_col_fe = str(age_min+k*5)+"-"+str(age_max+k*5)+' ans femmes'

        nb_fe = round(repart[name_col_fe][ss])

        currently_fe = pop[(pop.SectorStatID == ss) & (pop.GenderID == 1) & (pop.Age >= age_min+k*5) & (pop.Age <= age_max+k*5)]
        nb_fe_too_many = len(currently_fe)-nb_fe
        possible_fe = pop[(pop.SectorStatID == ss) & (pop.GenderID == 1) & (pop.Age >= age_min+k*5) & (pop.Age <= age_max+k*5) & (pop.HouseholdTypeID == 6)]

        ind_fe = possible_fe.index


        j = 0
        while nb_fe_too_many > 0 and len(possible_fe) > 0:
            print("j", j)
            possible_fe.drop([ind_fe[j]], inplace=True)
            pop.drop([ind_fe[j]], inplace=True)

            nb_fe_too_many -=1
            j+=1

    for k in range(0,20):
        print("k ho", k)
        if k == 19:
            name_col_ho = "95+ ans hommes"
        else:
            name_col_ho = str(age_min+k*5)+"-"+str(age_max+k*5)+' ans hommes'
            
        nb_ho = round(repart[name_col_ho][ss])
        currently_ho = pop[(pop.SectorStatID == ss) & (pop.GenderID == 1) & (pop.Age >= age_min+k*5) & (pop.Age <= age_max+k*5)]
        nb_ho_too_many = len(currently_ho)-nb_ho
        possible_ho = pop[(pop.SectorStatID == ss) & (pop.GenderID == 0) & (pop.Age >= age_min+k*5) & (pop.Age <= age_max+k*5) & (pop.HouseholdTypeID == 6)]
        ind_ho = possible_ho.index
        j = 0
        while nb_ho_too_many > 0 and len(possible_ho) > 0:
            print("j ho", j)
            possible_ho.drop([ind_ho[j]], inplace=True)
            pop.drop([ind_ho[j]], inplace=True)

            nb_ho_too_many -=1
            j+=1

print(pop)
pop.to_csv("all_hh_collectif_cleaned_v2.csv")
