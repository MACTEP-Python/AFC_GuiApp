import matplotlib.pyplot as plt
import numpy as np
from scipy import pi
from scipy import signal


def rms(x):
    return np.sqrt(x.dot(x)/x.size)


spr = 50_000
t = np.arange(0, 5, 1/spr)
y1 = np.sin(2*pi*t*300)+2
y2 = 0.7*np.sin(2*pi*t*600)+1
y3 = 1.7*np.sin(2*pi*t*200)
ySig = np.array([y1, y2, y3]).sum(axis=0)

# Проектирование цифрового полосового  фильтра с АЧХ Чебышева II
N = int(spr*1)
fc1 = 590  # Начальная частота пропускания
fc2 = 610  # Конечная частота пропускания
Rp = 3  # Допустимый уровень пропускания (дБ) - значит -3 дБ
Rs = 40  # Уровень задержания (дБ) - значит -40 дБ
# Нормализуем частоты пропускания (Найквиста)
Wp = (np.array([fc1, fc2])*2/spr)
Ws = (np.array([fc1-5, fc2+5])*2/spr)  # Нормализуем частоты задержания


# Определяем минимальный порядок фильтра ord и полосу Найквиста
ord, Wn = signal.cheb2ord(Wp, Ws, Rp, Rs)
# Расчитываем коэффициенты sos матрицы, как стабильной в отличие от коэффициентов b,a
sos = signal.cheby2(ord, Rs, Wn, btype='bandpass', output='sos')
sigbb = signal.sosfilt(sos, ySig)  # Производим фильтрацию сигнала
# Убираем первую секунду, как зону нестабильного сигнала после фильтрации
sigbb = sigbb[spr*1:]


# Вычисляем коэффициенты для построения АЧХ фильтра
w, h = signal.sosfreqz(sos, worN=spr)

# Выводим на график АЧХ фильтра
fig, ax1 = plt.subplots()
ax1.set_title('Частотная характеристика цифрового фильтра')
# Переводим ось х в Гц, а значения по y переводим в логарифмический масштаб
ax1.plot(spr*w/(2*pi), 20 * np.log10(abs(h)), 'b')
ax1.set_ylabel('Amplitude [dB]', color='b')  #
ax1.set_xlabel('Frequency [Hz]')
plt.axvline(fc1, color='green')
plt.axvline(fc2, color='green')
plt.axhline(-Rp, color='green')
plt.axhline(-Rs, color='red')
plt.xlim([fc1-100, fc2+100])  # Устатавливаем лимиты отрисовки по оси х
plt.grid()  # Добавляем сетку

# Выводим на график отфильтрованный сигнал
xValues = np.arange(0, (len(sigbb) / spr),
                    (1 / spr), dtype=np.float32)  # Создаем временной ряд
fig, ax = plt.subplots()            #
ax.plot(xValues, sigbb)
ax.set_title("Суммарный ток", fontsize=14)
ax.set_xlabel("Time")
ax.set_ylabel("Ток")
plt.xlim(0, (len(sigbb) / spr))
plt.grid()
plt.show()

print(rms(sigbb)*np.sqrt(2))


def rmssplitter(data, N, P=0, opt='nodelay'):
    """В базовую конструкцию splitter добавлен блок вычисления действующего значения на каждой итерации и далее выбирается максимум"""
    # Проводим проверку размера окна или длины участа расчета
    if N > len(data) or N <= 0:
        print(
            'Размер окна, не может быть больше размера исследуемого массива или меньше нуля')
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


q = rmssplitter(sigbb, N, 0, 'nodelay')*np.sqrt(2)
print(q)
