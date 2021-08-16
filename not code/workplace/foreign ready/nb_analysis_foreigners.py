import pandas as pd

work = pd.read_csv('foreign_worker_workplace.csv')
print(work) #410 381

unif = pd.read_csv('foreign_student_workplace.csv')
print(unif) #17 055

tourist = pd.read_csv('foreign_tourists_workplace.csv')
print(tourist) #10 069