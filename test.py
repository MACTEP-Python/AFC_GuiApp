import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from analysis import fs, df


inputData = df[:]

timeBegin = float(input('Введите время начала: '))
if timeBegin == '':
    timeBegin = 0
else:
    timeEnd = float(input('Введите время окончания: '))
    if timeEnd == '' or 0:
        timeEnd = len(inputData) / fs
    else:
        inputData = inputData[int(timeBegin * fs): int(timeEnd * fs)]

# Блок графики
xValues = np.arange(0, len(inputData) / fs, 1 / fs)
fig, ax = plt.subplots()
ax.plot(xValues, inputData)
ax.set_title("Суммарный ток", fontsize=16)
ax.set_xlabel("Time")
ax.set_ylabel("Ток")
plt.xlim(0, len(inputData) / fs)
plt.grid()
plt.show()

print("Готово!")
