# Fill missing data with previous value
# and also generates .txt file for further use
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from function import mean_wind

df = pd.read_csv('wol_2018.csv', sep = ",", header = 0, engine = 'python')

df.columns = ['year','month','day','hour','minute',
                'temp_10','direction_10','speed_10','maxspeed_10',
                'temp_58','direction_58','speed_58','maxspeed_58',
                'stability_temp','stability_10','stability_58'
            ]

df = np.array(df)

# Fill missing data marked with '-' 
index = []
for i in range(len(df)):
    if df[i,10] == '-' or df[i,11] == '-' or df[i,13] == '-':
        index = np.append(index,i)
if len(index) != 0:
    index  = index.astype(int)
    for i in range(len(index)):
        df[index[i],5:15] = df[index[i]-1,5:15]

# Standard Kori data
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

# Leap year check
if year[0] % 4 == 0:
    feb = 29; num = 366
else:
    feb = 28; num = 365
num_mon = [31, feb, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Index from 1 to 52560 (every 10 minutes)
index = np.zeros(len(df))

# Missing data index and differece temp
tempi = []
tempd = []

for i in range(len(df)):
    if month[i] == 1:
        index[i] = 144 * (day[i] - 1) + 6 * hour[i] + (minute[i] / 10)
    else:
        index[i] = 144 * np.sum(num_mon[0:month[i]-1]) + 144 * (day[i] - 1) + 6 * hour[i] + (minute[i] / 10)

    if i >= 1:
        diff = index[i]-index[i-1]
        diff = diff.astype(int)
        if diff != 1:
           tempi=np.append(tempi, i)
           tempd=np.append(tempd, diff)
tempi = tempi.astype(int); tempd = tempd.astype(int)

for i in range(len(tempi)-1):
    tempi[i+1] = tempi[i+1]+sum(tempd[0:i+1])-i-1

##########################################
## Choose speed and direction data here ##
speed = speed_58
direction = direction_58
stability = stability_temp
##########################################

# Insert previous value to each missing point
for i in range(len(tempi)):
    for j in range(tempd[i]-1):
        index = np.insert(index, tempi[i], index[tempi[i]]-1)
        speed = np.insert(speed, tempi[i], speed[tempi[i]-1])
        direction = np.insert(direction, tempi[i], direction[tempi[i]-1])
        stability = np.insert(stability, tempi[i], stability[tempi[i]-1])
        

index = index.astype(int)
speed = speed.astype(float)
direction = direction.astype(float)
stability = stability.astype(str)

############################################################################
## adjust the interval to desired value

# time series data interval in minutes
#interval = 10
#interval_new = 180

#[deg_mean, deg_std, v_mean]=mean_wind(direction, speed, minute, num, interval, interval_new)

############################################################################

#speed = v_mean
#direction = deg_mean

for i in range(len(speed)):
    if direction[i] < 11.25 or direction[i] >= 348.75:
        direction[i] = 1
    elif 11.25 <= direction[i] < 33.75:
        direction[i] = 2
    elif 33.75 <= direction[i] < 56.25:
        direction[i] = 3
    elif 56.25 <= direction[i] < 78.75:
        direction[i] = 4
    elif 78.75 <= direction[i] < 101.25: 
        direction[i] = 5
    elif 101.25 <= direction[i] < 123.75:
        direction[i] = 6
    elif 123.75 <= direction[i] < 146.25:
        direction[i] = 7
    elif 146.25 <= direction[i] < 168.75:
        direction[i] = 8
    elif 168.75 <= direction[i] < 191.25:
        direction[i] = 9
    elif 191.25 <= direction[i] < 213.75:
        direction[i] = 10
    elif 213.75 <= direction[i] < 236.25:
        direction[i] = 11
    elif 236.25 <= direction[i] < 258.75:
        direction[i] = 12
    elif 258.75 <= direction[i] < 281.25:
        direction[i] = 13
    elif 281.25 <= direction[i] < 303.75:
        direction[i] = 14
    elif 303.75 <= direction[i] < 326.25:
        direction[i] = 15
    elif 326.25 <= direction[i] < 348.75:
        direction[i] = 16

for i in range(len(speed)):
    if stability[i] == 'A':
        stability[i] = 1
    elif stability[i] == 'B':
        stability[i] = 2
    elif stability[i] == 'C':
        stability[i] = 3
    elif stability[i] == 'D':
        stability[i] = 4
    elif stability[i] == 'E':
        stability[i] = 5
    elif stability[i] == 'F':
        stability[i] = 6
    elif stability[i] == 'G':
        stability[i] = 7

direction = direction.astype(int)
stability = stability.astype(int)

f= open("speed.txt","w+")
for i in range(len(speed)):
     f.write("%f\n" % (speed[i]))