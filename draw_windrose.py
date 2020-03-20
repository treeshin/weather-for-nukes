import numpy as np
from windrose import WindroseAxes
from matplotlib import pyplot as plt
from function import load_aws, load_asos, missing, mean_10

np.set_printoptions(threshold=np.inf)

# Load AWS data (wind drection, wind speed, and time) 
filename = 'SURFACE_ASOS_108_MI_2019-01_2019-01_2019.csv'
[deg, v, minute] = load_asos(filename)

# Fill missing data by averaging adjacent values
[deg, v, minute] = missing(deg, v, minute)

# Calculate 10-minute average for wind direction and wind speed
[deg_10, v_10] = mean_10(deg, v, minute)

ws = np.array(v_10)
wd = np.array(deg_10)
ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()

plt.show()