from PyQt5 import QtWidgets
from AFCGui import Ui_Form
import getData
import numpy as np


class MainForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.graphicsView.setEnabled(True)
        self.browse_pushButton.setEnabled(True)
        self.showGraphic_pushButton.setEnabled(True)
        self.clear_pushButton.setEnabled(True)
        self.login_pushButton.clicked.connect(self.authorization)
        self.logout_pushButton.clicked.connect(self.logout)
        self.browse_pushButton.clicked.connect(self.browsefile)
        self.clear_pushButton.clicked.connect(self.clearing)
        self.filepath = 0  # Объявляю переменную, в которую буду сохранять путь до исследуемого файла.
        # Что бы была возможность использовать данную переменную в других функциях
        self.data = 0
        self.samplerate = 0
        self.showGraphic_pushButton.clicked.connect(self.showgraphic)

    def authorization(self):  # Функция авторизации в приложение
        user_name = 'admin'
        user_password = 'admin'
        # user_name = self.username_lineEdit.text()
        # user_password = self.password_lineEdit.text()
        if user_name == '' or user_password == '':
            QtWidgets.QMessageBox.critical(self, "Wrong!", f"You forgot to input Username or Password, sir!")
        else:
            if user_name == "admin" and user_password == "admin":
                QtWidgets.QMessageBox.information(self, "Success!", f"Welcome to program, {user_name}!")
                self.graphicsView.setEnabled(True)
                self.browse_pushButton.setEnabled(True)
                # self.showGraphic_pushButton.setEnabled(True)
                self.clear_pushButton.setEnabled(True)
            else:
                QtWidgets.QMessageBox.critical(self, "Wrong!", f"Sorry, User - {user_name} is not find!")

    def logout(self):  # Функция выходы из программы, переводит кнопки в неактивное состояние и затирает поле логина
        # и пароля
        self.graphicsView.setEnabled(False)
        self.browse_pushButton.setEnabled(False)
        self.showGraphic_pushButton.setEnabled(False)
        self.clear_pushButton.setEnabled(False)
        self.username_lineEdit.setText('')
        self.password_lineEdit.setText('')

    def browsefile(self):  # Функция поиска файла через диалоговое окно ОС
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self, caption='Выберите файл',
                                                              directory=r'D:\Диссертация\АЧХ катушек ОПК и '
                                                                        r'МПК\15022021 классич АЧХ '
                                                                        r'ПК над рельсом\2_15_2021_14_47_54_bin',
                                                              filter='*.wav')
        self.filepath = self.filepath[0]
        self.Browse_lineEdit.setText(self.filepath)  # вписываем в поле полный путь до исследуемого файла
        print(self.filepath)
        if self.filepath == '':
            self.filepath = 0
            self.showGraphic_pushButton.setEnabled(False)
        else:
            self.showGraphic_pushButton.setEnabled(True)

    def clearing(self):  # Вданный момент функция выводит в диалоговое окно распечатку пути до файла. Проверяю
        # перекрестные переменные
        self.graphicsView.clear()

    def showgraphic(self):
        a1 = getData.getdata(self.filepath)  # Создал отдельный файл с функцией для чтения wav формата и вывода
        # данных и частоты дисретизации
        self.samplerate = a1[0]
        self.data = a1[1]
        if a1[0] == 0:
            QtWidgets.QMessageBox.critical(self, "Warning!", "Файл не был выбран или прочитан!")
        else:
            print(self.samplerate)
            print(self.data)
            x = np.arange(0, len(a1[1]) / a1[0], (1 / a1[0]))
            y = self.data / 1E6
            self.graphicsView.plot(x, y)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MainForm()
    widget.show()
    sys.exit(app.exec_())
