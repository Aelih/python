import requests
from bs4 import BeautifulSoup

# https://www.youtube.com/watch?v=IEfQLbxHY_g
session = requests.Session()

link = "https://api.joyreactor.cc/graphql"

login = input("Enter LOGIN: ")
passwd = input("Enter PASSWORD: ")
variables = {"query":"mutation Login($login: String!, $password: String!){login(name:$login,password:$password) {me {token}}}",
                "variables":{"login":login,"password":passwd}}

header = {"accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47",
            "origin":"http://joyreactor.cc",
            "referer": "http://joyreactor.cc/"}

response = session.post(url=link, json=variables, headers=header)

print(response.text, f"Response status {response.status_code}")

profile = session.get(url="http://joyreactor.cc/user/"+login, headers=header)

print(profile.text)

