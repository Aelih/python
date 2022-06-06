import requests
import aiohttp

link = "https://api.joyreactor.cc/graphql"

header = {"accept": "*/*",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47",
                "origin":"http://joyreactor.cc",
                "referer": "http://joyreactor.cc/"}

def syncAuthorize(login, passwd):

    variables = {"query":"mutation Login($login: String!, $password: String!){login(name:$login,password:$password) {me {token}}}",
                    "variables":{"login":login,"password":passwd}}
    
    session = requests.Session()

    response = session.post(url=link, json=variables, headers=header)

    if response.status_code == 200:
        if type(response.json().get('data')) == type(None):
            return [None, response.status_code]        
        else:    
            return [response.json()["data"]["login"]["me"]["token"], response.status_code]
    else:
        return [None, response.status_code] 

async def asyncAuthorize(login, passwd):  

    variables = {"query":"mutation Login($login: String!, $password: String!){login(name:$login,password:$password) {me {token}}}",
                    "variables":{"login":login,"password":passwd}}
 
    async with aiohttp.ClientSession() as session:
        async with session.post(url=link, json=variables, headers=header) as response:
            result = await response.json(), response.status 
            if result[1] == 200:
                if type(result[0].get('data')) == type(None):
                    return [None, result[1]]        
                else:    
                    return [result[0]["data"]["login"]["me"]["token"], result[1]]
            else:
                return [None, result[1]]            

