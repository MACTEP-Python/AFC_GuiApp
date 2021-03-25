import pathlib
import numpy as np
import pandas as pd


def createDataFrame(FolderPath, pattern='*.ana', coefficient=(5 / 5.1)):
    # Модуль инициализации первичных данных
    indexes = []
    d = []  # Создаю пустой список, куда буду собирать числовые данные сигналов
    i = 1

    # Модуль выбора и чтения файла по шаблону
    currentDirectory = pathlib.Path(FolderPath)  # Определение текущей директории
    for currentFile in currentDirectory.glob(pattern):  # В цикле мы пробегаем по каждому файлу в директории
        # и работаем при совпадении с шаблоном
        with open(str(currentFile), 'rb') as f:
            data = np.fromfile(f, dtype=np.float32, count=-1)  # Считываю определенное количество данных из
            # файла
            d.append(data)  # На каждом витке цикла, добавляю данные их новых файлов
            indexes.append('sig' + f'{i}')  # Происходит процесс создания имен столбцов
            i += 1

    d = np.matrix(d)  # Преобразую данные, сохраненные в списках в матрицу и умножаю на коэфф датчика
    d = d.T * coefficient  # Транспонирую, что бы каждый столбец был отдельным сигналом
    d = np.concatenate((d, np.array(np.sum(d, axis=1))), axis=1)  # Добавляется столбец с построчной суммой
    indexes.append('Sumsig')  # Добавляется название столбца как суммарный сигнал
    dataframe = pd.DataFrame(d, columns=indexes).astype('float32')  # Создаю Фрейм из сигналов, с названиями столбцов.
    # Тип данных перевел в 32 с плавающей точкой, что бы меньше памяти ела
    return dataframe


def getslicefromdataframe(file, samplerate):
    tBegin = float(input('Введите время начала: '))
    if tBegin == '':
        tBegin = 0
    else:
        tEnd = float(input('Введите время окончания: '))
        if tEnd == '' or 0:
            timeEnd = len(file) / samplerate
        else:
            file = file[int(tBegin * samplerate): int(tEnd * samplerate)]
    return file
