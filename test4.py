# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:48:38 2021

@author: kabec
"""
import numpy as np
import scipy as sp
import pandas as pd
from winProcessing import fftsplitter
import matplotlib.pyplot as plt


freqskey = (600, 900, 1200, 1500, 2400, 2700, 3000, 3600, 50,
            425, 475, 575, 725, 775, 4261, 75, 125, 175, 225, 275, 325, 3348)
fc1 = (590, 890, 1190, 1490, 2390, 2690, 2990, 3590, 46,
       413, 463, 563, 713, 763, 4161, 70, 113, 162, 209, 258, 308, 3100)
fc2 = (610, 910, 1210, 1510, 2410, 2710, 3010, 3610, 54,
       437, 487, 587, 737, 787, 4361, 83, 134, 187, 238, 287, 336, 3600)
freqsLimit = (70, 66.7, 78.3, 90,  31.3, 10.7,  4.7,  1.2, 8.3,
              1.6, 1.6, 1.6, 1.6, 1.6,  2, 18.3, 12.3, 12.3, 8.99, 10.3, 8.3,  1.2)

All_freqsDB = {}
Harmonicks_freqsDB = {}
RC_freqsDB = {}
ALS_freqsDB = {}
for i, val in enumerate(freqskey):
    All_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
    if i in range(0, 8):
        Harmonicks_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
    elif i in range(8, 15):
        RC_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
    elif i in range(15, 22):
        ALS_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
del i, val, fc1, fc2, freqsLimit, freqskey
