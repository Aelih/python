import requests
from bs4 import BeautifulSoup
from validators import url
from time import sleep
import pandas as pd
from os import path, environ
from tkinter import Entry, Label, Tk, Frame, Button, messagebox, LEFT, X, RIGHT, BOTH
from tkinter.ttk import Style, Progressbar
import threading
from ctypes import wintypes, windll, create_unicode_buffer

# Конфигурационные параметры
stdurl = "https://old.reactor.cc"  # на старой верстке искать проще
starturl = "https://old.reactor.cc/tag/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0"  # ert
PagesRange = 20 

# Основной класс приложения
class MainForm(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.dataleaklinks = []  # Список для накопления результатов
        self.initUI()

    def initUI(self):
        self.parent.title("Парсер Joy")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.addElements()

    def addElements(self):
        # Верхняя часть (заголовок)
        self.frm_header = Frame(self)
        self.frm_header.pack()
        self.lbl_greeting = Label(master=self.frm_header, text="Привет! В разработке...")
        self.lbl_greeting.pack()

        # Основное тело формы
        self.frm_body = Frame(self)
        self.frm_body.pack()

        # Виджеты для ввода количества страниц
        self.lbl_pagesQty = Label(master=self.frm_body, text="Кол-во читаемых страниц")
        self.ent_pagesQty = Entry(master=self.frm_body, width=50)
        self.ent_pagesQty.insert(0, PagesRange)
        self.lbl_pagesQty.grid(row=0, column=0, sticky="w")
        self.ent_pagesQty.grid(row=0, column=1)

        # Виджеты для ввода начальной страницы
        self.lbl_starturl = Label(master=self.frm_body, text="Начальная страница")
        self.ent_starturl = Entry(master=self.frm_body, width=50)
        self.ent_starturl.insert(0, starturl)
        self.lbl_starturl.grid(row=1, column=0, sticky="w")
        self.ent_starturl.grid(row=1, column=1)

        # Прогресс-бар (новый элемент)
        self.frm_progress = Frame(self)
        self.frm_progress.pack(fill=X, padx=10, pady=10)
        self.progress = Progressbar(self.frm_progress, orient="horizontal", mode="determinate", length=300)
        self.progress.pack(fill=X)

        # Подвал с кнопками
        self.frm_footer = Frame(self)
        self.frm_footer.pack(fill=X, ipadx=5, ipady=5)
        self.btn_quit = Button(master=self.frm_footer, text="Закрыть", command=self.quit)
        self.btn_quit.pack(side=RIGHT, padx=10, ipadx=10)
        # Кнопка "Запустить" запускает парсинг в отдельном потоке
        self.btn_run = Button(master=self.frm_footer, text="Запустить", command=self.start_parsing_thread)
        self.btn_run.pack(side=RIGHT, ipadx=10)
        self.btn_about = Button(master=self.frm_footer, text="?", command=self.About, bg="#83c795")
        self.btn_about.pack(side=LEFT, padx=10)

    def About(self):
        messagebox.showinfo("О программе", "Сделано Aelih. Спасибо за использование :-)")

    # Чтение и подготовка страницы по URL с обработкой ошибок
    def ReadPageSoup(self, pageUrl):
        try:
            response = requests.get(pageUrl)
            response.raise_for_status()  # Генерирует исключение при ошибке запроса
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить страницу:\n{e}")
            return None
        return BeautifulSoup(response.text, "html.parser")

    # Проверка на корректность URL
    def CorrectUrl(self, commenttext):
        return url(commenttext) and ('instagram' not in commenttext) and ('reactor' not in commenttext)

    def get_desktop_path(self):
        CSIDL_DESKTOPDIRECTORY = 0x10  # Константа для рабочего стола
        MAX_PATH = 260
        buf = create_unicode_buffer(MAX_PATH)
        # SHGetFolderPathW возвращает 0 при успехе
        result = windll.shell32.SHGetFolderPathW(None, CSIDL_DESKTOPDIRECTORY, None, 0, buf)
        if result == 0:
            return buf.value
        else:
            raise Exception("Не удалось получить путь к рабочему столу")

    # Сохранение результатов в CSV-файл через pandas
    def SaveToCsv(self):
        desktoppath = self.get_desktop_path() 
        header = ['link', 'post']
        filepath = path.join(desktoppath, 'leaked.csv')
        df = pd.DataFrame(self.dataleaklinks, columns=header)
        df.to_csv(filepath, sep=';', encoding='utf8')
        messagebox.showinfo("Готово!", "Файл найдёшь здесь: " + filepath)

    # Разбор комментариев с обновлением прогресс-бара
    def ParseComments(self):
        # Сбрасываем список результатов
        self.dataleaklinks = []
        try:
            pages_range = int(self.ent_pagesQty.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число страниц")
            return
        start_url = self.ent_starturl.get()

        # Инициализируем прогресс-бар: максимум = количеству страниц, текущее значение = 0
        self.progress.config(maximum=pages_range, value=0)

        SoupStartpage = self.ReadPageSoup(start_url)
        if SoupStartpage is None:
            return

        for i in range(pages_range):
            # Ищем ссылку "Вперед"
            next_link = SoupStartpage.find('a', class_='next')
            if next_link and next_link.get('href'):
                NextPageUrl = stdurl + next_link.get('href')
            else:
                messagebox.showerror("Ошибка", "Не найдена ссылка 'Вперед'. Операция прервана.")
                break

            posts = SoupStartpage.findAll('span', class_='manage')
            datapostlinks = []
            for post in posts:
                link_tag = post.find('a', class_='link')
                if not link_tag:
                    continue
                href = link_tag.get('href')
                if not href:
                    continue
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
                        if self.CorrectUrl(ref.text):
                            self.dataleaklinks.append([ref.text, datapostlink])

            # Читаем следующую страницу (кнопка "Вперед")
            SoupStartpage = self.ReadPageSoup(NextPageUrl)
            if SoupStartpage is None:
                break

            # Обновляем прогресс-бар: шаг увеличивается на 1
            self.progress.step(1)

        self.SaveToCsv()

    # Запуск парсинга в отдельном потоке для сохранения отзывчивости интерфейса
    def start_parsing_thread(self):
        self.btn_run.config(state="disabled") # Деактивируем кнопку
        thread = threading.Thread(target=self.thread_wrapper)
        thread.daemon = True
        thread.start()

    def thread_wrapper(self):
        self.ParseComments()
        # По окончании работы включаем кнопку обратно
        self.parent.after(0, lambda: self.btn_run.config(state="normal"))

# Персональные настройки окна    
def WindowCustomize(Window):
    Window.resizable(width=False, height=False)

# Создаём главное окно
def main():
    Window = Tk()
    MainForm(Window)
    WindowCustomize(Window)
    Window.mainloop()

if __name__ == '__main__':
    main()