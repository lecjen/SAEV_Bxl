import pandas as pd

creche = pd.read_csv('places_creches_restantes_for_foreigners.csv') #730
print(creche)

mat = pd.read_csv('mat_places_restantes_for_foreigners.csv') #14 should 4 557
print(mat)

prim = pd.read_csv('prim_places_restantes_for_foreigners.csv') #41 should 10 410
print(prim)

sec = pd.read_csv('sec_places_restantes_for_foreigners.csv') #265 should 18 635
print(sec)


