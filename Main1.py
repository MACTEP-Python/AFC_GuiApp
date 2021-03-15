from PyQt5 import QtWidgets
from AFCGui import Ui_Form


class MainForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.login_pushButton.clicked.connect(self.autorization)

    def autorization(self):
        user_name = self.username_lineEdit.text()
        user_password = self.password_lineEdit.text()
        if user_name == '' or user_password == '':
            QtWidgets.QMessageBox.critical(self, "Wrong!", f"You fogot to input Username or Password, sir!")
        else:
            if user_name == "admin" and user_password == "admin":
                QtWidgets.QMessageBox.information(self, "Success!", f"Welcome to programm, {user_name}!")
                self.graphicsView.setEnabled(True)
                self.browse_pushButton.setEnabled(True)
                self.showGraphic_pushButton.setEnabled(True)
                self.clear_pushButton.setEnabled(True)
            else:
                QtWidgets.QMessageBox.critical(self, "Wrong!", f"Sorry, User - {user_name} is not find!")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MainForm()
    widget.show()
    sys.exit(app.exec_())
