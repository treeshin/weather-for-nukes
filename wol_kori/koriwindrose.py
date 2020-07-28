# Wind rose plotting
# sorting time and season

import numpy as np
import pandas as pd
from windrose import WindroseAxes
from matplotlib import pyplot as plt

df = pd.read_csv('kori_2018.csv',
                    sep = ",",
                    header = 0,
                    engine = 'python')

df.columns = ['year','month','day','hour','minute',
                'temp_1point5','temp_10','direction_10','speed_10',
                'temp_58','direction_58','speed_58',
                'stability_temp'
            ]

df = np.array(df)

index = []
for i in range(len(df)):
    if df[i,10] == '-' or df[i,11] == '-':
        index = np.append(index,i)

if len(index) != 0:
    index  = index.astype(int)
    df = np.delete(df, index, axis = 0)

year = df[:,0]
month = df[:,1]
day = df[:,2]
hour = df[:,3]
minute = df[:,4]
temp_1point5 = df[:,5]
temp_10 = df[:,6]
direction_10 = df[:,7]
speed_10 = df[:,8]
temp_58 = df[:,9]
direction_58 = df[:,10]
speed_58 = df[:,11]
stability_temp = df[:,12]

stability = stability_temp
direction = direction_58.astype(float)
winspeed  = speed_58.astype(float)

speed_new=[]
direction_new=[]


for i in range(len(winspeed)):
#    if 6 <= hour[i] < 18: # daytime
#    if hour[i] < 6 or hour[i] >= 18 : # nighttime
#    if month[i] == 3 or month[i] == 4 or month[i] == 5: # spring
#    if month[i] == 6 or month[i] == 7 or month[i] == 8: # summer
#    if month[i] == 9 or month[i] == 10 or month[i] == 11: # autumn
    if month[i] == 1 or month[i] == 2 or month[i] == 12: # winter
#    if stability[i] == 'A':
        speed_new = np.append(speed_new, winspeed[i])
        direction_new = np.append(direction_new, direction[i])

ws = np.array(speed_new)
wd = np.array(direction_new)
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
plt.title('Kori 2018 DEC-FEB')
plt.show()