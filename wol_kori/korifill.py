# Fill missing data with previous value
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from function import mean_wind

df = pd.read_csv('kori_2016.csv', sep = ",", header = 0, engine = 'python')

df.columns = ['year','month','day','hour','minute',
                'temp_1point5','temp_10','direction_10','speed_10',
                'temp_58','direction_58','speed_58',
                'stability_temp']

df = np.array(df)

# Fill missing data marked with '-' 
index = []
for i in range(len(df)):
    if df[i,10] == '-' or df[i,11] == '-':
        index = np.append(index,i)
if len(index) != 0:
    index  = index.astype(int)
    for i in range(len(index)):
        df[index[i],5:12] = df[index[i]-1,5:12]

# Standard Kori data
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
##########################################

# Insert previous value to each missing point
for i in range(len(tempi)):
    for j in range(tempd[i]-1):
        index = np.insert(index, tempi[i], index[tempi[i]]-1)
        speed = np.insert(speed, tempi[i], speed[tempi[i]-1])
        direction = np.insert(direction, tempi[i], direction[tempi[i]-1])

index = index.astype(int)
speed = speed.astype(float)
direction = direction.astype(float)

############################################################################
## adjust the interval to desired value

# time series data interval in minutes
interval = 10
interval_new = 180

[deg_mean, deg_std, v_mean]=mean_wind(direction, speed, minute, num, interval, interval_new)

############################################################################

speed = v_mean
direction = deg_mean