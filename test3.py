# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 17:34:39 2021

@author: kabec
"""
import numpy as np
import scipy as sp
import pandas as pd
from scipy import signal


def filterCheb2(data, N, freqs, fc1, fc2, Rp, Rs, spr):
    filteredDatas = []
    colNames = []
    rmsData = []
    for i, val in enumerate(fc1):
        Wp = np.array([fc1[i], fc2[i]])*2/spr
        Ws = np.array([fc1[i]-1, fc2[i]+1])*2/spr
        # Определяем минимальный порядок фильтра ord и полосу Найквиста
        ord, Wn = signal.cheb2ord(Wp, Ws, Rp, Rs)
        # Расчитываем коэффициенты sos матрицы, как       стабильной в отличие от коэффициентов b,a
        sos = signal.cheby2(ord, Rs, Wn, btype='bandpass', output='sos')

        # Производим фильтрацию сигнала
        filteredDatas.append(signal.sosfilt(sos, data))
        # Происходит процесс создания имен столбцов
        colNames.append(f'{freqs[i]}')
    # Преобразую данные, сохраненные в списках в матрицу и умножаю на коэфф датчика
    filteredDatas = np.matrix(filteredDatas).T
    # Создаю Фрейм из сигналов, с названиями столбцов.
    filteredDatabase = pd.DataFrame(filteredDatas[int(spr*1):, :], index=np.arange(
        0, len(filteredDatas[int(spr*1):, :])/spr, 1/spr), columns=colNames).astype('float32')
    for i in filteredDatabase.values.T:
        rmsData.append(rmssplitter(i, N))
    rmsDatabase = pd.DataFrame(np.matrix(rmsData), index=colNames)
    return rmsDatabase, filteredDatabase