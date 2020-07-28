# Wind rose plotting
# sorting time and season

import numpy as np
import pandas as pd
from windrose import WindroseAxes
from matplotlib import pyplot as plt

df = pd.read_csv('wol_2016.csv',
                    sep = ",",
                    header = 0,
                    engine = 'python')

df.columns = ['year','month','day','hour','minute',
                'temp_10','direction_10','speed_10','maxspeed_10',
                'temp_58','direction_58','speed_58','maxspeed_58',
                'stability_temp','stability_10','stability_58'
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
temp_10 = df[:,5]
direction_10 = df[:,6]
speed_10 = df[:,7] 
maxspeed_10 = df[:,8]
temp_58 = df[:,9]
direction_58 = df[:,10]
speed_58 = df[:,11]
maxspeed_58 = df[:,12]
stability_temp = df[:,13]
stability_10 = df[:,14]
stability_58 = df[:,15]

stability = stability_58
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
    if month[i] == 1: # or month[i] == 2 or month[i] == 12: # winter
        speed_new = np.append(speed_new, winspeed[i])
        direction_new = np.append(direction_new, direction[i])

ws = np.array(speed_new)
wd = np.array(direction_new)
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
plt.title('Wolsong 2016 JAN')
plt.show()