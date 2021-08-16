import pandas as pd

tourists = pd.read_csv('tourists_tripchaintype.csv')
print(tourists)

maj = pd.read_csv('all_pers_tripchaintype_including_at_home.csv')
maj.drop(columns=['Unnamed: 0.1.1', 'ChildOrParent'], inplace=True)
print(maj)

foreign = pd.read_csv('all_pers_tripchaintype_foreign.csv')
print(foreign)


all_pers = pd.concat([tourists, maj, foreign])
all_pers.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'], inplace=True)
print(all_pers)
all_pers.to_csv('all_pers_tripchaintype_in_and_out.csv')

for i in range(1, 32):
    all_pers_i = all_pers[all_pers.TripChainType == i]
    name = 'all_pers_type_' + str(i) + '.csv'
    print('i', i)
    print(all_pers_i)
    all_pers_i.to_csv(name)

