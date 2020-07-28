import numpy as np
from windrose import WindroseAxes
from matplotlib import pyplot as plt
from function import load_aws, load_asos, missing, mean_10

np.set_printoptions(threshold=np.inf)

m = ['01','02','03','04','05','06','07','08','09','10','11','12']
deg_year = []
v_year = []

for i in range(len(m)):
    if i < 11:
        filename = 'SURFACE_ASOS_108_MI_2019-' + m[i] + '_2019-' + m[i] + '_2019.csv'
    else:
        filename = 'SURFACE_ASOS_108_MI_2019-' + m[i] + '_2019-' + m[i] + '_2020.csv'

    # Load AWS/ASOS data (wind drection, wind speed, and time) 
    [deg, v, minute] = load_asos(filename)

    # Fill missing data by averaging adjacent values
    [deg, v, minute] = missing(deg, v, minute)

    # Calculate 10-minute average for wind direction and wind speed
    [deg_10, v_10] = mean_10(deg, v, minute)
    deg_year = np.append(deg_year, deg_10)
    v_year = np.append(v_year, v_10)
    print("in progress ", i+1, "/ 12")


ws = np.array(v_year)
wd = np.array(deg_year)
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
plt.show()
"""

del_year = np.zeros(len(deg_year)-1)
stability = np.zeros(len(del_year))
for i in range(len(deg_year)-1):
    del_year[i] = abs(deg_year[i+1] - deg_year[i])
    if del_year[i] > 180:
        del_year[i] = 360 - del_year[i]

for i in range(len(deg_year)-1):
    if del_year[i] >= 22.5:
        stability[i] = 1
    elif del_year[i] >= 17.5 and del_year[i] < 22.5:
        stability[i] = 2
    elif del_year[i] >= 12.5 and del_year[i] < 17.5:
        stability[i] = 3
    elif del_year[i] >= 7.5 and del_year[i] < 12.5:
        stability[i] = 4
    elif del_year[i] >= 3.8 and del_year[i] < 7.5:
        stability[i] = 5
    elif del_year[i] >= 2.1 and del_year[i] < 3.8:
        stability[i] = 6
    elif del_year[i] < 2.1:
        stability[i] = 7

d = np.diff(np.unique(stability)).min()
left_of_first_bin = stability.min() - float(d)/2
right_of_last_bin = stability.max() + float(d)/2
plt.hist(stability, np.arange(left_of_first_bin, right_of_last_bin + d, d), edgecolor = 'white')
plt.show()
"""
