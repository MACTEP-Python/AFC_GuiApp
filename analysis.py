# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from OpenFileModule import createDataFrame
from OpenFileModule import getslicefromdataframe
from winProcessing import fftsplitter, filterCheb2
import seaborn


def rms(x):
    return np.sqrt(x.dot(x)/x.size)


if __name__ == '__main__':
    FldrPath = r"F:\Документы\2020 год\Штадлер 5ти вагонник\данные\5ти вагонный\испытания в ночь с 10 на 11 марта 2020\s200311_012325"
    currentPattern = '*.ana'  # Шаблон для выбора необходимых файлов с расширением ana
    SPR = float(50_000)  # Частота дискретизации
    freqs = np.array([50, 75, 125, 175,  225, 275, 325, 600, 900, 3350])
    fc1 = np.array([46, 70, 113, 162, 209, 258, 308, 590, 890, 3100])
    fc2 = np.array([54, 83, 134, 187, 238, 287, 336, 610, 910, 3600])
    Rp = 3
    Rs = 80
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

            sig, f = fftsplitter(inputData.values, int(
                SPR*0.2), SPR, 0, 'max', 'nodelay')

            fftDatabase = pd.DataFrame(sig, index=f).loc[freqs]/np.sqrt(2)

            bpfs, rmsDatas = filterCheb2(inputData.values, int(
                SPR*0.2), freqs, fc1, fc2, Rp, Rs, SPR)

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

            fig, ax = plt.subplots()
            ax.plot(f, sig/np.sqrt(2))
            plt.xlim([50, 3600])
            plt.ylim([-1, 1.15*sig[50:3600].max()])
            plt.grid()
            plt.show()

            #bpfs['3350'].plot(grid=True, xlim=[0, len(bpfs)/SPR])
            print("Готово!")


        elif contin == '2':
            print('Обработка завершена!')
