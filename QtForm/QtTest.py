from PyQt5 import QtWidgets
from FormDesign import Ui_MainWindow # импорт сгенеренного файла
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
         # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_connect.clicked.connect(self.btnClicked)

    def btnClicked(self):
        ApiKey = self.ui.lineEdit_apikey.text()
        if len(ApiKey) == 32:
            QtWidgets.QMessageBox.about(self, "Correct API!", "You're goddamn right!")
        else:
            QtWidgets.QMessageBox.about(self, "Incorrect API!", "No! Goddamn, No!!!")    


App = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(App.exec())