import pandas as pd


distances = pd.read_csv('distances_ss.csv')
distances.set_index("SectorStatID_1", inplace=True, drop=True)
distances.drop(columns=["SectorStatID_1.1"], inplace=True)
print(distances) #TODO check format

v = 23.7/60 #km/min

time_to = distances/v
print(time_to)

res = pd.DataFrame(columns=time_to.columns.tolist())

for delta in range(0, 40):
    print(delta)
    final = time_to[time_to<=delta]
    
    
    for col in final.columns.tolist():
        r = final[col]
        #r = final["21001A00-"]
        r.dropna(inplace=True)
        r = r.index.tolist()
        
        res.loc[delta, col]= r

print(res)
res.to_csv("delta_t_ori_destis.csv")

#d = res.loc[30]
for col in res.columns:
    if len(res.loc[39, col])<724:
        
        print(col)
        stop
