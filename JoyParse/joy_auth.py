import requests
from bs4 import BeautifulSoup
import fake_useragent

session = requests.Session()

link = "https://api.joyreactor.cc/graphql"

login = input("Enter LOGIN: ")
passwd = input("Enter PASSWORD: ")
variables = {"query":"mutation Login($login: String!, $password: String!){login(name:$login,password:$password) {me {token}}}",
                "variables":{"login":login,"password":passwd}}

user = fake_useragent.UserAgent().random

header = {"user-agent":user}

response = session.post(link, data=variables, headers=header).text
print(response)