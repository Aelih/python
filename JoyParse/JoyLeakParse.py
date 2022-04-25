import requests
from bs4 import BeautifulSoup
from validators import url
from time import sleep
import pandas as pd
from os import path, environ
from tkinter import LEFT, Entry, Label, Tk, Frame, Button, messagebox, PhotoImage, X, RIGHT, BOTH
from tkinter.ttk import Style

stdurl = "http://joyreactor.cc"
starturl = "http://joyreactor.cc/tag/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0"
dataleaklinks = []
sleeptime = 1
PagesRange = 20
desktoppath = path.join((environ['USERPROFILE']), 'Desktop')

# Строим форму на tkinter
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
        self.addElements()

    def addElements(self):
        # Создается новая рамка `frm_header` для заголовка.
        self.frm_header = Frame(self)
        # Помещает рамку в окно приложения.
        self.frm_header.pack()
        
        # Создает ярлык и текстовок поле для ввода имени.
        self.lbl_greeting = Label(master=self.frm_header, text="Привет! В разработке...")
        self.lbl_greeting.pack()

        self.frm_body = Frame(self)
        self.frm_body.pack()

        self.lbl_pagesQty = Label(master=self.frm_body, text="Кол-во читаемых страниц")
        self.ent_pagesQty = Entry(master=self.frm_body, width=50)
        self.ent_pagesQty.insert(0, PagesRange)
        # Использует менеджер геометрии grid для размещения ярлыка и
        # однострочного поля для ввода текста в первый и второй столбец
        # первой строки сетки.
        self.lbl_pagesQty.grid(row=0, column=0, sticky="e")
        self.ent_pagesQty.grid(row=0, column=1)

        # Создает ярлык и текстовое поле для ввода начальной страницы.
        self.lbl_starturl = Label(master=self.frm_body, text="Начальная страница", )
        self.ent_starturl = Entry(master=self.frm_body, width=50)
        self.ent_starturl.insert(0, starturl)
        # Размещает виджеты на вторую строку сетки
        self.lbl_starturl.grid(row=1, column=0, sticky="e")
        self.ent_starturl.grid(row=1, column=1)
        
        self.frm_footer = Frame(self)
        self.frm_footer.pack(fill=X, ipadx=5, ipady=5)
        
        self.btn_quit = Button(master=self.frm_footer, text="Закрыть", command=self.quit)
        self.btn_quit.pack(side=RIGHT, padx=10, ipadx=10)

        self.btn_run = Button(master=self.frm_footer, text="Запустить", command=self.ParseComments)
        self.btn_run.pack(side=RIGHT, ipadx=10) 

        self.btn_about = Button(master=self.frm_footer, text="?", command=self.About, bg="#83c795")
        self.btn_about.pack(side=LEFT, padx=10)  

    # Окно "О программе"
    def About(Self):
        messagebox.showinfo("О программе", "Сделано Aelih. Спасибо за использование :-)")

    # Чтение и подготовка страницы по URL
    def ReadPageSoup(self, pageUrl):
        Startpage = requests.get(pageUrl)
        sleep(sleeptime)
        SoupStartpage = BeautifulSoup(Startpage.text, "html.parser")
        return SoupStartpage

    # Проверка на корректность URL
    def CorrectUrl(self, commenttext):
        if url(commenttext) == True and commenttext.find('instagram') == -1 and commenttext.find('reactor') == -1:
            return True
        else:
            return False

    # Сохраняем таблицу в CSV через pandas
    def SaveToCsv(self):
        header = ['link', 'post']
        df = pd.DataFrame(dataleaklinks, columns=header)
        df.to_csv(desktoppath+'\leaked.csv', sep=';', encoding='utf8')
        messagebox.showinfo("Готово!", "Файл найдёшь здесь: " +
                            desktoppath+'\leaked.csv')

    # Разбор комментариев
    def ParseComments(self):
        #Обновляем переменные забирая значения из окна
        PagesRange = int(self.ent_pagesQty.get())

        # Читает начальную страницу
        SoupStartpage = self.ReadPageSoup(starturl)

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
                        if self.CorrectUrl(ref.text) == True:
                            dataleaklinks.append([ref.text, datapostlink])

            # Читает следующую страницу (кнопка Вперед)
            SoupStartpage = self.ReadPageSoup(NextPageUrl)

        self.SaveToCsv()

# Персональные настройки окна    
def WindowCustomize(Window):
    Window.resizable(width=False, height=False)
    iconpic = PhotoImage(file="JoyParse/tux.png")
    Window.iconphoto(False, iconpic)

# Создаём главное-корневое окно
def main():
    Window = Tk()
    MainForm(Window)
    WindowCustomize(Window)
    Window.mainloop()

if __name__ == '__main__':
    main()