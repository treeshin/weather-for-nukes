################################
##                            ##
##  See 'wol_test3.py' first  ##
##                            ##
## Allwine and Whiteman, 1994 ##
##  Quantifying wind run and  ##
##    recirculation index     ##
##                            ##
################################

import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from wolfill import index, speed, direction

n = np.zeros(len(speed))
e = np.zeros(len(speed))
V = np.zeros(len(speed))

for i in range(len(speed)):
    n[i] = speed[i] * math.cos(direction[i] - 180)
    e[i] = speed[i] * math.sin(direction[i] - 180)
    V[i] = math.sqrt(n[i]**2 + e[i]**2)
print(n)
print(e)

num = len(speed)/8
num = int(num)

X = np.zeros(num)
Y = np.zeros(num)
S = np.zeros(num)
L = np.zeros(num)
R = np.zeros(num)

for i in range(num):
    for j in range(8):
        X[i] = X[i] + 10800 * n[i*8+j]
        Y[i] = Y[i] + 10800 * e[i*8+j]
        S[i] = S[i] + 10800 * V[i*8+j]
    L[i] = math.sqrt(X[i]**2 + Y[i]**2)
    R[i] = 1 - L[i]/S[i]

print('V is', sum(V)/len(V))
print('S is', sum(S)/(1000*len(S)))
print('R is', sum(R)/len(R))