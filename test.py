import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


dt = np.zeros((3, 6))


def fftmag(data, n=int(), P=int()):
    P = n * P/100
    step = n - P
    ind1 = np.arange(0, len(data)-n, step)
    ind2 = ind1 + n
    result = pd.DataFrame(np.zeros((n, len(ind1))))
    for i in np.arange(0, len(ind1)):
        result['i'] = data[ind1[i]:ind2[i]]


def ploty(data, fs):
    xVal = np.arange(0, len(data) / fs, 1 / fs)
    figure, axx = plt.subplots()
    axx.plot(xVal, data)
    axx.set_xlabel("Time")
    axx.set_ylabel("Уровень")
    plt.xlim(0, len(data) / fs)
    plt.grid()
    plt.show()
