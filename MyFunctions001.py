# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 12:05:41 2021

@author: kabec
"""
import pandas as pd
import numpy as np
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

def stdFreqDataBase():
    """Формирует 3 базы данных для разных стандартов. Формируется словарь - БД, который
    содержит центральную частоту(как индекс), полосу с частотой начала и частотой конца (список),
    норму по току в действующих значениях.
    Вызов с параметром [0] - Общая ДБ
    Вызов с параметром [1] - ДБ с гармониками
    Вызов с параметром [2] - ДБ Рельсовые цепи (РЦ50, ТРЦ и КРЦ)
    Вызов с параметром [3] - ДБ с АЛС-АРС (АЛС с ЧК и ФРМ)"""
    freqskey = (600, 900, 1200, 1500, 2400, 2700, 3000, 3600, 50,
                425, 475, 575, 725, 775, 4261, 75, 125, 175, 225, 275, 325, 3348)
    fc1 = (590, 890, 1190, 1490, 2390, 2690, 2990, 3590, 46,
           413, 463, 563, 713, 763, 4161, 70, 113, 162, 209, 258, 308, 3100)
    fc2 = (610, 910, 1210, 1510, 2410, 2710, 3010, 3610, 54,
           437, 487, 587, 737, 787, 4361, 83, 134, 187, 238, 287, 336, 3600)
    freqsLimit = (70, 66.7, 78.3, 90,  31.3, 10.7,  4.7,  1.2, 8.3,
                  1.6, 1.6, 1.6, 1.6, 1.6,  2, 18.3, 12.3, 12.3, 8.99, 10.3, 8.3,  1.2)
    All_freqsDB = {}
    Harmonicks_freqsDB = {}
    RC_freqsDB = {}
    ALS_freqsDB = {}
    for i, val in enumerate(freqskey):
        All_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
        if i in range(0, 8):
            Harmonicks_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
        elif i in range(8, 15):
            RC_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
        elif i in range(15, 22):
            ALS_freqsDB[val] = (fc1[i], fc2[i], freqsLimit[i])
    return All_freqsDB, Harmonicks_freqsDB, RC_freqsDB, ALS_freqsDB


def testSignal(freqs, t, SPR):
    """Функция формирует тестовый сигнал со случайным выбором амплитуд и 
    постоянной составляющей для частот, которые задаются в переменную 
        freqs-(список или NumPy массив);
        t - длительность сигнала в секундах;
        SPR - частота дискретизации сигнала.
    Сигнал складывается с оконной функцией Хемминга с амплитудой 500.
    В качестве выходных параметров:
        [0] - В виде таблицы Параметры каждого отдельного сигнала
        [1] - Массив самого сформированного сигнала
        [2] - DataFrame модуля pandas"""
    tf = np.arange(0, t, 1/SPR)
    Sig = []
    Params = []
    testSig = []
    for f in freqs:
        A = round(np.random.random()*10, 2)
        Bias = round(np.random.random(), 2)
        testSig = A*np.sin(2*np.pi*tf*f) + Bias
        Sig.append(testSig)
        Params.append(np.array([f, A, Bias]))

    Sig = np.array(Sig).T
    Signal = np.sum(Sig, axis=1)+np.hamming(len(Sig))*100
    Params = pd.DataFrame(Params, columns=(['Hz', 'Ampl', 'Bias']))
    return Params, Signal

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

def filterCheb2(data, N, freqs, fc1, fc2, Rp, Rs, SPR):
    """Модуль фильтрации с использованием АЧХ фильтра Чебышева второго рода. 
    В качестве выходных параметров:
        [0] - Максимальные действующие значения
        [1] - Массив, где в столбцах отфильтрованные сигналы для каждой из частот.
    В качестве входных параметров:
        data - массив входных данных;
        N - интервал расчета (размер окна);
        freqs - центральные частоты, по которым производится фитрация;
        fc1, fc2 -  начальная и конечная полоса центральной частоты;
        Rp и Rs - уровень пропускания и уровень подавления (в дБ);
        SPR - частота дискретизации сигнала."""
    
    filteredDatas = []
    colNames = []
    rmsData = []
    for i, val in enumerate(fc1):
        Wp = np.array([fc1[i], fc2[i]])*2/SPR
        Ws = np.array([fc1[i]-1, fc2[i]+1])*2/SPR
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
    filteredDatabase = pd.DataFrame(filteredDatas[int(SPR*1):, :], index=np.arange(
        0, len(filteredDatas[int(SPR*1):, :])/SPR, 1/SPR), columns=colNames).astype('float32')
    for i in filteredDatabase.values.T:
        rmsData.append(rmssplitter(i, N))
    rmsDatabase = pd.DataFrame(np.matrix(rmsData), index=colNames, columns=['RMS'])
    return rmsDatabase, filteredDatabase

def fftsplitter(data, N, SPR, P=0, funk='max', opt='nodelay'):
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
                xf = fftfreq(N, 1 / SPR)
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

if __name__ == '__main__':
    stdFreqDataBase()
    testSignal()
    fftsplitter()
    filterCheb2()