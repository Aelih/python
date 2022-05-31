from email import header
from urllib import response
import requests
from bs4 import BeautifulSoup
import fake_useragent

link = "https://api.joyreactor.cc/graphql"

query = "mutation Login($login: String!, $password: String!){login(name:$login,password:$password) {me {token}}}"

variables = {"login": "fsdfsd",
        "password": "sdfsdfw4345"}

user = fake_useragent.UserAgent().random

header = {"user-agent":user}

response = requests.post(link, data=variables, headers=header).text
print(response)