from PyQt5 import QtWidgets

from AFCGui import Ui_Form


class MainForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.autorization)
        self.browse_pushButton.clicked.connect(self.browsefile)
        self.clear_pushButton.clicked.connect(self.clearing)
        self.filepath = ''  # Объявляю переменную, в которую буду сохранять путь до исследуемого файла.
        # Что бы была возможность использовать данную переменную в других функциях

    def autorization(self):  # Функция авторизации в приложение
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
                self.showGraphic_pushButton.setEnabled(True)
                self.clear_pushButton.setEnabled(True)
            else:
                QtWidgets.QMessageBox.critical(self, "Wrong!", f"Sorry, User - {user_name} is not find!")

    def browsefile(self):  # Функция поиска файла через диалоговое окно ОС
        self.filepath = QtWidgets.QFileDialog.getOpenFileName(self, caption='Choose file',
                                                              directory=r'D:\Диссертация\АЧХ катушек ОПК и '
                                                                        r'МПК\15022021 классич АЧХ '
                                                                        r'ПК над рельсом\2_15_2021_14_47_54_bin')

    def clearing(self):  # Вданный момент функция выводит в диалоговое окно распечатку пути до файла. Проверяю
        # перекрестные переменные
        print(self.filepath[0])


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MainForm()
    widget.show()
    sys.exit(app.exec_())
