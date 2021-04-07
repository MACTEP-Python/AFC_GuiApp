# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 11:22:03 2021

@author: kabec
"""
#import matplotlib.pyplot as plt
import numpy as np
from scipy import pi
from scipy import signal
import pandas as pd
import seaborn

def rms(x):
    return np.sqrt(x.dot(x)/x.size)

def rmssplitter(data, N, P=0, opt = 'nodelay'):
    """В базовую конструкцию splitter добавлен блок вычисления действующего значения на каждой итерации и далее выбирается максимум"""
    # Проводим проверку размера окна или длины участа расчета
    if N > len(data) or N <=0:
        print('Размер окна, не может быть больше размера исследуемого массива или меньше нуля')
    else:
        step = int(N - (N*P)/100)  # Определяем шаг движения окна
        ind1 = np.arange(0, len(data), step)  # Определяем индексы начальной выборки
        zeroMatrix = np.empty([1, len(ind1)])  # Создаем нулевую матрицу для сохранения результатов
        # Цикл. Выделяем кусок N из data и сохраняем в массив, двигаемся с шагом step
        for i, val in enumerate(range(0, len(data), step)):
            if val+N <= len(data):
                iCur = i
                rmsOutData = rms(data[val:val+N])
                zeroMatrix[:, i] = rmsOutData
        # Опция, которая убирает оставшиеся нулевые столбцы
        if opt == 'nodelay':
            sData = zeroMatrix[:,0:np.size(zeroMatrix,1)-(i-iCur)]
        else:
            sData = zeroMatrix
    return sData.max(axis=1)

spr = 50_000
t = np.arange(0, 5, 1/spr)
y3 = np.sqrt(2)*1.7*np.sin(2*pi*t*200)
y1 = np.sqrt(2)*1*np.sin(2*pi*t*300)+2
y2 = np.sqrt(2)*5.7*np.sin(2*pi*t*600)+1
y4 = np.sqrt(2)*3.7*np.sin(2*pi*t*900)
ySig = np.array([y1, y2, y3, y4]).sum(axis=0)


def filterCheb2(data, N, freqs, fc1, fc2, Rp, Rs, spr):
    filteredDatas = []
    colNames = []
    rmsData = []
    for i, val in enumerate(fc1):
        Wp = np.array([fc1[i], fc2[i]])*2/spr
        Ws = np.array([fc1[i]-1, fc2[i]+1])*2/spr
        ord, Wn = signal.cheb2ord(Wp, Ws, Rp, Rs)  # Определяем минимальный порядок фильтра ord и полосу Найквиста
        sos = signal.cheby2(ord, Rs, Wn, btype='bandpass', output='sos')  # Расчитываем коэффициенты sos матрицы, как       стабильной в отличие от коэффициентов b,a

        filteredDatas.append(signal.sosfilt(sos, data))  # Производим фильтрацию сигнала
        colNames.append(f'{freqs[i]}')  # Происходит процесс создания имен столбцов
    filteredDatas = np.matrix(filteredDatas).T  # Преобразую данные, сохраненные в списках в матрицу и умножаю на коэфф датчика
    filteredDatabase = pd.DataFrame(filteredDatas[int(spr*1):,:], index=np.arange(0, len(filteredDatas[int(spr*1):,:])/spr, 1/spr), columns=colNames).astype('float32')  # Создаю Фрейм из сигналов, с названиями столбцов.
    for i in filteredDatabase.values.T:
        rmsData.append(rmssplitter(i, N))
    rmsDatabase = pd.DataFrame(np.matrix(rmsData).T, columns=colNames)
    return filteredDatabase, rmsDatabase

freqs = np.array([200, 300, 600, 900])
fc1 = np.array([190, 290, 590, 890])
fc2 = np.array([210, 310, 610, 910])
Rp = 3
Rs = 60
N = int(spr*0.2)
Filtered, RmsDatas = filterCheb2(ySig, N, freqs, fc1, fc2, Rp, Rs, spr)


Filtered.plot(grid=True, xlim=[1, 1.5])

