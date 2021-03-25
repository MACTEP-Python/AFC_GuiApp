import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy.fft import fft, fftfreq
from scipy.signal import windows
from analysis import SPR, df

inputData = np.array(df['Sumsig'])

N = len(inputData)
outFFTData = 2 * abs(fft(inputData, N) / N)
xf = fftfreq(N, 1 / SPR)
plt.plot(xf, outFFTData)
plt.show()
