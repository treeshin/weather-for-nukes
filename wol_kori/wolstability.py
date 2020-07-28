# Stability index histogram
# sorting time and season

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('wol_2018.csv',
                    sep = ",",
                    header = 0,
                    engine = 'python')

df.columns = ['year','month','day','hour','minute',
                'temp_10','direction_10','speed_10','maxspeed_10',
                'temp_58','direction_58','speed_58','maxspeed_58',
                'stability_temp','stability_10','stability_58'
            ]

stability = df.stability_58
stability_index = np.zeros(len(stability))

for i in range(len(stability)):
#    if 6 <= df.hour[i] < 18: # daytime
#    if df.hour[i] < 6 or df.hour[i] >= 18 : # nighttime
#    if df.month[i] == 3 or df.month[i] == 4 or df.month[i] == 5: # spring
#    if df.month[i] == 6 or df.month[i] == 7 or df.month[i] == 8: # summer
#    if df.month[i] == 9 or df.month[i] == 10 or df.month[i] == 11: # autumn
    if df.month[i] == 1 or df.month[i] == 2 or df.month[i] == 12: # winter
        if stability[i] == 'A':
            stability_index[i] = 1
        elif stability[i] == 'B':
            stability_index[i] = 2
        elif stability[i] == 'C':
            stability_index[i] = 3
        elif stability[i] == 'D':
            stability_index[i] = 4
        elif stability[i] == 'E':
            stability_index[i] = 5
        elif stability[i] == 'F':
            stability_index[i] = 6
        elif stability[i] == 'G':
            stability_index[i] = 7

plt.figure(figsize=(5, 5))
d = np.diff(np.unique(stability_index)).min()
left_of_first_bin = 0.5
right_of_last_bin = 7.5
plt.hist(stability_index, np.arange(left_of_first_bin, right_of_last_bin + d, d),
        color = 'darkgrey', edgecolor = 'white', rwidth = 0.8)
plt.title('Wolsong 2018 58m DEC-FEB')
plt.show()