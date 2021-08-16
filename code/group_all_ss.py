import pandas as pd


#df = pandas.read_csv(filepath, sep='delimiter', header=None)
ss_age_fe = pd.read_csv('SectorStat_Age_Femme.csv', sep=';')
print(ss_age_fe)

territoires = ss_age_fe.Territoire
print(territoires)

#all_hh = pd.DataFrame()
i = 0
persid = 0
for ter in territoires:
    
    if i == 0:
        print("zero", i)
        filename = 'hh_'+str(ter)+'.csv'
        file = pd.read_csv(filename)
        all_hh = file
        persid = len(all_hh)
        
    elif i <3 and i >0:
        print("next", i)
        filename = 'hh_'+str(ter)+'.csv'
        file = pd.read_csv(filename)
        persid = len(all_hh)
        #print(file.HouseholdID)
        file['PersID']=file['PersID']+persid
        hhid= max(file['HouseholdID'])+1
        file['HouseholdID']=file['HouseholdID']+hhid
        all_hh = pd.concat([all_hh, file], ignore_index=True)
        
        #print(file.HouseholdID)
        
    else:
        break
    
    i+=1
    
print(all_hh)
    
all_hh.to_csv("all_hh_ss.csv")
