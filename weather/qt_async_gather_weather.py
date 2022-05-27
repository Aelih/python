from PyQt5 import QtWidgets
from weatherForm import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import asyncio
import time
import aiohttp

cities = ['Bratsk', 'Novosibirsk', 'St. Petersburg']

async def get_weather(city):
    async with aiohttp.ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather' \
                f'?q={city}&APPID=2a4ff86f9aaa70041ec8e82db64abf56'

        async with session.get(url) as response:
            weather_json = await response.json()
            return f'{city}: {weather_json["weather"][0]["main"]}'

async def main(listWidget, cities_):
    tasks = []
    for city in cities_:
        tasks.append(asyncio.create_task(get_weather(city)))            

    results = await asyncio.gather(*tasks)

    for result in results:
        item = QtWidgets.QListWidgetItem()
        item.setText(result)
        listWidget.addItem(item)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту ParseComments
        self.ui.pushButton.clicked.connect(self.Run) 
    
    def Run(self):
        asyncio.run(main(self.ui.listWidget, cities))
    
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
 
sys.exit(app.exec())