from email.mime import application
from PyQt5 import QtWidgets
from FormDesign import Ui_MainWindow # импорт сгенеренного файла
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

App = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(App.exec())