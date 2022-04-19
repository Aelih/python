# %%
from cgitb import html
from operator import truediv
import requests
from bs4 import BeautifulSoup
import validators
from time import sleep
import pandas as pd
import os

# %%
stdurl = "http://joyreactor.cc"
#starturl = "http://joyreactor.cc/tag/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0"
starturl = "http://joyreactor.cc/tag/%D0%AD%D1%80%D0%BE%D1%82%D0%B8%D0%BA%D0%B0/4509"
dataleaklinks = []
sleeptime = 0
PagesRange = 2
desktoppath = os.path.join((os.environ['USERPROFILE']), 'Desktop')

def CorrectUrl(commenttext):
    if validators.url(commenttext) == True and commenttext.find('instagram') == -1 and commenttext.find('joyreactor') == -1: 
        return True
    else:
        return False

# %%
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


# %%
header = ['link', 'post']
df = pd.DataFrame(dataleaklinks, columns=header)
df.to_csv(desktoppath+'\leaked.csv', sep=';', encoding='utf8')


