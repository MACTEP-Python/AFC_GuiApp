# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 13:52:48 2021

@author: MACTEP
"""
import numpy as np

matrix = np.arange(0, 99)

# Базовая конструкция для того, что бы разбивать последовательность на части, определенной длины 
def splitter(data, N, P=0, opt = None):
    # Проводим проверку размера окна или длины участа расчета
    if N > len(data) or N <=0:
        print('Размер окна, не может быть больше размера исследуемого массива или меньше нуля')
    else:
        step = int(N - (N*P)/100)  # Определяем шаг движения окна
        ind1 = np.arange(0, len(data), step)  # Определяем индексы начальной выборки
        zeroMatrix = np.zeros([N, len(ind1)])  # Создаем нулевую матрицу для сохранения результатов
        # Цикл. Выделяем кусок N из data и сохраняем в массив, двигаемся с шагом step
        for i, val in enumerate(range(0, len(data), step)):
            if val+N <= len(data):
                iCur = i
                zeroMatrix[:, i] = data[val:val+N]
        # Опция, которая убирает оставшиеся нулевые столбцы
        if opt == 'nodelay':
            sData = zeroMatrix[:,0:np.size(zeroMatrix,1)-(i-iCur)]
        else:
            sData = zeroMatrix
    return sData

qData = splitter(matrix, 10, 50, 'nodelay')

    
    