import pandas as pd

distances = pd.read_csv('distances_ss.csv')
print(distances) #TODO check whether unnamed col and SectorStatID_1 est une col comme les autres

colname = []
for place in range(1, 725):
    colname.append(place)


closeness = pd.DataFrame(columns=colname)
closeness['SectorStatID']=distances['SectorStatID_1']
closeness['SectorStatID_1']=distances['SectorStatID_1']

closeness.set_index('SectorStatID', inplace=True, drop=True)
print(closeness, "closeness")

def ranking(x, distances):
    print(x)
    row = distances[distances.SectorStatID_1 == x]
    row.drop(columns=["SectorStatID_1.1", "SectorStatID_1"], inplace=True)
    ind = row.index[0]
    print(ind, "ind")
    res = []
    for place in range(1, 725):
        print(place)
        print(row)
        ss = row.idxmin(axis=1)
        print(ss.loc[ind], 'ss')
        #closeness.loc[x, place]= ss.loc[ind]
        res.append(ss.loc[ind])
        row.drop(columns=[ss.loc[ind]], inplace=True)

    #closeness.loc[x]=res

    return res #closeness

#print(closeness.SectorStatID_1)

#closeness = closeness["SectorStatID_1"].apply(lambda x: ranking(x, distances, closeness))

for ss in closeness.SectorStatID_1:
    closeness.loc[ss]=[ss]+ ranking(ss, distances)



print(closeness)

closeness.to_csv("ss_closeness_ranking_v2.csv")




