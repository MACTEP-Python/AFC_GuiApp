import numpy as np
import scipy as sp
from scipy import signal, misc
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.io import wavfile


def plotting(data, fs):  # Function that plotting input data on time axes
    t = np.arange(0, len(data) / fs, (1 / fs))
    plt.plot(t, data)
    plt.show()


def getdata(filepath):
    sample, data = wavfile.read(filepath)
    return sample, data
