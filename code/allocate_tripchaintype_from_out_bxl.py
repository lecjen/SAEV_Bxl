import random
import bisect
import numpy as np
import pandas as pd

#FROM THESIS
#'Create Cumulative Distribution'
def cdf(weights):
    total=sum(weights); result=[]; cumsum=0
    for w in weights:
        cumsum+=w
        result.append(cumsum/total)
    return result

#FROM THESIS
def assignActivityPattern(distribution):
    'Revise Traveler Type, In the event of no school assigned (incredibly fringe population < 0.001%)'
    """
    if person[len(person) - 3] == 'NA' and (travelerType == 3 or travelerType == 4 or travelerType == 2 or travelerType == 1):
        travelerType = 6
    """
    dist = distribution #allDistributions[travelerType]
    weights = cdf(dist)
    split = random.random()
    idx = bisect.bisect(weights, split)
    return idx

x = 0.06768567336390681 #from collectif ATTENTION pourcentage !!!!!
i = 0.225 - x #22.5 % ATTENTION au divisé par 100
a = 1 - i
"""
all_distributions = {0: [0, 1, 0, 0, 0, 0, 0, 0], 1: [0.05, 0.175, 0.25, 0.2, 0, 0.2, 0.075, 0.05], 2: [0.025, 0.15, 0.2, 0.275, 0, 0.2, 0.1, 0.05],
                     3: [0.025, 0.05, 0.2, 0.225, 0.05, 0.25, 0.15, 0.05], 4: [0.3, 0.3, 0.2, 0.1, 0, 0.04, 0.04, 0.02], 5: [0.05, 0.075, 0.25, 0.225, 0, 0.15, 0.15, 0.1],
                     6: [0.01, 0.05, 0.1, 0.15, 0.15, 0.25, 0.2, 0.09], 7: [0.1, 0.3, 0.2, 0.15, 0, 0.1, 0.1, 0.05], 8: [1, 0, 0, 0, 0, 0, 0, 0], 9: [1, 0, 0, 0, 0, 0, 0, 0],
                     10: [1, 0, 0, 0, 0, 0, 0, 0]}

all_distributions = {"immobile": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "worker": [i, a*0.575, a*0.139, a*0.085, a*0.037, a*0.036, a*0.026, a*0.024, a*0.015, a*0.013, a*0.011, a*0.011, a*0.009, a*0.009, a*0.007, a*0.002, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     "activity": [i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a*0.51, a*0.107, a*0.103, a*0.069, a*0.067, a*0.037, a*0.02, a*0.016, a*0.015, a*0.014, a*0.014, a*0.01, a*0.006, a*0.005, a*0.005, a*0.002]}
"""
distribution = [i, a*0.93, 0, 0, 0, a*0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#creche 0
mat = pd.read_csv("foreign_mat_workplace.csv")
print(mat)
prim = pd.read_csv('foreign_prim_workplace.csv')
print(prim)
sec = pd.read_csv('foreign_sec_workplace.csv')
print(sec)
student = pd.read_csv('foreign_student_workplace.csv')
print(student)
worker = pd.read_csv('foreign_worker_workplace.csv')
print(worker)

print(mat.columns)
print(prim.columns)
print(sec.columns)
print(student.columns)
print(worker.columns)
all_pers = pd.concat([mat, prim, sec, student, worker])
all_pers.drop(columns=['Unnamed: 0'], inplace=True)
all_pers.reset_index(inplace=True, drop=True)
print(all_pers)

all_pers["TripChainType"]=np.zeros(len(all_pers))

for pers in all_pers.index: #TODO adapt
    print("pers", pers)
    """
    worker_id = all_pers.loc[pers, "WorkTypeID"]
    if worker_id == 8 or worker_id == 9 or worker_id == 10:
        chain_key = "immobile"
    elif worker_id == 0 or worker_id == 1 or worker_id == 2 or worker_id == 3 or worker_id == 4 or worker_id == 5 or worker_id == 6:
        chain_key = "worker"
    elif worker_id == 7 or worker_id == 11:
        chain_key = "activity"
    else:
        print(worker_id)
        errorWorkerID
        
    dist = all_distributions[chain_key]
    """
    TripChainType = assignActivityPattern(distribution)
    all_pers.loc[pers, "TripChainType"]=TripChainType

print(all_pers)
all_pers.to_csv("all_pers_tripchaintype_foreign.csv")
