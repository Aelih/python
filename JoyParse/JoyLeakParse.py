import requests
from bs4 import BeautifulSoup
from validators import url
from time import sleep
import pandas as pd
from os import path, environ
from tkinter import Entry, Label, Tk, Frame, Button, messagebox, LEFT, X, RIGHT, BOTH
from tkinter.ttk import Style

stdurl = "https://old.reactor.cc" # на старой верстке искать проще
starturl = "https://old.reactor.cc/tag/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0" # ert
PagesRange = 20
desktoppath = path.join((environ['USERPROFILE']), 'Desktop')

# Строим форму на tkinter
class MainForm(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.dataleaklinks = []  # Инициализируем список для накопления результатов
        self.initUI()

    def initUI(self):
        self.parent.title("Парсер Joy")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.addElements()

    def addElements(self):
        # Создаем верхнюю часть формы (заголовок)
        # Создается новая рамка `frm_header` для заголовка.
        self.frm_header = Frame(self)
        # Помещает рамку в окно приложения.
        self.frm_header.pack()
        
        # Создает ярлык и текстовок поле для ввода имени.
        self.lbl_greeting = Label(master=self.frm_header, text="Привет! В разработке...")
        self.lbl_greeting.pack()

        # Создаем основное тело формы
        self.frm_body = Frame(self)
        self.frm_body.pack()

        # Виджеты для ввода количества страниц
        self.lbl_pagesQty = Label(master=self.frm_body, text="Кол-во читаемых страниц")
        self.ent_pagesQty = Entry(master=self.frm_body, width=50)
        self.ent_pagesQty.insert(0, PagesRange)
        self.lbl_pagesQty.grid(row=0, column=0, sticky="w")
        self.ent_pagesQty.grid(row=0, column=1)

        # Виджеты для ввода начальной страницы
        self.lbl_starturl = Label(master=self.frm_body, text="Начальная страница", )
        self.ent_starturl = Entry(master=self.frm_body, width=50)
        self.ent_starturl.insert(0, starturl)
        # Размещает виджеты на вторую строку сетки
        self.lbl_starturl.grid(row=1, column=0, sticky="w")
        self.ent_starturl.grid(row=1, column=1)

        # Подвал с кнопками
        self.frm_footer = Frame(self)
        self.frm_footer.pack(fill=X, ipadx=5, ipady=5)
        
        self.btn_quit = Button(master=self.frm_footer, text="Закрыть", command=self.quit)
        self.btn_quit.pack(side=RIGHT, padx=10, ipadx=10)

        self.btn_run = Button(master=self.frm_footer, text="Запустить", command=self.ParseComments)
        self.btn_run.pack(side=RIGHT, ipadx=10) 

        self.btn_about = Button(master=self.frm_footer, text="?", command=self.About, bg="#83c795")
        self.btn_about.pack(side=LEFT, padx=10)

    # Окно "О программе"
    def About(self):
        messagebox.showinfo("О программе", "Сделано Aelih. Спасибо за использование :-)")

    # Чтение и подготовка страницы по URL
    def ReadPageSoup(self, pageUrl):
        try:
            response = requests.get(pageUrl)
            response.raise_for_status()  # Генерирует исключение для неудачного кода ответа
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить страницу:\n{e}")
            return None  # Возвращаем None, чтобы сигнализировать о проблеме

        return BeautifulSoup(response.text, "html.parser")

    # Проверка на корректность URL
    def CorrectUrl(self, commenttext):        
        return url(commenttext) and ('instagram' not in commenttext) and ('reactor' not in commenttext)

    # Сохраняем таблицу в CSV через pandas
    def SaveToCsv(self):
        header = ['link', 'post']
        filepath = path.join(desktoppath, 'leaked.csv')

        df = pd.DataFrame(self.dataleaklinks, columns=header)
        df.to_csv(filepath, sep=';', encoding='utf8')

        messagebox.showinfo("Готово!", "Файл найдёшь здесь: " + filepath)

    # Разбор комментариев
    def ParseComments(self):    
        # Сбрасываем список при каждом новом запуске парсинга
        self.dataleaklinks = []

        #Обновляем переменные забирая значения из окна
        PagesRange = int(self.ent_pagesQty.get())
        starturl = self.ent_starturl.get()
        
        # Читаем начальную страницу
        SoupStartpage = self.ReadPageSoup(starturl)
        if SoupStartpage is None:
            # Если не удалось загрузить начальную страницу, прерываем парсинг
            return

        for i in range(PagesRange):
            # Ищем ссылку "Вперед"
            next_link = SoupStartpage.find('a', class_='next')
            if next_link and next_link.get('href'):
                NextPageUrl = stdurl + next_link.get('href')
            else:
                # Если ссылка не найдена, информируем пользователя и прерываем цикл
                messagebox.showerror("Ошибка", "Не найдена ссылка 'Вперед'. Операция прервана.")
                break    

            posts = SoupStartpage.findAll('span', class_='manage')
            datapostlinks = []

            for post in posts:
                # Пытаемся найти тег <a> с классом "link"
                link_tag = post.find('a', class_='link')
                if not link_tag:
                    # Если тег не найден переходим к следующему посту
                    continue

                # Получаем значение атрибута href
                href = link_tag.get('href')
                if not href:
                    # Если атрибут отсутствует или пуст пропускаем пост
                    continue
                
                # Если всё в порядке, формируем полный URL
                postlink = stdurl + href
                datapostlinks.append(postlink)

            for datapostlink in datapostlinks:
                try:
                    response = requests.get(datapostlink)
                    response.raise_for_status()
                except requests.RequestException as e:
                    messagebox.showerror("Ошибка", f"Не удалось загрузить страницу: {e}")
                    continue  # Переход к следующему datapostlink
                
                soup = BeautifulSoup(response.text, "html.parser")
                comments = soup.findAll('div', class_='post_comment_list')

                for comment in comments:
                    refs = comment.findAll('a')

                    for ref in refs:
                        if self.CorrectUrl(ref.text) == True:
                            self.dataleaklinks.append([ref.text, datapostlink])

            # Читает следующую страницу (кнопка Вперед)
            SoupStartpage = self.ReadPageSoup(NextPageUrl)
            if SoupStartpage is None:
                break

        self.SaveToCsv()

# Персональные настройки окна    
def WindowCustomize(Window):
    Window.resizable(width=False, height=False)

# Создаём главное-корневое окно
def main():
    Window = Tk()
    MainForm(Window)
    WindowCustomize(Window)
    Window.mainloop()

if __name__ == '__main__':
    main()