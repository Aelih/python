import requests
from bs4 import BeautifulSoup

session = requests.Session()

link = "https://api.joyreactor.cc/graphql"

login = input("Enter LOGIN: ")
passwd = input("Enter PASSWORD: ")
variables = {"query":"mutation Login($login: String!, $password: String!){login(name:$login,password:$password) {me {token}}}",
                "variables":{"login":login,"password":passwd}}

header = {"accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47",
            "origin":"http://joyreactor.cc",
            "referer": "http://joyreactor.cc/",
            "cookie": "joyreactor_api_session=eyJpdiI6IjBGMFIxdDQ2L0JYVDVldkZrU25xbWc9PSIsInZhbHVlIjoiZDUyY2JYNmNHOUtKWm42TDhvWWlqcnNObFRoWit2aWlMMDExV2pGQlRTa1VPdFc0RXZrRUplVW45SWx4N29KZWJUYXZPYXNNL3V3bC96YU1waVRvTmhVR0NKRXZmWjhRZlQzM2ZGTUdoMzVrQy9hOHE2ZlM5MnJlV2ZlVE1zMGUiLCJtYWMiOiI5ODM4NThlZjQ0Yzk5MDJiNWViMTkzMGE3ZTJmMDM4MzAyNDA5MTJmNDliNTJiNGViN2Y5MDQ5NzlmYmY0MjQ4IiwidGFnIjoiIn0%3D"}

# response = session.post(link, data=variables, headers=header).text
response = requests.api.post(url=link, data=variables, headers=header)

print(response)