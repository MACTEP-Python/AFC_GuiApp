# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:34:39 2021

@author: kabec
"""
import numpy as np
import scipy as sp
import pandas as pd
from winProcessing import fftsplitter, filterCheb2
import matplotlib.pyplot as plt

SPR = 50e3
N = int(SPR*0.2)
t = np.arange(0, 5, 1/SPR)
freqs = np.array([50, 75, 125, 175,  225, 275, 325, 600, 900, 3350])
fc1 = np.array([46, 70, 113, 162, 209, 258, 308, 590, 890, 3100])
fc2 = np.array([54, 83, 134, 187, 238, 287, 336, 610, 910, 3600])
Rp = 3
Rs = 60

def testSignal(freqs, t, SPR):
    Sig = []
    Params = []
    for f in freqs:
        A = round(np.random.random()*10, 2)
        Bias = round(np.random.random()*10, 2)
        testSig = A*np.sin(2*sp.pi*t*f) + Bias
        Sig.append(testSig)
        Params.append(np.array([f, A, Bias]))

    Sig = np.array(Sig).T
    Signal = np.sum(Sig, axis=1)+np.hamming(len(Sig))*500
    plotSignal = pd.DataFrame(Signal, index=(t))
    Params = pd.DataFrame(Params, columns=(['Hz', 'Ampl', 'Bias']))
    return Params, Signal, plotSignal


Params, Signal, plotSignal = testSignal(freqs, t, SPR)
#plotSignal.plot(grid=True, xlim=([0, len(plotSignal.values)/SPR]))

fftOutSig, f = fftsplitter(Signal, N, SPR, 0, 'max', 'nodelay')
fftDataParams = pd.DataFrame(fftOutSig, index=f).loc[freqs]

rmsDb, qqq = filterCheb2(Signal, N, freqs, fc1, fc2, Rp, Rs, SPR)



commonTab = Params
commonTab['AmplFFT'] = np.round(fftDataParams.values, 2)
commonTab['AmplCheb2'] = np.round(rmsDb.values*np.sqrt(2), 2)

del commonTab['Bias']

# fig, ax = plt.subplots()
# ax.plot(f, fftOutSig)
# plt.xlim([50, 3600])
# plt.ylim([-1, 1.15*fftOutSig[50:3600].max()])
# plt.grid()
# plt.show()
