import joy_auth as auth
import asyncio

async def AuthTry(login, passwd):
    Tasks = []
    Tasks.append(asyncio.create_task(auth.asyncAuthorize(login, passwd)))

    result = await asyncio.gather(*Tasks)

    if result[0][0] == None:
        print("Problems with authorization. Please try again!")
        print(f"Status {result[0][1]}")
    else:
        print(result[0][0]) 

def syncAuthTry(login, passwd):
    result = auth.syncAuthorize(login, passwd)

    if result[0] == None:
        print("Problems with authorization. Please try again!")
        print(f"Status {result[1]}")
    else:
        print(result[0])         


if __name__ == "__main__":
    choice = input("Enter 0 - for Sync, 1 - for Async: ")
    login = input("Enter LOGIN: ")
    passwd = input("Enter PASSWORD: ")

    if choice == "0":
        syncAuthTry(login, passwd)
    else:
        asyncio.run(AuthTry(login, passwd))