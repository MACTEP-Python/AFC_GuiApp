import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Модуль инициализации первичных данных
indexes = []
d = []  # Создаю пустой список, куда буду собирать числовые данные сигналов
i = 1
k = 5 / 5.1
fs = float(50e3)  # Частота дискретизации

# Модуль выбора и чтения файла по шаблону
FolderName = r"D:\Штадлер 2020\5ти вагонный\испытания в ночь с 10 на 11 марта 2020\s200311_012325"
currentDirectory = pathlib.Path(FolderName)  # Определение текущей директории
currentPattern = '*.ana'  # Шаблон для выбора необходимых файлов с расширением ana
for currentFile in currentDirectory.glob(currentPattern):  # В цикле мы пробегаем по каждому файлу в директории
    # и работаем при совпадении с шаблоном
    with open(str(currentFile), 'rb') as f:
        data = np.fromfile(f, dtype=np.float32, count=-1)  # Считываю определенное количество данных из
        # файла
        d.append(data)  # На каждом витке цикла, добавляю данные их новых файлов
        indexes.append('sig' + f'{i}')  # Происходит процесс создания имен столбцов
        i += 1

d = np.matrix(d) * k  # Преобразую данные, сохраненные в списках в матрицу и умножаю на коэфф датчика
d = d.T  # Транспонирую, что бы каждый столбец был отдельным сигналом
d = np.concatenate((d, np.array(np.sum(d, axis=1))), axis=1)  # Добавляется столбец с построчной суммой
indexes.append('Sumsig')  # Добавляется название столбца как суммарный сигнал
df = pd.DataFrame(d, columns=indexes)  # Создаю Фрейм из сигналов, с названиями столбцов.

# Блок графики
xValues = np.arange(0, len(df['Sumsig']) / fs, 1 / fs)
fig, ax = plt.subplots()
ax.plot(xValues, df['Sumsig'])
ax.set_title("Суммарный ток", fontsize=16)
ax.set_xlabel("Time")
ax.set_ylabel("Ток")
plt.xlim(0, len(df['Sumsig']) / fs)
plt.grid()
plt.show()

print("Готово!")

# Блок выделения фрагмента данных
