import pathlib

import numpy as np
import pandas as pd


indexes = []
d = []
i = 1
FolderName = r"D:\TEST_Stadler\s160918_020000"
currentDirectory = pathlib.Path(FolderName)  # Определение текущей директории
currentPattern = '*.ana'  # Шаблон для выбора необходимых файлов с расширением ana
for currentFile in currentDirectory.glob(currentPattern):  # В цикле мы пробегаем по каждому файлу в директории
    # и работаем при совпадении с шаблоном
    with open(str(currentFile), 'rb') as f:
        data = np.fromfile(f, dtype=np.float32, count=20)  # Массив чисел
        d.append(pd.Series(data))
        indexes.append('sig'+f'{i}')
        print(indexes)
        i += 1

df = pd.DataFrame(d, index=indexes)
print("Готово!")
