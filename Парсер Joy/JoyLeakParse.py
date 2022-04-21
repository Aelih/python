import requests
from bs4 import BeautifulSoup
from validators import url
from time import sleep
import pandas as pd
from os import path, environ
from tkinter import Entry, Label, Tk, Frame, messagebox, BOTH
from tkinter.ttk import Frame, Button, Style

stdurl = "http://joyreactor.cc"
starturl = "http://joyreactor.cc/tag/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0"
dataleaklinks = []
sleeptime = 1
PagesRange = 2
desktoppath = path.join((environ['USERPROFILE']), 'Desktop')

#Проверка на корректность URL
def CorrectUrl(commenttext):
    if url(commenttext) == True and commenttext.find('instagram') == -1 and commenttext.find('joyreactor') == -1: 
        return True
    else:
        return False

#Сохраняем таблицу в CSV через pandas
def SaveToCsv():
    header = ['link', 'post']
    df = pd.DataFrame(dataleaklinks, columns=header)
    df.to_csv(desktoppath+'\leaked.csv', sep=';', encoding='utf8')
    messagebox.showinfo("Готово!", "Файл найдёшь здесь: "+desktoppath+'\leaked.csv')

#Разбор комментариев
def ParseComments():
    Startpage = requests.get(starturl)
    sleep(sleeptime)
    SoupStartpage = BeautifulSoup(Startpage.text, "html.parser")

    for i in range(PagesRange):
        NextPageUrl = stdurl+SoupStartpage.find('a', class_='next').get('href')
        posts = SoupStartpage.findAll('span', class_='link_wr')
        datapostlinks = []

        for post in posts:
            postlink = stdurl+post.find('a', class_='link').get('href')
            datapostlinks.append(postlink)

        for datapostlink in datapostlinks:
            respost = requests.get(datapostlink)
            sleep(sleeptime)
            soup = BeautifulSoup(respost.text, "html.parser")
            comments = soup.findAll('div', class_='comment')

            for comment in comments:
                soupcomment = BeautifulSoup(str(comment), "html.parser")
                refs = soupcomment.findAll('a')
                
                for ref in refs:
                    if CorrectUrl(ref.text) == True:
                        dataleaklinks.append([ref.text, datapostlink])
        
        Startpage = requests.get(NextPageUrl)
        sleep(sleeptime)
        SoupStartpage = BeautifulSoup(Startpage.text, "html.parser")

    SaveToCsv()

def addElements(self):
    greeting = Label(self, text="Привет! Параметры нельзя изменить!")
    greeting.pack()

    emptyspace = Label(self)
    emptyspace.pack()

    pagesQtyLabel = Label(self, text="Кол-во страниц", )
    pagesQtyLabel.pack()

    pagesQty = Entry(self)
    pagesQty.insert(0, PagesRange)
    pagesQty.pack()

    runButton = Button(self, text="Запустить", command=ParseComments)
    runButton.place(x=50, y=100)

    quitButton = Button(self, text="Закрыть", command=self.quit)
    quitButton.place(x=175, y=100)

#Строим форму на tkinter
class MainForm(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI() 

    def initUI(self):
        self.parent.title("Парсер Joy")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        addElements(self)

    def centerWindow(self):
        w = 300
        h = 150
 
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
 
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
   

#Создаём главное-корневое окно
def main():
    root = Tk()
    MainForm(root)
    root.mainloop()

if __name__ == '__main__':
    main()        