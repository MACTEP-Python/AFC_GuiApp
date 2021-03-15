from PyQt5 import QtWidgets

from MyForm import Ui_MyForm
from PyQt5 import uic


# Ui_MyForm, baseClass = uic.loadUiType('MyForm.ui')


def quit_from():
    QtWidgets.QApplication.quit()


class OpenForm(QtWidgets.QWidget, Ui_MyForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.btnQuit.clicked.connect(self.close)
        self.btnOpen.clicked.connect(self.open_msg)

    def open_msg(self):
        QtWidgets.QMessageBox.information(self, 'Success', 'The proccess is giong!')


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    widget = OpenForm()
    widget.show()

    sys.exit(app.exec_())
