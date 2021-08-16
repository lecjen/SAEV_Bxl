import pandas as pd

distances = pd.read_csv('distances_ss.csv')
distances.set_index("SectorStatID_1", inplace=True, drop=True)
distances.drop(columns=["SectorStatID_1.1"], inplace=True)
print(distances)

inf_250 = dict()
d_250_500 = dict()
d_500_1 = dict()
d_1_2 = dict()
d_2_3 = dict()
d_3_5 = dict()
d_5_7_5 = dict()
d_7_5_10 = dict()
d_10_15 = dict()
d_15_25 = dict()
d_25_40 = dict()
#sup_40 = dict()

for ss in distances.index:
    print('ss', ss)
    
    inf_250[ss] = list()
    d_250_500[ss] = list()
    d_500_1[ss] = list()
    d_1_2[ss] = list()
    d_2_3[ss] = list()
    d_3_5[ss] = list()
    d_5_7_5[ss] = list()
    d_7_5_10[ss] = list()
    d_10_15[ss] = list()
    d_15_25[ss] = list()
    d_25_40[ss] = list()
    #sup_40[ss] = list()
    
    
    for ss_to in distances.index:
        print("ss to", ss_to)
        dist = distances.loc[ss, ss_to]
        if dist <= 0.25:
            inf_250[ss].append(ss_to)
        elif dist > 0.25 and dist <= 0.5:
            d_250_500[ss].append(ss_to)
        elif dist > 0.5 and dist <= 1:
            d_500_1[ss].append(ss_to)            
        elif dist > 1 and dist <= 2:
            d_1_2[ss].append(ss_to)             
        elif dist > 2 and dist <= 3:
            d_2_3[ss].append(ss_to) 
        elif dist > 3 and dist <= 5:
            d_3_5[ss].append(ss_to) 
        elif dist > 5 and dist <= 7.5:
            d_5_7_5[ss].append(ss_to) 
        elif dist > 7.5 and dist <= 10:
            d_7_5_10[ss].append(ss_to) 
        elif dist > 10 and dist <= 15:
            d_10_15[ss].append(ss_to) 
        elif dist > 15 and dist <= 25:
            d_15_25[ss].append(ss_to) 
        elif dist > 25 and dist <= 40:
            d_25_40[ss].append(ss_to)  #Regroupe 25-40 et < 40 car both empty
        else:
            errorDistance
        """
        elif dist > 40:
            sup_40[ss].append(ss_to) 
        """
            
print(inf_250)
print(d_250_500)
print(d_500_1)
print(d_1_2)
print(d_2_3)
print(d_3_5)
print(d_5_7_5)
print(d_7_5_10)
print(d_10_15)
print(d_15_25)
print(d_25_40)
#print(sup_40)

max_dist_ss = pd.DataFrame(columns=["SectorStatID", "Farest ss", "Max distance", "Distance category"])
max_dist_ss.set_index("SectorStatID", inplace=True, drop=True)

for ss in distances.index:
    max_d = max(distances.loc[ss])    
    max_ss = distances.loc[ss].idxmax()
    if max_d <= 0.25:
        dist_cat = 0
    elif max_d > 0.25 and max_d < 0.5:
        dist_cat = 1
    elif max_d > 0.5 and max_d < 1:
        dist_cat = 2
    elif max_d > 1 and max_d < 2:
        dist_cat = 3
    elif max_d > 2 and max_d < 3:
        dist_cat = 4
    elif max_d > 3 and max_d < 5:
        dist_cat = 5
    elif max_d > 5 and max_d < 7.5:
        dist_cat = 6
    elif max_d > 7.5 and max_d < 10:
        dist_cat = 7
    elif max_d > 10 and max_d < 15:
        dist_cat = 8
    elif max_d > 15 and max_d < 25:
        dist_cat = 9
    elif max_d > 25:
        dist_cat = 10
    else:
        errorMaxDist
    max_dist_ss.loc[ss]=[max_ss, max_d, dist_cat]
    

print(max_dist_ss)
    
        