# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 13:52:48 2021

@author: MACTEP
"""
import numpy as np
import pandas as pd
from scipy.fftpack import fft, fftfreq
from scipy import signal


def rms(x):
    return np.sqrt(x.dot(x)/x.size)


def buffer(data, N, P=0, opt='nodelay'):
    """Базовая конструкция для того, что бы разбивать последовательность на части,
    определенной длины N, с перекрытием Р (в процентах, по умолчанию 0)
    и опцией ('nodelay'), если нужно убрать нули"""
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
                zeroMatrix[:, i] = data[val:val+N]
        # Опция, которая убирает оставшиеся нулевые столбцы
        if opt == 'nodelay':
            sData = zeroMatrix[:, 0:np.size(zeroMatrix, 1)-(i-iCur)]
        else:
            sData = zeroMatrix
    return sData


def fftsplitter(data, N, spr, P=0, funk='max', opt='nodelay'):
    """Данная функция производить расчет ДПФ сигнала с использованием оконной функции Хемминга.
    Функция возвращает максимальные данные для каждой частоты и частотную ось.
    data - входные данные - матрица в строку или столбец или последовательность
    N - интервал расчета (ширина окна) (количество точек) - целочисленное значение
    SPR - частота дискретизации сигнала - целочисленное значение
    P - перекрытие окон - Задается в процентах от 0 - 99
    funk - функциональная опция по умолчанию -'max'- После обработки выбирает максимальные значения
    опция - по умолчанию -'nodelay'- убирает нулевые столбцы"""
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
                #N = len(inputData)
                win = np.hamming(N)  # Оконная функция Хемминга
                # значение -5,37 в дБ, переводим в линейное значение
                beta = 10**(-5.37/20)
                inputData = inputData * win
                xf = fftfreq(N, 1 / spr)
                # Умножаем на 2 действ часть
                outFFTData = 2 * abs(fft(inputData, N) / (N * beta))
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


def rmssplitter(data, N, P=0, opt='nodelay'):
    """В базовую конструкцию splitter добавлен блок вычисления действующего 
    значения на каждой итерации и далее выбирается максимум"""
    # Проводим проверку размера окна или длины участа расчета
    if N > len(data) or N <= 0:
        print(
            'Размер окна, не может быть больше размера исследуемого массива или\
            меньше нуля')
    else:
        step = int(N - (N*P)/100)  # Определяем шаг движения окна
        # Определяем индексы начальной выборки
        ind1 = np.arange(0, len(data), step)
        # Создаем нулевую матрицу для сохранения результатов
        zeroMatrix = np.empty([1, len(ind1)])
        # Цикл. Выделяем кусок N из data и сохраняем в массив, двигаемся с шагом step
        for i, val in enumerate(range(0, len(data), step)):
            if val+N <= len(data):
                iCur = i
                rmsOutData = rms(data[val:val+N])
                zeroMatrix[:, i] = rmsOutData
        # Опция, которая убирает оставшиеся нулевые столбцы
        if opt == 'nodelay':
            sData = zeroMatrix[:, 0:np.size(zeroMatrix, 1)-(i-iCur)]
        else:
            sData = zeroMatrix
    return sData.max(axis=1)


if __name__ == '__main__':
    matrix = np.arange(0, 99)
    qData = splitter(matrix, 10, 50, 'nodelay')
