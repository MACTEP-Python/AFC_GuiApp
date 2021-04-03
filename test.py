import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import scipy as sp
from scipy import pi
from scipy.fftpack import fft, fftfreq
#from scipy.signal import windows


# Базовая конструкция для того, что бы разбивать последовательность на части, определенной длины
def fftsplitter(data, N, SPR, P=0, funk='max', opt='nodelay'):
    # Проводим проверку размера окна или длины участа расчета
    if N > len(data) or N <= 0:
        print(
            'Размер окна, не может быть больше размера исследуемого массива или меньше нуля')
    else:
        step = int(N - (N*P)/100)  # Определяем шаг движения окна
        # Определяем индексы начальной выборки
        ind1 = np.arange(0, len(data), step)
        # Создаем нулевую матрицу для сохранения результатов
        zeroMatrix = np.zeros([N, len(ind1)])
        # Цикл. Выделяем кусок N из data и сохраняем в массив, двигаемся с шагом step
        for i, val in enumerate(range(0, len(data), step)):
            if val+N <= len(data):
                iCur = i
                inputData = data[val:val+N]
# ---------------Блок кода вычисляющего ДПФ участка последовательности---------------
                N = len(inputData)
                xf = fftfreq(N, 1 / spr)
                # Умножаем на 2 действ часть
                outFFTData = 2 * abs(fft(inputData, N) / N)
                # Постоянную составляющую нужно разделить на 2
                outFFTData[0] = outFFTData[0]/2
# --------------------------------
                zeroMatrix[:, i] = outFFTData
        # Опция, которая убирает оставшиеся нулевые столбцы
        if opt == 'nodelay':
            sData = zeroMatrix[:, 0:np.size(zeroMatrix, 1)-(i-iCur)]
        else:
            sData = zeroMatrix
        if funk == 'max':
            sData = sData.max(axis=1)  # Выделяем максимумы в каждой строке
    sData = sData[0:int(N/2)]  # Убираю зеркальную половину
    xf = xf[0:int(N/2)]  # Убираю зеркальную половину
    return sData, xf

spr = 50_000
t = np.arange(0, 5, 1/spr)
y1 = np.sin(2*pi*t*300)+2
y2 = 0.7*np.sin(2*pi*t*600)+1
y3 = 1.7*np.sin(2*pi*t*200)
ySig = np.array([y1, y2, y3]).sum(axis=0)

N = int(spr*2)
sig, f = fftsplitter(ySig, N, spr, 50, 'max', 'nodelay')

sigff = pd.Series(sig, f, dtype='float32')

print(sigff.loc[300])

plt.plot(f, sig)
plt.xlim([0, 700])
plt.show()
