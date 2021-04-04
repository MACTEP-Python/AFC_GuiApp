# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from OpenFileModule import createDataFrame
from OpenFileModule import getslicefromdataframe
from winProcessing import fftsplitter


if __name__ == '__main__':
    FldrPath = r"D:\Штадлер 2020\Штадлер ТЕСТ\s190717_013140"
    currentPattern = '*.ana'  # Шаблон для выбора необходимых файлов с расширением ana
    SPR = float(50_000)  # Частота дискретизации
    try:
        # Вывел функцию открытия в отдельный файл
        df = createDataFrame(FldrPath, currentPattern)
    except ValueError:
        print('Отсутствуют данные')
    else:
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

            inputData = getslicefromdataframe(df.Sumsig, SPR)

            sig, f = fftsplitter(np.array(inputData), int(SPR*1), SPR, 0, 'max', 'nodelay')

            # Блок графики
            xValues = np.arange(0, (len(inputData) / SPR),
                                (1 / SPR), dtype=np.float32)  # Создаем временной ряд
            fig, ax = plt.subplots()            #
            ax.plot(xValues, inputData)
            ax.set_title("Суммарный ток", fontsize=14)
            ax.set_xlabel("Time")
            ax.set_ylabel("Ток")
            plt.xlim(0, (len(inputData) / SPR))
            plt.grid()
            plt.show()

            fig1, ax = plt.subplots()
            ax.plot(f, sig)
            plt.xlim([50, 3600])
            plt.ylim([-1, 1.15*sig[50:3600].max()])
            plt.grid()
            plt.show()

            print("Готово!")

        elif contin == '2':
            print('Обработка завершена!')
