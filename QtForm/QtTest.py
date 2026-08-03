from http.client import OK
from PyQt5 import QtWidgets
from FormDesign import Ui_MainWindow # импорт сгенеренного файла
import sys
import httpx
import asyncio

ApiUrl = "http://api.steampowered.com/"


async def ApiGet(Command):
    async with httpx.AsyncClient() as client:
        result = await client.get(url=Command)
        if result.status_code == httpx.codes.OK:
            jsonres = result.json()
            if type(jsonres.get("appnews")) == type(None):
                return [None, result.status_code]        
            else:    
                return [jsonres["appnews"]["newsitems"][0], result.status_code]
        else:
            return [None, result.status_code]

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
            result = asyncio.run(ApiGet(ApiUrl+"ISteamNews/GetNewsForApp/v0002/?appid=440&count=3&maxlength=300&format=json"))
            for element in result:
                TextMessage = f"Title{element['title']}"    
        else:
            QtWidgets.QMessageBox.about(self, "Incorrect API!", "No! Goddamn, No!!!")    



App = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(App.exec())