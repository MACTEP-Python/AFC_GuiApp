import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from analysis import df, fs


newData = df['Sumsig']

xValues = np.arange(0, len(newData) / fs, 1 / fs)
fig, ax = plt.subplots()
ax.plot(xValues, df['Sumsig'])
ax.set_title("Суммарный ток NewData", fontsize=16)
ax.set_xlabel("Time")
ax.set_ylabel("Ток")
plt.xlim(0, len(newData) / fs)
plt.grid()
plt.show()

print("Готово!")
