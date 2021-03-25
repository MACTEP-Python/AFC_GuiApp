import matplotlib.pyplot as plt
import numpy as np
from OpenFileModule import createDataFrame

FldrPath = r"D:\TEST_Stadler\s160918_020000"
currentPattern = '*.ana'  # Шаблон для выбора необходимых файлов с расширением ana
SPR = float(50e3)  # Частота дискретизации
df = createDataFrame(FldrPath, currentPattern)  # Вывел функцию открытия в отдельный файл

# Блок графики
xValues = np.arange(0, len(df['Sumsig']) / SPR, 1 / SPR)
fig, ax = plt.subplots()
ax.plot(xValues, df['Sumsig'])
ax.set_title("Суммарный ток", fontsize=16)
ax.set_xlabel("Time")
ax.set_ylabel("Ток")
plt.xlim(0, len(df['Sumsig']) / SPR)
plt.grid()
plt.show()

print("Готово!")

contin = input("Продолжить?(да(1)/нет(2)): ")
if contin == '1' or contin == '':
    # Блок выделения фрагмента данных
    from OpenFileModule import getslicefromdataframe
    inputData = getslicefromdataframe(df, SPR)
    # Блок графики
    xValues = np.arange(0, len(inputData) / SPR, 1 / SPR)
    fig, ax = plt.subplots()
    ax.plot(xValues, inputData)
    ax.set_title("Суммарный ток", fontsize=16)
    ax.set_xlabel("Time")
    ax.set_ylabel("Ток")
    plt.xlim(0, len(inputData) / SPR)
    plt.grid()
    plt.show()

    print("Готово!")

elif contin == '2':
    print('Обработка завершена!')
