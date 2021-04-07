# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:48:38 2021

@author: kabec
"""
from MyFunctions001 import stdFreqDataBase, testSignal, filterCheb2, fftsplitter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def rms(x):
    return np.sqrt(x.dot(x)/x.size)

SPR = 50e3
t = 5
Rp = 3
Rs = 80

FullStdBase = pd.DataFrame(stdFreqDataBase()[1], index=['fc1', 'fc2', 'Limit'])

freqs = FullStdBase.columns.values

ySigParams, ySig = testSignal(freqs, t, SPR)


#freqs = FullStdBase.columns.values
fc1 = FullStdBase.iloc[0].values
fc2 = FullStdBase.iloc[1].values
N = int(SPR*1)

rmsFiltered, filteredData = filterCheb2(ySig, N, freqs, fc1, fc2, Rp, Rs, SPR)

fftSig, f = fftsplitter(ySig, N, SPR)
fftData = pd.DataFrame(fftSig[freqs], index=[freqs], columns=['Ampl'])

fig, ax = plt.subplots()
ax.plot(f, fftSig)
plt.xlim([50, 3600])
plt.ylim([-1, 1.15*fftSig[50:3600].max()])
plt.grid()
plt.show()

AllDB = pd.DataFrame(((ySigParams['Ampl'].values), (fftData['Ampl'].values), (rmsFiltered['RMS'].values*np.sqrt(2))), columns=(freqs))
