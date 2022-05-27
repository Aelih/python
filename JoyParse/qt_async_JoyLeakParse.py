from PyQt5 import QtWidgets
from MainFormDesign import Ui_MainWindow # импорт сгенеренного файла
import sys
from bs4 import BeautifulSoup
from validators import url
from time import sleep
import pandas as pd
from os import path, environ
import webbrowser
import asyncio
import aiohttp

stdurl = "http://joyreactor.cc"
starturl = "http://joyreactor.cc/tag/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0" #ert
#starturl = "http://joyreactor.cc/tag/%D0%9F%D0%BE%D1%80%D0%BD%D0%BE" #prn
dataleaklinks = []
sleeptime = 1
PagesRange = 20
desktoppath = path.join((environ['USERPROFILE']), 'Desktop')
chromepath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito"

 # Проверка на корректность URL
async def CorrectUrl(commenttext):
    if url(commenttext) == True and commenttext.find('instagram') == -1 and commenttext.find('reactor') == -1:
        return True
    else:
        return False

# Чтение и подготовка страницы по URL
async def ReadPageSoup(pageUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(pageUrl) as response:
            StartpageText = await response.text()
            SoupStartpage = BeautifulSoup(StartpageText, "html.parser")
            return SoupStartpage

async def get_URLs(pageUrl, PagesRange):
    urlList = []
    urlList.append[pageUrl]

    async with aiohttp.ClientSession() as session:
        for i in range(PagesRange):
            async with session.get(pageUrl) as response:
                StartpageText = await response.text()
                SoupStartpage = BeautifulSoup(StartpageText, "html.parser")
                pageUrl = stdurl+SoupStartpage.find('a', class_='next').get('href')
                urlList.append[pageUrl]

    return urlList

async def get_links(url):
    leakurllist = []

    ParseTasks = []
    ParseTasks.append(asyncio.create_task(ReadPageSoup(url)))

    Result = await asyncio.gather(*ParseTasks)
    SoupStartpage = Result[0]

    posts = SoupStartpage.findAll('span', class_='link_wr')
    datapostlinks = []

    for post in posts:
        postlink = stdurl+post.find('a', class_='link').get('href')
        datapostlinks.append(postlink)

    for datapostlink in datapostlinks:
        datapostlinkTasks = []
        datapostlinkTasks.append(asyncio.create_task(ReadPageSoup(datapostlink)))

        datapostlinkResult = await asyncio.gather(*datapostlinkTasks)
        soup = datapostlinkResult[0]

        comments = soup.findAll('div', class_='comment')

        for comment in comments:
            soupcomment = BeautifulSoup(str(comment), "html.parser")
            refs = soupcomment.findAll('a')

            for ref in refs:
                if CorrectUrl(ref.text) == True:
                    leakurllist.append(ref.text)

    return leakurllist     

# Разбор комментариев
async def ParseComments(self):
    # Обновляем переменные забирая значения из окна
    PagesRange = int(self.ui.lineEdit_PagesQty.text())
    starturl = self.ui.lineEdit_StartUrl.text()

    # Подготовка progress bar
    #self.ProgressBarInit(PagesRange)

    # Читает начальную страницу
    urlTasks = []
    urlTasks.append(asyncio.create_task(get_URLs(starturl, PagesRange)))

    urlList = await asyncio.gather(*urlTasks) 

    tasks = []
    for urlElem in urlList:
        for url in urlElem:
            tasks.append(asyncio.create_task(get_links(url)))  
 
    results = await asyncio.gather(*tasks)

    for result in results:
        for leakurl in result:
            item = QtWidgets.QListWidgetItem()
            item.setText(leakurl)
            self.ui.listWidget.addItem(item)
    
    # self.SaveToCsv()


# Инициализация главного окна
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # заполнение полей на форме
        self.ui.lineEdit_PagesQty.setText(str(PagesRange))
        self.ui.lineEdit_StartUrl.setText(starturl)
        # подключение клик-сигнал к слоту ParseComments
        self.ui.pushButton_Run.clicked.connect(self.Run)
        self.ui.listWidget.itemClicked.connect(self.OpenClickedItem)

    def Run(self):
        asyncio.run(ParseComments(self)) 

    # # Метод-слот, срабатывающий при сигнале с другого потока
    # @QtCore.pyqtSlot(str, str)
    # def ResultFixation(self, urltext, urlpost):
    #     dataleaklinks.append([urltext, urlpost])
    #     self.AddListElement(urltext)

    # @QtCore.pyqtSlot(int)
    # def ProgressBarIterator(self, i):
    #     self.ui.progressBar.setValue(i+1)

    # # Добавление элемента в список
    # def AddListElement(self, urltext):
    #     item = QtWidgets.QListWidgetItem()
    #     item.setText(urltext)
    #     self.ui.listWidget.addItem(item)

    # # Инициализация progress bar
    # def ProgressBarInit(self, PagesRange):
    #     self.ui.progressBar.setValue(0)
    #     # self.ui.progressBar.setMinimum = 0
    #     # self.ui.progressBar.setMaximum = PagesRange
    #     self.ui.progressBar.setRange(0, PagesRange)

    # Сохраняем таблицу в CSV через pandas
    def SaveToCsv(self):
        header = ['link', 'post']
        df = pd.DataFrame(dataleaklinks, columns=header)
        df.to_csv(desktoppath+'\leaked.csv', sep=';', encoding='utf8')
        QtWidgets.QMessageBox.information(self, "Готово!", "Файл находится тут: "+ desktoppath+"\leaked.csv")

    def OpenClickedItem(self, item):
        webbrowser.get(chromepath).open(item.text())


App = QtWidgets.QApplication([])
application = MainWindow()
application.show()

sys.exit(App.exec())