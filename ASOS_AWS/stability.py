import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from function import load_aws, load_asos, missing, mean_10

np.set_printoptions(threshold=np.inf)

# Load AWS data (wind drection, wind speed, and time) 
filename = 'SURFACE_ASOS_108_MI_2019-01_2019-01_2019.csv'
[deg, v, minute] = load_asos(filename)

# Fill missing data by averaging adjacent values
[deg, v, minute] = missing(deg, v, minute)

# Calculate 10-minute average for wind direction and wind speed
[deg_10, v_10] = mean_10(deg, v, minute)


del_10 = np.zeros(len(deg_10)-1)
stability = np.zeros(len(del_10))
for i in range(len(deg_10)-1):
    del_10[i] = abs(deg_10[i+1] - deg_10[i])
    if del_10[i] > 180:
        del_10[i] = 360 - del_10[i]

for i in range(len(deg_10)-1):
    if del_10[i] >= 22.5:
        stability[i] = 1
    elif del_10[i] >= 17.5 and del_10[i] < 22.5:
        stability[i] = 2
    elif del_10[i] >= 12.5 and del_10[i] < 17.5:
        stability[i] = 3
    elif del_10[i] >= 7.5 and del_10[i] < 12.5:
        stability[i] = 4
    elif del_10[i] >= 3.8 and del_10[i] < 7.5:
        stability[i] = 5
    elif del_10[i] >= 2.1 and del_10[i] < 3.8:
        stability[i] = 6
    elif del_10[i] < 2.1:
        stability[i] = 7

d = np.diff(np.unique(stability)).min()
left_of_first_bin = stability.min() - float(d)/2
right_of_last_bin = stability.max() + float(d)/2
plt.hist(stability, np.arange(left_of_first_bin, right_of_last_bin + d, d), edgecolor = 'white')
plt.show()


        

    
