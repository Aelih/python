from PyQt5 import QtWidgets
from MainFormDesign import Ui_MainWindow # импорт сгенеренного файла
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
         # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_Run.clicked.connect(self.btnClicked)

    def btnClicked(self):
        QtWidgets.QMessageBox.about(self, "Correct!", "You're goddamn right!")   


App = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(App.exec())